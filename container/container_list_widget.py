from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSlot, Qt

from qt_signal import DockerSignals


class DockerContainerListWidget(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(list, name=DockerSignals.DOCKER_REFRESH_CONTAINERS_SIGNAL)
    def refresh_containers(self, containers=None):
        self.clear()
        for container in containers:
            item = DockerContainerListWidgetItem()
            item.setText('%s - %s' % (container.name, container.status))
            item.setData(Qt.UserRole, container)
            self.addItem(item)


class DockerContainerListWidgetItem(QListWidgetItem):

    def __init__(self, parent=None):
        super().__init__(parent)
