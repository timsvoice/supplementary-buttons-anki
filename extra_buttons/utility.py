# -*- coding: utf-8 -*-
#
# Copyright 2014-2015 Stefan van den Akker <srvandenakker.dev@gmail.com>
#
# This file is part of Supplementary Buttons for Anki.
#
# Supplementary Buttons for Anki is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Supplementary Buttons for Anki is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with Supplementary Buttons for Anki. If not, see http://www.gnu.org/licenses/.

import string
import sys
import os
import re
import base64

from PyQt4 import QtGui, QtCore
import BeautifulSoup
import sqlite3 as lite
from anki.db import DB
from anki.utils import intTime, json

from html2text import html2text
import const

import markdown
from markdown.extensions import Extension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.smart_strong import SmartEmphasisExtension
from markdown.extensions.footnotes import FootnoteExtension
from markdown.extensions.attr_list import AttrListExtension
from markdown.extensions.def_list import DefListExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.abbr import AbbrExtension
from markdown.extensions.nl2br import Nl2BrExtension
from markdown.extensions.admonition import AdmonitionExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.sane_lists import SaneListExtension

class Utility(object):
    """Utility class with all helper functions that are needed throughout
    the addon. All methods are static, and all fields are constants."""

    # Constants
    ##################################################

    const.PROGRAM_NAME  = "Supplementary Buttons for Anki"
    const.VERSION       = "0.8.0"
    const.YEAR_START    = 2014
    const.YEAR_LAST     = 2015
    const.ANKIWEB_URL   = "https://ankiweb.net/shared/info/162313389"
    const.GITHUB_URL    = "https://github.com/Neftas/supplementary-buttons-anki"
    const.EMAIL         = "srvandenakker.dev@gmail.com"
    const.FOLDER_NAME   = "extra_buttons"

    const.OPERATING_SYSTEMS = {
            "linux2": "Linux",
            "win32" : "Windows",
            "cygwin": "Windows",
            "darwin": "Mac OS X"
    }
    const.PLATFORM      = sys.platform

    # size of the dialog windows
    const.DIALOG_SIZE_X = 350
    const.DIALOG_SIZE_Y = 200

    const.HTML_TAGS     = ("b", "i", "u", "span", "font", "sup", "sub",
                           "dl", "dt", "dd", "code", "s", "pre", "kbd",
                           "a", "strike", "blockquote", "abbr")

    const.HEADING_TAGS  = ("h1", "h2", "h3", "h4", "h5", "h6")

    const.CODE_AND_PRE_CLASS = "c"

    # names of the buttons used for the keybindings
    const.CODE                          = "code"
    const.UNORDERED_LIST                = "unordered_list"
    const.ORDERED_LIST                  = "ordered_list"
    const.STRIKETHROUGH                 = "strikethrough"
    const.PRE                           = "pre"
    const.HORIZONTAL_RULE               = "horizontal_rule"
    const.INDENT                        = "indent"
    const.OUTDENT                       = "outdent"
    const.DEFINITION_LIST               = "definition_list"
    const.TABLE                         = "table"
    const.KEYBOARD                      = "keyboard"
    const.HYPERLINK                     = "hyperlink"
    const.REMOVE_HYPERLINK              = "remove_hyperlink"
    const.BACKGROUND_COLOR              = "background_color"
    const.BACKGROUND_COLOR_CHANGE       = "background_color_change"
    const.BLOCKQUOTE                    = "blockquote"
    const.TEXT_ALLIGN                   = "text_align"
    const.TEXT_ALLIGN_FLUSH_LEFT        = "text_align_flush_left"
    const.TEXT_ALLIGN_FLUSH_RIGHT       = "text_align_flush_right"
    const.TEXT_ALLIGN_JUSTIFIED         = "text_align_justified"
    const.TEXT_ALLIGN_CENTERED          = "text_align_centered"
    const.HEADING                       = "heading"
    const.ABBREVIATION                  = "abbreviation"
    const.MARKDOWN                      = "markdown"
    const.CODE_CLASS                    = "code_class"
    const.LAST_BG_COLOR                 = "last_bg_color"
    const.FIXED_OL_TYPE                 = "fixed_ol_type"
    const.MARKDOWN_SYNTAX_STYLE         = "markdown_syntax_style"

    # constants for key sequence
    const.KEY_MODIFIERS                 = ("ctrl", "alt", "shift")
    const.KEY_MODIFIERS_MACOSX          = ("meta",)
    const.KEYS_SEQUENCE                 = tuple(string.ascii_lowercase) + \
                                          tuple(string.punctuation) + \
                                          tuple(string.digits)
    const.FUNCTION_KEYS                 = ("f1", "f2", "f3", "f4", "f5", "f6",
                                           "f7", "f8", "f9", "f10", "f11", "f12")

    # markers to be wrapped around Markdown data in fields
    const.START_HTML_MARKER             = "<!----SBAdata:"
    const.END_HTML_MARKER               = "---->"

    # change field to this background color
    const.MARKDOWN_BG_COLOR             = "#FFEDD3"

    # Storage of Markdown syntax
    ##################################################

    const.MARKDOWN_DB_NAME  = "extra_buttons"

    @staticmethod
    def _prepare_db(preferences):
        db_path = os.path.join(preferences.addons_folder(),
                               const.FOLDER_NAME,
                               const.MARKDOWN_DB_NAME + ".db")
        # path should be unicode
        if isinstance(db_path, str):
            db_path = unicode(db_path, sys.getfilesystemencoding())
        print "DATABASE PATH:", repr(db_path)

        const.MD_DB_PATH = db_path

        create_db = not os.path.exists(const.MD_DB_PATH)
        con = lite.connect(db_path)
        with con:
            cur = con.cursor()
            if create_db:
                Utility._init_db(cur)
        con.close()
        print con

    @staticmethod
    def _init_db(cur):
        print "INITIALIZING DATABASE MARKDOWN"
        # TODO: add last_modified column
        cur.executescript("""
            create table if not exists markdown (
                id text primary key,
                isconverted text not null,
                md text not null,
                html text not null,
                lastmodified integer not null
            );
        """)

    @staticmethod
    def execute_query(sql, *args):
        # path should exist
        try:
            const.MD_DB_PATH
        except AttributeError:
            Utility._prepare_db()
        print "SQL:", sql
        print "Args:", args

        # certain SQL statements do not return a result set
        return_resultset = True
        if any(sql.startswith(word) for word in ("insert", "update", "delete")):
            return_resultset = False

        con = lite.connect(const.MD_DB_PATH)
        with con:
            cur = con.cursor()
            cur.execute(sql, args)
            if return_resultset:
                resultset = cur.fetchall()
                return resultset

    # Methods
    ##################################################

    @staticmethod
    def convert_html_to_markdown(html, keep_empty_lines=False):
        """
        Take html and return to Markdown. Empty lines are removed from
        the result.
        """
        h = html2text.HTML2Text()
        h.body_width = 0
        md_text = h.handle(html)
        # print "Dirty markdown:\n", repr(md_text)
        if keep_empty_lines:
            clean_md = md_text
        else:
            # remove white lines
            clean_md = ""
            for line in md_text.split("\n"):
                if line:
                    clean_md += (line + "\n")
        # print "Markdown: ", repr(clean_md)
        # undo the html2text escaping of dots which interferes with
        # the creation of ordered lists
        regex = re.compile(r"(\d+)\\(\.\s)")
        clean_md = re.sub(regex, r"\g<1>\g<2>", clean_md)
        return clean_md

    @staticmethod
    def convert_clean_md_to_html(md, put_breaks=False):
        """
        Convert a string containing Markdown syntax to a string with HTML that
        Anki expects.
        """
        result = "<div>"
        location_last_nbsp = -999999999
        last_char = ""
        for index, char in enumerate(md):
            if char == "\n":
                result += "</div><div>"
            elif char == " ":
                if (index - location_last_nbsp) == 1:
                    result += char
                else:
                    if last_char == "\n" or last_char in " ":
                        result += "&nbsp;"
                        location_last_nbsp = index
                    else:
                        result += char
            else:
                result += char
            last_char = char
        # remove last opening <div> tag
        if result.endswith("<div>"):
            result = result[:(len(result) - len("<div>"))]
        # or add a closing <div> tag
        else:
            result += "</div>"

        # <div></div> needs to be a visible empty line
        if put_breaks:
            soup = BeautifulSoup.BeautifulSoup(result)
            for elem in soup.findAll("div"):
                if not elem.contents:
                    elem.append(BeautifulSoup.Tag(soup, "br"))
            result = str(soup)
            soup = None

        # remove "empty" lines that consist solely of (non-breakable) spaces
        soup = BeautifulSoup.BeautifulSoup(result)
        for elem in soup.findAll("div"):
            if elem.string is not None:
                if all(x in ("&nbsp;", " ") for x in elem.string.split()):
                    elem.setString(BeautifulSoup.Tag(soup, "br"))

        return result

    @staticmethod
    def convert_markdown_to_html(preferences, clean_md):
        print "APPLYING MARKDOWN"
        new_html = markdown.markdown(clean_md, output_format="xhtml1",
            extensions=[
                SmartEmphasisExtension(),
                FencedCodeExtension(),
                FootnoteExtension(),
                AttrListExtension(),
                DefListExtension(),
                TableExtension(),
                AbbrExtension(),
                Nl2BrExtension(),
                CodeHiliteExtension(noclasses=True,
                    pygments_style=preferences.prefs.get(const.MARKDOWN_SYNTAX_STYLE)),
                SaneListExtension()
            ], lazy_ol=False)
        # print "New HTML: ", new_html
        return new_html

    @staticmethod
    def is_same_html(html_one, html_two):
        """
        Return True when html_one is the same as html_two, False otherwise.
        """
        return html_one == html_two

    @staticmethod
    def is_same_markdown(md_one, md_two):
        """
        Return True when md_one is the same as md_two, False otherwise.
        """
        # print "md_one before:\n", repr(md_one)
        # print "md_two before:\n", repr(md_two)
        compare_one = Utility.remove_white_space(md_one)
        compare_two = Utility.remove_white_space(md_two)
        return compare_one == compare_two

    @staticmethod
    def is_same_text(text_one, text_two):
        """
        Return True when text_one is the same as text_two, False otherwise.
        """
        return text_one == text_two

    @staticmethod
    def remove_white_space(s):
        return "".join(char for char in s if not char.isspace())

    @staticmethod
    def put_md_data_in_json_format(unique_id, isconverted, md, html):
        """
        Return a dictionary with information that is needed for the database.
        """
        return  {
                "id": unique_id,
                "isconverted": isconverted,
                "md": md,
                "html": html,
                "lastmodified": intTime()
                }

    @staticmethod
    def merge_dicts(existing, new):
        """
        Merge two dictionaries. The values from 'new' dictionary take
        precedence over the values from the 'existing' dictionary where
        there are duplicate keys. Return a dictionary that contains the
        key-value pairs from both dicts.
        """
        return dict(existing.items() + new.items())

    @staticmethod
    def json_dump_and_compress(data):
        print "DATA IN:", repr(data)
        ret = base64.b64encode(json.dumps(data))
        print repr(ret)
        return ret

    @staticmethod
    def decompress_and_json_load(data):
        print "DATA OUT:", repr(data)
        ret = json.loads(base64.b64decode(data))
        print repr(ret)
        return ret

    @staticmethod
    def wrap_string(at_start, a_string, at_end):
        """
        Return a string `a_string` that has the `at_start` string prepended and
        the `at_end` string appended to it.
        """
        return at_start + a_string + at_end

    @staticmethod
    def append_data_to_string(html, wrapped_compr_data):
        """
        Return a string that contains compressed data at the end. The data
        is wrapped in a marker to signify it is data and not to be displayed
        in the field.
        """
        return html + wrapped_compr_data

    @staticmethod
    def make_data_ready_to_insert(unique_id, isconverted, md, html):
        md_dict = Utility.put_md_data_in_json_format(
                unique_id, isconverted, md, html)
        md_dict_compr = Utility.json_dump_and_compress(md_dict)
        wrapped_md_dict_compr = Utility.wrap_string(const.START_HTML_MARKER,
                                                    md_dict_compr,
                                                    const.END_HTML_MARKER)
        return Utility.append_data_to_string(html, wrapped_md_dict_compr)


    @staticmethod
    def get_md_data_from_string(html):
        """
        Read a string `html` and extract compressed Markdown data from it, if it is
        available. Return a dictionary that contains this data, otherwise
        return None.
        """
        if not const.START_HTML_MARKER in html:
            return None
        start = html.find(const.START_HTML_MARKER) + \
                len(const.START_HTML_MARKER)
        end = html.find(const.END_HTML_MARKER, start)
        if start == -1 or end == -1:
            return None
        compr_str = html[start:end]
        return Utility.decompress_and_json_load(compr_str)

    @staticmethod
    def counter(start=0, step=1):
        """
        Generator that creates infinite numbers.
        """
        num = start
        while True:
            yield num
            num += step

    @staticmethod
    def set_icon(button, name, current_preferences):
        """
        Define the path for the icon the corresponding button should have.
        """
        icon_path = os.path.join(current_preferences.addons_folder(),
            const.FOLDER_NAME, "icons", "{}.png".format(name))
        button.setIcon(QtGui.QIcon(icon_path))

    @staticmethod
    def escape_html_chars(s):
        """
        Escape HTML characters in a string. Return a safe string.
        """
        html_escape_table = {
            "&": "&amp;",
            '"': "&quot;",
            "'": "&apos;",
            ">": "&gt;",
            "<": "&lt;",
        }

        return "".join(html_escape_table.get(c, c) for c in s)

    @staticmethod
    def check_alignment(s):
        """
        Return the alignment of a table based on input s. If s not in the
        list, return the default value.
        """
        alignments = {":-": "left", ":-:": "center", "-:": "right"}
        default = "left"
        if not s in alignments:
            return default
        return alignments[s]

    @staticmethod
    def check_size_heading(s):
        """
        Determine by counting the number of leading hashes in the string the
        size of the heading. Return an int that is the length of the hashes.
        """
        regex = re.compile(r"^(#+)")
        if s.strip().startswith("#"):
            return len(regex.match(s).group(1))
        else:
            return -1

    @staticmethod
    def strip_leading_whitespace(s):
        """
        Remove leading whitespace from a string s. Whitespace is defined as
        a space, a tab or a non-breakable space.
        """
        while True:
            if s.startswith(" "):
                s = s.lstrip()
            elif s.startswith("&nbsp;"):
                s = s.lstrip("&nbsp;")
            else:
                break
        return s

    @staticmethod
    def create_horizontal_rule():
        """
        Returns a QFrame that is a sunken, horizontal rule.
        """
        frame = QtGui.QFrame()
        frame.setFrameShape(QtGui.QFrame.HLine)
        frame.setFrameShadow(QtGui.QFrame.Sunken)
        return frame

    @staticmethod
    def normalize_user_prefs(default_prefs, user_prefs):
        """
        Check if the user preferences are compatible with the currently
        used preferences within the addon. Adds keys if they don't exist, and
        removes those that are not recognized.
        """
        # add items that are not in prefs, but should be (e.g. after update)
        for key, value in default_prefs.iteritems():
            if user_prefs.get(key) is None:
                user_prefs[key] = value
        # delete items in prefs that should not be there (e.g. after update)
        for key in user_prefs.keys()[:]:
            if default_prefs.get(key) is None:
                del user_prefs[key]
        # print "In use:", user_prefs

    @staticmethod
    def split_string(text, splitlist):
        """
        Change all separators defined in a string splitlist to the first
        separator in splitlist and then split the text on that one separator.
        Return a list with the original string if splitlist is the empty string
        or None. Return a list of strings, with no empty strings in it.
        """
        if not splitlist:
            return [text]
        for sep in splitlist:
            text = text.replace(sep, splitlist[0])
        return [x for x in text.split(splitlist[0]) if x]

    @staticmethod
    def validate_key_sequence(sequence, platform=""):
        """
        Check a string that contains a key sequence and determine whether it
        fulfills the key sequence contract: one non-modifier key, and optionaly
        one or more modifier keys. Return a prettified key sequence when the
        key sequence is valid, or else an empty string.
        """
        if not sequence: return ""
        modkeys = const.KEY_MODIFIERS
        # Mac OS X has a special modifier, the Cmd key
        if platform.startswith("darwin"):
            modkeys += const.KEY_MODIFIERS_MACOSX
        sequence = sequence.lower()
        # the plus and minus signs can also be part of the key sequence
        # not just serve as delimiters
        if any(sequence.endswith(c) for c in "+-"):
            parts = split_string(sequence[:-1], "+-")
            parts += list(sequence[-1:])
        else:
            parts = Utility.split_string(sequence, "+-")
        # print parts
        parts = Utility.filter_duplicates(parts)
        # sequence can only contain one function key and cannot be used
        # in combination with a character key
        function_key_found = False
        char_key_found = False
        for word in parts:
            if word in const.KEYS_SEQUENCE:
                # f12+a
                if function_key_found:
                    return ""
                char_key_found = True
            if word in const.FUNCTION_KEYS:
                # f12+f11 or a+f12
                if function_key_found or char_key_found:
                    return ""
                function_key_found = True
        # sequence should contain at least one non-modifier key
        if all(word in modkeys for word in parts):
            return ""
        for word in parts:
            # unknown modifiers or non-modifiers are not allowed
            if not word in modkeys + const.KEYS_SEQUENCE + const.FUNCTION_KEYS:
                # print "RETURNING THE EMPTY STRING"
                return ""
        # print "returning:", Utility.create_pretty_sequence(parts)
        return Utility.create_pretty_sequence(parts)

    @staticmethod
    def filter_duplicates(sequence):
        """
        Return a list of elements without duplicates. The order of the
        original collection may be changed in the returned list.
        """
        if not sequence: return list()
        return list(set(sequence))

    @staticmethod
    def create_pretty_sequence(sequence):
        """
        Return an ordered string created from a key sequence that contains
        modifier and non-modifier keys. The returned order is ctrl, meta, shift,
        alt, non-modifier.
        """
        if not sequence: return ""
        seq = sequence[:]
        pretty_sequence = list()
        if "ctrl" in sequence:
            seq.remove("ctrl")
            pretty_sequence.append("ctrl")
        if "meta" in sequence:
            seq.remove("meta")
            pretty_sequence.append("meta")
        if "shift" in sequence:
            seq.remove("shift")
            pretty_sequence.append("shift")
        if "alt" in sequence:
            seq.remove("alt")
            pretty_sequence.append("alt")
        pretty_sequence += seq
        return "+".join(x for x in pretty_sequence if x)

    @staticmethod
    def check_user_keybindings(default_keybindings, user_keybindings, platform=""):
        """
        Check the correctness of the user keybindings. If not correct, the
        default binding will be used instead. Return a check dictionary of
        valid keybindings.
        """
        validated_keybindings = dict()
        for key, value in user_keybindings.iteritems():
            val_binding = Utility.validate_key_sequence(value, platform)
            if not val_binding:
                validated_keybindings[key] = default_keybindings.get(key)
            else:
                validated_keybindings[key] = val_binding
        return validated_keybindings
