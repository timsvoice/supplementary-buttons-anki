# -*- coding: utf-8 -*-

import unittest
import base64
import json
import time

import sys
if "/usr/share/anki/" not in sys.path:
    sys.path.append("/usr/share/anki/")
from power_format_pack.markdowner import Markdowner


class MarkdownerTester(unittest.TestCase):

    def setUp(self):
        print "Setting up MarkdownerTester..."
        Markdowner.__init__ = self.markdowner_custom__init__
        self.data = dict(id=1, md="**text**",
                         isconverted=True, lastmodified=time.time())
        b64encoded_data = base64.b64encode(json.dumps(self.data))
        self.html = u"<div></div><!----SBAdata:{}---->".format(b64encoded_data)
        self.current_field = 0
        self.markdowner = Markdowner(self.html, self.current_field)
        print self.markdowner.html

    @staticmethod
    def markdowner_custom__init__(self, html, current_field):
        self.html           = html
        self.current_field  = current_field

    def test_get_data_from_field_returns_true_when_html_contains_base64_encoded_dict(self):
        expected    = True
        result      = self.markdowner.get_data_from_field()
        self.assertEqual(expected, result)

        self.assertEqual(self.data.get("id"), self.markdowner._id)
        self.assertEqual(self.data.get("md"), self.markdowner.md)
        self.assertNotIn("html", self.data)
        self.assertEqual(self.data.get("isconverted"), self.markdowner.isconverted)
        self.assertEqual(self.data.get("lastmodified"), self.markdowner._lastmodified)

    def test_get_data_from_field_returns_false_when_html_contains_corrupted_data(self):
        corrupted_data  = u"randomtext"
        html            = u"<div></div><!----SBAdata:{}---->".format(corrupted_data)
        markdowner      = Markdowner(html, 0)
        expected        = False
        result          = markdowner.get_data_from_field()
        self.assertEqual(expected, result)

        self.assertRaises(AttributeError, getattr, markdowner, "_id")
        self.assertRaises(AttributeError, getattr, markdowner, "md")
        self.assertRaises(AttributeError, getattr, markdowner, "_html")
        self.assertRaises(AttributeError, getattr, markdowner, "isconverted")
        self.assertRaises(AttributeError, getattr, markdowner, "_lastmodified")
