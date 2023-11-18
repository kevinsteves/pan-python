import os
import sys
import unittest
import xml.etree.ElementTree as etree

from . import xapi_mixin

libpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(libpath, os.pardir, 'lib')]
import pan.xapi

BASE_XPATH = ("/config/devices/entry[@name='localhost.localdomain']"
              "/vsys/entry[@name='vsys1']/address")
XPATH_ADDR = BASE_XPATH + "/entry[@name='%s']"
IP_ADDRESS1 = '192.0.2.1/32'
IP_ADDRESS2 = '192.0.2.2/32'
IP_ADDRESS3 = '192.0.2.3/32'
ELEMENT_PATH = './result/entry/ip-netmask'


def multi_config(actions):
    root = etree.Element('multi-config')
    id = 100
    for _action, attributes, element in actions:
        if 'id' not in attributes:
            id += 1
            attributes.update({'id': str(id)})
        action = etree.SubElement(root, _action, attributes)
        if element is not None:
            action.append(element)

    document = etree.tostring(root, encoding='UTF-8')

    return document


class PanXapiTest(xapi_mixin.Mixin, unittest.TestCase):
    def test_01(self):
        address = self.name('address', 16)
        xpath = XPATH_ADDR % address
        element = etree.Element('ip-netmask')
        element.text = IP_ADDRESS1

        actions = [
            ('set', {'xpath': xpath}, element),
        ]
        document = multi_config(actions)
        self.api.multi_config(element=document)
        self.assertEqual(self.api.status, 'success', msg=document)

        self.api.get(xpath=xpath)
        self.assertEqual(self.api.status, 'success')
        self.assertEqual(self.api.status_code, '19')
        x = self.api.element_root.find(ELEMENT_PATH)
        self.assertIsNotNone(x)
        self.assertEqual(x.text, IP_ADDRESS1)

        actions = [
            ('delete', {'xpath': xpath}, None),
        ]
        document = multi_config(actions)
        self.api.multi_config(element=document)
        self.assertEqual(self.api.status, 'success', msg=document)

        self.api.get(xpath=xpath)
        self.assertEqual(self.api.status, 'success')
        self.assertEqual(self.api.status_code, '7')
        x = self.api.element_root.find('./result')
        self.assertIsNotNone(x)
        self.assertEqual(len(x), 0)

    def test_02(self):
        # set addr1, then set addr2 (valid), addr3 (invalid).
        # with strict-transactional, addr1 rolled back,
        # addr2 rolled back due to addr3 error.

        address1 = self.name('address1', 16)
        xpath1 = XPATH_ADDR % address1
        element1 = etree.Element('ip-netmask')
        element1.text = IP_ADDRESS1

        actions = [
            ('set', {'xpath': xpath1}, element1),
        ]
        document = multi_config(actions)
        self.api.multi_config(element=document)
        self.assertEqual(self.api.status, 'success', msg=document)

        self.api.get(xpath=xpath1)
        self.assertEqual(self.api.status, 'success')
        self.assertEqual(self.api.status_code, '19')
        x = self.api.element_root.find(ELEMENT_PATH)
        self.assertIsNotNone(x)
        self.assertEqual(x.text, IP_ADDRESS1)

        address2 = self.name('address2', 16)
        xpath2 = XPATH_ADDR % address2
        element2 = etree.Element('ip-netmask')
        element2.text = IP_ADDRESS2

        address3 = self.name('address3', 32)  # error, max length 63
        xpath3 = XPATH_ADDR % address3
        element3 = etree.Element('ip-netmask')
        element3.text = IP_ADDRESS3

        actions = [
            ('set', {'xpath': xpath2}, element2),
            ('set', {'xpath': xpath3,
                     'id': 'LEN-ERROR'}, element3),  # error
        ]
        document = multi_config(actions)
        with self.assertRaises(pan.xapi.PanXapiError) as e:
            self.api.multi_config(element=document, strict=True)
        self.assertEqual(self.api.status, 'error', msg=document)
        msg = ('status="error" code="12" id="LEN-ERROR"  %s '
               'can be at most 63 characters, but current length: 64')
        msg = msg % address3
        self.assertIn(msg, self.api.status_detail)

        for xpath in [xpath1, xpath2, xpath3]:
            self.api.get(xpath=xpath)
            self.assertEqual(self.api.status, 'success')
            self.assertEqual(self.api.status_code, '7')
            x = self.api.element_root.find('./result')
            self.assertIsNotNone(x)
            self.assertEqual(len(x), 0)
