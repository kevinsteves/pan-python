from datetime import date, timedelta
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
    def _date(days):
        d = date.today()
        if days < 1:
            d = d - timedelta(-days)
        else:
            d = d + timedelta(days)
        x = d.isoformat()
        return x

    def test_01(self):
        with self.assertRaises(pan.wfapi.PanWFapiError) as e:
            self.api.verdicts_changed()
        self.assertEqual(self.api.http_code, 420, str(e.exception))
        self.assertEqual(self.api.response_type, 'xml')
        root = etree.fromstring(self.api.response_body)
        x = root.find('./error-message')
        self.assertEqual(x.text, "'Missing required field date'")

    def test_02(self):
        date_ = self._date(2)
        with self.assertRaises(pan.wfapi.PanWFapiError) as e:
            self.api.verdicts_changed(date=date_)
        self.assertEqual(self.api.http_code, 403, str(e.exception))
        self.assertEqual(self.api.response_type, 'xml')
        root = etree.fromstring(self.api.response_body)
        x = root.find('./error-message')
        s = "'Invalid Date (longer than 30 days from now or newer than now)'"
        self.assertEqual(x.text, s)

    def test_03(self):
        date_ = self._date(-31)
        with self.assertRaises(pan.wfapi.PanWFapiError) as e:
            self.api.verdicts_changed(date=date_)
        self.assertEqual(self.api.http_code, 403, str(e.exception))
        self.assertEqual(self.api.response_type, 'xml')
        root = etree.fromstring(self.api.response_body)
        x = root.find('./error-message')
        s = "'Invalid Date (longer than 30 days from now or newer than now)'"
        self.assertEqual(x.text, s)

    def test_04(self):
        date_ = self._date(-1)
        self.api.verdicts_changed(date=date_)
        self.assertEqual(self.api.http_code, 200)
        self.assertEqual(self.api.response_type, 'xml')
        root = etree.fromstring(self.api.response_body)
        verdicts = root.findall('./get-verdict-info')
        self.assertGreater(len(verdicts), 0)

        sha256 = verdicts[0].find('./sha256').text
        verdict = verdicts[0].find('./verdict').text
        self.api.verdict(hash=sha256)
        self.assertEqual(self.api.http_code, 200)
        root = etree.fromstring(self.api.response_body)
        verdict2 = root.find('./get-verdict-info/verdict').text
        self.assertEqual(verdict, verdict2)
