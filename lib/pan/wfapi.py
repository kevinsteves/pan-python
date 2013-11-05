#
# Copyright (c) 2013 Kevin Steves <kevin.steves@pobox.com>
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

"""Interface to the WildFire  API

The pan.wfapi module implements the PanWFapi class.  It provides an
interface to the WildFire API on Palo Alto Networks' WildFire Cloud.
"""

# XXX Using the requests module which uses urllib3 and has support
# for multipart form-data would make this much simpler/cleaner (main
# issue is support for Python 2.x and 3.x in one source).  However I
# decided to not require non-default modules.  That decision may need
# to be revisited as some parts of this are not clean.

from __future__ import print_function
import sys
import re
import os
from io import BytesIO
import email.utils
try:
    # 3.2
    from urllib.request import Request, urlopen
    from urllib.error import URLError
    from urllib.parse import urlencode
    from http.client import responses
    _legacy_urllib = False
except ImportError:
    # 2.7
    from urllib2 import Request, urlopen, URLError
    from urllib import urlencode
    from httplib import responses
    _legacy_urllib = True

import xml.etree.ElementTree as etree
from . import __version__
import pan.rc

_cloud_server = 'wildfire.paloaltonetworks.com'
_encoding = 'utf-8'
_tags_forcelist = set(['entry'])
_rfc2231_encode = False
#_rfc2231_encode = True


def _isunicode(s):
    try:
        if isinstance(s, unicode):
            return True
        return False
    except NameError:
        if isinstance(s, str):
            return True
        return False


def _isbytes(s):
    try:
        if isinstance(s, basestring) and isinstance(s, bytes):
            return True
        return False
    except NameError:
        if isinstance(s, bytes):
            return True
        return False


class PanWFapiError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        if self.msg is None:
            return ''
        return self.msg


class PanWFapi:
    def __init__(self,
                 debug=0,
                 tag=None,
                 hostname=None,
                 api_key=None,
                 timeout=None,
                 cafile=None,
                 capath=None):
        self.debug = debug
        self.debug1, self.debug2, self.debug3 = False, False, False
        if self.debug > 0:
            self.debug1 = True
        if self.debug > 1:
            self.debug2 = True
        if self.debug > 2:
            self.debug3 = True
        self.tag = tag
        self.hostname = hostname
        self.api_key = None
        self.timeout = timeout
        # WildFire cloud cafile:
        # https://certs.godaddy.com/anonymous/repository.pki
        # Go Daddy Class 2 Certification Authority Root Certificate
        self.cafile = cafile
        self.capath = capath

        if self.debug > 3:
            raise PanWFapiError('Maximum debug level is 3')

        if self.debug3:
            print('Python version:', sys.version, file=sys.stderr)
            print('xml.etree.ElementTree version:', etree.VERSION,
                  file=sys.stderr)
            print('pan-python version:', __version__, file=sys.stderr)

        if self.timeout is not None:
            try:
                self.timeout = int(self.timeout)
                if not self.timeout > 0:
                    raise ValueError
            except ValueError:
                raise PanWFapiError('Invalid timeout: %s' % self.timeout)

        init_panrc = {}  # .panrc args from constructor
        if hostname is not None:
            init_panrc['hostname'] = hostname
        if api_key is not None:
            init_panrc['api_key'] = api_key

        try:
            panrc = pan.rc.PanRc(debug=self.debug,
                                 tag=self.tag,
                                 init_panrc=init_panrc)
        except pan.rc.PanRcError as msg:
            raise PanWFapiError(str(msg))

        if 'api_key' in panrc.panrc:
            self.api_key = panrc.panrc['api_key']
        if 'hostname' in panrc.panrc:
            self.hostname = panrc.panrc['hostname']
        else:
            self.hostname = _cloud_server

        if self.api_key is None:
            raise PanWFapiError('api_key required')

        self.uri = 'https://%s' % self.hostname

        if self.debug2 and _legacy_urllib:
            print('using legacy urllib', file=sys.stderr)

    def __str__(self):
        return '\n'.join((': '.join((k, str(self.__dict__[k]))))
                         for k in sorted(self.__dict__))

    def __clear_response(self):
        # XXX naming
        self._msg = None
        self.http_code = None
        self.http_reason = None
        self.response_body = None
        self.response_type = None
        self.xml_element_root = None
        self.attachment = None

    def __get_header(self, response, name):
        """use getheader() method depending or urllib in use"""

        s = None
        body = set()

        if hasattr(response, 'getheader'):
            # 3.2, http.client.HTTPResponse
            s = response.getheader(name)
        elif hasattr(response.info(), 'getheader'):
            # 2.7, httplib.HTTPResponse
            s = response.info().getheader(name)
        else:
            raise PanWFapiError('no getheader() method found in ' +
                                'urllib response')

        if s is not None:
            body = [x.lower() for x in s.split(';')]
            body = [x.lstrip() for x in body]
            body = [x.rstrip() for x in body]
            body = set(body)

        if self.debug3:
            print('__get_header(%s):' % name, s, file=sys.stderr)
            print('__get_header:', body, file=sys.stderr)

        return body

    def __set_response(self, response):
        message_body = response.read()

        content_type = self.__get_header(response, 'content-type')
        if not content_type:
            self._msg = 'no content-type response header'
            return False

        if 'application/octet-stream' in content_type:
            return self.__set_stream_response(response, message_body)

        # XXX text/xml RFC 3023
        elif ('application/xml' in content_type or
              'text/xml' in content_type):
