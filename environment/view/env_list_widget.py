from PyQt5.Qt import QItemSelectionModel
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListView, QAction

from db.dao_environment import DaoEnvironment
from environment.model.env_list_model import EnvironmentListModel
from qt_signal.docker_signal import DockerSignals


class EnvListWidget(QListView):

    def __init__(self, dao: DaoEnvironment = None, signals: DockerSignals = None):
        super(EnvListWidget, self).__init__()
        self._dao = dao
        self._signals = signals
        self._init_ui()

    def _init_ui(self):
        self.setModel(EnvironmentListModel(parent=self, dao=self._dao))
        self.setSelectionModel(QItemSelectionModel(self.model()))

        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        connect_action = QAction("Connect", self, triggered=self.docker_connect)
        self.addAction(connect_action)

    def signals(self):
        return self._signals

    def docker_connect(self):
        if len(self.selectedIndexes()) > 0:
            current_index = self.selectionModel().currentIndex()
            current_model = self.model().data(current_index, EnvironmentListModel.DATA_ROLE)
            self._signals.start_docker_service.emit(current_model)


