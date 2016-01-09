# -*- coding: utf-8 -*-
import unittest
import re
import base64
import json

import sys
if "/usr/share/anki/" not in sys.path:
    sys.path.append("/usr/share/anki/")
from extra_buttons.utility import Utility


class UtilityTester(unittest.TestCase):
    def __init__(self, arg1):
        super(UtilityTester, self).__init__(arg1)
        self.whitespace_regex = re.compile(r"\s+")
        self.left_paren_regex = re.compile(r"\\\(")
        self.right_paren_regex = re.compile(r"\\\)")

    # replace_link_img_matches
    def test_replace_link_img_matches_should_accept_and_return_unicode(self):
        image               = "![](image \(1\).jpg)"
        self.assertRaises(AssertionError,
                          Utility.replace_link_img_matches,
                          self.whitespace_regex, "&#32;", image)

    def test_replace_link_img_matches_accepts_russian_input(self):
        image       = u"![](изображение \(1\).jpg)"
        expected    = u"![](изображение&#32;\(1\).jpg)"
        result      = Utility.replace_link_img_matches(self.whitespace_regex,
                                                       "&#32;",
                                                       image)
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_replaces_single_whitespace(self):
        image               = u"![](image \(1\).jpg)"
        expected            = u"![](image&#32;\(1\).jpg)"
        result = Utility.replace_link_img_matches(self.whitespace_regex, "&#32;", image)
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_replaces_link_with_whitespace(self):
        image               = u"[](image \(1\).jpg)"
        expected            = u"[](image&#32;\(1\).jpg)"
        result = Utility.replace_link_img_matches(self.whitespace_regex, "&#32;", image)
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_replaces_link_with_title(self):
        image               = u"[text](image \(1\).jpg)"
        expected            = u"[text](image&#32;\(1\).jpg)"
        result = Utility.replace_link_img_matches(self.whitespace_regex, "&#32;", image)
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_replaces_link_with_title_that_contains_whitespace(self):
        image               = u"[random text](image \(1\).jpg)"
        expected            = u"[random&#32;text](image&#32;\(1\).jpg)"
        result = Utility.replace_link_img_matches(self.whitespace_regex, "&#32;", image)
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_makes_no_changes_when_final_paren_is_missing(self):
        image               = u"[](image \(1\).jpg"
        expected            = u"[](image \(1\).jpg"
        result = Utility.replace_link_img_matches(self.whitespace_regex, "&#32;", image)
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_does_not_replace_unescaped_left_parens(self):
        image               = u"[](image (1\).jpg"
        expected            = u"[](image (1\).jpg"
        result = Utility.replace_link_img_matches(self.left_paren_regex, "&#32;", image)
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_returns_same_when_whitespace_before_opening_paren(self):
        image               = u"![] (image \(1\).jpg)"
        expected            = u"![] (image \(1\).jpg)"
        result = Utility.replace_link_img_matches(self.whitespace_regex, "&#32;", image)
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_replaces_whitespace_in_different_parts(self):
        image               = u"![](image \(1\) .jpg)"
        expected            = u"![](image&#32;\(1\)&#32;.jpg)"
        result = Utility.replace_link_img_matches(self.whitespace_regex,
                                                  "&#32;",
                                                  image)
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_replace_left_paren_with_char_entity(self):
        image               = u"![](image \(1\).jpg)"
        expected            = u"![](image &#40;1\).jpg)"
        result = Utility.replace_link_img_matches(self.left_paren_regex,
                                                  "&#40;",
                                                  image)
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_replace_multiple_left_parens_with_char_entity(self):
        image               = u"![](image \(\(\(1\)\)\).jpg)"
        expected            = u"![](image &#40;&#40;&#40;1\)\)\).jpg)"
        result = Utility.replace_link_img_matches(self.left_paren_regex,
                                                  "&#40;",
                                                  image)
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_replaces_multiple_escaped_right_parens(self):
        image               = u"![](image \(\(\(1\)\)\).jpg)"
        expected            = u"![](image \(\(\(1&#41;&#41;&#41;.jpg)"
        result = Utility.replace_link_img_matches(self.right_paren_regex,
                                                  "&#41;",
                                                  image)
        self.assertEqual(expected, result)

    def test_replace_link_img_matches_replaces_whitespace_in_multiple_imgs(self):
        image       = u"random text before\n" + \
                      u"![](image \(1\).jpg)\n" + \
                      u"and more text\n" + \
                      u"![](image \(2\).jpg)"
        expected    = u"random text before\n" + \
                      u"![](image&#32;\(1\).jpg)\n" + \
                      u"and more text\n" + \
                      u"![](image&#32;\(2\).jpg)"
        result = Utility.replace_link_img_matches(self.whitespace_regex,
                                                  "&#32;",
                                                  image)
        self.assertEqual(expected, result)
        self.assertEqual(len(expected), len(result))

    def test_replace_link_img_matches_replaces_whitespace_and_parens_in_multiple_imgs(self):
        image       = u"random text before\n" + \
                      u"![](image \(1\).jpg)\n" + \
                      u"and more text\n" + \
                      u"![](image \(2\).jpg)"
        expected    = u"random text before\n" + \
                      u"![](image&#32;&#40;1&#41;.jpg)\n" + \
                      u"and more text\n" + \
                      u"![](image&#32;&#40;2&#41;.jpg)"
        result = Utility.replace_link_img_matches(self.whitespace_regex,
                                                  "&#32;",
                                                  image)
        result = Utility.replace_link_img_matches(self.left_paren_regex,
                                                  "&#40;",
                                                  result)
        result = Utility.replace_link_img_matches(self.right_paren_regex,
                                                  "&#41;",
                                                  result)
        self.assertEqual(expected, result)
        self.assertEqual(len(expected), len(result))

    # escape_html_chars
    def test_escape_html_chars_throws_assertion_error_when_input_is_not_unicode(self):
        s        = "this&that"
        self.assertRaises(AssertionError, Utility.escape_html_chars, s)

    def test_escape_html_chars_returns_correctly_escaped_string_when_input_is_russian(self):
        s           = u"об этом & о том"
        expected    = u"об этом &amp; о том"
        result      = Utility.escape_html_chars(s)
        self.assertEqual(expected, result)

    def test_escape_html_chars_returns_string_with_ampersand_escaped(self):
        s        = u"this&that"
        expected = u"this&amp;that"
        result = Utility.escape_html_chars(s)
        self.assertEqual(expected, result)

    def test_escape_html_chars_returns_string_with_multiple_ampersands_escaped(self):
        s        = u"this&that&so"
        expected = u"this&amp;that&amp;so"
        result = Utility.escape_html_chars(s)
        self.assertEqual(expected, result)

    def test_escape_html_chars_returns_empty_string_when_empty_string_passed(self):
        s        = u""
        expected = u""
        result = Utility.escape_html_chars(s)
        self.assertEqual(expected, result)

    def test_escape_html_chars_returns_string_with_five_chars_that_should_be_escaped(self):
        s        = u"this&that\"so\'and<and>"
        expected = u"this&amp;that&quot;so&apos;and&lt;and&gt;"
        result = Utility.escape_html_chars(s)
        self.assertEqual(expected, result)

    def test_escape_html_chars_fails_when_input_is_not_unicode(self):
        s        = "this&that\"so\'and<and>"
        self.assertRaises(AssertionError, Utility.escape_html_chars, s)

    # check_alignment
    def test_check_alignment_fails_when_input_is_not_unicode(self):
        s = ""
        self.assertRaises(AssertionError, Utility.check_alignment, s)

    def test_check_alignment_returns_center_when_input_is_colon_dash_colon(self):
        s        = u":-:"
        expected = u"center"
        result = Utility.check_alignment(s)
        self.assertEqual(expected, result)

    def test_check_alignment_returns_left_when_input_is_not_recognized_string(self):
        s        = u"random"
        expected = u"left"
        result = Utility.check_alignment(s)
        self.assertEqual(expected, result)

    def test_check_alignment_returns_left_when_input_is_empty_string(self):
        s        = u""
        expected = u"left"
        result = Utility.check_alignment(s)
        self.assertEqual(expected, result)

    def test_check_alignment_returns_left_when_input_is_none(self):
        self.assertRaises(AssertionError, Utility.check_alignment, None)

    # check_size_heading
    def test_check_size_heading_throws_assertion_error_when_input_not_unicode(self):
        s       = ""
        self.assertRaises(AssertionError, Utility.check_size_heading, s)


    def test_check_size_heading_returns_minus_one_when_input_is_empty_string(self):
        s        = u""
        expected = -1
        result = Utility.check_size_heading(s)
        self.assertEqual(expected, result)

    def test_check_size_heading_returns_minus_one_when_input_is_random_text(self):
        s        = u"random text"
        expected = -1
        result = Utility.check_size_heading(s)
        self.assertEqual(expected, result)

    def test_check_size_heading_returns_six_when_input_is_seven_hashes(self):
        s        = u"#######heading"
        expected = 6
        result = Utility.check_size_heading(s)
        self.assertEqual(expected, result)

    def test_check_size_heading_returns_three_when_input_is_seven_hashes_with_a_space(self):
        s        = u"### ####heading"
        expected = 3
        result = Utility.check_size_heading(s)
        self.assertEqual(expected, result)

    def test_check_size_heading_returns_three_when_input_starts_with_space(self):
        s        = u"    ###heading"
        expected = 3
        result = Utility.check_size_heading(s)
        self.assertEqual(expected, result)

    def test_check_size_heading_returns_three_when_input_starts_with_tab(self):
        s        = u"\t###heading"
        expected = 3
        result = Utility.check_size_heading(s)
        self.assertEqual(expected, result)

    def test_check_size_heading_returns_three_when_input_starts_with_newline(self):
        s        = u"\n###heading"
        expected = 3
        result = Utility.check_size_heading(s)
        self.assertEqual(expected, result)

    # string_leading_whitespace
    def test_strip_leading_whitespace_throws_assertion_error_when_input_is_not_unicode(self):
        s = " text"
        self.assertRaises(AssertionError, Utility.strip_leading_whitespace, s)

    def test_strip_leading_whitespace_deletes_tab_from_start_of_string(self):
        s        = u"\ttext"
        expected = u"text"
        result = Utility.strip_leading_whitespace(s)
        self.assertEqual(expected, result)

    def test_strip_leading_whitespace_deletes_multiple_nbsp_from_start_of_string(self):
        s        = u"&nbsp;&nbsp;&nbsp;text"
        expected = u"text"
        result = Utility.strip_leading_whitespace(s)
        self.assertEqual(expected, result)

    def test_strip_leading_whitespace_does_not_delete_non_leading_nbsp(self):
        s        = u"text&nbsp;text"
        expected = u"text&nbsp;text"
        result = Utility.strip_leading_whitespace(s)
        self.assertEqual(expected, result)

    def test_strip_leading_whitespace_returns_same_string_when_input_is_empty_string(self):
        s        = u""
        expected = u""
        result = Utility.strip_leading_whitespace(s)
        self.assertEqual(expected, result)

    # normalize_user_prefs
    def test_normalize_user_prefs_adds_key_that_is_not_in_user_prefs(self):
        default_prefs   = dict(a=u"one")
        user_prefs      = dict()
        expected        = dict(a=u"one")
        result = Utility.normalize_user_prefs(default_prefs, user_prefs)
        self.assertEqual(expected, result)

    def test_normalize_user_prefs_deletes_key_that_is_not_in_default_prefs(self):
        default_prefs   = dict()
        user_prefs      = dict(a=u"one")
        expected        = dict()
        result = Utility.normalize_user_prefs(default_prefs, user_prefs)
        self.assertEqual(expected, result)

    def test_normalize_user_prefs_add_and_delete_key_from_user_dict(self):
        default_prefs   = dict(b=u"two")
        user_prefs      = dict(a=u"one")
        expected        = dict(b=u"two")
        result = Utility.normalize_user_prefs(default_prefs, user_prefs)
        self.assertEqual(expected, result)

    def test_normalize_user_prefs_empty_input_dicts_return_empty_dict(self):
        default_prefs   = dict()
        user_prefs      = dict()
        expected        = dict()
        result = Utility.normalize_user_prefs(default_prefs, user_prefs)
        self.assertEqual(expected, result)


    def test_split_string_throws_assertion_error_when_text_is_not_unicode(self):
        text        = ""
        splitlist   = ""
        self.assertRaises(AssertionError, Utility.split_string, text, splitlist)

    def test_split_string_returns_list_with_text_when_input_starts_with_delim(self):
        text        = u"!text"
        splitlist   = u"!"
        expected    = ["text"]
        result = Utility.split_string(text, splitlist)
        self.assertEqual(expected, result)


    def test_split_string_returns_empty_list_when_text_is_only_delims(self):
        text        = u"!@#"
        splitlist   = u"!@#"
        expected    = []
        result = Utility.split_string(text, splitlist)
        self.assertEqual(expected, result)

    def test_split_string_returns_list_with_items_using_multiple_delims(self):
        text        = u"!one@two#three$"
        splitlist   = u"!@#$"
        expected    = [u"one", u"two", u"three"]
        result = Utility.split_string(text, splitlist)
        self.assertEqual(expected, result)

    def test_split_string_returns_list_with_single_item_when_splitlist_is_empty_str(self):
        text        = u"!one@two#three$"
        splitlist   = u""
        expected    = [u"!one@two#three$"]
        result = Utility.split_string(text, splitlist)
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
        invalid_keybinding  = {u"a":u"ctrl-iota-a"}
        default_keybindings = {u"a":u"ctrl-alt-del"}
        expected            = default_keybindings
        result = Utility.check_user_keybindings(default_keybindings, invalid_keybinding)
        self.assertEqual(expected, result)

    def test_check_user_keybindings_return_new_upon_valid_user_keybinding(self):
        valid_keybinding    = {u"a":u"ctrl-shift-a"}
        default_keybindings = {u"a":u"ctrl-alt-del"}
        expected            = {u"a":u"ctrl+shift+a"}
        result = Utility.check_user_keybindings(default_keybindings, valid_keybinding)
        self.assertEqual(expected, result)

    def test_check_user_keybindings_return_empty_dict_when_user_keybindings_is_empty(self):
        valid_keybinding    = dict()
        default_keybindings = dict(a=u"ctrl-alt-del")
        expected            = dict()
        result = Utility.check_user_keybindings(default_keybindings, valid_keybinding)
        self.assertEqual(expected, result)

    # start_safe_block
    def test_start_safe_block_return_none_when_hashmap_is_empty(self):
        hashmap     = dict()
        expected    = None
        result = Utility.start_safe_block(hashmap)
        self.assertEqual(expected, result)

    def test_start_safe_block_returns_map_with_two_keys_when_input_is_map_with_two_valid_keys(self):
        hashmap     = dict(start_time="", safe_block="")
        self.assertFalse(hashmap.get("start_time"))
        result = Utility.start_safe_block(hashmap)
        self.assertEqual(True, hashmap.get("safe_block"))
        self.assertTrue(hashmap.get("start_time"))

    # end_safe_block
    def test_end_safe_block_return_none_when_hashmap_is_empty(self):
        hashmap     = dict()
        expected    = None
        result = Utility.end_safe_block(hashmap)
        self.assertEqual(expected, result)

    def test_end_safe_block_sets_hashmap_key_to_false_when_correct_dict_is_passed(self):
        hashmap     = dict(start_time="", safe_block="")
        expected    = dict(start_time="", safe_block=False)
        Utility.end_safe_block(hashmap)
        self.assertEqual(expected.get("safe_block"), hashmap.get("safe_block"))

    # convert_clean_md_to_html
    def test_convert_clean_md_to_html_throws_assertion_error_when_input_is_not_unicode(self):
        s           = ""
        self.assertRaises(AssertionError, Utility.convert_clean_md_to_html, s)

    def test_convert_clean_md_to_html_returns_correct_html_when_input_is_correct_md(self):
        s        = u"    :::python\n    def fn(): pass"
        expected = u"<div>&nbsp; &nbsp; :::python</div><div>&nbsp; &nbsp; def fn(): pass</div>"
        result = Utility.convert_clean_md_to_html(s)
        self.assertEqual(expected, result)


    def test_convert_clean_md_to_html_returns_empty_string_when_input_is_empty_string(self):
        s        = u""
        expected = u""
        result = Utility.convert_clean_md_to_html(s)
        self.assertEqual(expected, result)


    def test_convert_clean_md_to_html_returns_div_with_break_when_input_is_solely_whitespace(self):
        s        = u"    "
        expected = u"<div><br /></div>"
        result = Utility.convert_clean_md_to_html(s)
        self.assertEqual(expected, result)

    def test_convert_clean_md_to_html_returns_empty_div_when_input_is_solely_newline(self):
        s        = u"\n"
        expected = u"<div></div>"
        result = Utility.convert_clean_md_to_html(s)
        self.assertEqual(expected, result)

    def test_convert_clean_md_to_html_returns_div_with_break_when_input_is_solely_newline_and_put_breaks_is_true(self):
        s        = u"\n"
        expected = u"<div><br /></div>"
        result = Utility.convert_clean_md_to_html(s, put_breaks=True)
        self.assertEqual(expected, result)

    def test_convert_clean_md_to_html_returns_div_with_char_when_input_is_char_with_newline(self):
        s        = u"a\n"
        expected = u"<div>a</div>"
        result = Utility.convert_clean_md_to_html(s)
        self.assertEqual(expected, result)

    def test_convert_clean_md_to_html_returns_two_divs_with_char_when_input_is_newline_with_char(self):
        s        = u"\na"
        expected = u"<div></div><div>a</div>"
        result = Utility.convert_clean_md_to_html(s)
        self.assertEqual(expected, result)

    def test_convert_clean_md_to_html_returns_text_in_divs_when_input_contains_only_text(self):
        s        = u"random"
        expected = u"<div>random</div>"
        result = Utility.convert_clean_md_to_html(s, put_breaks=True)
        self.assertEqual(expected, result)

    def test_convert_clean_md_to_html_returns_two_divs_when_linebreak_in_input_text(self):
        s        = u"random\nrandom"
        expected = u"<div>random</div><div>random</div>"
        result = Utility.convert_clean_md_to_html(s, put_breaks=True)
        self.assertEqual(expected, result)

    def test_convert_clean_md_to_html_returns_correct_leading_whitespace_when_input_has_leading_whitespace(self):
        s        = u"    random"
        expected = u"<div>&nbsp; &nbsp; random</div>"
        result = Utility.convert_clean_md_to_html(s, put_breaks=True)
        self.assertEqual(expected, result)

    def test_convert_clean_md_to_html_returns_correct_leading_whitespace_when_input_has_two_lines_with_leading_whitespace(self):
        s        = u"    random\n    more"
        expected = u"<div>&nbsp; &nbsp; random</div><div>&nbsp; &nbsp; more</div>"
        result = Utility.convert_clean_md_to_html(s, put_breaks=True)
        self.assertEqual(expected, result)

    def test_convert_clean_md_to_html_returns_correct_leading_whitespace_when_input_is_russian(self):
        s        = u"    пизза"
        expected = u"<div>&nbsp; &nbsp; пизза</div>"
        result = Utility.convert_clean_md_to_html(s, put_breaks=True)
        self.assertEqual(expected, result)

    # convert_markdown_to_html
    def test_convert_markdown_to_html_throws_assertion_error_when_input_is_not_unicode(self):
        s           = ""
        self.assertRaises(AssertionError, Utility.convert_markdown_to_html, s)


    # get_md_data_from_string
    def test_get_md_data_from_string_throws_assertion_error_when_input_is_not_unicode(self):
        s           = "text"
        self.assertRaises(AssertionError, Utility.get_md_data_from_string, s)


    def test_get_md_data_from_string_returns_empty_unicode_string_when_input_is_empty_string(self):
        s           = ""
        expected    = u""
        result      = Utility.get_md_data_from_string(s)
        self.assertEqual(expected, result)

    def test_get_md_data_from_string_returns_empty_string_when_input_does_not_contain_any_marker(self):
        s           = u"<div></div>"
        expected    = u""
        result = Utility.get_md_data_from_string(s)
        self.assertEqual(expected, result)

    def test_get_md_data_from_string_returns_empty_string_when_input_does_not_contain_end_marker(self):
        s           = u"<div></div><!----SBAdata{data:data}"
        expected    = u""
        result = Utility.get_md_data_from_string(s)
        self.assertEqual(expected, result)

    def test_get_md_data_from_string_returns_dict_when_markers_are_present(self):
        d           = dict(a="one")
        encoded     = base64.b64encode(json.dumps(d))
        s           = u"<div></div><!----SBAdata:{}---->".format(encoded)
        expected    = encoded
        result = Utility.get_md_data_from_string(s)
        self.assertEqual(expected, result)

    def test_get_md_data_from_string_returns_random_string_in_data_part(self):
        s           = u"<div></div><!----SBAdata:randomtext---->"
        expected    = u"randomtext"
        result = Utility.get_md_data_from_string(s)
        self.assertEqual(expected, result)

    def test_get_md_data_from_string_returns_empty_string_when_data_part_is_empty(self):
        s           = u"<div></div><!----SBAdata:---->"
        expected    = u""
        result = Utility.get_md_data_from_string(s)
        self.assertEqual(expected, result)

    # decompress_and_json_load
    def test_decompress_and_json_load_throws_assertion_error_when_input_is_not_unicode(self):
        s           = "text"
        self.assertRaises(AssertionError, Utility.decompress_and_json_load, s)

    def test_decompress_and_json_load_returns_empty_unicode_string_when_input_is_empty_string(self):
        s           = ""
        expected    = u""
        result      = Utility.decompress_and_json_load(s)
        self.assertEqual(expected, result)

    def test_decompress_and_json_load_throws_type_error_when_padding_of_base64_data_is_invalid(self):
        data        = u"randomtext" # lenght of string should be multiples of 4
                                    # so `randomtext==` would not throw an error
                                    # because it is padded correctly
        expected    = "corrupted"
        result = Utility.decompress_and_json_load(data)
        self.assertEqual(expected, result)

    def test_decompress_and_json_load_returns_corrupted_when_base64_data_is_invalid_json(self):
        data        = u"randomtext=="
        expected    = "corrupted"
        result = Utility.decompress_and_json_load(data)
        self.assertEqual(expected, result)

    def test_decompress_and_json_load_returns_corrupted_when_base64_data_contains_non_ascii_chars(self):
        data        = u"ëandomtext=="
        expected    = "corrupted"
        result = Utility.decompress_and_json_load(data)
        self.assertEqual(expected, result)


    def test_decompress_and_json_load_returns_valid_json_when_base64_data_is_valid(self):
        d           = dict(a=u"one")
        data        = unicode(base64.b64encode(json.dumps(d)))
        expected    = d
        result = Utility.decompress_and_json_load(data)
        self.assertEqual(expected, result)

    # json_dump_and_compress
    def test_json_dump_and_compress_returns_base64_string_when_input_is_dict(self):
        data        = dict(a="one")
        expected    = unicode(base64.b64encode(json.dumps(data)))
        result      = Utility.json_dump_and_compress(data)
        self.assertEqual(expected, result)

    def test_json_dump_and_compress_returns_base64_string_when_input_is_russian(self):
        data        = u"привет"
        expected    = unicode(base64.b64encode(json.dumps(data)))
        result      = Utility.json_dump_and_compress(data)
        self.assertEqual(expected, result)

    # is_same_markdown
    def test_is_same_markdown_throws_assertion_error_when_input_is_not_unicode(self):
        s1      = ""
        s2      = ""
        self.assertRaises(AssertionError, Utility.is_same_markdown, s1, s2)

    def test_is_same_markdown_returns_true_when_markdown_with_russian_is_same(self):
        s1          = u"ещё **один** тест"
        expected    = True
        result      = Utility.is_same_markdown(s1, s1)
        self.assertEqual(expected, result)

    # remove_white_space
    def test_remove_white_space_returns_empty_unicode_string_when_input_is_empty_string(self):
        s           = u""
        expected    = u""
        result      = Utility.remove_white_space(s)
        self.assertEqual(expected, result)

    def test_remove_white_space_throws_assertion_error_when_input_is_not_unicode(self):
        s           = ""
        self.assertRaises(AssertionError, Utility.remove_white_space, s)

    def test_remove_white_space_returns_unicode_string_when_input_is_russian(self):
        s           = u"ой ты Пушкин, ой ты сукин сын"
        expected    = u"ойтыПушкин,ойтысукинсын"
        result      = Utility.remove_white_space(s)
        self.assertEqual(expected, result)

    # put_md_data_in_json_format
    def test_put_md_data_in_json_format_throws_assertion_error_when_md_is_not_unicode(self):
        md1         = ""
        self.assertRaises(AssertionError,
                          Utility.put_md_data_in_json_format,
                          1,
                          True,
                          md1)

    def test_put_md_data_in_json_format_returns_dict_when_md_contain_russian(self):
        md          = u"один"
        expected    = dict(id=1, isconverted=True, md=md, lastmodified="")
        result      = Utility.put_md_data_in_json_format(1, True, md)
        self.assertEqual(expected.get("md"), result.get("md"))
        self.assertNotIn("html", expected)

    # remove_whitespace_before_abbreviation_definition
    def test_remove_whitespace_before_abbreviation_definition_does_not_make_changes_when_no_leading_whitespace(self):
        s           = u"""The HTML specification
is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]:  World Wide Web Consortium"""
        expected    = s
        result      = Utility.remove_whitespace_before_abbreviation_definition(s)
        self.assertEqual(expected, result)

    def test_remove_whitespace_before_abbreviation_definition_throws_assertion_error_when_input_is_not_unicode(self):
        s           = "text"
        self.assertRaises(AssertionError, Utility.remove_whitespace_before_abbreviation_definition, s)

    def test_remove_whitespace_before_abbreviation_definition_returns_same_if_input_is_empty_string(self):
        s           = u""
        expected    = u""
        self.assertEqual(s, expected)

    def test_remove_whitespace_before_abbreviation_definition_removes_leading_whitespace_after_newline(self):
        s           = u"adsfsdfsd\n  \n  *[adsfsdfsd]: PSV!!!\n"
        expected    = u'adsfsdfsd\n  \n*[adsfsdfsd]: PSV!!!\n'
        result      = Utility.remove_whitespace_before_abbreviation_definition(s)
        self.assertEqual(expected, result)

    def test_remove_whitespace_before_abbreviation_definition_removes_leading_whitespace_with_multiple_abbreviations(self):
        s           = u"adsfsdfsd and PSV\n  \n  *[adsfsdfsd]: PSV!!!" + \
                      u"\n  *[PSV]: Philips Sport Vereniging\n"
        expected    = u"adsfsdfsd and PSV\n  \n*[adsfsdfsd]: PSV!!!" + \
                      u"\n*[PSV]: Philips Sport Vereniging\n"
        result      = Utility.remove_whitespace_before_abbreviation_definition(s)
        self.assertEqual(expected, result)

    def test_remove_whitespace_before_abbreviation_definition_does_not_remove_leading_whitespace_when_pattern_does_not_match(self):
        s           = u"adsfsdfsd and PSV\n  \n  [adsfsdfsd]: PSV!!!"
        expected    = u"adsfsdfsd and PSV\n  \n  [adsfsdfsd]: PSV!!!"
        result      = Utility.remove_whitespace_before_abbreviation_definition(s)
        self.assertEqual(expected, result)

    # remove_leading_whitespace_from_dd_element
    def test_remove_leading_whitespace_from_dd_element_removes_whitespace_when_input_is_valid(self):
        s           = u"**a**\n    : first letter\n  \n**b**\n    : second letter\n  \n"
        expected    = u"**a**\n: first letter\n  \n**b**\n: second letter\n  \n"
        result      = Utility.remove_leading_whitespace_from_dd_element(s)
        self.assertEqual(expected, result)

    def test_remove_leading_whitespace_from_dd_element_does_not_remove_whitespace_when_input_contains_three_spaces(self):
        s           = u"**a**\n   : first letter\n  \n**b**\n   : second letter\n  \n"
        expected    = u"**a**\n   : first letter\n  \n**b**\n   : second letter\n  \n"
        result      = Utility.remove_leading_whitespace_from_dd_element(s)
        self.assertEqual(expected, result)

    def test_remove_leading_whitespace_from_dd_element_does_not_remove_whitespace_when_input_does_not_contain_colons(self):
        s           = u"**a**\n     first letter\n  \n**b**\n     second letter\n  \n"
        expected    = u"**a**\n     first letter\n  \n**b**\n     second letter\n  \n"
        result      = Utility.remove_leading_whitespace_from_dd_element(s)
        self.assertEqual(expected, result)

    def test_remove_leading_whitespace_from_dd_element_does_not_remove_whitespace_when_input_does_not_contain_space_after_colon(self):
        s           = u"**a**\n    :first letter\n  \n**b**\n    :second letter\n  \n"
        expected    = u"**a**\n    :first letter\n  \n**b**\n    :second letter\n  \n"
        result      = Utility.remove_leading_whitespace_from_dd_element(s)
        self.assertEqual(expected, result)

    def test_remove_leading_whitespace_from_dd_element_removes_whitespace_from_correct_input_but_does_not_from_incorrect_input_in_same_string(self):
        s           = u"**a**\n    : first letter\n  \n**b**\n    :second letter\n  \n"
        expected    = u"**a**\n: first letter\n  \n**b**\n    :second letter\n  \n"
        result      = Utility.remove_leading_whitespace_from_dd_element(s)
        self.assertEqual(expected, result)

    def test_remove_leading_whitespace_from_dd_element_inserts_newline_between_two_dd_elements(self):
        s           = u"**a**\n    : first letter\n**b**\n    :second letter\n  \n"
        expected    = u"**a**\n: first letter\n\n**b**\n    :second letter\n  \n"
        result      = Utility.remove_leading_whitespace_from_dd_element(s, True)
        self.assertEqual(expected, result)

    # put_colons_in_html_def_list
    def test_put_colons_in_html_def_list_throws_assertion_error_when_input_is_not_unicode(self):
        s           = "text"
        self.assertRaises(AssertionError, Utility.put_colons_in_html_def_list, s)

    def test_put_colons_in_html_def_list_returns_empty_string_when_input_is_empty_string(self):
        s           = u""
        expected    = s
        result      = Utility.put_colons_in_html_def_list(s)
        self.assertEqual(expected, result)

    def test_put_colons_in_html_def_list_returns_string_with_colons_when_input_is_correct(self):
        s           = u'\n<dl>\n<dt align="left"><strong>a</strong></dt>\n' + \
                       '<dd align="left">one</dd>\n<dt align="left"><strong>' + \
                       'b</strong></dt>\n<dd align="left">two</dd>\n</dl>'
        expected    = u'\n<dl>\n<dt align="left"><strong>a</strong></dt>\n' + \
                       '<dd align="left">: one</dd>\n<dt align="left"><strong>' + \
                       'b</strong></dt>\n<dd align="left">: two</dd>\n</dl>'
        result      = Utility.put_colons_in_html_def_list(s)
        self.assertEqual(expected, result)

    def test_put_colons_in_html_def_list_returns_string_with_colons_when_input_nodevalue_is_empty(self):
        s           = u'\n<dl>\n<dt align="left"><strong>a</strong></dt>\n' + \
                       '<dd align="left"></dd>\n<dt align="left"><strong>' + \
                       'b</strong></dt>\n<dd align="left"></dd>\n</dl>'
        expected    = u'\n<dl>\n<dt align="left"><strong>a</strong></dt>\n' + \
                       '<dd align="left">: </dd>\n<dt align="left"><strong>' + \
                       'b</strong></dt>\n<dd align="left">: </dd>\n</dl>'
        result      = Utility.put_colons_in_html_def_list(s)
        self.assertEqual(expected, result)

    def test_put_colons_in_html_def_list_should_return_unaltered_string_when_input_does_not_contain_dt(self):
        s           = u'\n<dl>\n' + \
                       '<dd align="left"></dd>\n<dd align="left">text</dd>\n</dl>'
        expected    = u'\n<dl>\n' + \
                       '<dd align="left"></dd>\n<dd align="left">text</dd>\n</dl>'
        result      = Utility.put_colons_in_html_def_list(s)
        self.assertEqual(expected, result)

    def test_put_colons_in_html_def_list_should_return_colon_after_dt_but_nothing_when_not_dt(self):
        s           = u'\n<dl>\n' + \
                       '<dt></dt><dd align="left"></dd>\n<dd align="left">text</dd>\n</dl>'
        expected    = u'\n<dl>\n' + \
                       '<dt></dt><dd align="left">: </dd>\n<dd align="left">text</dd>\n</dl>'
        result      = Utility.put_colons_in_html_def_list(s)
        self.assertEqual(expected, result)
