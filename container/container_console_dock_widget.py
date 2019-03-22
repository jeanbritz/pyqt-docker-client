from PyQt5.QtWidgets import QDockWidget, QTextEdit
from PyQt5.QtGui import QTextCursor

from docker.types.daemon import CancellableStream
from util import Log

class ContainerConsoleDockWidget(QDockWidget):

    def __init__(self, *__args):
        super().__init__(*__args)

        self._main_widget: QTextEdit = None

        self._init_ui()

    def _init_ui(self):
        self._main_widget = QTextEdit(self)
        self.setWidget(self._main_widget)

    def println(self, msg=None):
        if msg is not None:
            self._main_widget.insertPlainText('$s \n' % msg)
            self._main_widget.moveCursor(QTextCursor.End)

    def stream(self, stream: CancellableStream):
        for log in stream:
            print(str(log, 'utf-8'))
            #DebugConsole.println(str(log, 'utf-8'))
            #self._main_widget.insertPlainText(str(log, 'utf-8'))

    def set_data(self):
        pass
