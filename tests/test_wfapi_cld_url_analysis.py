import json
import os
import random
import sys
import unittest

from . import wfapi_mixin

libpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(libpath, os.pardir, 'lib')]
import pan.wfapi

VERDICTS = [
    pan.wfapi.BENIGN,
    pan.wfapi.MALWARE,
    pan.wfapi.GRAYWARE,
    pan.wfapi.PHISHING,
    pan.wfapi.C2,
]


class PanWFapiTest(wfapi_mixin.Mixin, unittest.TestCase):
    def test_01(self):
        tests = 0
        tests_total = 30
        skipped = 0

        start = 1000
        stop = start + 10000

        while True:
            ip = random.randrange(start, stop)
            url = 'http://%d/' % ip

            self.api.verdict(url=url)
            self.assertEqual(self.api.http_code, 200)
            self.assertEqual(self.api.response_type, 'xml')
            self.assertIsNotNone(self.api.xml_element_root)
            x = self.api.xml_element_root.find('get-verdict-info/verdict')
            verdict = int(x.text)
            if verdict not in VERDICTS:
                skipped += 1
                continue

            self.api.report(url=url)
            self.assertEqual(self.api.http_code, 200)
            self.assertEqual(self.api.response_type, 'json')
            x = json.loads(self.api.response_body)
            try:
                report_str = x['result']['report']
            except KeyError as e:
                self.fail(e)
            report = json.loads(report_str)
            self.assertIn('verdict', report)
            self.assertEqual(pan.wfapi.VERDICTS[verdict][0],
                             report['verdict'], url)

            tests += 1
            if tests > tests_total:
                break
