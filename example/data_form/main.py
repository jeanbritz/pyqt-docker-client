import sys

from PyQt5.Qt import QApplication, QItemSelectionModel, QModelIndex
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QListView, QHBoxLayout, QVBoxLayout, QPushButton, QDesktopWidget, QInputDialog, \
    QLineEdit, QMainWindow

from example.data_form.data_form import DataForm
from example.listview_mvc import DbManager, AlbumDao, AlbumListModel, Album


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Data Form Example")

        self.init_ui()

    def init_ui(self):
        config = [{'bind': 'name', 'type': 'text', 'label': 'Name', 'enabled': 'false', 'group': 'env'},
                  {'bind': 'password', 'type': 'password', 'label': 'Password', 'group': 'env'},
                  {'bind': 'host', 'type': 'text', 'label': 'Host', 'group': 'env'},
                  {'bind': 'tls', 'type': 'boolean', 'label': 'Use TLS?', 'group': 'tls'}]
        grouping = [{'label': 'Environment', 'name': 'env'},
                    {'label': "TLS", 'name': 'tls'}]

        form = DataForm(config=config, grouping=grouping)
        form.draw()
        self.setCentralWidget(form)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    app.setActiveWindow(window)
    window.show()
    sys.exit(app.exec_())
