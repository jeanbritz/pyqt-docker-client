from PyQt5.QtWidgets import QStatusBar, QLabel
from PyQt5.QtCore import pyqtSlot, QVariant

from core.docker_manager_service import ManagerStatus


class DefaultStatusBar(QStatusBar):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.text: QLabel = None

        self._init_ui()

    def _init_ui(self):
        self.text = QLabel("Status")
        self.addPermanentWidget(self.text, 0)

    @pyqtSlot(ManagerStatus)
    def on_stats_update(self, status):
        self.text.setText(status.value)
