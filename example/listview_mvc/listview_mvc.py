import sys

from PyQt5.Qt import QApplication, Qt, QModelIndex, QAbstractListModel, QVariant
from PyQt5.QtWidgets import QMainWindow, QListView

from example.listview_mvc import DbManager
from example.listview_mvc import Album
from example.listview_mvc import AlbumDao


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.top: int = 400
        self.left: int = 400
        self.width: int = 600
        self.height: int = 500

        self.setWindowTitle("Albums - List View Example")
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.dbm: DbManager = None
        self.dao: AlbumDao = None

        self.list_view: QListView = None
        self.list_model: QAbstractListModel = None

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
        self.list_view.setModel(self.list_model)
        self.setCentralWidget(self.list_view)
#
# PyQt (Qt) list of model types:
# ==============================
# - List model - 1-dimensional array
# - Table model - 2-dimensional array
# - Tree Model - Stores in a hierarchical relationship (parent and child)
#
# What is a QModelIndex?
# ======================
# It is an object used to locate data within a model. This class is also used to locate data in different model types
#
#

class AlbumListModel(QAbstractListModel):

    id_role = Qt.UserRole + 1
    name_role = id_role + 1

    def __init__(self, parent=None, dao=None):
        """
        :param dao - This is the link to the database. In the Model/View schema, the model will communicate with
                     the data layer through DAO
        :param parent:
        """
        super().__init__(parent)
        self._dao = dao
        self._data = dao.albums()

    def add_album(self, album: Album) -> QModelIndex:
        row_index = self.rowCount()
        self.beginInsertRows(QModelIndex(), row_index, row_index)  # Informs that rows are about to change for the
                                                                 # given index
        self._dao.add_album(album)
        self._data.append(album)
        self.endInsertRows()                                     # Informs that the rows have been changed
        return self.index(row_index, 0)

    def rowCount(self, parent: QModelIndex = None, *args, **kwargs) -> int:
        """
        Overridden from QAbstractItemModel
        This function is used to get the list size
        :param parent: Unknown parameter
        :param args:
        :param kwargs:
        :return:
        """
        return len(self._data)

    def data(self, index: QModelIndex, role=None) -> QVariant:
        """
        Overridden from QAbstractItemModel
        This function is used to get a specific piece of info about the data to display
        :param index:
        :param role:
        :return:
        """
        if self._is_index_valid(index):
            return QVariant()

        album = self._data[index.row()]  # Data is 1-dimensional array

        if role == self.id_role:
            return album.id
        elif role in (Qt.DisplayRole, self.name_role):
            return album.name
        else:
            return QVariant()

    def setData(self, index: QModelIndex, value: QVariant, role: int = None) -> bool:
        """
        Overridden from QAbstractItemModel
        This function is used to update data
        :param index:
        :param value:
        :param role:
        :return:
        """

        if not self._is_index_valid(index) or role is not self.name_role:
            return False

        album = self._data[index.row()]
        album._name = value.value()

        if self._dao.update_album(album) is True:
            self.dataChanged.emit(index, index)
            return True  # Indicates that update with database was successful
        return False

    def removeRows(self, row: int, count: int, parent: QModelIndex = None, *args, **kwargs) -> bool:
        """
        Overridden from QAbstractItemModel
        This function is used to remove data
        :param row:
        :param count:
        :param parent:
        :param args:
        :param kwargs:
        :return:
        """

        if row < 0 or row >= self.rowCount() or count < 0 or (row + count) > self.rowCount():
            return False

        self.beginRemoveRows(parent, row, row + count - 1)
        count_left = count
        while count_left > 0:
            album = self._data[row + count_left]
            self._dao.delete_album(album)
            count_left = count_left - 1

        self.endRemoveRows()
        return True

    def roleNames(self) -> dict:
        """
        Overridden from QAbstractItemModel
        This function is used to indicate to the framework the name for each 'role'.
        :return: dict - key is the role id and the value is the pretty name
        """
        return {self.id_role: 'id', self.name_role: 'name'}

    def _is_index_valid(self, index: QModelIndex) -> bool:
        """

        :param index:
        :return:
        """
        if index.row() < 0 or index.row() >= self.rowCount() or not index.isValid():
            return False
        return True


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    app.setActiveWindow(window)
    window.show()
    sys.exit(app.exec_())
