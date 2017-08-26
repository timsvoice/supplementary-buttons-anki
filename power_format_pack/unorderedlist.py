from PyQt4 import QtGui, QtCore

from power_format_pack import const
from power_format_pack.qt.views.unordered_list_types import Ui_unordered_list_dialog


class UnorderedList(QtGui.QDialog):
    """
    Create an unordered list.
    """

    def __init__(self, editor, fixed_type=""):
        super(UnorderedList, self).__init__(editor.web)
        self.editor = editor
        self.setProperty("fixed_type", fixed_type)
        self.ui = None
        self.editor.web.page().mainFrame().addToJavaScriptWindowObject("unorderedList", self)
        self._start()

    @QtCore.pyqtSlot()
    def show_types_window(self):
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

    def _start(self):
        """
        Begin the process of creating the unordered list. If the cursor is currectly
        inside a list, the list will be removed. If not, create a new list.
        """
        self.editor.web.eval("""
            var orgNode = window.getSelection().focusNode;
            node = orgNode;
            var insideList = false;
            while (node = node.parentNode) {
                if (["OL", "UL", "LI"].indexOf(node.tagName) > -1) {
                    insideList = true;
                    document.execCommand('insertUnorderedList');
                    break;
                }
            }
            if (!insideList) {
                if (unorderedList.fixed_type) {
                    unorderedList._apply(unorderedList.fixed_type);
                } else {
                    unorderedList.show_types_window();
                }
            }
        """)

