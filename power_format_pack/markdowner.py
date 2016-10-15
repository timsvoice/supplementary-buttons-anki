# -*- coding: utf-8 -*-
#
# Copyright 2014-2016 Stefan van den Akker <srvandenakker.dev@gmail.com>
#
# This file is part of Power Format Pack.
#
# Power Format Pack is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Power Format Pack is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with Power Format Pack. If not, see http://www.gnu.org/licenses/.

import re

from anki.utils import json
from aqt import mw
from PyQt4 import QtGui

import utility
import const
import preferences


class Markdowner(object):
    """
    Convert HTML to Markdown and the other way around. Store the data in the
    field. Revert to previous Markdown or overwrite the data when conflicts
    arise.
    """
    # signal that we don't want the onEdit focus behavior
    button_pressed = False

    def __init__(self, other, parent_window, note, html,
                 current_field, selected_html):
        assert isinstance(html, unicode), "Input `html` is not Unicode"
        assert isinstance(selected_html, unicode), "Input `selected_html` is not Unicode"
        self.c                              = utility.get_config_parser()
        self.p                              = preferences.PREFS
        self.editor_instance                = other
        self.parent_window                  = parent_window
        self.col                            = mw.col
        self.note                           = note
        self.html                           = html
        self.cancel_html                    = ""
        self.current_field                  = current_field
        self.selected_html                  = selected_html
        self.current_note_id_and_field      = str(self.note.id) + \
                                              "-{:03}".format(self.current_field)
        self._id                            = None
        self.isconverted                    = None
        self.md                             = None
        self._lastmodified                  = None
        self.has_data                       = self.get_data_from_field()
        if not self.has_data:
            self.remove_warn_msg(self.editor_instance, self.current_field)
        const.MARKDOWN_PREFS["isconverted"] = self.isconverted

    def on_focus_gained(self):
        if self.isconverted:
            const.MARKDOWN_PREFS["disable_buttons"] = True
            self.warn_about_changes(self.editor_instance,
                                    self.current_field,
                                    const.MARKDOWN_BG_COLOR)
        else:
            const.MARKDOWN_PREFS["disable_buttons"] = False

    def apply_markdown(self):
        self.cancel_html = self.html
        has_def_list = False
        if "<dl>" in self.html:
            has_def_list = True
            self.create_correct_md_for_def_list()
            self.html = self.note.fields[self.current_field]
        clean_md = utility.convert_html_to_markdown(self.html)
        if has_def_list:
            clean_md = utility.remove_leading_whitespace_from_dd_element(clean_md)
        clean_md = utility.remove_whitespace_before_abbreviation_definition(
                clean_md)
        clean_md_escaped = utility.escape_html_chars(clean_md)
        if not clean_md:
            return
        # check for changed Markdown between the stored data and the current text
        if (self.has_data and self.isconverted == "True"):
            compare_md = utility.convert_markdown_to_html(self.md)
            compare_md = utility.put_colons_in_html_def_list(compare_md)
            compare_md = utility.convert_html_to_markdown(compare_md)
            if has_def_list:
                compare_md = utility.remove_leading_whitespace_from_dd_element(compare_md)
            compare_md = utility.remove_whitespace_before_abbreviation_definition(
                    compare_md)
            if not any(x in compare_md for x in("&amp;", "&quot;", "&apos;",
                                                "&gt;", "&lt;")):
                compare_md_escaped = utility.escape_html_chars(compare_md)
                compare_md = compare_md_escaped
            if (utility.is_same_markdown(clean_md_escaped, compare_md) or
                   self.p.get(const.MARKDOWN_ALWAYS_REVERT)):
                self.revert_to_stored_markdown()
            else:
                self.handle_conflict()
        else:
            # make abbreviations behave correctly
            new_html = utility.convert_markdown_to_html(clean_md)
            # needed for proper display of images
            if "<img" in new_html:
                new_html = utility.unescape_html(new_html)
            html_with_data = utility.make_data_ready_to_insert(
                    self.current_note_id_and_field, "True",
                    clean_md_escaped, new_html)
            self.insert_markup_in_field(
                    html_with_data, self.editor_instance.currentField)
            self.align_elements()
            const.MARKDOWN_PREFS["disable_buttons"] = True
            self.warn_about_changes(self.editor_instance,
                                    self.current_field,
                                    const.MARKDOWN_BG_COLOR)

    def get_data_from_field(self):
        """
        Get the HTML from the current field and try to extract Markdown data
        from it. The side effect of calling this function is that several
        instance variables get set. Return True when data was found in the
        field, False otherwise.
        """
        compr_dict = utility.get_md_data_from_string(self.html)
        md_dict = utility.decompress_and_json_load(compr_dict)
        if md_dict and md_dict == "corrupted":
            # TODO: fallback when JSON is corrupted
            # TODO: log this
            pass
        elif md_dict:
            self._id            = md_dict.get("id")
            self.md             = md_dict.get("md")
            self.isconverted    = md_dict.get("isconverted")
            self._lastmodified  = md_dict.get("lastmodified")
            return True
        return False

    def insert_markup_in_field(self, markup, field):
        """
        Put markup in the specified field.
        """
        self.editor_instance.web.eval("""
            document.getElementById('f%s').innerHTML = %s;
        """ % (field, json.dumps(unicode(markup))))

    def warn_about_changes(self, editor_instance, field, color):
        """
        Disable the specified contenteditable field.
        """
        if self.p.get(const.MARKDOWN_OVERRIDE_EDITING):
            warning_text = self.c.get(const.CONFIG_TOOLTIPS,
                                      "md_warning_editing_enabled_tooltip")
        else:
            warning_text = self.c.get(const.CONFIG_TOOLTIPS,
                                      "md_warning_editing_disabled_tooltip")
        editor_instance.web.eval("""
            if (document.getElementById('mdwarn%s') === null) {
                var style_tag_list = document.getElementsByTagName('style');
                if (style_tag_list.length === 0) {
                    // there is no <style> element in the document
                } else {
                    var style_tag = style_tag_list[0];

                    if (style_tag.innerHTML.indexOf('mdstyle') === -1) {
                        style_tag.innerHTML +=
                                '.mdstyle { background-color: %s !important; }\\n';
                    }

                    var field = document.getElementById('f%s');
                    field.setAttribute('title', '%s');
                    field.classList.add('mdstyle');

                    var warn_div = document.createElement('div');
                    warn_div.id = 'mdwarn%s';
                    warn_div.setAttribute('style', 'margin: 10px 0px;');
                    var text = document.createTextNode('%s');
                    warn_div.appendChild(text);
                    field.parentNode.insertBefore(warn_div, field.nextSibling);
                }
            }
        """ % (field, color, field, warning_text, field, warning_text))

    @staticmethod
    def remove_warn_msg(editor_instance, field):
        editor_instance.web.eval("""
            if (document.getElementById('mdwarn%s') !== null) {
                var field = document.getElementById('f%s');
                field.classList.remove('mdstyle');
                field.removeAttribute('title');
                var warn_msg = document.getElementById('mdwarn%s');
                warn_msg.parentNode.removeChild(warn_msg);
            }
        """ % (field, field, field))

    def handle_conflict(self):
        """
        Show a warning dialog. Based on the user decision, either revert the
        changes to the text, replace the stored data, or cancel.
        """
        ret = self.show_overwrite_warning()
        if ret == 0:
            self.revert_to_stored_markdown()
        elif ret == 1:
            # overwrite data
            self.overwrite_stored_data()
        else:
            print "User canceled on warning dialog."
            self.insert_markup_in_field(self.cancel_html, self.current_field)

    def overwrite_stored_data(self):
        """
        Create new Markdown from the current HTML.
        """
        clean_md = utility.convert_html_to_markdown(
                self.html, keep_empty_lines=True)
        clean_md = utility.remove_whitespace_before_abbreviation_definition(
                clean_md)
        if "<dl" in self.html:
            clean_md = utility.remove_leading_whitespace_from_dd_element(
                    clean_md, add_newline=True)
        if re.search(const.IS_LINK_OR_IMG_REGEX, clean_md):
            clean_md = utility.escape_html_chars(clean_md)
        new_html = utility.convert_clean_md_to_html(clean_md,
                                                    put_breaks=True)
        self.insert_markup_in_field(new_html, self.current_field)
        const.MARKDOWN_PREFS["disable_buttons"] = False
        const.MARKDOWN_PREFS["isconverted"] = False
        self.remove_warn_msg(self.editor_instance, self.current_field)

    def revert_to_stored_markdown(self):
        """
        Revert to the previous version of Markdown that was stored in the field.
        """
        new_html = utility.convert_clean_md_to_html(self.md, put_breaks=True)
        self.insert_markup_in_field(new_html, self.current_field)
        const.MARKDOWN_PREFS["disable_buttons"] = False
        const.MARKDOWN_PREFS["isconverted"] = False
        self.remove_warn_msg(self.editor_instance, self.current_field)

    def show_overwrite_warning(self):
        """
        Show a warning modal dialog box, informing the user that the changes
        have taken place in the formatted text that are not in the Markdown.
        Return a 0 for replacing the new changes with the stored version of
        the Markdown, 1 for overwriting the data, and QMessageBox.Cancel for
        no action.
        """
        mess = QtGui.QMessageBox(self.parent_window)
        mess.setIcon(QtGui.QMessageBox.Warning)
        # TODO: think about putting the text of the dialog in property files
        mess.setWindowTitle(self.c.get(const.CONFIG_WINDOW_TITLES,
                                       "md_overwrite_warning"))
        mess.setText(self.c.get(const.CONFIG_WARNINGS,
                                "md_overwrite_warning_text"))
        mess.setInformativeText(self.c.get(const.CONFIG_WARNINGS,
                                "md_overwrite_warning_additional_text"))
        replaceButton = QtGui.QPushButton("&Replace", mess)
        mess.addButton(replaceButton, QtGui.QMessageBox.ApplyRole)
        mess.addButton("&Overwrite", QtGui.QMessageBox.ApplyRole)
        mess.setStandardButtons(QtGui.QMessageBox.Cancel)
        mess.setDefaultButton(replaceButton)
        return mess.exec_()

    def align_elements(self):
        """
        Left align footnotes, lists, etc. that would otherwise get
        centered or be at the mercy of the general alignment CSS of the card.
        Code blocks can be given a specific `code_direction`.
        """
        # align text in code blocks to the left
        if not self.p.get(const.MARKDOWN_CLASSFUL_PYGMENTS):
            self.editor_instance.web.eval("""
                $('.codehilite').attr('align', 'left');
            """)

        # align the code block itself
        if self.p.get(const.MARKDOWN_CODE_DIRECTION) != const.LEFT:
            self.editor_instance.web.eval("""
                var table = '<table><tbody><tr><td></td></tr></tbody></table>';
                $('.codehilite:not(.codehilitetable .codehilite)').wrap(table);
                $('.codehilite').parents().filter('table').addClass('codehilitetable').attr('align', '%s');
            """ % self.p.get(const.MARKDOWN_CODE_DIRECTION))

        # footnotes
        self.editor_instance.web.eval("""
            var elems = document.getElementsByTagName('*');
            var regex = /fn:/;
            for (var i = 0; i < elems.length; i++) {
                var elem = elems[i].id;
                if (regex.test(elem)) {
                    elems[i].children[0].setAttribute('align', 'left');
                }
            }
        """)

        # definition lists, lists
        self.editor_instance.web.eval("""
            var elems = document.querySelectorAll('dt,dd,li');
            for (var i = 0; i < elems.length; i++) {
                elems[i].setAttribute('align', 'left');
            }
        """)

    def create_correct_md_for_def_list(self):
        """
        Change the input `md` to make sure it will transform to the
        correct HTML.
        """
        self.editor_instance.web.eval("""\
            var dds = document.getElementsByTagName('dd');
            for (var i = 0; i < dds.length; i++) {
                var theDD = dds[i];
                firstChild = theDD.firstChild;
                if (firstChild === null) {
                    var text = document.createTextNode(': ');
                    theDD.appendChild(text);
                } else {
                    theDD.firstChild.nodeValue = ': ' + theDD.firstChild.nodeValue;
                }
                if (theDD.nextSibling !== null &&
                        theDD.nextSibling.tagName === 'DT') {
                    var br = document.createElement('br');
                    theDD.parentNode.insertBefore(br, theDD.nextSibling);
                }
            }
        """)
        self.editor_instance.web.setFocus()
        self.editor_instance.web.eval("focusField(%d);" % self.current_field)
        self.editor_instance.saveNow()
