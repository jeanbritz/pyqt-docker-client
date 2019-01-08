from PyQt5.QtWidgets import QStatusBar, QLabel
from PyQt5.QtCore import pyqtSlot

from qt_signal import DockerSignals


class DefaultStatusBar(QStatusBar):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.text: QLabel = None

        self.init_ui()

    def init_ui(self):
        self.text = QLabel("Status")
        self.addPermanentWidget(self.text, 0)

    @pyqtSlot(name=DockerSignals.DOCKER_CONNECT_SIGNAL)
    def on_stats_update(self):
        self.text.setText("Connected")
