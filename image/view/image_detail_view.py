from PyQt5.QtWidgets import QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem
from PyQt5.Qt import Qt


class DockerImageDialog(QDialog):

    def __init__(self, parent=None):
        # super().__init__(parent=None, flags=(Qt.Window | Qt.WindowStaysOnTopHint))
        super(DockerImageDialog, self).__init__(parent)

        self.table_widget: DetailTableView = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Docker Image")
        self.setWindowModality(Qt.ApplicationModal)
        self.setGeometry(0, 0, 800, 800)

        self.table_widget = DetailTableView()
        self.table_widget.setColumnCount(2)
        self.table_widget.setColumnWidth(1, 400)
        self.table_widget.setHorizontalHeaderItem(0, QTableWidgetItem("Name"))
        self.table_widget.setHorizontalHeaderItem(1, QTableWidgetItem("Value"))

        layout = QVBoxLayout(self)
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

    def set_data(self, data : dict = None):
        self.table_widget.clear()
        self.table_widget.setRowCount(len(data))
        if data is not None:
            row: int = 0
            for key in data:
                self.table_widget.setItem(row, 0, QTableWidgetItem(key))
                self.table_widget.setItem(row, 1, QTableWidgetItem(str(data[key])))
                row += 1


class DetailTableView(QTableWidget):

    pass

class DetailTableWidgetItem(QTableWidgetItem):
    pass