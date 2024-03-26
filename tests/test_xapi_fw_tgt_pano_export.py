import os
import sys
import unittest

from . import xapi_mixin

libpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(libpath, os.pardir, 'lib')]
import pan.xapi


class PanXapiTest(xapi_mixin.Mixin, unittest.TestCase):
    def test_01(self):
        self.api.export(category='configuration')
        self.assertEqual(self.api.status, 'success')
        x = self.api.element_root.find('./mgt-config')
        self.assertIsNotNone(x)

    def test_02(self):
        name = '0041_Entrust.net_Certification_Authority_(2048)'
        kwargs = {
            'category': 'certificate',
            'extra_qs': {
                'certificate-name': name,
                'format': 'pem',
                'include-key': 'no',
            },
        }

        self.api.export(**kwargs)
        self.assertEqual(self.api.status, 'success')
        self.assertIsNotNone(self.api.export_result)
        self.assertIsNotNone(self.api.export_result['file'])
        self.assertIsNotNone(self.api.export_result['content'])
        x = name.lower() + '.pem'
        self.assertEqual(self.api.export_result['file'], x)
