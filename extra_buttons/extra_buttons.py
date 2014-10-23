# -*- coding: utf-8 -*-
#
# Copyright 2014 Stefan van den Akker <srvandenakker@gmail.com>
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

# TO DO:
# - prevent QActions from hiding after they are triggered
# - tables: get selection, split selection, build automatic table
# - add icons for URLS and kbd
# - have a look at remove formatting

import os
import re

from anki.utils import json
from aqt import editor, mw
from anki.hooks import wrap
from PyQt4 import QtGui, QtCore

# Helper functions
##################################################

def counter(start=0, step=1):
    "Generator to create infinite numbers."
    n = start
    while True:
        yield n
        n += step

def set_icon(button, name):
    icon_path = os.path.join(addons_folder(),
        "extra_buttons/icons/{}.png".format(name))
    button.setIcon(QtGui.QIcon(icon_path))

def escape_html_chars(s):
    """Escape HTML characters in a string. Return a safe string."""
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }

    return "".join(html_escape_table.get(c, c) for c in s)

# Preferences
##################################################

def addons_folder():
    """Return the addon folder used by Anki."""
    return mw.pm.addonFolder()

addon_path = os.path.join(addons_folder(), "extra_buttons/.extra_buttons_prefs")

default_conf = {"class_name": "",
                "Show <code> button": True,
                "Show unordered list button": True,
                "Show ordered list button": True,
                "Show strikethrough button": True,
                "Show code block button": True,
                "Show horizontal rule button": True,
                "Show indent button": True,
                "Show outdent button": True,
                "Show definition list button": True,
                "Show table button": True,
                "Show create button button": True,
                "Show create link button": True}

try:
    with open(addon_path, "r") as f:
        prefs = json.load(f)
except IOError:
    with open(addon_path, "w") as f:
        prefs = default_conf
        json.dump(prefs, f)

def save_prefs():
    """Save the preferences to disk."""
    with open(addon_path, "w") as f:
        json.dump(prefs, f)

def get_class_name(self):
    """Sets the CSS styling for the <code> and <pre> tags."""

    current_text = prefs.get("class_name", "")

    text, ok = QtGui.QInputDialog.getText(mw, "Set class for <code> and <pre>",
        "Enter a class name for your custom CSS &lt;code&gt; and &lt;pre&gt; style",
        QtGui.QLineEdit.Normal, current_text)

    if ok:
        prefs["class_name"] = text
        save_prefs()


# Menu
##################################################

class ExtraButtons_Options(QtGui.QMenu):
    """Display the various options in the main menu."""

    def __init__(self, mw):
        super(ExtraButtons_Options, self).__init__()
        self.mw = mw

    def button_switch(self):
        "Puts a button either on or off. Reverses current state."
        source = self.sender()
        name = source.text()
        current_state = prefs[name]
        prefs[name] = not current_state
        save_prefs()

    def create_action(self, name, mw, checkable=True):
        action = QtGui.QAction(name, mw)
        if checkable:
            action.setCheckable(True)
            if prefs[name]:
                action.setChecked(True)
        action.toggled.connect(self.button_switch)
        return action

    def setup_extra_buttons_options(self):

        sub_menu_title = "&Supplementary buttons add-on (options)"
        sub_menu = mw.form.menuTools.addMenu(sub_menu_title)

        # go through all the keys in the preferences and make QActions for them
        for option in sorted(prefs.keys()):
            if option in ["class_name"]:
                continue
            else:
                action = self.create_action(option, mw)
                sub_menu.addAction(action)

        custom_css = QtGui.QAction("&Alter <code> and <pre> CSS...", mw)
        custom_css.triggered.connect(get_class_name)
        
        sub_menu.addAction(custom_css)


# Buttons
##################################################

