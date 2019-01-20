import sys

from PyQt5.Qt import QApplication, Qt, QModelIndex, QAbstractListModel, QVariant


class MainWindow:
    pass

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
#
#
#
#
#

class Album:

    def __init__(self, album_id=None, name=None) -> None:
        self._id = album_id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name


class AlbumModel(QAbstractListModel):

    id_role = Qt.UserRole + 1
    name_role = id_role + 1

    def __init__(self, parent=None):
        """
        :param dbm - This is the link to the database. In the Model/View schema, the model will communicate with
                     the data layer through DAO
        :param parent:
        """
        super().__init__(parent)
        self._dbm = None
        self._data = None

    def add_album(self, album) -> QModelIndex:
        pass

    def rowCount(self, parent: QModelIndex=None, *args, **kwargs) -> int:
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
        return super().setData(index, value, role)

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
        super().removeRows(row, count, parent, *args, **kwargs)

    def roleNames(self) -> dict:
        """
        Overridden from QAbstractItemModel
        This function is used to indicate to the framework the name for each 'role'.
        :return: dict - key is the role id and the value is the pretty name
        """
        return {self.id_role: 'id', self.name_role: 'name'}

    def _is_index_valid(self, index: QModelIndex) -> bool:
        pass


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    app.setActiveWindow(window)
    window.show()