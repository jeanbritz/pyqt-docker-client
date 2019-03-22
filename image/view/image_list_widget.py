from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSlot, Qt

from core import ImageClientModel
from util import DebugConsole



class DockerImageListWidget(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(list, name='docker_refresh_images_signal')
    def refresh_images(self, images=None):
        self.clear()
        for image in images:
            model = ImageClientModel(image)
            item = DockerImageListWidgetItem(parent=self, details=model)
            self.addItem(item)
        DebugConsole.println("Images refreshed")


class DockerImageListWidgetItem(QListWidgetItem):

    def __init__(self, parent=None, details=None):
        super().__init__(parent)
        if details:
            self.setText(str(details))
            self.setData(Qt.UserRole, details)

