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

import const
from power_format_pack.list import List


class OrderedList(List):
    """
    Create an ordered list.
    """
    def __init__(self, editor, preferences, fixed_type=""):
        super(OrderedList, self).__init__(editor, fixed_type)
        self.c = preferences.CONFIG
        self._start("insertOrderedList")

    @QtCore.pyqtSlot()
    def show_dialog(self):
        self.setWindowTitle(self.c.get(const.CONFIG_WINDOW_TITLES, "ordered_list"))

        groupbox = QtGui.QGroupBox(
                self.c.get(const.CONFIG_LABELS, "ordered_list_type_label"),
                self)
        groupbox.setStyleSheet(const.QGROUPBOX_STYLE)

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

        start_label = QtGui.QLabel(
                self.c.get(const.CONFIG_LABELS, "ordered_list_start_label"),
                self)

        spinbox = QtGui.QSpinBox(self)
        spinbox.setMinimum(1)
        spinbox.setMaximum(100)

        spinbox_vbox = QtGui.QVBoxLayout()
        spinbox_vbox.addWidget(start_label)
        spinbox_vbox.addWidget(spinbox)
        spinbox_vbox.addStretch(1)

        button_box = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
                                            QtGui.QDialogButtonBox.Cancel,
                                            QtCore.Qt.Horizontal,
                                            self)

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

            selected_radio_button_id = radio_button_group.id(radio_button_group.checkedButton())
            choice = type_of_list.get(selected_radio_button_id, "1")

            self._apply(choice, spinbox.value())

    @QtCore.pyqtSlot(str)
    def _apply(self, type_of_list="1", start_num=1):
        """
        Create a new ordered list based on the input of the user.
        `type_of_list` is a string ("1", "A", "a", "I", "i") and
        `start_num` is an integer.
        """
        self.editor.web.eval("""
            document.execCommand('insertOrderedList');
            var olElem = window.getSelection().focusNode.parentNode;
            if (olElem !== null) {
                var setAttrs = true;
                while (olElem.toString() !== "[object HTMLOListElement]") {
                    olElem = olElem.parentNode;
                    if (olElem === null) {
                        setAttrs = false;
                        break;
                    }
                }
                if (setAttrs) {
                    olElem.setAttribute("type", "%s");
                    olElem.setAttribute("start", "%s");
                }
            }
        """ % (type_of_list[0], str(start_num)))