def mySetupButtons(self):

    if prefs["Show <code> button"]:
        b = self._addButton("text_code", lambda: self.wrapInTags("code",
            prefs["class_name"]), _("Ctrl+,"), _("Code format text (Ctrl+,)"),
            check=False)
        set_icon(b, "text_code")

    if prefs["Show unordered list button"]:
        b = self._addButton("unordered_list", self.toggleUnorderedList,
            _("Ctrl+["), _("Create unordered list (Ctrl+[)"), check=False)
        set_icon(b, "unordered_list")

    if prefs["Show ordered list button"]:
        b = self._addButton("ordered_list", self.toggleOrderedList, _("Ctrl+]"),
            _("Create ordered list (Ctrl+])"), check=False)
        set_icon(b, "ordered_list")

    if prefs["Show strikethrough button"]:
        b = self._addButton("text_strikethrough", self.toggleStrikeThrough,
            _("Alt+Shift+5"), _("Strikethrough text (Alt+Shift+5)"), check=True)
        set_icon(b, "text_strikethrough")

    # FIX ME: think of better symbol to represent a <pre> block
    if prefs["Show code block button"]:
        b = self._addButton("text_pre", lambda: self.wrapInTags("pre",
            prefs["class_name"]), _("Ctrl+."),
            tip=_("Create a code block (Ctrl-.)"), check=False)
        set_icon(b, "text_pre")

    if prefs["Show horizontal rule button"]:
        b = self._addButton("hor_rule", self.toggleHorizontalLine, _("Ctrl+h"),
            tip=_("Create a horizontal rule (Ctrl+H)"), check=False)
        set_icon(b, "hor_rule")

    if prefs["Show indent button"]:
        b = self._addButton("indent", self.toggleIndent, _("Ctrl+Shift+]"),
            _("Indent text or list (Ctrl+Shift+])"), check=False)
        set_icon(b, "indent")

    if prefs["Show outdent button"]:
        b = self._addButton("outdent", self.toggleOutdent, _("Ctrl+Shift+["),
            _("Outdent text or list (Ctrl+Shift+[)"), check=False)
        set_icon(b, "outdent")

    # FIX ME: better symbol for <dl>
    if prefs["Show definition list button"]:
        b = self._addButton("deflist", self.toggleDefList, _("Ctrl+Shift+d"),
            _("Create definition list (Ctrl+Shift+D)"), check=False)
        set_icon(b, "deflist")

    if prefs["Show table button"]:
        b = self._addButton("table", self.toggleTable, _("Ctrl+Shift+3"),
            _("Create a table (Ctrl+Shift+3)"), check=False)
        set_icon(b, "table")

    if prefs["Show create button button"]:
        b = self._addButton("kbd", lambda: self.wrapInTags("kbd"),
            _("Ctrl+Shift+k"), _("Create a mimic button (Ctrl+Shift+K)"),
            check=False)
        # TODO ICON
        # set_icon(b, "kbd")

    if prefs["Show create link button"]:
        b = self._addButton("anchor", self.create_hyperlink, _("Ctrl+Shift+h"),
            _("Insert link (Ctrl+Shift+H)"), check=False)
        # TODO ICON
        # set_icon(b, "anchor")

def wrapInTags(self, tag, class_name=None):
    """Wrap selected text in selected a tag."""
    selection = self.web.selectedText()

    selection = escape_html_chars(selection)

    pattern = "@%*"
    self.web.eval("wrap('{0}', '{1}')".format(pattern, pattern[::-1]))
    
    # focus the field, so that changes are saved
    # this causes the cursor to go to the end of the field
    self.web.setFocus()
    self.web.eval("focusField(%d);" % self.currentField)

    self.saveNow()
    
    html = self.note.fields[self.currentField]

    tag_string_begin = ("<{0} class='{1}'>".format(tag, class_name) if
        class_name else "<{0}>".format(tag))
    tag_string_end = "</{0}>".format(tag)

    begin = html.find(pattern)
    end = html.find(pattern[::-1], begin)

    html = (html[:begin] + tag_string_begin + selection + tag_string_end +
        html[end+3:])

    # cleanup HTML: change all non-breakable spaces to normal spaces
    html = html.replace("&nbsp;", " ")

    # delete the current HTML and replace it by our new & improved one
    self.web.eval("setFormat('selectAll')")
    self.web.eval("document.execCommand('insertHTML', false, %s);"
            % json.dumps(html))

    # focus the field, so that changes are saved
    self.saveNow()
    
    self.web.setFocus()
    self.web.eval("focusField(%d);" % self.currentField)    

