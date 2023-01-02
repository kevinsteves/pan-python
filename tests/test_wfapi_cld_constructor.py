import hashlib
import os
import ssl
import sys
import unittest

from . import wfapi_mixin

libpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(libpath, os.pardir, 'lib')]
import pan.wfapi


class PanWFapiTest(wfapi_mixin.Mixin, unittest.TestCase):
    def test_01(self):
        with self.assertRaises(pan.wfapi.PanWFapiError) as e:
            api = pan.wfapi.PanWFapi()
        self.assertEqual(str(e.exception), 'api_key required')

    def test_02(self):
        api_key = hashlib.md5(b'panw').hexdigest()
        api = pan.wfapi.PanWFapi(api_key=api_key)
        with self.assertRaises(pan.wfapi.PanWFapiError) as e:
            api.verdict(hash=api_key)
        self.assertEqual(api.http_code, 401, str(e.exception))
        self.assertEqual(api.http_reason,
                         'Invalid API key', str(e.exception))

    def test_03(self):
        api = pan.wfapi.PanWFapi(api_key='',
                                 hostname='wildfire-x.paloaltonetworks.com')
        with self.assertRaises(pan.wfapi.PanWFapiError) as e:
            api.verdict()
        self.assertIn('no address associated with name', str(e.exception))

    def test_04(self):
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        api = pan.wfapi.PanWFapi(api_key='',
                                 ssl_context=ssl_context)
        with self.assertRaises(pan.wfapi.PanWFapiError) as e:
            api.testfile()
        self.assertIn('CERTIFICATE_VERIFY_FAILED', str(e.exception))

        ssl_context = pan.wfapi.cloud_ssl_context()
        api = pan.wfapi.PanWFapi(api_key='',
                                 ssl_context=ssl_context)
        api.testfile()
        self.assertEqual(api.http_code, 200)

    def test_05(self):
        api = pan.wfapi.PanWFapi(api_key='',
                                 http=True)
        api.testfile()
        self.assertEqual(api.http_code, 200)

        with self.assertRaises(pan.wfapi.PanWFapiError) as e:
            api.verdict()
        self.assertEqual(api.http_code, 302)
