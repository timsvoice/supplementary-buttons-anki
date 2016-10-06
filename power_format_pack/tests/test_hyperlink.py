#!/usr/bin/python2
# -*- coding: utf8 -*-

import unittest
import sys
if "/usr/share/anki/" not in sys.path:
    sys.path.append("/usr/share/anki/")
from aqt.editor import Editor
from power_format_pack.hyperlink import Hyperlink


class HyperlinkTester(unittest.TestCase):
    def setUp(self):
        print "Setting up HyperlinkTester..."
        Hyperlink.__init__ = self.hyperlink_custom__init__
        self.hyperlink = Hyperlink("text")

    def hyperlink_custom__init__(self, selected_text):
        self.selected_text = selected_text

    def test_create_anchor_should_raise_assertion_error_when_input_is_not_unicode(self):
        url  = "text"
        text = "text"
        self.assertRaises(AssertionError, self.hyperlink.create_anchor, url, text);

    def test_create_anchor_should_return_anchor_when_input_is_valid_text(self):
        url         = u"text"
        text        = u"random"
        result      = self.hyperlink.create_anchor(url, text)
        expected    = u"<a href=\"text\">random</a>"
        self.assertEqual(expected, result)

    def test_create_anchor_should_return_anchor_when_url_is_empty_string(self):
        url         = u""
        text        = u"random"
        result      = self.hyperlink.create_anchor(url, text)
        expected    = u"<a href=\"\">random</a>"
        self.assertEqual(expected, result)

    def test_create_anchor_should_return_anchor_when_url_is_russian(self):
        url         = u"ничё, пацаны, пробьёмся!"
        text        = u"random"
        result      = self.hyperlink.create_anchor(url, text)
        expected    = u"<a href=\"{0}\">{1}</a>".format(url, text)
        self.assertEqual(expected, result)

    def test_create_anchor_should_return_anchor_when_url_is_valid_url(self):
        url         = u"https://www.google.com"
        text        = u"random"
        result      = self.hyperlink.create_anchor(url, text)
        expected    = u"<a href=\"{0}\">{1}</a>".format(url, text)
        self.assertEqual(expected, result)

    def test_create_anchor_should_break_html_when_html_injection_is_used(self):
        url         = u"</a>"
        text        = u"random"
        result      = self.hyperlink.create_anchor(url, text)
        expected    = u"<a href=\"{0}\">{1}</a>".format(url, text)
        self.assertEqual(expected, result)