def create_hyperlink(self):
    dialog = QtGui.QDialog(self.parentWindow)
    dialog.setWindowTitle("Create a hyperlink")
    dialog.resize(350, 200)

    ok_button_anchor = QtGui.QPushButton("&OK", dialog)
    ok_button_anchor.setEnabled(False)
    ok_button_anchor.clicked.connect(lambda: self.insert_anchor(
        str(url_edit.text()), str(urltext_edit.text())))
    ok_button_anchor.clicked.connect(dialog.hide)

    ok_button_anchor.setAutoDefault(True)

    cancel_button_anchor = QtGui.QPushButton("&Cancel", dialog)
    cancel_button_anchor.clicked.connect(dialog.hide)
    cancel_button_anchor.setAutoDefault(True)

    url_label = QtGui.QLabel("Link to:")
    url_edit = QtGui.QLineEdit()
    url_edit.setPlaceholderText("URL")
    url_edit.textChanged.connect(lambda: self.enable_ok_button(ok_button_anchor,
        str(url_edit.text()), str(urltext_edit.text())))

    urltext_label = QtGui.QLabel("Text to display:")
    urltext_edit = QtGui.QLineEdit()
    urltext_edit.setPlaceholderText("Text")
    urltext_edit.textChanged.connect(lambda: self.enable_ok_button(
        ok_button_anchor, str(url_edit.text()), str(urltext_edit.text())))

    # if user already selected text, put it in urltext_edit
    selection = self.web.selectedText()
    if selection:
        urltext_edit.setText(selection)
    
    button_box = QtGui.QHBoxLayout()
    button_box.addStretch(1)
    button_box.addWidget(cancel_button_anchor)
    button_box.addWidget(ok_button_anchor)

    dialog_vbox = QtGui.QVBoxLayout()
    dialog_vbox.addWidget(url_label)
    dialog_vbox.addWidget(url_edit)
    dialog_vbox.addWidget(urltext_label)
    dialog_vbox.addWidget(urltext_edit)
    dialog_vbox.addLayout(button_box)

    dialog.setLayout(dialog_vbox)

    # give url_edit focus
    url_edit.setFocus()

    dialog.exec_()

def insert_anchor(self, url, text):
    # check for valid URL
    pattern = re.compile("(?i)https?://")
    match = re.match(pattern, text)
    if not match:
        url = "http://" + url

    text = escape_html_chars(text)

    replacement = "<a href=\"{0}\">{1}</a>".format(url, text)

    self.web.eval("document.execCommand('insertHTML', false, %s);"
        % json.dumps(replacement))

def enable_ok_button(self, button, url, text):
    if url and text:
        button.setEnabled(True)
    else:
        button.setEnabled(False)

def toggleUnorderedList(self):
    self.web.eval("setFormat('insertUnorderedList')")

def toggleOrderedList(self):
    self.web.eval("setFormat('insertOrderedList')")

def toggleStrikeThrough(self):
    self.web.eval("setFormat('strikeThrough')")

def togglePre(self):
    self.web.eval("setFormat('formatBlock', 'pre')")

def toggleHorizontalLine(self):
    self.web.eval("setFormat('insertHorizontalRule')")

def toggleIndent(self):
    self.web.eval("setFormat('indent')")

def toggleOutdent(self):
    self.web.eval("setFormat('outdent')")

