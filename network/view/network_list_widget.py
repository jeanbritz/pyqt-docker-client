from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSlot, Qt

from util import DebugConsole
from qt_signal import DockerSignals


class NetworkListWidget(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(list, name=DockerSignals.DOCKER_REFRESH_IMAGES_SIGNAL)
    def refresh_networks(self, networks=None):
        self.clear()
        for network in networks:
            item = NetworkListWidgetItem()
            item.setText(network.name)
            item.setData(Qt.UserRole, network)
            self.addItem(item)
        DebugConsole.println("Networks refreshed")


class NetworkListWidgetItem(QListWidgetItem):

    def __init__(self, parent=None):
        super().__init__(parent)

