from PyQt5.Qt import Qt, QModelIndex, QAbstractListModel, QVariant

from environment.model import DEnvEnvironment


class EnvironmentListModel(QAbstractListModel):

    ID_ROLE = Qt.UserRole + 1
    NAME_ROLE = ID_ROLE + 1
    DATA_ROLE = NAME_ROLE + 1

    def __init__(self, parent=None, dao=None):
        """
        :param dao - This is the link to the database. In the Model/View schema, the model will communicate with
                     the data layer through DAO
        :param parent:
        """
        super().__init__(parent)
        self._dao = dao
        self._data = dao.environments()

    def add_environment(self, env: DEnvEnvironment) -> QModelIndex:
        row_index = self.rowCount()
        self.beginInsertRows(QModelIndex(), row_index, row_index)

        updated_env = self._dao.create_env(env)
        self._data.append(updated_env)
        self.endInsertRows()
        return self.index(row_index, 0)

    def rowCount(self, parent=None, *args, **kwargs) -> int:
        return len(self._data)

    def data(self, index: QModelIndex = None, role=None) -> QVariant:
        if not self._is_index_valid(index=index):
            return QVariant()

        environment = self._data[index.row()] # Data is 1-dimensional array

        if role == self.ID_ROLE:
            return environment.id
        elif role in (Qt.DisplayRole, self.NAME_ROLE):
            return environment.name
        elif role is self.DATA_ROLE:
            return environment
        else:
            return QVariant()

    def setData(self, index: QModelIndex, value: QVariant, role=None):
        if not self._is_index_valid(index) or role is not self.NAME_ROLE:
            return False
        environment = self._data[index.row()]
        environment._name = value

        if self._dao.update_env(environment) is True:
            self.dataChanged.emit(index, index)
            return True
        return False

    def removeRows(self, row: int, count: int, parent: QModelIndex = None, *args, **kwargs) -> bool:
        if row < 0 or row >= self.rowCount() or count < 0 or (row + count) > self.rowCount():
            return False

        self.beginRemoveRows(parent, row, row + count - 1)

        environment = self._data[row]
        if self._dao.delete_env(environment):
            self._data.pop(row)
        self.endRemoveRows()
        return True

    def roleNames(self):
        return {self.ID_ROLE: 'id', self.NAME_ROLE: 'name'}

    def _is_index_valid(self, index: QModelIndex) -> bool:
        if index.row() < 0 or index.row() >= self.rowCount() or not index.isValid():
            return False
        return True
