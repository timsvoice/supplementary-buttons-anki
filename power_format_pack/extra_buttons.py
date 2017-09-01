# -*- coding: utf-8 -*-
#
# Copyright 2014-2017 Stefan van den Akker <neftas@protonmail.com>
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


# import warnings
# warnings.simplefilter("ignore", UserWarning)

from PyQt4 import QtGui

import const
import preferences
import utility
from abbreviation import Abbreviation
from anki.hooks import wrap, addHook
from anki.utils import isMac
from anki_modules.aqt import editor as myeditor
from aqt import editor as anki_editor, mw
from blockquote import Blockquote
from deflist import DefList
from heading import Heading
from hilite_color import HiliteColor
from hyperlink import Hyperlink
from markdowner import Markdowner
from menu import Options
from orderedlist import OrderedList
from power_format_pack.button import Button
from power_format_pack.unorderedlist import UnorderedList
from preferences import Preferences
from table import Table

# Preferences
##################################################
Preferences.init()


# Overrides
##################################################
anki_editor.Editor.onHtmlEdit = myeditor.onHtmlEdit


# Buttons
##################################################

def place_button(editor, button):
    const.BUTTONS.append(button)

    button_placement_pref = preferences.PREFS.get(const.BUTTON_PLACEMENT)

    if button_placement_pref == "adjacent":
        editor.iconsBox.addWidget(button)
    else:
        editor.supp_buttons_hbox.addWidget(button)


