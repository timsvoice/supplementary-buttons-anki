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

from PyQt4 import QtGui, QtCore

import const
from utility import Utility


class ExtraButtons_Options(QtGui.QMenu):
    """Display the various options in the main menu."""

    def __init__(self, main_window, preferences):
        super(ExtraButtons_Options, self).__init__()
        self.main_window = main_window
        self.preferences = preferences
        self.listOfRadioButtons = list()

    def button_switch(self, state):
        """Puts a button either on or off. Reverses current state."""
        source = self.sender()
        name = source.text()
        current_state = self.preferences.prefs[name]
        if bool(state) != current_state:
            self.preferences.prefs[name] = not current_state

    def create_checkbox(self, name, main_window):
        checkbox = QtGui.QCheckBox(name, self)
        if self.preferences.prefs[name]:
            checkbox.setChecked(True)
        checkbox.stateChanged.connect(self.button_switch)
        return checkbox

    def create_radiobutton(self, name):
        radiobutton = QtGui.QRadioButton(name)
        return radiobutton

    def setup_extra_buttons_options(self):

        sub_menu_title = "&Supplementary buttons add-on (options)"
        sub_menu = self.main_window.form.menuTools.addMenu(sub_menu_title)

        options_action = QtGui.QAction("&Button options...", self.main_window)
        options_action.triggered.connect(self.show_option_dialog)

        about_action = QtGui.QAction(
                "&About {0}...".format(const.PROGRAM_NAME), self.main_window)
        about_action.triggered.connect(self.show_about_dialog)

        # custom_css = QtGui.QAction("&Alter <code> and <pre> CSS...", main_window)
        # custom_css.triggered.connect(self.preferences.set_css_class_name_code_pre)

        sub_menu.addAction(options_action)
        # sub_menu.addAction(custom_css)
        sub_menu.addAction(about_action)

    def show_about_dialog(self):
        about_dialog = QtGui.QMessageBox.about(self.main_window,
            "About {0} v{1}".format(const.PROGRAM_NAME, const.VERSION),
            """\
        Copyright: <b>Stefan van den Akker</b>, {0}-{1}<br />
        Version: {2}<br />
        Email: <a href="mailto:{3}">{3}</a><br />
        Bugs & feature requests or if you want to help out with code:
            <a href="{4}">Github</a><br /><br />
        Don't forget to rate and share your thoughts on <a href="{5}">AnkiWeb</a>!
            """.format(const.YEAR_START, const.YEAR_LAST, const.VERSION,
                        const.EMAIL, const.GITHUB_URL, const.ANKIWEB_URL)
        )

    def enableRadioButtons(self, checkbox):
        if checkbox.isChecked():
            # enable radio buttons
            for rb in self.listOfRadioButtons:
                rb.setEnabled(True)
        else:
            # disable radiobuttons
            for rb in self.listOfRadioButtons:
                rb.setEnabled(False)

    def show_option_dialog(self):
        option_dialog = QtGui.QDialog(self.main_window)
        option_dialog.setWindowTitle("Options for Supplementary Buttons")

        grid = QtGui.QGridLayout()

        # create a dict that has all the relevant buttons to be displayed
        l = [k for k in self.preferences.prefs.keys() if k not in
                ("class_name", "last_bg_color", "fixed_ol_type")]

        # determine number of items in each column in the grid
        num_items = len(l) / 2.0
        num_items = num_items + 0.5 if (num_items % 1.0 > 0.0) else num_items

        # go through the keys in the prefs and make QCheckBoxes for them
        for index, option in enumerate(sorted(l)):
            checkbox = self.create_checkbox(option, self.main_window)
            if index >= num_items:
                col = 1
                row = index - num_items
                grid.addWidget(checkbox, row, col)
            else:
                col = 0
                row = index
                grid.addWidget(checkbox, row, col)

        cssClassLabel = QtGui.QLabel(
                "CSS class for &lt;code&gt; and &lt;pre&gt; code blocks", self)
        cssClassText = QtGui.QLineEdit(
                self.preferences.prefs.get("class_name"), self)
        cssClassHBox = QtGui.QHBoxLayout()
        cssClassHBox.addWidget(cssClassLabel)
        cssClassHBox.addWidget(cssClassText)

        checkBox = QtGui.QCheckBox("Fix ordered list type", self)
        if self.preferences.prefs["fixed_ol_type"]:
            checkBox.setChecked(True)
        else:
            checkBox.setChecked(False)

        checkBox.stateChanged.connect(lambda: self.enableRadioButtons(checkBox))

        # make sure self.listOfRadioButtons is empty before adding new buttons
        self.listOfRadioButtons = list()
        for type_ol in ("1.", "A.", "a.", "I.", "i."):
            rb = self.create_radiobutton(type_ol)
            self.listOfRadioButtons.append(rb)

        ol_type = self.preferences.prefs.get("fixed_ol_type")
        if not ol_type:
            self.listOfRadioButtons[0].toggle()
        else:
            for rb in self.listOfRadioButtons:
                if ol_type == rb.text():
                    rb.toggle()
                    break

        buttonGroup = QtGui.QButtonGroup(self)

        numRadioButton = 0
        for rb in self.listOfRadioButtons:
            buttonGroup.addButton(rb, numRadioButton)
            numRadioButton += 1

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(checkBox)
        for rb in self.listOfRadioButtons:
            if not checkBox.isChecked():
                rb.setEnabled(False)
            hbox.addWidget(rb)

        button_box = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
                QtGui.QDialogButtonBox.Cancel)
        button_box.accepted.connect(option_dialog.accept)
        button_box.rejected.connect(option_dialog.reject)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addWidget(Utility.create_horizontal_rule())
        vbox.addLayout(cssClassHBox)
        vbox.addWidget(Utility.create_horizontal_rule())
        vbox.addLayout(hbox)
        vbox.addWidget(button_box)

        option_dialog.setLayout(vbox)

        if option_dialog.exec_() == QtGui.QDialog.Accepted:
            if checkBox.isChecked():
                selectedRadioButton = buttonGroup.id(buttonGroup.checkedButton())
                self.preferences.prefs["fixed_ol_type"] = (
                        self.listOfRadioButtons[selectedRadioButton].text())
            else:
                self.preferences.prefs["fixed_ol_type"] = ""

            # change CSS class for <code> and <pre>
            self.preferences.prefs["class_name"] = cssClassText.text()

            # save preferences to disk
            self.preferences.save_prefs()


