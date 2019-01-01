from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from io import StringIO

import time
import datetime


class DebugConsoleWidget(QTextEdit):

    def __init__(self, parent=None):
        super(DebugConsoleWidget, self).__init__(parent)

        self._buffer = StringIO()
        self.setReadOnly(True)
        self.font = QFont('Courier New', 8, QFont.Normal)
        self.setFont(self.font)

    def println(self, msg):
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        self.insertPlainText('[%s] %s \n' % (timestamp, msg))
        # Autoscroll
        self.moveCursor(QTextCursor.End)
        self._buffer.write(msg)