def setup_buttons(editor):
    const.BUTTONS = list()

    p = preferences.PREFS

    button_placement_pref = p.get(const.BUTTON_PLACEMENT)

    editor.supp_buttons_hbox = QtGui.QHBoxLayout()

    if p.get(const.CODE):
        shortcut = preferences.KEYS.get(const.CODE)
        tooltip = u"Code format text ({})".format(utility.key_to_text(shortcut))
        callback = lambda: utility.wrap_in_tags(editor, "code", p.get(const.CODE_CLASS))
        button = Button(const.CODE, shortcut, tooltip, callback)
        place_button(editor, button)

    if p.get(const.UNORDERED_LIST):
        shortcut = preferences.KEYS.get(const.UNORDERED_LIST)
        tooltip = u"Create unordered list ({})".format(utility.key_to_text(shortcut))
        callback = lambda: toggle_unordered_list(editor)
        button = Button(const.UNORDERED_LIST, shortcut, tooltip, callback)
        place_button(editor, button)

    if p.get(const.ORDERED_LIST):
        shortcut = preferences.KEYS.get(const.ORDERED_LIST)
        tooltip = u"Create ordered list ({})".format(utility.key_to_text(shortcut))
        callback = lambda: toggle_ordered_list(editor)
        button = Button(const.ORDERED_LIST, shortcut, tooltip, callback)
        place_button(editor, button)

    if p.get(const.STRIKETHROUGH):
        shortcut = preferences.KEYS.get(const.STRIKETHROUGH)
        tooltip = u"Strikethrough text ({})".format(utility.key_to_text(shortcut))
        button = Button(const.STRIKETHROUGH, shortcut, tooltip, editor.toggle_strikethrough)
        place_button(editor, button)

    # FIXME (neftas): think of better symbol to represent a <pre> block
    if p.get(const.PRE):
        shortcut = preferences.KEYS.get(const.PRE)
        tooltip = u"Create a code block ({})".format(utility.key_to_text(shortcut))
        callback = lambda: utility.wrap_in_tags(editor, "pre", p.get(const.CODE_CLASS))
        button = Button(const.PRE, shortcut, tooltip, callback)
        place_button(editor, button)

    if p.get(const.HORIZONTAL_RULE):
        shortcut = preferences.KEYS.get(const.HORIZONTAL_RULE)
        tooltip = u"Create a horizontal rule ({})".format(utility.key_to_text(shortcut))
        button = Button(const.HORIZONTAL_RULE, shortcut, tooltip, editor.toggle_horizontal_line)
        place_button(editor, button)

    if p.get(const.INDENT):
        shortcut = preferences.KEYS.get(const.INDENT)
        tooltip = u"Indent text or list ({})".format(utility.key_to_text(shortcut))
        button = Button(const.INDENT, shortcut, tooltip, editor.toggle_indent)
        place_button(editor, button)

    if p.get(const.OUTDENT):
        shortcut = preferences.KEYS.get(const.OUTDENT)
        tooltip = u"Outdent text or list ({})".format(utility.key_to_text(shortcut))
        button = Button(const.OUTDENT, shortcut, tooltip, editor.toggle_outdent)
        place_button(editor, button)

    # FIXME (neftas): better symbol for <dl>
    if p.get(const.DEFINITION_LIST):
        shortcut = preferences.KEYS.get(const.DEFINITION_LIST)
        tooltip = u"Create definition list ({})".format(utility.key_to_text(shortcut))
        button = Button(const.DEFINITION_LIST, shortcut, tooltip, editor.toggle_definition_list)
        place_button(editor, button)

    if p.get(const.TABLE):
        shortcut = preferences.KEYS.get(const.TABLE)
        tooltip = u"Create a table ({})".format(utility.key_to_text(shortcut))
        button = Button(const.TABLE, shortcut, tooltip, editor.toggle_table)
        place_button(editor, button)

    if p.get(const.KEYBOARD):
        shortcut = preferences.KEYS.get(const.KEYBOARD)
        tooltip = u"Create a keyboard button ({})".format(utility.key_to_text(shortcut))
        callback = lambda: utility.wrap_in_tags(editor, "kbd")
        button = Button(const.KEYBOARD, shortcut, tooltip, callback)
        place_button(editor, button)

    if p.get(const.HYPERLINK):
        shortcut = preferences.KEYS.get(const.HYPERLINK)
        tooltip = u"Insert link ({})".format(utility.key_to_text(shortcut))
        button1 = Button(const.HYPERLINK, shortcut, tooltip, editor.toggle_hyperlink)
        place_button(editor, button1)

        shortcut = preferences.KEYS.get(const.REMOVE_HYPERLINK)
        tooltip = u"Unlink ({})".format(utility.key_to_text(shortcut))
        button2 = Button(const.REMOVE_HYPERLINK, shortcut, tooltip, editor.unlink)
        place_button(editor, button2)

    if p.get(const.BACKGROUND_COLOR):
        hilite_color = HiliteColor(editor, preferences)
        shortcut = preferences.KEYS.get(const.BACKGROUND_COLOR)
        tooltip = u"Set background color ({})".format(utility.key_to_text(shortcut))
        button1 = Button(const.BACKGROUND_COLOR, shortcut, tooltip, hilite_color.apply_color, text=" ")
        hilite_color.setup_background_button(button1)
        place_button(editor, button1)

        shortcut = preferences.KEYS.get(const.BACKGROUND_COLOR_CHANGE)
        tooltip = u"Change color ({})".format(utility.key_to_text(shortcut))
        button2 = Button(const.BACKGROUND_COLOR_CHANGE,
                         shortcut,
                         tooltip,
                         hilite_color.change_color,
                         # space is needed to center the arrow
                         text=utility.downArrow())
        button2.setFixedWidth(12)
        place_button(editor, button2)

    if p.get(const.BLOCKQUOTE):
        shortcut = preferences.KEYS.get(const.BLOCKQUOTE)
        tooltip = u"Insert blockquote ({})".format(utility.key_to_text(shortcut))
        button = Button(const.BLOCKQUOTE, shortcut, tooltip, editor.toggle_blockquote)
        place_button(editor, button)

    if p.get(const.TEXT_ALLIGN):
        shortcut = preferences.KEYS.get(const.TEXT_ALLIGN_FLUSH_LEFT)
        tooltip = u"Align text left ({})".format(utility.key_to_text(shortcut))
        button1 = Button(const.TEXT_ALLIGN_FLUSH_LEFT, shortcut, tooltip, editor.justify_left)
        place_button(editor, button1)

        shortcut = preferences.KEYS.get(const.TEXT_ALLIGN_CENTERED)
        tooltip = u"Align text center ({})".format(utility.key_to_text(shortcut))
        button2 = Button(const.TEXT_ALLIGN_CENTERED, shortcut, tooltip, editor.justify_center)
        place_button(editor, button2)

        shortcut = preferences.KEYS.get(const.TEXT_ALLIGN_FLUSH_RIGHT)
        tooltip = u"Align text right ({})".format(utility.key_to_text(shortcut))
        button3 = Button(const.TEXT_ALLIGN_FLUSH_RIGHT, shortcut, tooltip, editor.justify_right)
        place_button(editor, button3)

        shortcut = preferences.KEYS.get(const.TEXT_ALLIGN_JUSTIFIED)
        tooltip = u"Justify text ({})".format(utility.key_to_text(shortcut))
        button4 = Button(const.TEXT_ALLIGN_JUSTIFIED, shortcut, tooltip, editor.justify_full)
        place_button(editor, button4)

    if p.get(const.HEADING):
        shortcut = preferences.KEYS.get(const.HEADING)
        tooltip = u"Insert heading ({})".format(utility.key_to_text(shortcut))
        button = Button(const.HEADING, shortcut, tooltip, editor.toggle_heading)
        place_button(editor, button)

    if p.get(const.ABBREVIATION):
        shortcut = preferences.KEYS.get(const.ABBREVIATION)
        tooltip = u"Insert abbreviation ({})".format(utility.key_to_text(shortcut))
        button = Button(const.ABBREVIATION, shortcut, tooltip, editor.toggle_abbreviation)
        place_button(editor, button)

    if p.get(const.MARKDOWN):
        shortcut = preferences.KEYS.get(const.MARKDOWN)
        tooltip = u"Toggle Markdown ({})".format(utility.key_to_text(shortcut))
        button = Button(const.MARKDOWN, shortcut, tooltip, editor.toggle_markdown)
        place_button(editor, button)

    for button in const.BUTTONS:
        if editor.plastiqueStyle:
            button.setStyle(editor.plastiqueStyle)
        editor._buttons[button.name] = button

    if button_placement_pref != "adjacent":
        editor.supp_buttons_hbox.insertStretch(0, 1)
        if not isMac:
            editor.supp_buttons_hbox.setMargin(6)
            editor.supp_buttons_hbox.setSpacing(0)
        else:
            editor.supp_buttons_hbox.setMargin(0)
            editor.supp_buttons_hbox.setSpacing(14)

        if button_placement_pref == "below":
            editor.outerLayout.insertLayout(1, editor.supp_buttons_hbox)
        elif button_placement_pref == "above":
            editor.outerLayout.insertLayout(0, editor.supp_buttons_hbox)


