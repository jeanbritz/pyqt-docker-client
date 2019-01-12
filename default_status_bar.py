from PyQt5.QtWidgets import QStatusBar, QLabel
from PyQt5.QtCore import pyqtSlot

from core.docker_manager import DockerManager
from qt_signal import DockerSignals


class DefaultStatusBar(QStatusBar):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.text: QLabel = None

        self._init_ui()

    def _init_ui(self):
        self.text = QLabel("Status")
        self.addPermanentWidget(self.text, 0)

    @pyqtSlot(int, name=DockerSignals.DOCKER_STATUS_CHANGE_SIGNAL)
    def on_stats_update(self, state):
        if state == DockerManager.CONNECTED:
            self.text.setText("Connected")
        if state == DockerManager.DISCONNECTED:
            self.text.setText("Disconnected")
