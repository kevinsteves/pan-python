import os
import sys
import unittest

from . import xapi_mixin

libpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(libpath, os.pardir, 'lib')]
import pan.xapi


class PanXapiTest(xapi_mixin.Mixin, unittest.TestCase):
    def test_01(self):
        self.api.log(log_type='config', nlogs=1)
        self.assertEqual(self.api.status, 'success')
        self.assertEqual(self.api.status_code, '19')
        x = self.api.element_root.find('./result/log/logs')
        self.assertIsNotNone(x)
        self.assertIn('count', x.attrib)
        self.assertEqual(x.attrib['count'], '1')

        x = x.find('./entry/type')
        self.assertIsNotNone(x)
        self.assertEqual(x.text, 'CONFIG')

    def test_02(self):
        self.api.log(log_type='config', filter='( cmd eq delete )')
        self.assertEqual(self.api.status, 'success')
        self.assertEqual(self.api.status_code, '19')
        x = self.api.element_root.findall('./result/log/logs/entry')
        self.assertIsNotNone(x)
        for entry in x:
            self.assertEqual(entry.find('./cmd').text, 'delete')
