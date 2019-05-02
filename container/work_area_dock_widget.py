from io import StringIO

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDockWidget, QTextEdit, QTabWidget
from PyQt5.QtGui import QTextCursor, QFont, QColor
from docker import DockerClient

from core import ClientModel
from util.streaming_thread import StreamingThread


class WorkAreaDockWidget(QDockWidget):

    log_signal = pyqtSignal(bytes, name='log')

    def __init__(self, args, client: DockerClient = None, model: ClientModel = None):
        super().__init__(args)

        self.log_signal.connect(self.on_log_event)

        self._selected_model: ClientModel = model
        self._client: DockerClient = client
        self._main_widget: QTabWidget = None
        self._logger: LogConsole = None
        self._init_ui()

    def _init_ui(self):
        self._main_widget = QTabWidget()
        self._logger = LogConsole(self)
        self.setWidget(self._main_widget)
        self._main_widget.addTab(self._logger, "Log")
        thread = StreamingThread(client=self._client, model=self._selected_model, log_signal=self.log_signal)
        thread.start()

    @pyqtSlot(bytes, name='log')
    def on_log_event(self, line=None):
        self._logger.println(line)


class LogConsole(QTextEdit):

    def __init__(self, parent=None):
        super(LogConsole, self).__init__(parent)
        self._buffer = StringIO()
        self.setReadOnly(True)
        self.font = QFont('Courier New', 8, QFont.Normal)
        self.setFont(self.font)
        # self.setTextColor(QColor.White)
        # self.setTextBackgroundColor(QColor.Black)

    def println(self, msg):
        string = str(msg, 'utf8')
        self.insertPlainText('%s' % string)
        # Autoscroll
        self.moveCursor(QTextCursor.End)
        self._buffer.write(string)

