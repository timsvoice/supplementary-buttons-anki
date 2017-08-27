from PyQt4 import QtGui, QtCore


class List(QtGui.QDialog):
    def __init__(self, editor, fixed_type):
        super(List, self).__init__(editor.web)
        self.editor = editor
        self.setProperty("fixed_type", fixed_type)
        self.setProperty("is_inside_list", False)
        self.editor.web.page().mainFrame().addToJavaScriptWindowObject("listObj", self)
        self._is_inside_list()

    @QtCore.pyqtSlot()
    def show_dialog(self):
        pass

    def _is_inside_list(self):
        """
        Indicates whether the user's cursor is currently inside a list.
        """
        self.editor.web.eval("""
            var node = window.getSelection().focusNode;
            while (node = node.parentNode) {
                if (["OL", "UL", "LI"].indexOf(node.tagName) > -1) {
                    listObj.is_inside_list = true;
                    break;
                }
            }
        """)

    def _start(self, command):
        """
        Begin the process of creating the list. If the cursor is currectly
        inside a list, the list will be removed. If not, create a new list determined
        by `command`.
        """
        self.editor.web.eval("""
            if (listObj.is_inside_list) {
                document.execCommand('%s');
            } else {
                if (listObj.fixed_type) {
                    listObj._apply(fixed_type=listObj.fixed_type);
                } else {
                    listObj.show_dialog();
                }
            }
        """ % command)
