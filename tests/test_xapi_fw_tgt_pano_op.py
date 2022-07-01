import os
import sys
import unittest

from . import xapi_mixin

libpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(libpath, os.pardir, 'lib')]
import pan.xapi


class PanXapiTest(xapi_mixin.Mixin, unittest.TestCase):
    def test_01(self):
        tests = [
            (True,
             'show system info',
             './result/system/serial'
             ),
            (False,
             '<show><system><info></info></system></show>',
             './result/system/devicename',
             ),
            (True,
             'show jobs all',
             './result/job/status',
             ),
            (False,
             '<show><jobs><all/></jobs></show>',
             './result/job/type',
             ),
            (True,
             'show interface "management"',
             './result/info/name',
             ),
            (False,
             '<show><interface>management</interface></show>',
             './result/counters/tx-packets',
             ),
            (True,
             'check pending-changes',
             './result',
             ),
            (False,
             '<check><pending-changes/></check>',
             './result',
             ),
        ]

        for cmd_xml, cmd, path in tests:
            self.api.op(cmd_xml=cmd_xml, cmd=cmd)
            self.assertEqual(self.api.status, 'success')
            x = self.api.element_root.find(path)
            self.assertIsNotNone(x)
            self.assertTrue(x.text)

    def test_02(self):
        with self.assertRaises(pan.xapi.PanXapiError) as e:
            self.api.op(cmd_xml=True, cmd='show jobs id "4294967295"')
        self.assertEqual(self.api.status, 'error')
        msg = 'job -1 not found'
        self.assertEqual(str(e.exception), msg)
        x = self.api.element_root.find('./msg/line')
        self.assertIsNotNone(x)
        self.assertEqual(x.text, msg)
