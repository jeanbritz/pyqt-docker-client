from PyQt5.QtWidgets import QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem
from PyQt5.Qt import Qt

class DockerImageDialog(QDialog):

    def __init__(self):
        super().__init__(parent=None, flags=(Qt.Window | Qt.WindowStaysOnTopHint))

        self.table_widget : DetailTableView = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Docker Image")
        self.setWindowModality(Qt.ApplicationModal)
        self.setGeometry(0,0,300,200)

        self.table_widget = DetailTableView()
        self.table_widget.setColumnCount(2)
        self.table_widget.setC

        layout = QVBoxLayout(self)
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

    def setData(self, data : dict = None):
        self.table_widget.clear()
        if data is not None:
            row: int = 0
            for key in data:
                self.table_widget.setItem(row, 0, DetailTableWidgetItem(key))
                self.table_widget.setItem(row, 1, DetailTableWidgetItem(str(data[key])))
                row += 1


class DetailTableView(QTableWidget):

    pass

class DetailTableWidgetItem(QTableWidgetItem):
    pass