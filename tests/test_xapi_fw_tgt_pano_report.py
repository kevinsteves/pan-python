import os
import sys
import unittest

from . import xapi_mixin

libpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(libpath, os.pardir, 'lib')]
import pan.xapi


class PanXapiTest(xapi_mixin.Mixin, unittest.TestCase):
    def test_01(self):
        self.api.report(reporttype='dynamic',
                        reportname='top-applications-summary',
                        extra_qs={'period': 'last-hour',
                                  'topn': 5})
        self.assertEqual(self.api.status, 'success')
        x = self.api.element_root.find('./result/report')
        self.assertIsNotNone(x)
        self.assertIn('name', x.attrib)
        self.assertEqual(x.attrib['name'], 'Top applications')
        self.assertIn('start-epoch', x.attrib)
        self.assertIn('end-epoch', x.attrib)
        start = int(x.attrib['start-epoch'])
        end = int(x.attrib['end-epoch'])
        self.assertEqual(end - start, 3599)
