import hashlib
import os
import sys
import tempfile
import unittest
import xml.etree.ElementTree as etree

from . import wfapi_mixin

libpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(libpath, os.pardir, 'lib')]
import pan.wfapi

# known sample
helloworld = b"document.write('Hello, World!');\n"


class PanWFapiTest(wfapi_mixin.Mixin, unittest.TestCase):
    def test_01(self):
        digest_sha256 = hashlib.sha256(helloworld).hexdigest()
        digest_md5 = hashlib.md5(helloworld).hexdigest()
        fd, path = tempfile.mkstemp(prefix='wildfire-tempfile',
                                    suffix='.js')
        os.write(fd, helloworld)

        try:
            self.api.submit(file=path)
        finally:
            os.unlink(path)

        self.assertEqual(self.api.http_code, 200)
        root = etree.fromstring(self.api.response_body)
        sha256 = root.find('./upload-file-info/sha256').text
        self.assertEqual(digest_sha256, sha256)
        md5 = root.find('./upload-file-info/md5').text
        self.assertEqual(digest_md5, md5)

        # XXX delay for appliance?
        for hash in [sha256, md5]:
            self.api.verdict(hash=hash)
            self.assertEqual(self.api.http_code, 200)
            root = etree.fromstring(self.api.response_body)
            verdict = root.find('./get-verdict-info/verdict').text
            self.assertEqual(int(verdict), pan.wfapi.BENIGN)
