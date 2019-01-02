from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSlot, Qt

from signal.docker_signal import DockerSignals

class DockerImageListWidget(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(list, name='docker_refresh_images_signal')
    def refresh_images(self, images=None):
        self.clear()
        for image in images:
            item = DockerImageListWidgetItem()
            item.setText(str(image))
            item.setData(Qt.UserRole, image)
            self.addItem(item)


class DockerImageListWidgetItem(QListWidgetItem):

    def __init__(self, parent=None):
        super().__init__(parent)

