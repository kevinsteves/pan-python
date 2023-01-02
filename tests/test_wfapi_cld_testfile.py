import os
import sys
import unittest

from . import wfapi_mixin

libpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(libpath, os.pardir, 'lib')]
import pan.wfapi


class PanWFapiTest(wfapi_mixin.Mixin, unittest.TestCase):
    def test_01(self):
        with self.assertRaises(pan.wfapi.PanWFapiError) as e:
            self.api.testfile(file_type='x-invalid')
        self.assertEqual(self.api.http_code, 404)
        self.assertIsNone(self.api.attachment, None)

    def test_02(self):
        file_types = [
            (None, 'wildfire-test-pe-file.exe'),
            ('pe', 'wildfire-test-pe-file.exe'),
            ('macos', 'wildfire-test-macos-file'),
            ('apk', 'wildfire-test-apk-file.apk'),
            ('elf', 'wildfire-test-elf-file'),
        ]

        for type_ in file_types:
            self.api.testfile(file_type=type_[0])
        self.assertEqual(self.api.http_code, 200)
        self.assertEqual(self.api.attachment['filename'], type_[1])
