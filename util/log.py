import logging
import logging.config
import yaml
import time
import datetime

from io import StringIO

from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QFont, QTextCursor


class Log:

    def __init__(self):
        with open('config/logging.yml', 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)

        global logger
        logger = logging.getLogger()

    @staticmethod
    def i(msg=None):
        """
        Log info message
        :param self:
        :param msg:
        :return:
        """
        logger.info(msg)

    @staticmethod
    def e(msg=None):
        """
        Log error message
        :param self:
        :param msg:
        :return:
        """
        logger.error(msg, exc_info=True)

    @staticmethod
    def w(msg=None):
        """
        Log warning message
        :param self:
        :param msg:
        :return:
        """
        logger.warning(msg)


class DebugConsole(QTextEdit):

    def __init__(self, parent=None):
        super(DebugConsole, self).__init__(parent)
        global buffer
        global this
        this = self
        buffer = StringIO()
        self.setReadOnly(True)
        self.font = QFont('Courier New', 8, QFont.Normal)
        self.setFont(self.font)

    @staticmethod
    def println(msg):
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        this.insertPlainText('[%s] %s \n' % (timestamp, msg))
        # Autoscroll
        this.moveCursor(QTextCursor.End)
        buffer.write(msg)
