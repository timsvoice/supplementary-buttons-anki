from PyQt4 import QtGui, QtCore

from power_format_pack import const
from power_format_pack.list import List
from power_format_pack.qt.views.unordered_list_types import Ui_unordered_list_dialog


class UnorderedList(List):
    """
    Create an unordered list.
    """

    def __init__(self, editor, fixed_type=""):
        super(UnorderedList, self).__init__(editor, fixed_type)
        self.ui = None
        self._start("insertUnorderedList")

    @QtCore.pyqtSlot()
    def show_dialog(self):
        """
        Create and display a dialog window displaying options for the unordered list.
        """
        self.ui = Ui_unordered_list_dialog()
        self.ui.setupUi(self)
        self.ui.group_box_types.setStyleSheet(const.QGROUPBOX_STYLE)
        ok_button = self.ui.button_box.button(QtGui.QDialogButtonBox.Ok)
        ok_button.setDefault(True)
        ok_button.setAutoDefault(True)
        ok_button.setFocus(True)
        cancel_button = self.ui.button_box.button(QtGui.QDialogButtonBox.Cancel)
        cancel_button.setDefault(False)
        cancel_button.setAutoDefault(False)
        self.exec_()

    def accept(self):
        selected_radiobutton = self.ui.qradiobutton_group_types.checkedButton()
        type_of_list = {
            "radio_button_disc": "disc",
            "radio_button_circle": "circle",
            "radio_button_square": "square"
        }
        choice = type_of_list.get(selected_radiobutton.objectName())
        self._apply(choice)
        super(UnorderedList, self).accept()

    @QtCore.pyqtSlot(str)
    def _apply(self, list_type):
        """
        Create the HTML list and set the type of the list.
        """
        self.editor.web.eval("""
            document.execCommand('insertUnorderedList');
            var ulElem = window.getSelection().focusNode.parentNode;
            if (ulElem !== null) {
                var setAttrs = true;
                while (ulElem.toString() !== "[object HTMLUListElement]") {
                    ulElem = ulElem.parentNode;
                    if (ulElem === null) {
                        setAttrs = false;
                        break;
                    }
                }
                if (setAttrs) {
                    ulElem.style.listStyleType = "%s";
                }
            }
        """ % list_type)


