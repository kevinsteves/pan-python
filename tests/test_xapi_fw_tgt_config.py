import os
import sys
import unittest

from . import xapi_mixin

libpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(libpath, os.pardir, 'lib')]
import pan.xapi

BASE_XPATH = ("/config/devices/entry[@name='localhost.localdomain']"
              "/vsys/entry[@name='vsys1']/address")
XPATH_ADDR = BASE_XPATH + "/entry[@name='%s']"
IP_ADDRESS = '192.0.2.1/32'
ELEMENT = '<ip-netmask>%s</ip-netmask>' % IP_ADDRESS
ELEMENT_PATH = './result/entry/ip-netmask'


class PanXapiTest(xapi_mixin.Mixin, unittest.TestCase):
    def test_01(self):
        address = self.name('address', 16)
        xpath = XPATH_ADDR % address

        self.api.get(xpath=xpath)
        self.assertEqual(self.api.status, 'success')
        self.assertEqual(self.api.status_code, '7')
        x = self.api.element_root.find('./result')
        self.assertIsNotNone(x)
        self.assertEqual(len(x), 0)

        with self.assertRaises(pan.xapi.PanXapiError) as e:
            self.api.show(xpath=xpath)
        self.assertEqual(self.api.status, 'error')
        msg = 'No such node'
        self.assertEqual(str(e.exception), msg)
        self.assertEqual(self.api.status_detail, msg)

        self.api.set(element=ELEMENT, xpath=xpath)
        self.assertEqual(self.api.status, 'success')

        self.api.get(xpath=xpath)
        self.assertEqual(self.api.status, 'success')
        self.assertEqual(self.api.status_code, '19')
        x = self.api.element_root.find(ELEMENT_PATH)
        self.assertIsNotNone(x)
        self.assertEqual(x.text, IP_ADDRESS)

        address1 = address + '-1'
        self.api.clone(xpath_from=xpath,
                       xpath=BASE_XPATH,
                       newname=address1)
        self.assertEqual(self.api.status, 'success')

        xpath1 = XPATH_ADDR % address1
        self.api.get(xpath=xpath)
        self.assertEqual(self.api.status, 'success')
        self.assertEqual(self.api.status_code, '19')
        x = self.api.element_root.find(ELEMENT_PATH)
        self.assertIsNotNone(x)
        self.assertEqual(x.text, IP_ADDRESS)

        address2 = address + '-2'
        self.api.rename(xpath=xpath1,
                        newname=address2)
        self.assertEqual(self.api.status, 'success')

        xpath2 = XPATH_ADDR % address2
        self.api.get(xpath=xpath)
        self.assertEqual(self.api.status, 'success')
        self.assertEqual(self.api.status_code, '19')
        x = self.api.element_root.find(ELEMENT_PATH)
        self.assertIsNotNone(x)
        self.assertEqual(x.text, IP_ADDRESS)

        for path in [xpath, xpath2]:
            self.api.delete(xpath=path)
            self.assertEqual(self.api.status, 'success')

        for path in [xpath, xpath2]:
            self.api.get(xpath=path)
            self.assertEqual(self.api.status, 'success')
            self.assertEqual(self.api.status_code, '7')
            x = self.api.element_root.find('./result')
            self.assertIsNotNone(x)
            self.assertEqual(len(x), 0)
