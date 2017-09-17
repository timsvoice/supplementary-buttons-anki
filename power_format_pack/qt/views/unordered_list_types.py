# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'unordered_list_types.ui'
#
# Created by: PyQt4 UI code generator 4.12
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_unordered_list_dialog(object):
    def setupUi(self, unordered_list_dialog):
        unordered_list_dialog.setObjectName(_fromUtf8("unordered_list_dialog"))
        unordered_list_dialog.setWindowModality(QtCore.Qt.WindowModal)
        unordered_list_dialog.resize(228, 181)
        unordered_list_dialog.setMinimumSize(QtCore.QSize(228, 181))
        unordered_list_dialog.setMaximumSize(QtCore.QSize(228, 181))
        unordered_list_dialog.setModal(True)
        self.button_box = QtGui.QDialogButtonBox(unordered_list_dialog)
        self.button_box.setGeometry(QtCore.QRect(0, 140, 221, 41))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(False)
        self.button_box.setObjectName(_fromUtf8("button_box"))
        self.group_box_types = QtGui.QGroupBox(unordered_list_dialog)
        self.group_box_types.setGeometry(QtCore.QRect(9, 10, 211, 131))
        self.group_box_types.setStyleSheet(_fromUtf8(""))
        self.group_box_types.setAlignment(QtCore.Qt.AlignCenter)
        self.group_box_types.setFlat(False)
        self.group_box_types.setObjectName(_fromUtf8("group_box_types"))
        self.verticalLayoutWidget = QtGui.QWidget(self.group_box_types)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 191, 104))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.radio_button_disc = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.radio_button_disc.setChecked(True)
        self.radio_button_disc.setObjectName(_fromUtf8("radio_button_disc"))
        self.qradiobutton_group_types = QtGui.QButtonGroup(unordered_list_dialog)
        self.qradiobutton_group_types.setObjectName(_fromUtf8("qradiobutton_group_types"))
        self.qradiobutton_group_types.addButton(self.radio_button_disc)
        self.verticalLayout.addWidget(self.radio_button_disc)
        self.radio_button_circle = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.radio_button_circle.setObjectName(_fromUtf8("radio_button_circle"))
        self.qradiobutton_group_types.addButton(self.radio_button_circle)
        self.verticalLayout.addWidget(self.radio_button_circle)
        self.radio_button_square = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.radio_button_square.setStyleSheet(_fromUtf8(""))
        self.radio_button_square.setObjectName(_fromUtf8("radio_button_square"))
        self.qradiobutton_group_types.addButton(self.radio_button_square)
        self.verticalLayout.addWidget(self.radio_button_square)

        self.retranslateUi(unordered_list_dialog)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), unordered_list_dialog.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), unordered_list_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(unordered_list_dialog)

    def retranslateUi(self, unordered_list_dialog):
        unordered_list_dialog.setWindowTitle(_translate("unordered_list_dialog", "Choose type", None))
        self.group_box_types.setTitle(_translate("unordered_list_dialog", "Types", None))
        self.radio_button_disc.setText(_translate("unordered_list_dialog", "● disc", None))
        self.radio_button_circle.setText(_translate("unordered_list_dialog", "○ circle", None))
        self.radio_button_square.setText(_translate("unordered_list_dialog", "⬛ square", None))