#              'text/xml' in content_type) and
#              'charset=utf-8' in content_type):
            return self.__set_xml_response(message_body)

        elif 'text/html' in content_type:
            return self.__set_html_response(message_body)

        else:
            msg = 'no handler for content-type: %s' % content_type
            self._msg = msg
            return False

    def __set_stream_response(self, response, message_body):
        content_disposition = self.__get_header(response,
                                                'content-disposition')
        if not content_disposition:
            self._msg = 'no content-disposition response header'
            return False

        if not 'attachment' in content_disposition:
            msg = 'no handler for content-disposition: %s' % \
                content_disposition
            self._msg = msg
            return False

        filename = None
        for type in content_disposition:
            result = re.search(r'^filename=([-\w\.]+)$', type)
            if result:
                filename = result.group(1)
                break

        attachment = {}
        attachment['filename'] = filename
        attachment['content'] = message_body
        self.attachment = attachment
        return True

    def __set_xml_response(self, message_body):
        if self.debug2:
            print(message_body, file=sys.stderr)
        self.response_body = message_body.decode(_encoding)
        self.response_type = 'xml'

        # ParseError: "XML or text declaration not at start of entity"
        # fix: remove leading blank lines if exist
        _message_body = message_body
        while (_message_body[0:1] == b'\r' or
               _message_body[0:1] == b'\n'):
            _message_body = _message_body[1:]

        try:
            element = etree.fromstring(_message_body)
        except etree.ParseError as msg:
            self._msg = 'ElementTree.fromstring ParseError: %s' % msg
            return False

        self.xml_element_root = element

        return True

    def __set_html_response(self, message_body):
        if self.debug2:
            print(message_body, file=sys.stderr)
        self.response_body = message_body.decode()
        self.response_type = 'html'

        return True

    # XXX store tostring() results?
    # XXX rework this
    def xml_root(self):
        if self.xml_element_root is None:
            return None

        s = etree.tostring(self.xml_element_root, encoding=_encoding)

        if not s:
            return None

        if self.debug3:
            print('xml_root:', type(s), file=sys.stderr)
            print('xml_root.decode():', type(s.decode(_encoding)),
                  file=sys.stderr)
        return s.decode(_encoding)

    def xml_python(self):
        try:
            import pan.config
        except ImportError:
            raise PanWFapiError('xml_python() no pan.config')

        if self.xml_element_root is None:
            return None
        elem = self.xml_element_root

        try:
            conf = pan.config.PanConfig(debug=self.debug,
                                        config=elem,
                                        tags_forcelist=_tags_forcelist)
        except pan.config.PanConfigError as msg:
            raise PanWFapiError('pan.config.PanConfigError: %s' % msg)

        return conf.python()

