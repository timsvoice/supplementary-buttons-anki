# -*- coding: utf-8 -*-
# Written by Stefan van den Akker in 2014 <srvandenakker@gmail.com>
# License: GNU GPLv3 or later; https://www.gnu.org/licenses/gpl.html
#
# TO DO:
# - prevent QActions from hiding after they are triggered

import os

from anki.utils import json
from aqt import editor, mw
from anki.hooks import wrap
from PyQt4 import QtGui, QtCore


# Preferences
##################################################

def addons_folder():
    return mw.pm.addonFolder()

addon_path = os.path.join(addons_folder(), ".extra_buttons_prefs")

default_conf = {"class_name": "",
                "Show <code> button": True,
                "Show unordered list button": True,
                "Show ordered list button": True,
                "Show strikethrough button": True,
                "Show code block button": True,
                "Show horizontal rule button": True,
                "Show indent button": True,
                "Show outdent button": True}

try:
    with open(addon_path, "r") as f:
        prefs = json.load(f)
except IOError:
    with open(addon_path, "w") as f:
        prefs = default_conf
        json.dump(prefs, f)

def save_prefs():
    with open(addon_path, "w") as f:
        json.dump(prefs, f)

def get_class_name(self):
    """Sets the CSS styling for the <code> and <pre> tags"""

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
    "Displays the various options in the main menu."

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

        custom_css = QtGui.QAction("&Alter <code> CSS...", mw)
        custom_css.triggered.connect(get_class_name)
        
        sub_menu.addAction(custom_css)


# Buttons
##################################################

def mySetupButtons(self):

    if prefs["Show <code> button"]:
        self._addButton("text_code", self.toggleCode, _("Ctrl+,"),
            _("Code format text (Ctrl+,)"), check=False, text=u"<>")

    if prefs["Show unordered list button"]:
        self._addButton("unordered_list", self.toggleUnorderedList, _("Ctrl+["),
            _("Create unordered list (Ctrl+[)"), check=False, text=u"*")

    if prefs["Show ordered list button"]:
        self._addButton("ordered_list", self.toggleOrderedList, _("Ctrl+]"),
            _("Create ordered list (Ctrl+])"), check=False, text=u"1.")

    if prefs["Show strikethrough button"]:
        self._addButton("text_strikethrough", self.toggleStrikeThrough,
            _("Alt+Shift+5"), _("Strikethrough text (Alt+Shift+5)"), check=True,
            text=u"Z\u0336")

    if prefs["Show code block button"]:
        # FIX ME: think of better symbol to represent a <pre> block
        self._addButton("text_pre", self.togglePre, _("Ctrl-."),
            tip=_("Create a code block (Ctrl-.)"), check=False, text=u"{}")

    if prefs["Show horizontal rule button"]:
        self._addButton("hor_line", self.toggleHorizontalLine, _("Ctrl+h"),
            tip=_("Create a horizontal line (Ctrl+H)"),
            check=False, text=u"\u2014")

    if prefs["Show indent button"]:
        self._addButton("indent", self.toggleIndent, _("Ctrl+Shift+i"),
            _("Indent text or list (Ctrl+Shift+I)"), check=False, text=u">>")

    if prefs["Show outdent button"]:
        self._addButton("outdent", self.toggleOutdent, _("Ctrl+Shift+o"),
            _("Outdent text or list (Ctrl+Shift+O)"), check=False, text=u"<<")

def toggleCode(self):
    # FIX ME: if an <div> element appears before the selected text
    # the wrap will not work; as a workaround I check for <div>s before the
    # selected text and create a recognizable pattern @%* that is put before
    # every <code> element, and subsequently delete it

    selection = self.web.selectedText()

    # check whether we are dealing with a new or existing note; if the 
    # currentField is empty, the note did not yet exist prior to editing
    self.saveNow()
    html = self.note.fields[self.currentField]

    # check if the current selected is preceded by a <div> element
    b = "<div>" + selection in html or selection + "</div>" in html

    if b:
        pattern = "@%*"
    else:
        pattern = ""
    
    # if a custom name for the CSS governing <code> is given, use it
    if prefs["class_name"]:
        self.web.eval("document.execCommand('insertHTML', false, %s);"
            % json.dumps("{0}<code class={1}>".format(pattern, prefs["class_name"]) + 
                selection + "</code>"))
    else:
        self.web.eval("wrap('{0}<code>', '</code>');".format(pattern))
    
    # focus the field, so that changes are saved
    # this causes the cursor to go to the end of the field
    self.web.setFocus()
    self.web.eval("focusField(%d);" % self.currentField)

    self.saveNow()
    
    if b:
        html = self.note.fields[self.currentField]

        html = html.replace("@%*", "")

        # cleanup HTML: change all non-breakable spaces to normal spaces
        html = html.replace("&nbsp;", " ")

        # delete the current HTML and replace it by our new & improved one
        self.web.eval("setFormat('selectAll')")
        self.web.eval("setFormat('delete')")
        self.web.eval("document.execCommand('insertHTML', false, %s);"
                % json.dumps(html))

    # focus the field, so that changes are saved
    self.saveNow()
    
    self.web.setFocus()
    self.web.eval("focusField(%d);" % self.currentField)
    

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


editor.Editor.toggleCode = toggleCode
editor.Editor.toggleOrderedList = toggleOrderedList
editor.Editor.toggleUnorderedList = toggleUnorderedList
editor.Editor.toggleStrikeThrough = toggleStrikeThrough
editor.Editor.togglePre = togglePre
editor.Editor.toggleHorizontalLine = toggleHorizontalLine
editor.Editor.toggleIndent = toggleIndent
editor.Editor.toggleOutdent = toggleOutdent
editor.Editor.setupButtons = wrap(editor.Editor.setupButtons, mySetupButtons)

mw.ExtraButtons_Options = ExtraButtons_Options(mw)
mw.ExtraButtons_Options.setup_extra_buttons_options()
