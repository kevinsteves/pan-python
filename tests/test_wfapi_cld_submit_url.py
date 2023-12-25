import hashlib
import os
import sys
import time
import unittest
import xml.etree.ElementTree as etree

from . import wfapi_mixin

libpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(libpath, os.pardir, 'lib')]
import pan.wfapi


class PanWFapiTest(wfapi_mixin.Mixin, unittest.TestCase):
    def test_01(self):
        url = 'https://wildfire.paloaltonetworks.com/publicapi/test/pe'
        self.api.submit(url=url)
        self.assertEqual(self.api.http_code, 200)
        root = etree.fromstring(self.api.response_body)
        x = root.find('./upload-file-info/sha256')
        sha256 = x.text
        print('testfile SHA256 %s ' % sha256, end='', flush=True)

        elapsed = 0
        wait = 30
        maximum = 60 * 5

        while True:
            time.sleep(wait)
            elapsed += wait
            self.api.verdict(hash=sha256)
            self.assertEqual(self.api.http_code, 200)
            root = etree.fromstring(self.api.response_body)
            x = root.find('./get-verdict-info/verdict')
            verdict = int(x.text)
            if verdict == pan.wfapi.MALWARE:
                break
            elif verdict == pan.wfapi.PENDING:
                pass
            else:
                self.fail('%s invalid verdict %d' % (sha256, verdict))
            if elapsed >= maximum:
                self.fail('%s no verdict in analysis window of %d seconds' % (
                    sha256, elapsed))

        elapsed = 0

        while True:
            time.sleep(wait)
            elapsed += wait
            try:
                self.api.report(hash=sha256)
            except pan.wfapi.PanWFapiError:
                if self.api.http_code == 404:
                    if elapsed >= maximum:
                        self.fail('%s no report available after %d seconds' % (
                            sha256, elapsed))
                    else:
                        continue
            else:
                break

        self.assertEqual(self.api.http_code, 200)
        self.assertEqual(self.api.response_type, 'xml')

        self.api.report(hash=sha256, format='maec')
        self.assertEqual(self.api.http_code, 200)
        self.assertEqual(self.api.response_type, 'json')

        self.api.report(hash=sha256, format='pdf')
        self.assertEqual(self.api.http_code, 200)
        self.assertIsNotNone(self.api.attachment)
        self.assertEqual(self.api.attachment['filename'], sha256 + '.pdf')

        self.api.sample(hash=sha256)
        self.assertEqual(self.api.http_code, 200)
        self.assertIsNotNone(self.api.attachment)
        self.assertEqual(self.api.attachment['filename'], sha256 + '.exe.000')
        digest = hashlib.sha256(self.api.attachment['content']).hexdigest()
        self.assertEqual(sha256, digest)

        self.api.pcap(hash=sha256)
        self.assertEqual(self.api.http_code, 200)
        self.assertIsNotNone(self.api.attachment)
        self.assertTrue(self.api.attachment['filename'].startswith(sha256))