class DefList(QtGui.QDialog):
    """Creates a definition list with one or more terms and descriptions."""
    def __init__(self, other, parentWindow):
        super(DefList, self).__init__()
        # other is whatever self is in the other methods
        self.other = other
        self.parentWindow = parentWindow
        self.data = list()
        self.setupUI()

    def setupUI(self):
        self.widget = QtGui.QDialog(self.parentWindow)
        # self.widget.resize(500, 300)
        self.widget.setWindowTitle("Add a definition list")

        self.dt_part = QtGui.QLineEdit(self.widget)
        self.dt_part.setPlaceholderText("definition term")
        dl_part_label = QtGui.QLabel("Definition term:")

        self.dd_part = QtGui.QTextEdit(self.widget)
        self.dd_part.setAcceptRichText(False)
        dd_part_label = QtGui.QLabel("Definition description:")

        addButton = QtGui.QPushButton("&Add more", self.widget)
        addButton.clicked.connect(self.addMore)

        buttonBox = QtGui.QDialogButtonBox(self.widget)
        buttonBox.addButton(addButton, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(QtGui.QDialogButtonBox.Ok)
        buttonBox.addButton(QtGui.QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.widget.accept)
        buttonBox.rejected.connect(self.widget.reject)

        vbox = QtGui.QVBoxLayout(self.widget)
        vbox.addWidget(dl_part_label)
        vbox.addWidget(self.dt_part)
        vbox.addWidget(dd_part_label)
        vbox.addWidget(self.dd_part)
        vbox.addWidget(buttonBox)

        self.widget.setLayout(vbox)

        if self.widget.exec_() == QtGui.QDialog.Accepted:
            # we won't allow any empty terms
            if not self.dt_part.text() == "":
                self.data.append((self.dt_part.text(), self.dd_part.toPlainText()))

            # if OK button pressed, but empty self.data list
            if not self.data:
                return

            # create all the terms and descriptions
            result = "<dl>"
            for key, value in self.data:
                result = result + "<dt><b>" + key + "</b></dt><dd>" + \
                    value + "</dd>"

            # we need the break <br /> at the end to "get out" of the <dl>
            result = result + "</dl><br />"

            self.other.web.eval("document.execCommand('insertHTML', false, %s);"
                % json.dumps(result))

    def addMore(self):
        """Adds a new definition term and description."""
        if not self.dt_part.text() == "":
            self.data.append((self.dt_part.text(), self.dd_part.toPlainText()))
        self.dt_part.clear()
        self.dd_part.clear()
        self.dt_part.setFocus()

def toggleDefList(self):
    dl = DefList(self, self.parentWindow)    

def toggleTable(self):
    "Set the number of columns and rows for a new table."

    dialog = QtGui.QDialog(self.parentWindow)
    dialog.setWindowTitle("Enter columns and rows")

    form = QtGui.QFormLayout()
    form.addRow(QtGui.QLabel("Enter the number of columns and rows"))
    
    columnSpinBox = QtGui.QSpinBox(dialog)
    columnSpinBox.setMinimum(1)
    columnSpinBox.setMaximum(10)
    columnSpinBox.setValue(2)
    columnLabel = QtGui.QLabel("Number of columns:")
    form.addRow(columnLabel, columnSpinBox)

    rowSpinBox = QtGui.QSpinBox(dialog)
    rowSpinBox.setMinimum(1)
    rowSpinBox.setMaximum(20)
    rowSpinBox.setValue(3)
    rowLabel = QtGui.QLabel("Number of rows:")
    form.addRow(rowLabel, rowSpinBox)

    buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
        QtGui.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, dialog)

    buttonBox.accepted.connect(dialog.accept)
    buttonBox.rejected.connect(dialog.reject)

    form.addRow(buttonBox)

    dialog.setLayout(form)

    if dialog.exec_() == QtGui.QDialog.Accepted:

        num_columns = columnSpinBox.value()
        num_rows = rowSpinBox.value() - 1

        num_header = counter(start=1, step=1)
        num_data = counter(start=1, step=1)

        header_column = "".join("<th align=\"left\" style=\"padding: 5px;"
            "border-bottom: 2px solid #00B3FF\">header{}</th>".format(
                next(num_header)) for _ in xrange(num_columns))
        body_column = "".join("<td style=\"padding: 5px; border-bottom:"
            "1px solid #B0B0B0\">data{}</td>".format(next(num_data))
            for _ in xrange(num_columns))
        body_row = "<tr>{}</tr>".format(body_column) * num_rows

        html = """
        <table style="width: 100%; border-collapse: collapse;">
            <thead><tr>{0}</tr></thead>
            <tbody>{1}</tbody>
        </table>""".format(header_column, body_row)

        self.web.eval("document.execCommand('insertHTML', false, %s);"
            % json.dumps(html))

# editor.Editor.ok_button_anchor = None
editor.Editor.enable_ok_button = enable_ok_button
editor.Editor.insert_anchor = insert_anchor
editor.Editor.create_hyperlink = create_hyperlink
editor.Editor.wrapInTags = wrapInTags
editor.Editor.toggleOrderedList = toggleOrderedList
editor.Editor.toggleUnorderedList = toggleUnorderedList
editor.Editor.toggleStrikeThrough = toggleStrikeThrough
editor.Editor.togglePre = togglePre
editor.Editor.toggleHorizontalLine = toggleHorizontalLine
editor.Editor.toggleIndent = toggleIndent
editor.Editor.toggleOutdent = toggleOutdent
editor.Editor.toggleDefList = toggleDefList
editor.Editor.toggleTable = toggleTable
editor.Editor.setupButtons = wrap(editor.Editor.setupButtons, mySetupButtons)

mw.ExtraButtons_Options = ExtraButtons_Options(mw)
mw.ExtraButtons_Options.setup_extra_buttons_options()
