# -*- coding: utf-8 -*-
#
# Copyright 2014-2016 Stefan van den Akker <srvandenakker.dev@gmail.com>
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
import utility
import const
import preferences
from prefhelper import PrefHelper


class ExtraButtons_Options(QtGui.QMenu):
    """
    Display the various options in the main menu.
    """

    def __init__(self, main_window, preferences):
        super(ExtraButtons_Options, self).__init__()
        self.main_window = main_window
        self.list_of_radio_buttons = list()
        config_path = os.path.join(PrefHelper.get_addons_folder(),
                                   const.FOLDER_NAME,
                                   const.CONFIG_FILENAME)
        self.c = utility.get_config_parser(config_path)

    def button_switch(self, state, name):
        """
        Puts a button either on or off. Reverses current state.
        """
        # source = self.sender()
        # name = source.text()
        # deprettify
        # name = self.deprettify_option_name(name)
        current_state = preferences.PREFS.get(name)
        if current_state is None:
            raise Exception("{!r} not in preferences".format(name))
        if bool(state) != current_state:
            preferences.PREFS[name] = not current_state

    def prettify_option_name(self, s):
        """
        Replace the underscore in the option name with a space and capitalize
        the resulting string.
        """
        return s.replace("_", " ").capitalize()

    def deprettify_option_name(self, s):
        """
        Replace the space in the option name with an underscore and make the
        resultant string lowercase.
        """
        return s.replace(" ", "_").lower()

    def create_checkbox(self, name, pretty_name=None, label=None):
        checkbox = QtGui.QCheckBox(pretty_name or label or name, self)
        if preferences.PREFS.get(name):
            checkbox.setChecked(True)
        checkbox.stateChanged.connect(
                lambda: self.button_switch(checkbox.isChecked(), name))
        return checkbox

    def create_radiobutton(self, name):
        return QtGui.QRadioButton(name)

    def setup_extra_buttons_options(self):

        sub_menu_title = self.c.get(const.CONFIG_MENU_NAMES, "sub_menu")
        sub_menu = self.main_window.form.menuTools.addMenu(sub_menu_title)

        options_action = QtGui.QAction(
                self.c.get(const.CONFIG_MENU_NAMES, "options_action"),
                self.main_window)
        options_action.triggered.connect(self.show_option_dialog)

        about_action = QtGui.QAction(
                self.c.get(const.CONFIG_MENU_NAMES, "about_action"),
                self.main_window)
        about_action.triggered.connect(self.show_about_dialog)

        doc_action = QtGui.QAction(
                self.c.get(const.CONFIG_MENU_NAMES, "doc_action"),
                self.main_window)
        doc_action.triggered.connect(self.show_doc_dialog)

        sub_menu.addAction(options_action)
        sub_menu.addAction(about_action)
        sub_menu.addAction(doc_action)

    def show_doc_dialog(self):
        dialog = QtGui.QDialog(self)
        dialog.setWindowTitle(self.c.get(const.CONFIG_WINDOW_TITLES,
                                         "doc_dialog"))

        filename = os.path.join(PrefHelper.get_addons_folder(),
                                const.FOLDER_NAME,
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
        QtGui.QMessageBox.about(self.main_window,
                                self.c.get(const.CONFIG_WINDOW_TITLES, "about"),
                                self.c.get(const.CONFIG_ABOUT, "about"))

    def enable_radio_buttons(self, checkbox):
        if checkbox.isChecked():
            # enable radio buttons
            for rb in self.list_of_radio_buttons:
                rb.setEnabled(True)
        else:
            # disable radiobuttons
            for rb in self.list_of_radio_buttons:
                rb.setEnabled(False)

    def override_disabled_buttons_rendered_markdown(self):
        """
        Create a checkbox that controls whether or not to allow editing when
        the Markdown is rendered.
        """
        cb = self.create_checkbox(const.MARKDOWN_OVERRIDE_EDITING,
                                  None,
                                  self.c.get(const.CONFIG_LABELS,
                                             "edit_rendered_markdown_label"))
        utility.set_tool_tip(cb, self.c.get(const.CONFIG_TOOLTIPS,
                                            "edit_rendered_markdown_tooltip"))
        return cb

    def show_option_dialog(self):
        option_dialog = QtGui.QDialog(self.main_window)
        option_dialog.setWindowTitle(self.c.get(const.CONFIG_WINDOW_TITLES,
                                                "option_dialog"))

        grid = QtGui.QGridLayout()
        l = [k for k in preferences.PREFS.keys() if k not in (
                                                const.CODE_CLASS,
                                                const.LAST_BG_COLOR,
                                                const.FIXED_OL_TYPE,
                                                const.MARKDOWN_SYNTAX_STYLE,
                                                const.MARKDOWN_LINE_NUMS,
                                                const.MARKDOWN_ALWAYS_REVERT,
                                                const.MARKDOWN_CODE_DIRECTION,
                                                const.BUTTON_PLACEMENT,
                                                const.MARKDOWN_OVERRIDE_EDITING
                                            )]
        num_items = len(l) / 2.0
        num_items = num_items + 0.5 if (num_items % 1.0 > 0.0) else num_items

        # go through the keys in the prefs and make QCheckBoxes for them
        for index, option in enumerate(sorted(l)):
            pretty_option = self.prettify_option_name(option)
            checkbox = self.create_checkbox(option, pretty_option)
            if index >= num_items:
                col = 1
                row = index - num_items
                grid.addWidget(checkbox, row, col)
            else:
                col = 0
                row = index
                grid.addWidget(checkbox, row, col)

        cssClassLabel = QtGui.QLabel(
            self.c.get(const.CONFIG_LABELS, "code_pre_label"), self)
        cssClassLabel.setToolTip(self.c.get(const.CONFIG_TOOLTIPS,
                                            "code_pre_tooltip"))
        cssClassText = QtGui.QLineEdit(
                preferences.PREFS.get(const.CODE_CLASS), self)
        cssClassHBox = QtGui.QHBoxLayout()
        cssClassHBox.addWidget(cssClassLabel)
        cssClassHBox.addWidget(cssClassText)

        checkBox = QtGui.QCheckBox(
                self.c.get(const.CONFIG_LABELS,
                           "ordered_list_type_label"),
                self)
        checkBox.setToolTip(self.c.get(const.CONFIG_TOOLTIPS,
                                       "ordered_list_type_tooltip"))
        if preferences.PREFS.get(const.FIXED_OL_TYPE):
            checkBox.setChecked(True)
        else:
            checkBox.setChecked(False)

        checkBox.stateChanged.connect(
                lambda: self.enable_radio_buttons(checkBox))

        # make sure self.list_of_radio_buttons is empty
        # before adding new buttons
        self.list_of_radio_buttons = list()
        for type_ol in ("1.", "A.", "a.", "I.", "i."):
            rb = self.create_radiobutton(type_ol)
            self.list_of_radio_buttons.append(rb)

        ol_type = preferences.PREFS.get(const.FIXED_OL_TYPE)
        if not ol_type:
            self.list_of_radio_buttons[0].toggle()
        else:
            for rb in self.list_of_radio_buttons:
                if ol_type == rb.text():
                    rb.toggle()
                    break

        buttonGroup = QtGui.QButtonGroup(self)

        numRadioButton = 0
        for rb in self.list_of_radio_buttons:
            buttonGroup.addButton(rb, numRadioButton)
            numRadioButton += 1

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(checkBox)
        for rb in self.list_of_radio_buttons:
            if not checkBox.isChecked():
                rb.setEnabled(False)
            hbox.addWidget(rb)

        # Markdown syntax highlighting

        md_style_label = QtGui.QLabel(
                    self.c.get(const.CONFIG_LABELS, "md_style_label"), self)
        md_style_combo = QtGui.QComboBox(self)
        md_style_combo.setMinimumWidth(const.MIN_COMBOBOX_WIDTH)
        md_style_files = os.listdir(os.path.join(PrefHelper.get_addons_folder(),
                                                 const.FOLDER_NAME,
                                                 "pygments",
                                                 "styles"))

        # pretty print styles
        for filename in sorted(md_style_files):
            if filename.startswith("_") or filename.endswith(".pyc"):
                continue
            (style, _) = os.path.splitext(filename)
            style = style.replace("_", " ").capitalize()
            md_style_combo.addItem(style)

        all_items_in_combo = \
            [md_style_combo.itemText(i) for i in xrange(md_style_combo.count())]
        current_style = preferences.PREFS.get(const.MARKDOWN_SYNTAX_STYLE)
        current_style = current_style.replace("_", " ").capitalize()
        if current_style and current_style in all_items_in_combo:
            index_current_style = all_items_in_combo.index(current_style)
            md_style_combo.setCurrentIndex(index_current_style)

        md_style_hbox = QtGui.QHBoxLayout()
        md_style_hbox.addWidget(md_style_label)
        md_style_hbox.addStretch(1)
        md_style_hbox.addWidget(md_style_combo)

        # line numbers Markdown code highlighting
        linenums_cb = QtGui.QCheckBox(
                self.c.get(const.CONFIG_LABELS, "linenums_cb_label"), self)
        if preferences.PREFS.get(const.MARKDOWN_LINE_NUMS):
            linenums_cb.setChecked(True)

        linenums_hbox = QtGui.QHBoxLayout()
        linenums_hbox.addWidget(linenums_cb)

        # align Markdown code block
        code_align_label = QtGui.QLabel(self.c.get(const.CONFIG_LABELS,
                                                   "code_align_label"))
        code_align_combo = QtGui.QComboBox(self)
        code_align_combo.setMinimumWidth(const.MIN_COMBOBOX_WIDTH)
        alignments = ("left", "center", "right")
        for alignment in alignments:
            code_align_combo.addItem(alignment)
        current_alignment = preferences.PREFS.get(
                const.MARKDOWN_CODE_DIRECTION)
        code_align_combo.setCurrentIndex(alignments.index(current_alignment))
        code_align_hbox = QtGui.QHBoxLayout()
        code_align_hbox.addWidget(code_align_label)
        code_align_hbox.addStretch(1)
        code_align_hbox.addWidget(code_align_combo)

        # option to always revert automatically back to old Markdown
        # and skip the warning dialog
        automatic_revert_cb = QtGui.QCheckBox(
                self.c.get(const.CONFIG_LABELS,
                           "automatic_revert_cb_label"),
                self)
        utility.set_tool_tip(automatic_revert_cb,
                             self.c.get(const.CONFIG_TOOLTIPS,
                                        "automatic_revert_cb_tooltip"))
        if preferences.PREFS.get(const.MARKDOWN_ALWAYS_REVERT):
            automatic_revert_cb.setChecked(True)

        automatic_revert_hbox = QtGui.QHBoxLayout()
        automatic_revert_hbox.addWidget(automatic_revert_cb)

        # override disabled buttons in rendered Markdown
        edit_rendered_md_cb = self.override_disabled_buttons_rendered_markdown()
        edit_rendered_md_cb_hbox = QtGui.QHBoxLayout()
        edit_rendered_md_cb_hbox.addWidget(edit_rendered_md_cb)

        # button placement
        button_placement_label = QtGui.QLabel(u"Buttons placement")
        button_placement_combo = QtGui.QComboBox(self)
        button_placement_combo.setMinimumWidth(const.MIN_COMBOBOX_WIDTH)
        for placement in const.PLACEMENT_POSITIONS:
            button_placement_combo.addItem(placement)
        current_placement = preferences.PREFS.get(
                const.BUTTON_PLACEMENT)
        button_placement_combo.setCurrentIndex(
                const.PLACEMENT_POSITIONS.index(current_placement))
        button_placement_hbox = QtGui.QHBoxLayout()
        button_placement_hbox.addWidget(button_placement_label)
        button_placement_hbox.addStretch(1)
        button_placement_hbox.addWidget(button_placement_combo)

        button_box = QtGui.QDialogButtonBox(
                QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        button_box.accepted.connect(option_dialog.accept)
        button_box.rejected.connect(option_dialog.reject)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addWidget(utility.create_horizontal_rule())
        vbox.addLayout(button_placement_hbox)
        vbox.addWidget(utility.create_horizontal_rule())
        vbox.addLayout(cssClassHBox)
        vbox.addWidget(utility.create_horizontal_rule())
        vbox.addLayout(hbox)
        vbox.addWidget(utility.create_horizontal_rule())
        vbox.addLayout(md_style_hbox)
        vbox.addLayout(code_align_hbox)
        vbox.addLayout(linenums_hbox)
        vbox.addLayout(automatic_revert_hbox)
        vbox.addLayout(edit_rendered_md_cb_hbox)
        vbox.addWidget(button_box)

        option_dialog.setLayout(vbox)

        if option_dialog.exec_() == QtGui.QDialog.Accepted:
            # fixed ordered list type
            if checkBox.isChecked():
                selected_radio_button = \
                        buttonGroup.id(buttonGroup.checkedButton())
                preferences.PREFS[const.FIXED_OL_TYPE] = \
                    self.list_of_radio_buttons[selected_radio_button].text()
            else:
                preferences.PREFS[const.FIXED_OL_TYPE] = ""

            # line numbers for Markdown code highlighting
            if linenums_cb.isChecked():
                preferences.PREFS[const.MARKDOWN_LINE_NUMS] = True
            else:
                preferences.PREFS[const.MARKDOWN_LINE_NUMS] = False

            # always revert automatically back to old Markdown
            if automatic_revert_cb.isChecked():
                preferences.PREFS[const.MARKDOWN_ALWAYS_REVERT] = True
            else:
                preferences.PREFS[const.MARKDOWN_ALWAYS_REVERT] = False

            # style for code highlighting
            chosen_style = str(md_style_combo.currentText())
            chosen_style = chosen_style.lower().replace(" ", "_")
            preferences.PREFS[const.MARKDOWN_SYNTAX_STYLE] = chosen_style

            # alignment for Markdown code blocks
            chosen_alignment = str(code_align_combo.currentText())
            preferences.PREFS[const.MARKDOWN_CODE_DIRECTION] = \
                chosen_alignment

            # button placement
            chosen_placement = str(button_placement_combo.currentText())
            preferences.PREFS[const.BUTTON_PLACEMENT] = chosen_placement

            preferences.PREFS[const.CODE_CLASS] = cssClassText.text()

            PrefHelper.save_prefs(preferences.PREFS)
