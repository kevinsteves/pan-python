import hashlib
import os
import random
import sys
import unittest
import xml.etree.ElementTree as etree

from . import wfapi_mixin

libpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(libpath, os.pardir, 'lib')]
import pan.wfapi


class PanWFapiTest(wfapi_mixin.Mixin, unittest.TestCase):
    @staticmethod
    def hashes(total, invalid=False):
        x = []
        data = 1
        while data <= total:
            if invalid:
                hash = data
            if data % 2:
                hash = hashlib.md5(str(data).encode()).hexdigest()
            else:
                hash = hashlib.sha256(str(data).encode()).hexdigest()
            x.append(hash)
            data += 1
        return x

    def test_01(self):
        with self.assertRaises(pan.wfapi.PanWFapiError) as e:
            self.api.verdicts()
        self.assertEqual(self.api.http_code, 420, str(e.exception))
        self.assertEqual(self.api.response_type, 'xml')
        root = etree.fromstring(self.api.response_body)
        x = root.find('./error-message')
        self.assertEqual(x.text, "'Missing required field file'")

    def test_02(self):
        with self.assertRaises(pan.wfapi.PanWFapiError) as e:
            self.api.verdicts(hashes=[])
        self.assertEqual(self.api.http_code, 422, str(e.exception))
        self.assertEqual(self.api.response_type, 'xml')
        root = etree.fromstring(self.api.response_body)
        x = root.find('./error-message')
        self.assertEqual(x.text, "'Unprocessable Entities'")

    def test_03(self):
        hashes = self.hashes(501)
        with self.assertRaises(pan.wfapi.PanWFapiError) as e:
            self.api.verdicts(hashes=hashes)
        self.assertEqual(self.api.http_code, 413, str(e.exception))
        self.assertEqual(self.api.response_type, 'xml')
        root = etree.fromstring(self.api.response_body)
        x = root.find('./error-message')
        self.assertEqual(x.text,
                         "'Only 500 entries are allowed for each file'")

    def test_04(self):
        num = 1
        hashes = self.hashes(num)
        self.api.verdicts(hashes=hashes)
        self.assertEqual(self.api.http_code, 200)
        self.assertEqual(self.api.response_type, 'xml')
        root = etree.fromstring(self.api.response_body)
        x = root.findall('./get-verdict-info')
        self.assertTrue(len(x) == num)

    def test_05(self):
        num = 1
        hashes = self.hashes(num, invalid=True)
        self.api.verdicts(hashes=hashes)
        self.assertEqual(self.api.http_code, 200)
        self.assertEqual(self.api.response_type, 'xml')
        root = etree.fromstring(self.api.response_body)
        x = root.findall('./get-verdict-info')
        self.assertTrue(len(x) == num)

    def test_06(self):
        num = random.randint(2, 499)
        hashes = self.hashes(num)
        self.api.verdicts(hashes=hashes)
        self.assertEqual(self.api.http_code, 200)
        self.assertEqual(self.api.response_type, 'xml')
        root = etree.fromstring(self.api.response_body)
        x = root.findall('./get-verdict-info')
        self.assertTrue(len(x) == num)

    def test_07(self):
        num = random.randint(2, 499)
        hashes = self.hashes(num, invalid=True)
        self.api.verdicts(hashes=hashes)
        self.assertEqual(self.api.http_code, 200)
        self.assertEqual(self.api.response_type, 'xml')
        root = etree.fromstring(self.api.response_body)
        x = root.findall('./get-verdict-info')
        self.assertTrue(len(x) == num)

    def test_08(self):
        num = 500
        hashes = self.hashes(num)
        self.api.verdicts(hashes=hashes)
        self.assertEqual(self.api.http_code, 200)
        self.assertEqual(self.api.response_type, 'xml')
        root = etree.fromstring(self.api.response_body)
        x = root.findall('./get-verdict-info')
        self.assertTrue(len(x) == num)
