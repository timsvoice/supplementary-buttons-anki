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

class OrderedList(QtGui.QDialog):
    def __init__(self, other, parent_window, preferences, fixed=False):
        super(OrderedList, self).__init__(parent_window)
        self.editor_instance = other

        if not fixed:
            self.setupGUI()
        else:
            self.insertOrderedList(const.preferences.prefs["fixed_ol_type"][0], 1)

    def setupGUI(self):
        self.setWindowTitle("Choose format for ordered list")

        stylesheet = """
        QGroupBox { border: 1px inset lightgrey;
                            border-radius: 5px;
                            margin-top: 10px;
                            font-weight: bold; }
        QGroupBox::title {  subcontrol-origin: margin;
                            subcontrol-position: top;
                            padding:0 3px 0 3px; }
        """

        groupbox = QtGui.QGroupBox("Type", self)
        groupbox.setStyleSheet(stylesheet)

        # stylesheet for the radio buttons
        self.setStyleSheet("QRadioButton { font-weight: bold; }")

        radio_button1 = QtGui.QRadioButton("1.", self)
        radio_button1.setChecked(True)
        radio_button2 = QtGui.QRadioButton("A.", self)
        radio_button3 = QtGui.QRadioButton("a.", self)
        radio_button4 = QtGui.QRadioButton("I.", self)
        radio_button5 = QtGui.QRadioButton("i.", self)

        radio_button_group = QtGui.QButtonGroup(self)
        radio_button_group.addButton(radio_button1)
        radio_button_group.setId(radio_button1, 1)
        radio_button_group.addButton(radio_button2)
        radio_button_group.setId(radio_button2, 2)
        radio_button_group.addButton(radio_button3)
        radio_button_group.setId(radio_button3, 3)
        radio_button_group.addButton(radio_button4)
        radio_button_group.setId(radio_button4, 4)
        radio_button_group.addButton(radio_button5)
        radio_button_group.setId(radio_button5, 5)

        radio_vbox = QtGui.QVBoxLayout(self)
        radio_vbox.addWidget(radio_button1)
        radio_vbox.addWidget(radio_button2)
        radio_vbox.addWidget(radio_button3)
        radio_vbox.addWidget(radio_button4)
        radio_vbox.addWidget(radio_button5)

        groupbox.setLayout(radio_vbox)

        start_label = QtGui.QLabel("<b>Start:</b>", self)

        spinbox = QtGui.QSpinBox(self)
        spinbox.setMinimum(1)
        spinbox.setMaximum(100)
        # get value with .value()

        spinbox_vbox = QtGui.QVBoxLayout()
        spinbox_vbox.addWidget(start_label)
        spinbox_vbox.addWidget(spinbox)
        spinbox_vbox.addStretch(1)

        button_box = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
            QtGui.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        spinbox_vbox.addWidget(button_box)

        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(groupbox)
        hbox.addLayout(spinbox_vbox)

        self.setLayout(hbox)

        if self.exec_() == QtGui.QDialog.Accepted:
            type_of_list = {
                    1: "1",
                    2: "A",
                    3: "a",
                    4: "I",
                    5: "i"
            }

            choice = type_of_list.get(
                    radio_button_group.id(radio_button_group.checkedButton()), "1")

            self.insertOrderedList(choice, spinbox.value())

    def insertOrderedList(self, type_of_list, start_num):
        """Create a new ordered list based on the input of the user.
        type_of_list is a string ("1", "A", "a", "I", "i") and
        start_num is an integer."""
        self.editor_instance.web.eval("""
            document.execCommand('insertOrderedList');
            var olElem = window.getSelection().focusNode.parentNode;
            if (olElem.toString() !== "[object HTMLOListElement]") {
                olElem = olElem.parentNode;
            }
            olElem.setAttribute("type", "%s");
            olElem.setAttribute("start", "%s");
            olElem.style.marginLeft = "20px";
            """ % (type_of_list, str(start_num))
        )

