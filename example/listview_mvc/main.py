import sys

from PyQt5.Qt import QApplication, QItemSelectionModel, QModelIndex
from PyQt5.QtWidgets import QWidget, QListView, QHBoxLayout, QVBoxLayout, QPushButton, QDesktopWidget, QInputDialog, \
                            QLineEdit


from example.listview_mvc import DbManager, AlbumDao, AlbumListModel, Album


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.top: int = 300
        self.left: int = 300
        self.width: int = 200
        self.height: int = 300

        self.setWindowTitle("Albums - List View Example")
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.dbm: DbManager = None
        self.dao: AlbumDao = None

        self.list_view: QListView = None
        self.list_model: AlbumListModel = None
        self.list_selection_model: QItemSelectionModel = None

        self.init_db()
        self.init_ui()

    def init_db(self):
        """
        Initialises DB connection
        :return:
        """
        self.dbm = DbManager()
        self.dbm.create()
        self.dao = AlbumDao(dbm=self.dbm)
        if not self.dao.init():
            print("Failed to initialise DAO for Albums")
        else:
            print("DAO initialised for Albums")

    def init_ui(self):
        """
        Initialises UI components
        :return:
        """
        self.list_view = QListView()
        self.list_model = AlbumListModel(dao=self.dao)
        self.list_model.dataChanged.connect(self.on_data_changed)
        self.list_selection_model = QItemSelectionModel(self.list_model)
        self.list_view.setModel(self.list_model)
        self.list_view.setSelectionModel(self.list_selection_model)

        btn_add = QPushButton('Add', self)
        btn_add.setToolTip('Add Album')

        btn_edit = QPushButton('Edit', self)
        btn_edit.setToolTip('Edit Album')

        btn_delete = QPushButton('Delete', self)
        btn_delete.setToolTip('Delete Album')

        btn_add.clicked.connect(self.create_album)
        btn_edit.clicked.connect(self.edit_album)
        btn_delete.clicked.connect(self.delete_album)

        list_layout = QHBoxLayout()
        list_layout.addStretch(1)
        list_layout.addWidget(self.list_view)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(btn_add)
        buttons_layout.addWidget(btn_edit)
        buttons_layout.addWidget(btn_delete)

        main_layout = QVBoxLayout()
        main_layout.addLayout(list_layout)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_album(self):
        input_name, ok_clicked = QInputDialog.getText(self, "Create a new Album", "Choose a name", QLineEdit.Normal, "")
        if ok_clicked:
            album = Album(name=input_name)
            created_index = self.list_model.add_album(album)
            self.list_view.setCurrentIndex(created_index)

    def edit_album(self):
        if len(self.list_selection_model.selectedIndexes()) > 0:
            current_index = self.list_selection_model.currentIndex()
            old_name = self.list_model.data(current_index, self.list_model.name_role)
            input_name, ok_clicked = QInputDialog.getText(self, "Album's name", "Change Album name", QLineEdit.Normal,
                                                          old_name)
            if ok_clicked:
                self.list_model.setData(current_index, input_name, self.list_model.name_role)

    def delete_album(self):
        if len(self.list_selection_model.selectedIndexes()) > 0:
            current_index = self.list_selection_model.currentIndex()
            row = current_index.row()
            self.list_model.removeRow(row)

            # Try to select the previous album
            previous_index = self.list_model.index(row - 1, 0)
            if previous_index.isValid():
                self.list_selection_model.setCurrentIndex(previous_index, QItemSelectionModel.SelectCurrent)
            else:
                # Try to select the next album
                next_index = self.list_model.index(row, 0)
                if next_index.isValid():
                    self.list_selection_model.setCurrentIndex(next_index, QItemSelectionModel.SelectCurrent)

    def on_data_changed(self, index_1:QModelIndex, index_2:QModelIndex):
        print('Data has been updated')

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    app.setActiveWindow(window)
    window.show()
    sys.exit(app.exec_())
