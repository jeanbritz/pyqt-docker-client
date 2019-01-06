from PyQt5.QtWidgets import QDockWidget, QTextEdit
from PyQt5.QtGui import QTextCursor


class ContainerConsoleDockWidget(QDockWidget):

    def __init__(self, *__args):
        super().__init__(*__args)
        print(self.titleBarWidget())

        self._main_widget: QTextEdit = None

        self._init_ui()

    def _init_ui(self):
        self._main_widget = QTextEdit(self)
        self.setWidget(self._main_widget)

    def println(self, msg=None):
        if msg is not None:
            self._main_widget.insertPlainText('$s \n' % msg)
            self._main_widget.moveCursor(QTextCursor.End)

    def set_data(self):
        pass