def unlink(self):
    self.web.eval("setFormat('unlink')")


def toggle_unordered_list(editor):
    fixed_type = preferences.PREFS.get("fixed_ul_type")
    UnorderedList(editor, fixed_type if fixed_type else "")


def toggle_ordered_list(editor):
    fixed_type = preferences.PREFS.get("fixed_ol_type")
    OrderedList(editor, preferences, fixed_type if fixed_type else "")


def toggle_strikethrough(editor):
    editor.web.eval("setFormat('strikeThrough')")


def toggle_pre(editor):
    editor.web.eval("setFormat('formatBlock', 'pre')")


def toggle_horizontal_line(editor):
    editor.web.eval("setFormat('insertHorizontalRule')")


def toggle_indent(editor):
    editor.web.eval("setFormat('indent')")


def toggle_outdent(editor):
    editor.web.eval("setFormat('outdent')")


def toggle_definition_list(editor):
    selection = editor.web.selectedText()
    DefList(editor, editor.parentWindow, selection if selection else None)


def toggle_table(editor):
    selection = editor.web.selectedText()
    Table(editor, editor.parentWindow, selection if selection else None, preferences)


def toggle_blockquote(editor):
    selected = editor.web.selectedHtml()
    Blockquote(editor, selected)


def justify_center(editor):
    editor.web.eval("setFormat('justifyCenter');")


