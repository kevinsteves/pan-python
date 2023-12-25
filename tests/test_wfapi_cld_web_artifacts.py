import io
import os
import sys
import tarfile
import unittest

from . import wfapi_mixin

libpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(libpath, os.pardir, 'lib')]
import pan.wfapi

URL = 'https://www.google.com'


class PanWFapiTest(wfapi_mixin.Mixin, unittest.TestCase):
    def test_01(self):
        with self.assertRaises(pan.wfapi.PanWFapiError) as e:
            self.api.web_artifacts()
        self.assertEqual(self.api.http_code, 420)

    def test_02(self):
        with self.assertRaises(pan.wfapi.PanWFapiError) as e:
            self.api.web_artifacts(url='')
        self.assertEqual(self.api.http_code, 421)

    def test_03(self):
        with self.assertRaises(pan.wfapi.PanWFapiError) as e:
            self.api.web_artifacts(url='0.0.0.0.0')
        self.assertEqual(self.api.http_code, 404)

    def test_04(self):
        for types in [None,
                      'screenshot,download_files',
                      'download_files,screenshot',
                      'download_files, screenshot',
                      ]:
            self.api.web_artifacts(url=URL, types=types)
            self.assertEqual(self.api.http_code, 200)
            self.assertIsNotNone(self.api.attachment)

            obj = io.BytesIO(self.api.attachment['content'])
            tar = tarfile.open(fileobj=obj)
            files = tar.getnames()
            self.assertIn('screenshot', files)
            self.assertIn('download_files', files)

    def test_05(self):
        self.api.web_artifacts(url=URL, types='screenshot')
        self.assertEqual(self.api.http_code, 200)
        self.assertIsNotNone(self.api.attachment)

        obj = io.BytesIO(self.api.attachment['content'])
        tar = tarfile.open(fileobj=obj)
        files = tar.getnames()
        self.assertIn('screenshot', files)
        self.assertNotIn('download_files', files)

    def test_06(self):
        self.api.web_artifacts(url=URL, types='download_files')
        self.assertEqual(self.api.http_code, 200)
        self.assertIsNotNone(self.api.attachment)

        obj = io.BytesIO(self.api.attachment['content'])
        tar = tarfile.open(fileobj=obj)
        files = tar.getnames()
        self.assertNotIn('screenshot', files)
        self.assertIn('download_files', files)
