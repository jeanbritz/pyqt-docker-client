from PyQt5.QtWidgets import QDockWidget, QTextEdit, QTabWidget
from PyQt5.QtGui import QTextCursor

from docker.types.daemon import CancellableStream

class WorkAreaDockWidget(QDockWidget):

    def __init__(self, args):
        super().__init__(args)

        self._main_widget: QTabWidget = None
        self._log_view: QTextEdit = None
        self._init_ui()

    def _init_ui(self):
        self._main_widget = QTabWidget()
        self._log_view = QTextEdit(self)
        self.setWidget(self._main_widget)
        self._main_widget.addTab(self._log_view, "Log")

    def println(self, msg=None):
        if msg is not None:
            self._log_view.insertPlainText('$s \n' % msg)
            self._log_view.moveCursor(QTextCursor.End)

    def stream(self, stream: CancellableStream):
        for log in stream:
            self.println(str(log, 'utf-8'))

    def set_data(self):
        pass