# XXX Unicode notes
# 2.7
# decode() str (bytes) -> unicode
# encode() unicode -> str (bytes)
# encode() of str will call decode()
# 3.x
# decode() bytes -> str (unicode)
# encode() str (unicode) -> bytes
# cannot encode() bytes
# cannot decode() str

    def __api_request(self, request_uri, body, headers={}):
        url = self.uri
        url += request_uri

        if self.debug1:
            print('URL:', url, file=sys.stderr)
            print('headers:', headers, file=sys.stderr)

        # body must by type 'bytes' for 3.x
        if _isunicode(body):
            body = body.encode()

        if self.debug3:
            print('body:', repr(body), file=sys.stderr)

        request = Request(url, body, headers)

        if self.debug1:
            print('method:', request.get_method(), file=sys.stderr)
            print('headers:', request.header_items(), file=sys.stderr)

        kwargs = {
            'url': request,
            }
        # Changed in version 3.2: cafile and capath were added.
        if sys.hexversion >= 0x03020000:
            kwargs['cafile'] = self.cafile
            kwargs['capath'] = self.capath
        # Changed in version 3.3: cadefault added
        if sys.hexversion >= 0x03030000:
            kwargs['cadefault'] = True

        if self.timeout is not None:
            kwargs['timeout'] = self.timeout

        try:
            response = urlopen(**kwargs)

        # XXX handle httplib.BadStatusLine when http to port 443

        except URLError as e:
            self._msg = str(e)
            return False
        # invalid cafile, capath
        except IOError as e:
            self._msg = str(e)
            return False

        self.http_code = response.getcode()
        # XXX can we access reason in 2.7?
        if hasattr(response, 'reason'):
            # 3.2
            self.http_reason = response.reason
        elif self.http_code in responses:
            self.http_reason = responses[self.http_code]

        if self.debug2:
            print('HTTP response code:', self.http_code,
                  file=sys.stderr)
            print('HTTP response reason:', self.http_reason,
                  file=sys.stderr)
            print('HTTP response headers:', file=sys.stderr)
            print(response.info(), file=sys.stderr)

        return response

    def _read_file(self, path):
        try:
            f = open(path, 'rb')
        except IOError as e:
            msg = 'open: %s: %s' % (path, e)
            self._msg = msg
            return None

        buf = f.read()
        f.close()

        if self.debug2:
            print('path:', type(path), len(path), file=sys.stderr)
            print('path: %s size: %d' % (path, len(buf)), file=sys.stderr)
        if self.debug3:
            import hashlib
            md5 = hashlib.md5()
            md5.update(buf)
            sha256 = hashlib.sha256()
            sha256.update(buf)
            print('MD5:', md5.hexdigest(), file=sys.stderr)
            print('SHA256:', sha256.hexdigest(), file=sys.stderr)

        return buf

    def report(self,
               hash=None,
               device_id=None,
               report_id=None,
               format=None):
        self.__clear_response()

        request_uri = '/publicapi/get/report'

        query = {}
        query['apikey'] = self.api_key
        if hash is not None:
            query['hash'] = hash
        if device_id is not None:
            query['device_id'] = device_id
        if report_id is not None:
            query['report_id'] = report_id
        if format is not None:
            query['format'] = format

        response = self.__api_request(request_uri=request_uri,
                                      body=urlencode(query))
        if not response:
            raise PanWFapiError(self._msg)

        if not self.__set_response(response):
            raise PanWFapiError(self._msg)

    def sample(self,
               hash=None):
        self.__clear_response()

        request_uri = '/publicapi/get/sample'

        query = {}
        query['apikey'] = self.api_key
        if hash is not None:
            query['hash'] = hash

        response = self.__api_request(request_uri=request_uri,
                                      body=urlencode(query))
        if not response:
            raise PanWFapiError(self._msg)

        if not self.__set_response(response):
            raise PanWFapiError(self._msg)

    def pcap(self,
             hash=None):
        self.__clear_response()

        request_uri = '/publicapi/get/pcap'

        query = {}
        query['apikey'] = self.api_key
        if hash is not None:
            query['hash'] = hash

        response = self.__api_request(request_uri=request_uri,
                                      body=urlencode(query))
        if not response:
            raise PanWFapiError(self._msg)

        if not self.__set_response(response):
            raise PanWFapiError(self._msg)

    def submit(self,
               file=None,
               url=None):
        self.__clear_response()

        if (file is not None and url is not None):
            raise PanWFapiError('must submit file or url, not both')

        if file is not None:
            request_uri = '/publicapi/submit/file'
        elif url is not None:
            request_uri = '/publicapi/submit/url'
        else:
            raise PanWFapiError('file or url not specified')

        form = _MultiPartFormData(debug=self.debug)
        form.add_field('apikey', self.api_key)
        if file is not None:
            buf = self._read_file(file)
            if buf is None:
                raise PanWFapiError(self._msg)
            filename = os.path.basename(file)
            form.add_file(filename, buf)

        if url is not None:
            form.add_field('url', url)

        headers = form.http_headers()
        body = form.http_body()

        response = self.__api_request(request_uri=request_uri,
                                      body=body, headers=headers)
        if not response:
            raise PanWFapiError(self._msg)

        if not self.__set_response(response):
            raise PanWFapiError(self._msg)


# Minimal RFC 2388 implementation

# Content-Type: multipart/form-data; boundary=___XXX
#
# Content-Disposition: form-data; name="apikey"
#
# XXXkey
# --___XXX
# Content-Disposition: form-data; name="file"; filename="XXXname"
# Content-Type: application/octet-stream
#
# XXXfilecontents
#--___XXX--

