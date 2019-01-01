from PyQt5.QtWidgets import QListWidget,QListWidgetItem


class DockerDaemonListWidget(QListWidget):
    pass


class DockerDaemonListWidgetItem(QListWidgetItem):

    def __init__(self, parent=None, type=QListWidgetItem.Type):
        super().__init__(parent, type)


