# -*- coding: utf-8 -*-
import unittest
import re
import time
import base64
import json

import sys
sys.path.append("/usr/share/anki/")
from ..utility import Utility

class UtilityTester(unittest.TestCase):
    def __init__(self, arg1):
        super(UtilityTester, self).__init__(arg1)
        self.whitespace_regex = re.compile(r"\s+")
        self.left_paren_regex = re.compile(r"\\\(")
        self.right_paren_regex = re.compile(r"\\\)")

    # replace_link_img_matches
    def test_replace_link_img_matches_should_accept_and_return_unicode(self):
        # arrange
        image               = "![](image \(1\).jpg)"
        # act
        # assert
        self.assertRaises(AssertionError,
                          Utility.replace_link_img_matches,
                          self.whitespace_regex, "&#32;", image)

    def test_replace_link_img_matches_accepts_russian_input(self):
        # arrange
        image       = u"![](изображение \(1\).jpg)"
        expected    = u"![](изображение&#32;\(1\).jpg)"
        # act
        result      = Utility.replace_link_img_matches(self.whitespace_regex,
                                                       "&#32;",
                                                       image)
        # assert
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_replaces_single_whitespace(self):
        # arrange
        image               = u"![](image \(1\).jpg)"
        expected            = u"![](image&#32;\(1\).jpg)"
        # act
        result = Utility.replace_link_img_matches(self.whitespace_regex, "&#32;", image)
        # assert
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_replaces_link_with_whitespace(self):
        # arrange
        image               = u"[](image \(1\).jpg)"
        expected            = u"[](image&#32;\(1\).jpg)"
        # act
        result = Utility.replace_link_img_matches(self.whitespace_regex, "&#32;", image)
        # assert
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_replaces_link_with_title(self):
        # arrange
        image               = u"[text](image \(1\).jpg)"
        expected            = u"[text](image&#32;\(1\).jpg)"
        # act
        result = Utility.replace_link_img_matches(self.whitespace_regex, "&#32;", image)
        # assert
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_replaces_link_with_title_that_contains_whitespace(self):
        # arrange
        image               = u"[random text](image \(1\).jpg)"
        expected            = u"[random&#32;text](image&#32;\(1\).jpg)"
        # act
        result = Utility.replace_link_img_matches(self.whitespace_regex, "&#32;", image)
        # assert
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_makes_no_changes_when_final_paren_is_missing(self):
        # arrange
        image               = u"[](image \(1\).jpg"
        expected            = u"[](image \(1\).jpg"
        # act
        result = Utility.replace_link_img_matches(self.whitespace_regex, "&#32;", image)
        # assert
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_does_not_replace_unescaped_left_parens(self):
        # arrange
        image               = u"[](image (1\).jpg"
        expected            = u"[](image (1\).jpg"
        # act
        result = Utility.replace_link_img_matches(self.left_paren_regex, "&#32;", image)
        # assert
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_returns_same_when_whitespace_before_opening_paren(self):
        # arrange
        image               = u"![] (image \(1\).jpg)"
        expected            = u"![] (image \(1\).jpg)"
        # act
        result = Utility.replace_link_img_matches(self.whitespace_regex, "&#32;", image)
        # assert
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_replaces_whitespace_in_different_parts(self):
        # arrange
        image               = u"![](image \(1\) .jpg)"
        expected            = u"![](image&#32;\(1\)&#32;.jpg)"
        # act
        result = Utility.replace_link_img_matches(self.whitespace_regex,
                                                  "&#32;",
                                                  image)
        # assert
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_replace_left_paren_with_char_entity(self):
        # arrange
        image               = u"![](image \(1\).jpg)"
        expected            = u"![](image &#40;1\).jpg)"
        # act
        result = Utility.replace_link_img_matches(self.left_paren_regex,
                                                  "&#40;",
                                                  image)
        # assert
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_replace_multiple_left_parens_with_char_entity(self):
        # arrange
        image               = u"![](image \(\(\(1\)\)\).jpg)"
        expected            = u"![](image &#40;&#40;&#40;1\)\)\).jpg)"
        # act
        result = Utility.replace_link_img_matches(self.left_paren_regex,
                                                  "&#40;",
                                                  image)
        # assert
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_replaces_multiple_escaped_right_parens(self):
        # arrange
        image               = u"![](image \(\(\(1\)\)\).jpg)"
        expected            = u"![](image \(\(\(1&#41;&#41;&#41;.jpg)"
        # act
        result = Utility.replace_link_img_matches(self.right_paren_regex,
                                                  "&#41;",
                                                  image)
        # assert
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_replaces_whitespace_in_multiple_imgs(self):
        # arrange
        image       = u"random text before\n" + \
                      u"![](image \(1\).jpg)\n" + \
                      u"and more text\n" + \
                      u"![](image \(2\).jpg)"
        expected    = u"random text before\n" + \
                      u"![](image&#32;\(1\).jpg)\n" + \
                      u"and more text\n" + \
                      u"![](image&#32;\(2\).jpg)"
        # act
        result = Utility.replace_link_img_matches(self.whitespace_regex,
                                                  "&#32;",
                                                  image)
        # assert
        self.assertEqual(expected, result)
        self.assertEqual(len(expected), len(result))

    def test_replace_link_img_matches_replaces_whitespace_and_parens_in_multiple_imgs(self):
        # arrange
        image       = u"random text before\n" + \
                      u"![](image \(1\).jpg)\n" + \
                      u"and more text\n" + \
                      u"![](image \(2\).jpg)"
        expected    = u"random text before\n" + \
                      u"![](image&#32;&#40;1&#41;.jpg)\n" + \
                      u"and more text\n" + \
                      u"![](image&#32;&#40;2&#41;.jpg)"
        # act
        result = Utility.replace_link_img_matches(self.whitespace_regex,
                                                  "&#32;",
                                                  image)
        result = Utility.replace_link_img_matches(self.left_paren_regex,
                                                  "&#40;",
                                                  result)
        result = Utility.replace_link_img_matches(self.right_paren_regex,
                                                  "&#41;",
                                                  result)
        # assert
        self.assertEqual(expected, result)
        self.assertEqual(len(expected), len(result))

    # escape_html_chars
    def test_escape_html_chars_throws_assertion_error_when_input_is_not_unicode(self):
        # arrange
        s        = "this&that"
        # act
        # assert
        self.assertRaises(AssertionError, Utility.escape_html_chars, s)

    def test_escape_html_chars_returns_correctly_escaped_string_when_input_is_russian(self):
        # arrange
        s           = u"об этом & о том"
        expected    = u"об этом &amp; о том"
        # act
        result      = Utility.escape_html_chars(s)
        # assert
        self.assertEqual(expected, result)

    def test_escape_html_chars_returns_string_with_ampersand_escaped(self):
        # arrange
        s        = u"this&that"
        expected = u"this&amp;that"
        # act
        result = Utility.escape_html_chars(s)
        # assert
        self.assertEqual(expected, result)

    def test_escape_html_chars_returns_string_with_multiple_ampersands_escaped(self):
        # arrange
        s        = u"this&that&so"
        expected = u"this&amp;that&amp;so"
        # act
        result = Utility.escape_html_chars(s)
        # assert
        self.assertEqual(expected, result)

    def test_escape_html_chars_returns_empty_string_when_empty_string_passed(self):
        # arrange
        s        = u""
        expected = u""
        # act
        result = Utility.escape_html_chars(s)
        # assert
        self.assertEqual(expected, result)

    def test_escape_html_chars_returns_string_with_five_chars_that_should_be_escaped(self):
        # arrange
        s        = u"this&that\"so\'and<and>"
        expected = u"this&amp;that&quot;so&apos;and&lt;and&gt;"
        # act
        result = Utility.escape_html_chars(s)
        # assert
        self.assertEqual(expected, result)

    def test_escape_html_chars_fails_when_input_is_not_unicode(self):
        # arrange
        s        = "this&that\"so\'and<and>"
        # act
        # assert
        self.assertRaises(AssertionError, Utility.escape_html_chars, s)

    # check_alignment
    def test_check_alignment_fails_when_input_is_not_unicode(self):
        # arrange
        s = ""
        # act
        # assert
        self.assertRaises(AssertionError, Utility.check_alignment, s)

    def test_check_alignment_returns_center_when_input_is_colon_dash_colon(self):
        # arrange
        s        = u":-:"
        expected = u"center"
        # act
        result = Utility.check_alignment(s)
        # assert
        self.assertEqual(expected, result)

    def test_check_alignment_returns_left_when_input_is_not_recognized_string(self):
        # arrange
        s        = u"random"
        expected = u"left"
        # act
        result = Utility.check_alignment(s)
        # assert
        self.assertEqual(expected, result)

    def test_check_alignment_returns_left_when_input_is_empty_string(self):
        # arrange
        s        = u""
        expected = u"left"
        # act
        result = Utility.check_alignment(s)
        # assert
        self.assertEqual(expected, result)

    def test_check_alignment_returns_left_when_input_is_none(self):
        # arrange
        # act
        # assert
        self.assertRaises(AssertionError, Utility.check_alignment, None)

    # check_size_heading
    def test_check_size_heading_throws_assertion_error_when_input_not_unicode(self):
        # arrange
        s       = ""
        # act
        # assert
        self.assertRaises(AssertionError, Utility.check_size_heading, s)


    def test_check_size_heading_returns_minus_one_when_input_is_empty_string(self):
        # arrange
        s        = u""
        expected = -1
        # act
        result = Utility.check_size_heading(s)
        # assert
        self.assertEqual(expected, result)

    def test_check_size_heading_returns_minus_one_when_input_is_random_text(self):
        # arrange
        s        = u"random text"
        expected = -1
        # act
        result = Utility.check_size_heading(s)
        # assert
        self.assertEqual(expected, result)

    def test_check_size_heading_returns_six_when_input_is_seven_hashes(self):
        # arrange
        s        = u"#######heading"
        expected = 6
        # act
        result = Utility.check_size_heading(s)
        # assert
        self.assertEqual(expected, result)

    def test_check_size_heading_returns_three_when_input_is_seven_hashes_with_a_space(self):
        # arrange
        s        = u"### ####heading"
        expected = 3
        # act
        result = Utility.check_size_heading(s)
        # assert
        self.assertEqual(expected, result)

    def test_check_size_heading_returns_three_when_input_starts_with_space(self):
        # arrange
        s        = u"    ###heading"
        expected = 3
        # act
        result = Utility.check_size_heading(s)
        # assert
        self.assertEqual(expected, result)

    def test_check_size_heading_returns_three_when_input_starts_with_tab(self):
        # arrange
        s        = u"\t###heading"
        expected = 3
        # act
        result = Utility.check_size_heading(s)
        # assert
        self.assertEqual(expected, result)

    def test_check_size_heading_returns_three_when_input_starts_with_newline(self):
        # arrange
        s        = u"\n###heading"
        expected = 3
        # act
        result = Utility.check_size_heading(s)
        # assert
        self.assertEqual(expected, result)

    # string_leading_whitespace
    def test_strip_leading_whitespace_throws_assertion_error_when_input_is_not_unicode(self):
        # arrange
        s = " text"
        # act
        # assert
        self.assertRaises(AssertionError, Utility.strip_leading_whitespace, s)

    def test_strip_leading_whitespace_deletes_tab_from_start_of_string(self):
        # arrange
        s        = u"\ttext"
        expected = u"text"
        # act
        result = Utility.strip_leading_whitespace(s)
        # assert
        self.assertEqual(expected, result)

    def test_strip_leading_whitespace_deletes_multiple_nbsp_from_start_of_string(self):
        # arrange
        s        = u"&nbsp;&nbsp;&nbsp;text"
        expected = u"text"
        # act
        result = Utility.strip_leading_whitespace(s)
        # assert
        self.assertEqual(expected, result)

    def test_strip_leading_whitespace_does_not_delete_non_leading_nbsp(self):
        # arrange
        s        = u"text&nbsp;text"
        expected = u"text&nbsp;text"
        # act
        result = Utility.strip_leading_whitespace(s)
        # assert
        self.assertEqual(expected, result)

    def test_strip_leading_whitespace_returns_same_string_when_input_is_empty_string(self):
        # arrange
        s        = u""
        expected = u""
        # act
        result = Utility.strip_leading_whitespace(s)
        # assert
        self.assertEqual(expected, result)

    # normalize_user_prefs
    def test_normalize_user_prefs_adds_key_that_is_not_in_user_prefs(self):
        # arrange
        default_prefs   = dict(a=u"one")
        user_prefs      = dict()
        expected        = dict(a=u"one")
        # act
        result = Utility.normalize_user_prefs(default_prefs, user_prefs)
        # assert
        self.assertEqual(expected, result)

    def test_normalize_user_prefs_deletes_key_that_is_not_in_default_prefs(self):
        # arrange
        default_prefs   = dict()
        user_prefs      = dict(a=u"one")
        expected        = dict()
        # act
        result = Utility.normalize_user_prefs(default_prefs, user_prefs)
        # assert
        self.assertEqual(expected, result)

    def test_normalize_user_prefs_add_and_delete_key_from_user_dict(self):
        # arrange
        default_prefs   = dict(b=u"two")
        user_prefs      = dict(a=u"one")
        expected        = dict(b=u"two")
        # act
        result = Utility.normalize_user_prefs(default_prefs, user_prefs)
        # assert
        self.assertEqual(expected, result)

    def test_normalize_user_prefs_empty_input_dicts_return_empty_dict(self):
        # arrange
        default_prefs   = dict()
        user_prefs      = dict()
        expected        = dict()
        # act
        result = Utility.normalize_user_prefs(default_prefs, user_prefs)
        # assert
        self.assertEqual(expected, result)


    def test_split_string_throws_assertion_error_when_text_is_not_unicode(self):
        # arrange
        text        = ""
        splitlist   = ""
        # act
        # assert
        self.assertRaises(AssertionError, Utility.split_string, text, splitlist)

    def test_split_string_returns_list_with_text_when_input_starts_with_delim(self):
        # arrange
        text        = u"!text"
        splitlist   = u"!"
        expected    = ["text"]
        # act
        result = Utility.split_string(text, splitlist)
        # assert
        self.assertEqual(expected, result)


    def test_split_string_returns_empty_list_when_text_is_only_delims(self):
        # arrange
        text        = u"!@#"
        splitlist   = u"!@#"
        expected    = []
        # act
        result = Utility.split_string(text, splitlist)
        # assert
        self.assertEqual(expected, result)

    def test_split_string_returns_list_with_items_using_multiple_delims(self):
        # arrange
        text        = u"!one@two#three$"
        splitlist   = u"!@#$"
        expected    = [u"one", u"two", u"three"]
        # act
        result = Utility.split_string(text, splitlist)
        # assert
        self.assertEqual(expected, result)

    def test_split_string_returns_list_with_single_item_when_splitlist_is_empty_str(self):
        # arrange
        text        = u"!one@two#three$"
        splitlist   = u""
        expected    = [u"!one@two#three$"]
        # act
        result = Utility.split_string(text, splitlist)
        # assert
        self.assertEqual(expected, result)

    # validate_key_sequence
    def test_validate_key_sequence_multiple_tests(self):
        assert Utility.validate_key_sequence(u"") == u""
        assert Utility.validate_key_sequence(None) == u""
        assert Utility.validate_key_sequence(u"-") == u"-"
        assert Utility.validate_key_sequence(u"a") == u"a"
        assert Utility.validate_key_sequence(u"ctrl+,") == u"ctrl+,"
        assert Utility.validate_key_sequence(u"ctrl-,") == u"ctrl+,"
        assert Utility.validate_key_sequence(u",+ctrl") == u"ctrl+,"
        assert Utility.validate_key_sequence(u"p-Alt-Ctrl") == u"ctrl+alt+p"
        assert Utility.validate_key_sequence(u",+ctr") == u""
        assert Utility.validate_key_sequence(u"alt+shift+greka+q") == u""
        assert Utility.validate_key_sequence(u"alt+shift+greka+q", u"darwin") == ""
        assert Utility.validate_key_sequence(u"alt+shift+ctrl") == u""
        assert Utility.validate_key_sequence(u"alt+alt+ctrl+p") == u"ctrl+alt+p"
        assert Utility.validate_key_sequence(u"alt-shift++") == u"shift+alt++"
        assert Utility.validate_key_sequence(u"alt-shift+++") == u"shift+alt++"
        assert Utility.validate_key_sequence(u"alt-alt------shift+p") == u"shift+alt+p"
        assert Utility.validate_key_sequence(u"alt-alt------shift+p", u"darwin") == u"shift+alt+p"
        print "OF INTEREST:"
        assert Utility.validate_key_sequence(u"Q-Meta-CTRL", u"darwin") == u"ctrl+meta+q"
        assert Utility.validate_key_sequence(u"MeTA---META---ShIFT++++", u"darwin") == u"meta+shift++"
        assert Utility.validate_key_sequence(u"ctrl alt p", u"darwin") == u""
        assert Utility.validate_key_sequence(u"ctrl+1") == u"ctrl+1"
        assert Utility.validate_key_sequence(u"ctrl+!") == u"ctrl+!"
        assert Utility.validate_key_sequence(u"F12") == u"f12"
        assert Utility.validate_key_sequence(u"F12+Shift") == u"shift+f12"
        assert Utility.validate_key_sequence(u"F12+F11") == u""
        assert Utility.validate_key_sequence(u"F12+a") == ""
        assert Utility.validate_key_sequence(u"ctrl+shift+alt+meta+f5", u"darwin") == u"ctrl+meta+shift+alt+f5"
        assert Utility.validate_key_sequence(u"shift+F12") == u"shift+f12"

    # check_user_keybindings
    def test_check_user_keybindings_return_default_upon_invalid_user_keybinding(self):
        # arrange
        invalid_keybinding  = dict(a=u"ctrl-iota-a")
        default_keybindings = dict(a=u"ctrl-alt-del")
        expected            = default_keybindings
        # act
        result = Utility.check_user_keybindings(default_keybindings, invalid_keybinding)
        # assert
        self.assertEqual(expected, result)

    def test_check_user_keybindings_return_new_upon_valid_user_keybinding(self):
        # arrange
        valid_keybinding    = dict(a=u"ctrl-shift-a")
        default_keybindings = dict(a=u"ctrl-alt-del")
        expected            = dict(a=u"ctrl+shift+a")
        # act
        result = Utility.check_user_keybindings(default_keybindings, valid_keybinding)
        # assert
        self.assertEqual(expected, result)

    def test_check_user_keybindings_return_empty_dict_when_user_keybindings_is_empty(self):
        # arrange
        valid_keybinding    = dict()
        default_keybindings = dict(a=u"ctrl-alt-del")
        expected            = dict()
        # act
        result = Utility.check_user_keybindings(default_keybindings, valid_keybinding)
        # assert
        self.assertEqual(expected, result)

    # start_safe_block
    def test_start_safe_block_return_none_when_hashmap_is_empty(self):
        # arrange
        hashmap     = dict()
        expected    = None
        # act
        result = Utility.start_safe_block(hashmap)
        # assert
        self.assertEqual(expected, result)

    def test_start_safe_block_returns_map_with_two_keys_when_input_is_map_with_two_valid_keys(self):
        # arrange
        hashmap     = dict(start_time="", safe_block="")
        self.assertFalse(hashmap.get("start_time"))
        # act
        result = Utility.start_safe_block(hashmap)
        # assert
        self.assertEqual(True, hashmap.get("safe_block"))
        self.assertTrue(hashmap.get("start_time"))

    # end_safe_block
    def test_end_safe_block_return_none_when_hashmap_is_empty(self):
        # arrange
        hashmap     = dict()
        expected    = None
        # act
        result = Utility.end_safe_block(hashmap)
        # assert
        self.assertEqual(expected, result)

    def test_end_safe_block_sets_hashmap_key_to_false_when_correct_dict_is_passed(self):
        # arrange
        hashmap     = dict(start_time="", safe_block="")
        expected    = dict(start_time="", safe_block=False)
        # act
        Utility.end_safe_block(hashmap)
        # assert
        self.assertEqual(expected.get("safe_block"), hashmap.get("safe_block"))

    # convert_clean_md_to_html
    def test_convert_clean_md_to_html_throws_assertion_error_when_input_is_not_unicode(self):
        # arrange
        s           = ""
        # act
        # assert
        self.assertRaises(AssertionError, Utility.convert_clean_md_to_html, s)

    def test_convert_clean_md_to_html_returns_correct_html_when_input_is_correct_md(self):
        # arrange
        s        = u"    :::python\n    def fn(): pass"
        expected = u"<div>&nbsp; &nbsp; :::python</div><div>&nbsp; &nbsp; def fn(): pass</div>"
        # act
        result = Utility.convert_clean_md_to_html(s)
        # assert
        self.assertEqual(expected, result)


    def test_convert_clean_md_to_html_returns_empty_string_when_input_is_empty_string(self):
        # arrange
        s        = u""
        expected = u""
        # act
        result = Utility.convert_clean_md_to_html(s)
        # assert
        self.assertEqual(expected, result)


    def test_convert_clean_md_to_html_returns_div_with_break_when_input_is_solely_whitespace(self):
        # arrange
        s        = u"    "
        expected = u"<div><br /></div>"
        # act
        result = Utility.convert_clean_md_to_html(s)
        # assert
        self.assertEqual(expected, result)

    def test_convert_clean_md_to_html_returns_empty_div_when_input_is_solely_newline(self):
        # arrange
        s        = u"\n"
        expected = u"<div></div>"
        # act
        result = Utility.convert_clean_md_to_html(s)
        # assert
        self.assertEqual(expected, result)

    def test_convert_clean_md_to_html_returns_div_with_break_when_input_is_solely_newline_and_put_breaks_is_true(self):
        # arrange
        s        = u"\n"
        expected = u"<div><br /></div>"
        # act
        result = Utility.convert_clean_md_to_html(s, put_breaks=True)
        # assert
        self.assertEqual(expected, result)

    def test_convert_clean_md_to_html_returns_div_with_char_when_input_is_char_with_newline(self):
        # arrange
        s        = u"a\n"
        expected = u"<div>a</div>"
        # act
        result = Utility.convert_clean_md_to_html(s)
        # assert
        self.assertEqual(expected, result)

    def test_convert_clean_md_to_html_returns_two_divs_with_char_when_input_is_newline_with_char(self):
        # arrange
        s        = u"\na"
        expected = u"<div></div><div>a</div>"
        # act
        result = Utility.convert_clean_md_to_html(s)
        # assert
        self.assertEqual(expected, result)

    def test_convert_clean_md_to_html_returns_text_in_divs_when_input_contains_only_text(self):
        # arrange
        s        = u"random"
        expected = u"<div>random</div>"
        # act
        result = Utility.convert_clean_md_to_html(s, put_breaks=True)
        # assert
        self.assertEqual(expected, result)

    def test_convert_clean_md_to_html_returns_two_divs_when_linebreak_in_input_text(self):
        # arrange
        s        = u"random\nrandom"
        expected = u"<div>random</div><div>random</div>"
        # act
        result = Utility.convert_clean_md_to_html(s, put_breaks=True)
        # assert
        self.assertEqual(expected, result)

    def test_convert_clean_md_to_html_returns_correct_leading_whitespace_when_input_has_leading_whitespace(self):
        # arrange
        s        = u"    random"
        expected = u"<div>&nbsp; &nbsp; random</div>"
        # act
        result = Utility.convert_clean_md_to_html(s, put_breaks=True)
        # assert
        self.assertEqual(expected, result)

    def test_convert_clean_md_to_html_returns_correct_leading_whitespace_when_input_has_two_lines_with_leading_whitespace(self):
        # arrange
        s        = u"    random\n    more"
        expected = u"<div>&nbsp; &nbsp; random</div><div>&nbsp; &nbsp; more</div>"
        # act
        result = Utility.convert_clean_md_to_html(s, put_breaks=True)
        # assert
        self.assertEqual(expected, result)

    def test_convert_clean_md_to_html_returns_correct_leading_whitespace_when_input_is_russian(self):
        # arrange
        s        = u"    пизза"
        expected = u"<div>&nbsp; &nbsp; пизза</div>"
        # act
        result = Utility.convert_clean_md_to_html(s, put_breaks=True)
        # assert
        self.assertEqual(expected, result)

    # convert_markdown_to_html
    def test_convert_markdown_to_html_throws_assertion_error_when_input_is_not_unicode(self):
        # arrange
        s           = ""
        # act
        # assert
        self.assertRaises(AssertionError, Utility.convert_markdown_to_html, s)


    # get_md_data_from_string
    def test_get_md_data_from_string_throws_assertion_error_when_input_is_not_unicode(self):
        # arrange
        s           = ""
        # act
        # assert
        self.assertRaises(AssertionError, Utility.get_md_data_from_string, s)


    def test_get_md_data_from_string_returns_none_when_input_does_not_contain_any_marker(self):
        # arrange
        s           = u"<div></div>"
        expected    = None
        # act
        result = Utility.get_md_data_from_string(s)
        # assert
        self.assertEqual(expected, result)

    def test_get_md_data_from_string_returns_none_when_input_does_not_contain_end_marker(self):
        # arrange
        s           = u"<div></div><!----SBAdata{data:data}"
        expected    = None
        # act
        result = Utility.get_md_data_from_string(s)
        # assert
        self.assertEqual(expected, result)

    def test_get_md_data_from_string_returns_dict_when_markers_are_present(self):
        # arrange
        d           = dict(a="one")
        encoded     = base64.b64encode(json.dumps(d))
        s           = u"<div></div><!----SBAdata:{}---->".format(encoded)
        expected    = encoded
        # act
        result = Utility.get_md_data_from_string(s)
        # assert
        self.assertEqual(expected, result)

    def test_get_md_data_from_string_returns_random_string_in_data_part(self):
        # arrange
        s           = u"<div></div><!----SBAdata:randomtext---->"
        expected    = u"randomtext"
        # act
        result = Utility.get_md_data_from_string(s)
        # assert
        self.assertEqual(expected, result)

    def test_get_md_data_from_string_returns_empty_string_when_data_part_is_empty(self):
        # arrange
        s           = u"<div></div><!----SBAdata:---->"
        expected    = u""
        # act
        result = Utility.get_md_data_from_string(s)
        # assert
        self.assertEqual(expected, result)

    # decompress_and_json_load
    def test_decompress_and_json_load_throws_assertion_error_when_input_is_not_unicode(self):
        # arrange
        s           = ""
        # act
        # assert
        self.assertRaises(AssertionError, Utility.decompress_and_json_load, s)

    def test_decompress_and_json_load_throws_type_error_when_padding_of_base64_data_is_invalid(self):
        # arrange
        data        = u"randomtext" # lenght of string should be multiples of 4
                                    # so `randomtext==` would not throw an error
                                    # because it is padded correctly
        expected    = "corrupted"
        # act
        result = Utility.decompress_and_json_load(data)
        # assert
        self.assertEqual(expected, result)

    def test_decompress_and_json_load_returns_corrupted_when_base64_data_is_invalid_json(self):
        # arrange
        data        = u"randomtext=="
        expected    = "corrupted"
        # act
        result = Utility.decompress_and_json_load(data)
        # assert
        self.assertEqual(expected, result)

    def test_decompress_and_json_load_returns_corrupted_when_base64_data_contains_non_ascii_chars(self):
        # arrange
        data        = u"ëandomtext=="
        expected    = "corrupted"
        # act
        result = Utility.decompress_and_json_load(data)
        # assert
        self.assertEqual(expected, result)


    def test_decompress_and_json_load_returns_valid_json_when_base64_data_is_valid(self):
        # arrange
        d           = dict(a=u"one")
        data        = unicode(base64.b64encode(json.dumps(d)))
        expected    = d
        # act
        result = Utility.decompress_and_json_load(data)
        # assert
        self.assertEqual(expected, result)

    # json_dump_and_compress
    def test_json_dump_and_compress_throws_assertion_error_when_input_is_not_unicode(self):
        # arrange
        data        = ""
        # act
        # assert
        self.assertRaises(AssertionError, Utility.json_dump_and_compress, data)

    def test_json_dump_and_compress_returns_base64_string_when_input_is_russian(self):
        # arrange
        data        = u"привет"
        expected    = unicode(base64.b64encode(json.dumps(data)))
        # act
        result      = Utility.json_dump_and_compress(data)
        # assert
        self.assertEqual(expected, result)

    # is_same_markdown
    def test_is_same_markdown_throws_assertion_error_when_input_is_not_unicode(self):
        # arrange
        s1      = ""
        s2      = ""
        # act
        # assert
        self.assertRaises(AssertionError, Utility.is_same_markdown, s1, s2)

    def test_is_same_markdown_returns_true_when_markdown_with_russian_is_same(self):
        # arrange
        s1          = u"ещё **один** тест"
        expected    = True
        # act
        result      = Utility.is_same_markdown(s1, s1)
        # assert
        self.assertEqual(expected, result)

    # remove_white_space
    def test_remove_white_space_returns_empty_unicode_string_when_input_is_empty_string(self):
        # arrange
        s           = u""
        expected    = u""
        # act
        result      = Utility.remove_white_space(s)
        # assert
        self.assertEqual(expected, result)

    def test_remove_white_space_throws_assertion_error_when_input_is_not_unicode(self):
        # arrange
        s           = ""
        # act
        # assert
        self.assertRaises(AssertionError, Utility.remove_white_space, s)

    def test_remove_white_space_returns_unicode_string_when_input_is_russian(self):
        # arrange
        s           = u"ой ты Пушкин, ой ты сукин сын"
        expected    = u"ойтыПушкин,ойтысукинсын"
        # act
        result      = Utility.remove_white_space(s)
        # assert
        self.assertEqual(expected, result)

    # put_md_data_in_json_format
    def test_put_md_data_in_json_format_throws_assertion_error_when_md_or_html_is_not_unicode(self):
        md1         = ""
        html1       = u""
        self.assertRaises(AssertionError,
                          Utility.put_md_data_in_json_format,
                          1,
                          True,
                          md1,
                          html1)
        md2         = u""
        html2       = ""
        self.assertRaises(AssertionError,
                          Utility.put_md_data_in_json_format,
                          1,
                          True,
                          md1,
                          html1)

    def test_put_md_data_in_json_format_returns_dict_when_md_and_html_contain_russian(self):
        md          = u"один"
        html        = u"два"
        expected    = dict(id=1, isconverted=True, md=md, html=html, lastmodified="")
        result      = Utility.put_md_data_in_json_format(1, True, md, html)
        self.assertEqual(expected.get("md"), result.get("md"))
        self.assertEqual(expected.get("html"), result.get("html"))
