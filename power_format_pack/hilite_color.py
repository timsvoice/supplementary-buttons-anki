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

from PyQt4 import QtGui, QtCore

from anki.utils import isMac, isWin
from prefhelper import PrefHelper


class HiliteColor(object):
    def __init__(self, editor, preferences):
        self.editor = editor
        self.p = preferences
        self.bg_color = self.p.PREFS.get("last_bg_color", "#00f")
        self.editor.setup_background_button = self.setup_background_button

    def setup_background_button(self, button):
        """
        Create the actual button that the user can click on.
        """
        self.editor.background_frame = QtGui.QFrame()
        self.editor.background_frame.setAutoFillBackground(True)
        self.editor.background_frame.setFocusPolicy(QtCore.Qt.NoFocus)
        self._on_bg_color_changed()
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.editor.background_frame)
        hbox.setMargin(5)
        button.setLayout(hbox)

    def apply_color(self):
        """
        Use last background color.
        """
        self._wrap_with_bg_color(self.bg_color)

    def change_color(self):
        """
        Choose new color.
        """
        new = QtGui.QColorDialog.getColor(QtGui.QColor(self.bg_color), None)
        # native dialog doesn't refocus us for some reason
        self.editor.parentWindow.activateWindow()
        if new.isValid():
            self.bg_color = new.name()
            self._on_bg_color_changed()
            self._wrap_with_bg_color(self.bg_color)

    def _update_background_button(self):
        """
        Update the button and show the last chosen background color.
        """
        self.editor.background_frame.setPalette(QtGui.QPalette(QtGui.QColor(self.bg_color)))

    def _on_bg_color_changed(self):
        """
        Event handler for when the hilite color has changed. Request to update the button,
        and save the new preferred color in the preferences.
        """
        self._update_background_button()
        self.p.PREFS["last_bg_color"] = self.bg_color
        PrefHelper.save_prefs(self.p.PREFS)

    def _wrap_with_bg_color(self, color):
        """
        Wrap the selected text in an appropriate tag with a background color.
        """
        # On Linux, the standard 'hiliteColor' method works. On Windows and OSX
        # the formatting seems to get filtered out

        self.editor.web.eval("""
            if (!setFormat('hiliteColor', '%s')) {
                setFormat('backcolor', '%s');
            }
            """ % (color, color))

        if isWin or isMac:
            # remove all Apple style classes, which is needed for
            # text highlighting on platforms other than Linux
            self.editor.web.eval("""
            var matches = document.querySelectorAll(".Apple-style-span");
            for (var i = 0; i < matches.length; i++) {
                matches[i].removeAttribute("class");
            }
            """)
