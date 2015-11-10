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

from PyQt4 import QtGui, QtCore, QtWebKit
import os
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
        # deprettify
        name = name.lower().replace(" ", "_")
        current_state = self.preferences.prefs.get(name)
        if current_state is None:
            raise Exception("{!r} not in preferences".format(name))
        if bool(state) != current_state:
            self.preferences.prefs[name] = not current_state

    def create_checkbox(self, name):
        # TODO: better names, maybe stored in properties file
        # prettify option name
        pretty_name = name.replace("_", " ").capitalize()
        checkbox = QtGui.QCheckBox(pretty_name, self)
        if self.preferences.prefs.get(name):
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

        doc_action = QtGui.QAction("&Documentation...", self.main_window)
        doc_action.triggered.connect(self.show_doc_dialog)

        sub_menu.addAction(options_action)
        sub_menu.addAction(about_action)
        sub_menu.addAction(doc_action)

    def show_doc_dialog(self):
        dialog = QtGui.QDialog(self)
        dialog.setWindowTitle("Supplementary Buttons for Anki Documentation")

        filename = os.path.join(self.preferences.addons_folder(),
                                "extra_buttons",
                                "docs",
                                "doc_start.html")

        if not os.path.exists(filename):
            print "FILENAME {!r} DOES NOT EXIST".format(filename)
            return

        help_buttons = QtGui.QDialogButtonBox(dialog)
        help_buttons.setStandardButtons(QtGui.QDialogButtonBox.Ok)

        help_buttons.accepted.connect(dialog.accept)

        view = QtWebKit.QWebView(dialog)
        view.load(QtCore.QUrl(filename))

        help_vbox = QtGui.QVBoxLayout()
        help_vbox.addWidget(view)
        help_vbox.addWidget(help_buttons)

        dialog.setLayout(help_vbox)

        dialog.exec_()

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
        l = [k for k in self.preferences.prefs.keys() if k not in (
                                                const.CODE_CLASS,
                                                const.LAST_BG_COLOR,
                                                const.FIXED_OL_TYPE,
                                                const.MARKDOWN_SYNTAX_STYLE,
                                                const.MARKDOWN_LINE_NUMS,
                                                const.MARKDOWN_ALWAYS_REVERT
                                            )]
        num_items = len(l) / 2.0
        num_items = num_items + 0.5 if (num_items % 1.0 > 0.0) else num_items

        # go through the keys in the prefs and make QCheckBoxes for them
        for index, option in enumerate(sorted(l)):
            checkbox = self.create_checkbox(option)
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
        cssClassLabel.setToolTip("""\
This class will be automatically added when you use the code and pre buttons.
You can add the CSS you want in your stylesheet and refer to this class. E.g.
.myCodeClass { color: red; } will color the text of your code and pre elements
red.\
        """)
        cssClassText = QtGui.QLineEdit(
                self.preferences.prefs.get(const.CODE_CLASS), self)
        cssClassHBox = QtGui.QHBoxLayout()
        cssClassHBox.addWidget(cssClassLabel)
        cssClassHBox.addWidget(cssClassText)

        checkBox = QtGui.QCheckBox("Fix ordered list type", self)
        checkBox.setToolTip("Do not show the choice dialog each time, "
                "but always use the selected list type.")
        if self.preferences.prefs.get(const.FIXED_OL_TYPE):
            checkBox.setChecked(True)
        else:
            checkBox.setChecked(False)

        checkBox.stateChanged.connect(lambda: self.enableRadioButtons(checkBox))

        # make sure self.listOfRadioButtons is empty before adding new buttons
        self.listOfRadioButtons = list()
        for type_ol in ("1.", "A.", "a.", "I.", "i."):
            rb = self.create_radiobutton(type_ol)
            self.listOfRadioButtons.append(rb)

        ol_type = self.preferences.prefs.get(const.FIXED_OL_TYPE)
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

        # Markdown syntax highlighting

        md_style_label = QtGui.QLabel("Markdown syntax highlighting style", self)
        md_style_combo = QtGui.QComboBox(self)
        md_style_files = os.listdir(os.path.join(
            self.preferences.addons_folder(), const.FOLDER_NAME, "pygments", "styles"))
        print "Files in style folder:\n",
        print md_style_files

        # pretty print styles
        for filename in sorted(md_style_files):
            if filename.startswith("_") or filename.endswith(".pyc"):
                continue
            (style, _) = os.path.splitext(filename)
            style = style.replace("_", " ").capitalize()
            md_style_combo.addItem(style)

        all_items_in_combo = \
            [md_style_combo.itemText(i) for i in xrange(md_style_combo.count())]
        current_style = self.preferences.prefs.get(const.MARKDOWN_SYNTAX_STYLE)
        current_style = current_style.replace("_", " ").capitalize()
        if current_style and current_style in all_items_in_combo:
            index_current_style = all_items_in_combo.index(current_style)
            md_style_combo.setCurrentIndex(index_current_style)

        md_style_hbox = QtGui.QHBoxLayout()
        md_style_hbox.addWidget(md_style_label)
        md_style_hbox.addWidget(md_style_combo)

        # line numbers Markdown code highlighting
        linenums_cb = QtGui.QCheckBox(
                "Toggle line numbers code highlighting", self)
        if const.preferences.prefs.get(const.MARKDOWN_LINE_NUMS):
            linenums_cb.setChecked(True)

        linenums_hbox = QtGui.QHBoxLayout()
        linenums_hbox.addWidget(linenums_cb)

        # always revert automatically back to old Markdown
        # and skip the warning dialog
        automatic_revert_cb = QtGui.QCheckBox(
                "Always revert back automatically to old Markdown", self)
        automatic_revert_cb.setToolTip("""\
Do not show the warning dialog each time a conflict occurs, but revert back to
the old Markdown, discarding any changes made.\
""")
        if const.preferences.prefs.get(const.MARKDOWN_ALWAYS_REVERT):
            automatic_revert_cb.setChecked(True)

        automatic_revert_hbox = QtGui.QHBoxLayout()
        automatic_revert_hbox.addWidget(automatic_revert_cb)

        button_box = QtGui.QDialogButtonBox(
                QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        button_box.accepted.connect(option_dialog.accept)
        button_box.rejected.connect(option_dialog.reject)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addWidget(Utility.create_horizontal_rule())
        vbox.addLayout(cssClassHBox)
        vbox.addWidget(Utility.create_horizontal_rule())
        vbox.addLayout(hbox)
        vbox.addWidget(Utility.create_horizontal_rule())
        vbox.addLayout(md_style_hbox)
        vbox.addLayout(linenums_hbox)
        vbox.addLayout(automatic_revert_hbox)
        vbox.addWidget(button_box)

        option_dialog.setLayout(vbox)

        if option_dialog.exec_() == QtGui.QDialog.Accepted:
            # fixed ordered list type
            if checkBox.isChecked():
                selectedRadioButton = buttonGroup.id(buttonGroup.checkedButton())
                self.preferences.prefs[const.FIXED_OL_TYPE] = \
                    self.listOfRadioButtons[selectedRadioButton].text()
            else:
                self.preferences.prefs[const.FIXED_OL_TYPE] = ""

            # line numbers for Markdown code highlighting
            if linenums_cb.isChecked():
                const.preferences.prefs[const.MARKDOWN_LINE_NUMS] = True
            else:
                const.preferences.prefs[const.MARKDOWN_LINE_NUMS] = False

            # always revert automatically back to old Markdown
            if automatic_revert_cb.isChecked():
                const.preferences.prefs[const.MARKDOWN_ALWAYS_REVERT] = True
            else:
                const.preferences.prefs[const.MARKDOWN_ALWAYS_REVERT] = False

            # style for code highlighting
            chosen_style = str(md_style_combo.currentText())
            chosen_style = chosen_style.lower().replace(" ", "_")
            self.preferences.prefs[const.MARKDOWN_SYNTAX_STYLE] = chosen_style

            self.preferences.prefs[const.CODE_CLASS] = cssClassText.text()

            self.preferences.save_prefs()
