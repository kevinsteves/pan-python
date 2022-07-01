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
