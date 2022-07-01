import os
import sys
import unittest
import xml.etree.ElementTree as etree

from . import xapi_mixin

libpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(libpath, os.pardir, 'lib')]
import pan.xapi


def ip_user(cmd, user, ip):
    root = etree.Element('uid-message')
    type_ = etree.SubElement(root, 'type')
    type_.text = 'update'
    payload = etree.SubElement(type_, 'payload')
    command = etree.SubElement(payload, cmd)
    entry = etree.SubElement(command, 'entry',
                             {'name': user,
                              'ip': ip})
    document = etree.tostring(root, encoding='UTF-8')

    return document


def registered_ip(cmd, tags, ip):
    root = etree.Element('uid-message')
    type_ = etree.SubElement(root, 'type')
    type_.text = 'update'
    payload = etree.SubElement(type_, 'payload')
    command = etree.SubElement(payload, cmd)
    entry = etree.SubElement(command, 'entry',
                             {'ip': ip})
    tag = etree.SubElement(entry, 'tag')
    for x in tags:
        etree.SubElement(tag, 'member').text = x

    document = etree.tostring(root, encoding='UTF-8')

    return document


class PanXapiTest(xapi_mixin.Mixin, unittest.TestCase):
    def test_01(self):
        ip = '192.0.2.1'
        document = ip_user('login',
                           self.name('user01', 8),
                           ip)
        self.api.user_id(cmd=document)
        self.assertEqual(self.api.status, 'success', msg=document)

        self.api.op(cmd_xml=True,
                    cmd='show user ip-user-mapping-mp ip "%s"' % ip)
        self.assertEqual(self.api.status, 'success')
        x = self.api.element_root.find('./result/entry/ip')
        self.assertIsNotNone(x)
        self.assertEqual(x.text, ip)

        document = ip_user('logout',
                           self.name('user01', 8),
                           ip)
        self.api.user_id(cmd=document)
        self.assertEqual(self.api.status, 'success', msg=document)

        self.api.op(cmd_xml=True,
                    cmd='show user ip-user-mapping-mp ip "%s"' % ip)
        self.assertEqual(self.api.status, 'success')
        x = self.api.element_root.find('./result/entry/ip')
        self.assertIsNone(x)

    def test_02(self):
        ip = '192.0.2.1'
        tags = [
            self.name('tag01', 8),
            self.name('tag02', 8),
        ]
        document = registered_ip('register',
                                 tags,
                                 ip)
        self.api.user_id(cmd=document)
        self.assertEqual(self.api.status, 'success', msg=document)

        self.api.op(cmd_xml=True,
                    cmd='show object registered-ip ip "%s"' % ip)
        self.assertEqual(self.api.status, 'success')
        x = self.api.element_root.find('./result/entry')
        self.assertIsNotNone(x)
        self.assertIn('ip', x.attrib)
        self.assertEqual(x.attrib['ip'], ip)

        document = ip_user('unregister',
                           tags,
                           ip)
        self.api.user_id(cmd=document)
        self.assertEqual(self.api.status, 'success', msg=document)

        self.api.op(cmd_xml=True,
                    cmd='show object registered-ip ip "%s"' % ip)
        self.assertEqual(self.api.status, 'success')
        x = self.api.element_root.find('./result/entry')
        self.assertIsNone(x)