class _MultiPartFormData:
    def __init__(self, debug=0):
        self.debug = debug
        self.parts = []
        self.boundary = self._boundary()

    def add_field(self, name, value):
        part = _FormDataPart(debug=self.debug,
                             name=name,
                             body=value)
        self.parts.append(part)

    def add_file(self, filename=None, body=None):
        part = _FormDataPart(debug=self.debug,
                             name='file')
        if filename is not None:
            part.append_header('filename', filename)
        if body is not None:
            part.add_header(b'Content-Type: application/octet-stream')
            part.add_body(body)
        self.parts.append(part)

    def _boundary(self):
        rand_bytes = 48
        prefix_char = b'_'
        prefix_len = 16

        import base64
        try:
            import os
            seq = os.urandom(rand_bytes)
            if self.debug:
                print('_MultiPartFormData._boundary:', 'using os.urandom',
                      file=sys.stderr)
        except NotImplementedError:
            import random
            if self.debug:
                print('_MultiPartFormData._boundary:', 'using random',
                      file=sys.stderr)
            seq = bytearray()
            [seq.append(random.randrange(256)) for i in range(rand_bytes)]

        prefix = prefix_char * prefix_len
        boundary = prefix + base64.b64encode(seq)

        return boundary

    def http_headers(self):
        # headers cannot be bytes
        boundary = self.boundary.decode('ascii')
        headers = {
            'Content-Type':
                'multipart/form-data; boundary=' + boundary,
            }

        return headers

    def http_body(self):
        bio = BytesIO()

        boundary = b'--' + self.boundary
        for part in self.parts:
            bio.write(boundary)
            bio.write(b'\r\n')
            bio.write(part.serialize())
            bio.write(b'\r\n')
        bio.write(boundary)
        bio.write(b'--')

        return bio.getvalue()


class _FormDataPart:
    def __init__(self, debug=0, name=None, body=None):
        self.debug = debug
        self.headers = []
        self.add_header(b'Content-Disposition: form-data')
        self.append_header('name', name)
        self.body = None
        if body is not None:
            self.add_body(body)

    def add_header(self, header):
        self.headers.append(header)
        if self.debug:
            print('_FormDataPart.add_header:', self.headers[-1],
                  file=sys.stderr)

    def append_header(self, name, value):
        self.headers[-1] += b'; ' + self._encode_field(name, value)
        if self.debug:
            print('_FormDataPart.append_header:', self.headers[-1],
                  file=sys.stderr)

    def _encode_field(self, name, value):
        if self.debug:
            print('_FormDataPart._encode_field:', type(name), type(value),
                  file=sys.stderr)
        if not _rfc2231_encode:
            s = '%s="%s"' % (name, value)
            if self.debug:
                print('_FormDataPart._encode_field:', type(s), s,
                      file=sys.stderr)
            if _isunicode(s):
                s = s.encode('utf-8')
                if self.debug:
                    print('_FormDataPart._encode_field:', type(s), s,
                          file=sys.stderr)
            return s

        if not [ch for ch in '\r\n\\' if ch in value]:
            try:
                return ('%s="%s"' % (name, value)).encode('ascii')
            except UnicodeEncodeError:
                if self.debug:
                    print('UnicodeEncodeError 3.x', file=sys.stderr)
            except UnicodeDecodeError:  # 2.x
                if self.debug:
                    print('UnicodeDecodeError 2.x', file=sys.stderr)
        # RFC 2231
        value = email.utils.encode_rfc2231(value, 'utf-8')
        return ('%s*=%s' % (name, value)).encode('ascii')

    def add_body(self, body):
        if _isunicode(body):
            body = body.encode('latin-1')
        self.body = body
        if self.debug:
            print('_FormDataPart.add_body:', type(self.body), len(self.body),
                  file=sys.stderr)

    def serialize(self):
        bio = BytesIO()
        bio.write(b'\r\n'.join(self.headers))
        bio.write(b'\r\n\r\n')
        if self.body is not None:
            bio.write(self.body)

        return bio.getvalue()

if __name__ == '__main__':
    # python -m pan.wfapi [tag] [sha256] [0-3]
    import pan.wfapi

    tag = None
    sha256 = '5f31d8658a41aa138ada548b7fb2fc758219d40b557aaeab80681d314f739f92'
    debug = 0

    if len(sys.argv) > 1 and sys.argv[1]:
        tag = sys.argv[1]
    if len(sys.argv) > 2:
        hash = sys.argv[2]
    if len(sys.argv) > 3 and int(sys.argv[3]):
        debug = int(sys.argv[3])

    try:
        wfapi = pan.wfapi.PanWFapi(debug=debug,
                                   tag=tag)
    except pan.wfapi.PanWFapiError as msg:
        print('pan.wfapi.PanWFapi:', msg, file=sys.stderr)
        sys.exit(1)

    try:
        wfapi.report(hash=sha256)

    except pan.wfapi.PanWFapiError as msg:
        print('report: %s' % msg, file=sys.stderr)
        sys.exit(1)

    if (wfapi.response_body is not None):
        print(wfapi.response_body)
