from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSlot, Qt

from core.network_client_model import NetworkClientModel
from util import DebugConsole
from core import DockerEntity


class DockerNetworkListWidget(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(DockerEntity, list, name='docker_refresh_signal')
    def refresh_networks(self, entity=None, networks=None):
        if entity is DockerEntity.NETWORK:
            self.clear()
            for network in networks:
                model = NetworkClientModel(network)
                item = DockerNetworkListWidgetItem(parent=self, details=model)
                self.addItem(item)
            DebugConsole.println("Networks refreshed")


class DockerNetworkListWidgetItem(QListWidgetItem):

    def __init__(self, parent=None, details=None):
        super().__init__(parent)
        if details:
            self.setText(str(details))
            self.setData(Qt.UserRole, details)
