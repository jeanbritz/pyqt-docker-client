from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSlot, Qt

from util import DebugConsole



class NetworkListWidget(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(list, name='docker_refresh_network_signal')
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

