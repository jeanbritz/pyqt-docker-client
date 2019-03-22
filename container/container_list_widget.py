from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSlot, Qt

from core import ContainerClientModel
from util import DebugConsole


class DockerContainerListWidget(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(list, name='docker_refresh_containers_signal')
    def refresh_containers(self, containers=None):
        self.clear()

        for container in containers:
            item = DockerContainerListWidgetItem(parent=self, details=container)
            self.addItem(item)
        DebugConsole.println("Containers refreshed")


class DockerContainerListWidgetItem(QListWidgetItem):

    def __init__(self, parent=None, details=None):
        super().__init__(parent)
        if details is not None:
            model = ContainerClientModel(details)
            self.setText(str(model))
            self.setData(Qt.UserRole, model)