def justify_left(editor):
    editor.web.eval("setFormat('justifyLeft');")


def justify_right(editor):
    editor.web.eval("setFormat('justifyRight');")


def justify_full(editor):
    editor.web.eval("setFormat('justifyFull');")


def toggle_heading(editor):
    selected = editor.web.selectedText()
    Heading(editor, editor.parentWindow, selected)


def toggle_abbreviation(editor):
    selected = editor.web.selectedText()
    Abbreviation(editor, editor.parentWindow, selected)


def toggle_hyperlink(editor):
    selected = editor.web.selectedText()
    Hyperlink(editor, editor.parentWindow, selected)


def toggle_markdown(editor):
    editor.saveNow()
    current_field = editor.currentField
    html_field = editor.note.fields[current_field]
    if not html_field:
        html_field = u""
    markdowner = Markdowner(editor, editor.parentWindow, editor.note, html_field, current_field, preferences)
    markdowner.start()
    editor.web.setFocus()
    editor.web.eval("focusField(%d);" % editor.currentField)


def init_hook(editor, mw, widget, parentWindow, addMode=False):
    addHook("editFocusGained", editor.on_focus_gained)


def on_focus_gained(editor, note, current_field_no):
    """
    Check if the current field contains Markdown. Change the appearance of
    the field if it does, or do nothing if not.
    """

    if not note.fields[current_field_no]:
        return

    markdown_warning_text = preferences.CONFIG.get(const.CONFIG_TOOLTIPS, "md_warning_editing_tooltip")

    Markdowner.manage_style(editor, current_field_no)
    editor.web.eval("""
        var field = $('#f%s');
        if (field.html().indexOf('SBAdata:') > -1) {
            var mdData = /<!----SBAdata:([a-zA-Z0-9+/]+=*)---->/.exec(field.html());
            var json = JSON.parse(atob(mdData[1]));
            if (json.isconverted) {
                if (!field.hasClass('mdstyle')) {
                    field.addClass('mdstyle');
                }
                if (!$('#f%s + [class^=mdwarning]').length) {
                    field.after($('<div/>', {class: 'mdwarning', text: '%s'}));
                }
                field.attr('title', '%s');
            }
        }
    """ % (current_field_no, current_field_no, markdown_warning_text, markdown_warning_text))


if preferences.PREFS.get(const.MARKDOWN):
    anki_editor.Editor.on_focus_gained = on_focus_gained
    anki_editor.Editor.__init__ = wrap(anki_editor.Editor.__init__, init_hook)


anki_editor.Editor.toggle_markdown = toggle_markdown
anki_editor.Editor.toggle_heading = toggle_heading
anki_editor.Editor.toggle_abbreviation = toggle_abbreviation
anki_editor.Editor.toggle_hyperlink = toggle_hyperlink
anki_editor.Editor.unlink = unlink
anki_editor.Editor.justify_full = justify_full
anki_editor.Editor.justify_right = justify_right
anki_editor.Editor.justify_left = justify_left
anki_editor.Editor.justify_center = justify_center
anki_editor.Editor.toggle_blockquote = toggle_blockquote
anki_editor.Editor.toggle_strikethrough = toggle_strikethrough
anki_editor.Editor.toggle_pre = toggle_pre
anki_editor.Editor.toggle_horizontal_line = toggle_horizontal_line
anki_editor.Editor.toggle_indent = toggle_indent
anki_editor.Editor.toggle_outdent = toggle_outdent
anki_editor.Editor.toggle_definition_list = toggle_definition_list
anki_editor.Editor.toggle_table = toggle_table
anki_editor.Editor.setupButtons = wrap(anki_editor.Editor.setupButtons, setup_buttons)

mw.ExtraButtons_Options = Options(mw)
mw.ExtraButtons_Options.setup_power_format_pack_options()
