import hashlib
import os
import sys
import unittest
import xml.etree.ElementTree as etree

from . import wfapi_mixin

libpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(libpath, os.pardir, 'lib')]
import pan.wfapi


class PanWFapiTest(wfapi_mixin.Mixin, unittest.TestCase):
    @staticmethod
    def hashes(total):
        x = []
        data = 1
        while data <= total:
            if data % 3 == 0:
                hash = str(data)
            elif data % 2 == 0:
                hash = hashlib.md5(str(data).encode()).hexdigest()
            else:
                hash = hashlib.sha256(str(data).encode()).hexdigest()
            x.append(hash)
            data += 1
        return x

    def test_01(self):
        with self.assertRaises(pan.wfapi.PanWFapiError) as e:
            self.api.submit(links=[])
        self.assertEqual(str(e.exception),
                         'must submit one of file, url or links')

    def test_02(self):
        tests = [
            [''],
            ['ftp://foo'],
            ['sftp://foo'],
        ]

        for links in tests:
            with self.assertRaises(pan.wfapi.PanWFapiError) as e:
                self.api.submit(links=links)
            self.assertEqual(self.api.http_code, 421, str(e.exception))
            self.assertEqual(self.api.response_type, 'xml')
            root = etree.fromstring(self.api.response_body)
            x = root.find('./error-message')
            s = ("'Invalid webpage type url, url should "
                 "start with http or https'")
            self.assertEqual(x.text, s)

    def test_03(self):
        tests = [
            ['\0'],
            [' '],
            ['foo'],
            ['http://foo'],
            ['https://foo'],
        ]

        for links in tests:
            self.api.submit(links=links)
            self.assertEqual(self.api.http_code, 200)
            self.assertEqual(self.api.response_type, 'xml')
            root = etree.fromstring(self.api.response_body)
            x = root.findall('./submit-link-info')
            self.assertEqual(len(x), 1)
            link = links[0]
            if not link.startswith(('http://', 'https://')):
                link = 'http://' + link
            link = link.encode()
            digest_sha256 = hashlib.sha256(link).hexdigest()
            digest_md5 = hashlib.md5(link).hexdigest()
            url = x[0].find('./url').text
            msg = '%s %s' % (link, url)
            sha256 = x[0].find('./sha256').text
            self.assertEqual(digest_sha256, sha256, msg=msg)
            md5 = x[0].find('./md5').text
            self.assertEqual(digest_md5, md5, msg=msg)

    def test_04(self):
        for total in [999, 1000]:
            links = self.hashes(total)
            self.api.submit(links=links)
            self.assertEqual(self.api.http_code, 200)
            self.assertEqual(self.api.response_type, 'xml')
            root = etree.fromstring(self.api.response_body)
            x = root.findall('./submit-link-info')
            self.assertEqual(len(x), total)

        links = self.hashes(1001)
        with self.assertRaises(pan.wfapi.PanWFapiError) as e:
            self.api.submit(links=links)
        self.assertEqual(self.api.http_code, 422, str(e.exception))
        self.assertEqual(self.api.response_type, 'xml')
        root = etree.fromstring(self.api.response_body)
        x = root.find('./error-message')
        s = "'File contains too many entities, maxium 1000 entities allowed'"
        self.assertEqual(x.text, s)
