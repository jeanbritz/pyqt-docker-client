from PyQt5.QtWidgets import QListWidget, QListWidgetItem


class DockerImageListWidget(QListWidget):

   pass


class DockerImageListWidgetItem(QListWidgetItem):

    def __init__(self, parent=None):
        super().__init__(parent)

