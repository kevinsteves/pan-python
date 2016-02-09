#
# Copyright (c) 2015 Palo Alto Networks, Inc. <techbizdev@paloaltonetworks.com>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

import re
import socket
import ssl
import sys

_using_requests = False

try:
    import requests
    _using_requests = True
except ImportError:
    try:
        # 3.2
        from urllib.request import Request, \
            build_opener, HTTPErrorProcessor, HTTPSHandler
        from urllib.error import URLError
        from urllib.parse import urlencode
    except ImportError:
        # 2.7
        from urllib2 import Request, URLError, \
            build_opener, HTTPErrorProcessor, HTTPSHandler
        from urllib import urlencode


def _isunicode(s):
    try:
        if isinstance(s, unicode):
            return True
        return False
    except NameError:
        if isinstance(s, str):
            return True
        return False


class PanHttpError(Exception):
    pass


class PanHttp:
    def __init__(self,
                 timeout=None,
                 verify_cert=True):
        self.timeout = timeout
        self.verify_cert = verify_cert

        if self.timeout is not None:
            try:
                self.timeout = float(self.timeout)
                if not self.timeout >= 0:
                    raise ValueError
            except ValueError:
                raise PanHttpError('Invalid timeout: %s' % self.timeout)

        self.using_requests = _using_requests

        if self.using_requests:
            self._http_request = self._http_request_requests
            if not self.verify_cert:
                requests.packages.urllib3.disable_warnings()
            self.requests_version = requests.__version__
        else:
            self._http_request = self._http_request_urllib

    def _init_attributes(self):
        self.code = None
        self.reason = None
        self.headers = None
        self.encoding = None
        self.text = None
        self.content = None

    def http_request(self, url=None, headers=None, data=None, params=None):
        self._init_attributes()
        self._http_request(url, headers, data, params)

    def raise_for_status(self):
        if self.code is None:
            return None

        if not (200 <= self.code < 300):
            e = 'HTTP Error %s' % self.code
            if self.reason is not None:
                e += ': %s' % self.reason
            raise PanHttpError(e)

        return None

    def _http_request_urllib(self, url, headers, data, params):
        # data must by type 'bytes' for 3.x
        if _isunicode(data):
            data = data.encode()

        if params is not None:
            url += '?' + urlencode(params)

        kwargs = {}
        if url is not None:
            kwargs['url'] = url
        if headers is not None:
            kwargs['headers'] = headers
        if data is not None:
            kwargs['data'] = data
        request = Request(**kwargs)

        kwargs = {
            'url': request,
        }
        if self.timeout is not None:
            kwargs['timeout'] = self.timeout

        if not self.verify_cert and \
            (sys.version_info.major == 2 and
             sys.hexversion >= 0x02070900 or
             sys.version_info.major == 3 and
             sys.hexversion >= 0x03040300):
            context = ssl._create_unverified_context()
            kwargs['context'] = context

        try:
            response = self._urlopen(**kwargs)
        except (URLError, IOError, ssl.CertificateError) as e:
            # IOError for urllib timeouts
            # ssl.CertificateError for mismatching hostname
            raise PanHttpError(str(e))

        self.code = response.getcode()
        if hasattr(response, 'reason'):
            # 3.2
            self.reason = response.reason
        elif hasattr(response, 'msg'):
            # 2.7
            self.reason = response.msg

        h = dict(response.info().items())
        self.headers = dict((k.lower(), v) for (k, v) in h.items())

        s = self.headers.get('content-type')
        # XXX
        self.encoding = 'utf8'
        if s is not None:
            types = [x.lower() for x in s.split(';')]
            types = [x.lstrip() for x in types]
            types = [x.rstrip() for x in types]
            types = set(types)
            for x in types:
                result = re.search(r'^charset=(.+)$', x)
                if result:
                    self.encoding = result.group(1)

        self.content = response.read()
        self.text = self.content.decode(self.encoding)

    def _http_request_requests(self, url, headers, data, params):
        kwargs = {
            'verify': self.verify_cert,
        }
        if url is not None:
            kwargs['url'] = url
        if headers is not None:
            kwargs['headers'] = headers
        if data is not None:
            kwargs['data'] = data
        if params is not None:
            kwargs['params'] = params
        if self.timeout is not None:
            kwargs['timeout'] = self.timeout

        try:
            if data is None:
                r = requests.get(**kwargs)
            else:
                r = requests.post(**kwargs)
        except requests.exceptions.RequestException as e:
            raise PanHttpError(str(e))

        self.code = r.status_code
        self.reason = r.reason
        self.headers = r.headers
        self.encoding = r.encoding
        self.content = r.content
        self.text = r.text

    # allow non-2XX error codes
    # see http://bugs.python.org/issue18543 for why we can't just
    # install a new HTTPErrorProcessor()
    @staticmethod
    def _urlopen(url, data=None,
                 timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
                 cafile=None, capath=None, cadefault=False,
                 context=None):

        def http_response(request, response):
            return response

        http_error_processor = HTTPErrorProcessor()
        http_error_processor.https_response = http_response

        if context:
            https_handler = HTTPSHandler(context=context)
            opener = build_opener(https_handler, http_error_processor)
        else:
            opener = build_opener(http_error_processor)

        return opener.open(url, data, timeout)
