from PyQt5.QtWidgets import QStatusBar, QLabel
from PyQt5.QtCore import pyqtSlot, QVariant

from core.docker_service import ManagerStatus


class DockerStatusBar(QStatusBar):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.text: QLabel = None

        self._init_ui()

    def _init_ui(self):
        self.text = QLabel("")
        self.addPermanentWidget(self.text, 0)

    @pyqtSlot(ManagerStatus)
    def on_change(self, status):
        self.text.setText(status.value)
