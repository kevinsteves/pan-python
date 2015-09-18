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

import json
import logging
import re
import sys

from .. import __version__, DEBUG1, DEBUG2, DEBUG3
import pan.rc
import pan.http
from pan.afapi import PanAFapiError

_cloud_server = 'autofocus.paloaltonetworks.com'


class PanAFapi:
    def __init__(self,
                 api_version=None,
                 panrc_tag=None,
                 hostname=None,
                 api_key=None,
                 timeout=None,
                 verify_cert=True):
        self._log = logging.getLogger(__name__).log
        self.api_version = api_version
        self.panrc_tag = panrc_tag
        self.hostname = hostname
        self.api_key = api_key
        self.timeout = timeout
        self.verify_cert = verify_cert

        self._log(DEBUG3, 'Python version: %s', sys.version)
        self._log(DEBUG3, 'pan-python version: %s', __version__)

        init_panrc = {}  # .panrc args from constructor
        if hostname is not None:
            init_panrc['hostname'] = hostname
        if api_key is not None:
            init_panrc['api_key'] = api_key

        try:
            panrc = pan.rc.PanRc(tag=self.panrc_tag,
                                 init_panrc=init_panrc)
        except pan.rc.PanRcError as e:
            raise PanAFapiError(e)

        if 'api_key' in panrc.panrc:
            self.api_key = panrc.panrc['api_key']
        if 'hostname' in panrc.panrc:
            self.hostname = panrc.panrc['hostname']
        else:
            self.hostname = _cloud_server

        if self.api_key is None:
            raise PanAFapiError('api_key required')

        self.uri = 'https://' + self.hostname
        self.base_uri = self.uri + '/api/' + str(api_version)
        self.headers = {'content-type': 'application/json'}

        try:
            self.http = pan.http.PanHttp(timeout=self.timeout,
                                         verify_cert=self.verify_cert)
        except pan.http.PanHttpError as e:
            raise PanAFapiError(e)

        if self.http.using_requests:
            s = 'using requests %s' % self.http.requests_version
        else:
            s = 'using urllib'
        self._log(DEBUG2, s)

    def _init_attributes(self):
        self.http_code = None
        self.http_reason = None
        self.http_headers = None
        self.http_encoding = None
        self.http_content = None
        self.http_text = None
        self.json = None

    def _set_attributes(self):
        self.http_code = self.http.code
        self.http_reason = self.http.reason
        self.http_headers = self.http.headers
        self.http_encoding = self.http.encoding
        if self.http_encoding is None:
            self.http_encoding = 'utf8'
        self.http_content = self.http.content
        self.http_text = self.http.text
        if self.http_headers is not None:
            x = self.http_headers.get('content-type')
            if x is not None and x.startswith('application/json'):
                try:
                    self.json = json.loads(self.http_text)
                except ValueError as e:
                    self._log(DEBUG1, 'json.loads: ', e)
        self._log(DEBUG3, self.http.text)

    def _set_apikey(self, data):
        try:
            obj = json.loads(data)
            obj['apiKey'] = self.api_key
            return json.dumps(obj)
        except ValueError as e:
            raise PanAFapiError(str(e))

    def _api_request(self, url, headers, data, params=None):
        self._log(DEBUG1, url)
        if params is not None:
            self._log(DEBUG1, params)
        self._log(DEBUG1, data)

        self._init_attributes()
        data = self._set_apikey(data)

        try:
            self.http.http_request(url=url,
                                   headers=self.headers,
                                   data=data,
                                   params=params)
        except pan.http.PanHttpError as e:
            self._set_attributes()
            raise PanAFapiError(str(e))

        self._set_attributes()

    def samples_search(self, data):
        endpoint = '/samples/search/'
        url = self.base_uri + endpoint
        self._api_request(url, self.headers, data)

    def samples_results(self, jobid):
        endpoint = '/samples/results/'
        url = self.base_uri + endpoint + jobid
        self._api_request(url, self.headers, '{}')

    def sessions_search(self, data):
        endpoint = '/sessions/search/'
        url = self.base_uri + endpoint
        self._api_request(url, self.headers, data)

    def sessions_results(self, jobid):
        endpoint = '/sessions/results/'
        url = self.base_uri + endpoint + jobid
        self._api_request(url, self.headers, '{}')

    def sessions_histogram_search(self, data, scope=None):
        endpoint = '/sessions/histogram/search/'
        url = self.base_uri + endpoint
        if scope is not None:
            url += scope
        self._api_request(url, self.headers, data)

    def sessions_histogram_results(self, jobid):
        endpoint = '/sessions/histogram/results/'
        url = self.base_uri + endpoint + jobid
        self._api_request(url, self.headers, '{}')

    def sessions_aggregate_search(self, data, scope=None):
        endpoint = '/sessions/aggregate/search/'
        url = self.base_uri + endpoint
        if scope is not None:
            url += scope
        self._api_request(url, self.headers, data)

    def sessions_aggregate_results(self, jobid):
        endpoint = '/sessions/aggregate/results/'
        url = self.base_uri + endpoint + jobid
        self._api_request(url, self.headers, '{}')

    def session(self, sessionid=None):
        endpoint = '/session/'
        if sessionid is not None:
            url = self.base_uri + endpoint + sessionid
        self._api_request(url, self.headers, '{}')

    def top_tags_search(self, data, scope=None):
        endpoint = '/top-tags/search/'
        url = self.base_uri + endpoint
        if scope is not None:
            url += scope
        self._api_request(url, self.headers, data)

    def top_tags_results(self, jobid):
        endpoint = '/top-tags/results/'
        url = self.base_uri + endpoint + jobid
        self._api_request(url, self.headers, '{}')

    def tags(self, data, query=None):
        endpoint = '/tags'
        url = self.base_uri + endpoint
        self._api_request(url, self.headers, data, query)

    def tag(self, tagname=None):
        endpoint = '/tag/'
        url = self.base_uri + endpoint
        if tagname is not None:
            url += tagname
        self._api_request(url, self.headers, '{}')

    def sample_analysis(self, data, sampleid=None):
        endpoint = '/sample/'
        url = self.base_uri + endpoint
        if sampleid is not None:
            url += sampleid + '/'
        url += 'analysis'
        self._api_request(url, self.headers, data)

    def export(self, data):
        endpoint = '/export/'
        url = self.base_uri + endpoint
        self._api_request(url, self.headers, data)
