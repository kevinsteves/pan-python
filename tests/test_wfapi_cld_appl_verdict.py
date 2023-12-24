import hashlib
import os
import sys
import unittest
import xml.etree.ElementTree as etree

from . import wfapi_mixin

libpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(libpath, os.pardir, 'lib')]
import pan.wfapi


class PanWFapiTest(wfapi_mixin.Mixin, unittest.TestCase):
    @staticmethod
    def _hash(data, type_):
        if type_ == 'sha256':
            hash = hashlib.sha256(data.encode()).hexdigest()
        elif type_ == 'md5':
            hash = hashlib.md5(data.encode()).hexdigest()
        else:
            assert False, type_
        return hash

    def test_01(self):
        with self.assertRaises(pan.wfapi.PanWFapiError) as e:
            self.api.verdict()
        self.assertEqual(self.api.http_code, 420, str(e.exception))
        self.assertEqual(self.api.response_type, 'xml')
        root = etree.fromstring(self.api.response_body)
        x = root.find('./error-message')
        self.assertEqual(x.text, "'Missing required field'")

    def test_02(self):
        with self.assertRaises(pan.wfapi.PanWFapiError) as e:
            self.api.verdict(hash='x-invalid')
        self.assertEqual(self.api.http_code, 421, str(e.exception))
        self.assertEqual(self.api.response_type, 'xml')
        root = etree.fromstring(self.api.response_body)
        x = root.find('./error-message')
        self.assertEqual(x.text, "'invalid hash value'")

    def test_03(self):
        # zero length string
        hash = self._hash('', 'sha256')
        self.api.verdict(hash=hash)
        self.assertEqual(self.api.http_code, 200)
        self.assertEqual(self.api.response_type, 'xml')
        root = etree.fromstring(self.api.response_body)
        x = root.findall('./get-verdict-info')
        self.assertTrue(len(x) == 1)
        verdict = x[0].find('./verdict').text
        self.assertEqual(int(verdict), pan.wfapi.BENIGN)
        sha256 = x[0].find('./sha256').text
        self.assertEqual(hash, sha256)
        md5 = x[0].find('./md5').text
        self.assertEqual(self._hash('', 'md5'), md5)

    def test_04(self):
        hash = self._hash('', 'md5')
        self.api.verdict(hash=hash)
        self.assertEqual(self.api.http_code, 200)
        self.assertEqual(self.api.response_type, 'xml')
        # XXX multiple verdicts with varying sha256 on cld, bug WTC-28639
        # test will fail when fixed
        root = etree.fromstring(self.api.response_body)
        x = root.findall('./get-verdict-info')
        self.assertTrue(len(x) > 1)
