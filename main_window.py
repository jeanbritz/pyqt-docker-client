from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QMenuBar, QTabWidget, QWidget, QAction, QLabel, QPushButton, QApplication

from db import DbManager, DaoEnvironment
from environment.model import DEnvEnvironment
from environment.view import EnvConnectDialog
from i18n import Strings
from qt_signal import GeneralSignals
from docker_window import DockerWindow
from util import Log


class MainWindow(QTabWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.top: int = 400
        self.left: int = 400
        self.width: int = 600
        self.height: int = 500

        self._tabs = []

        # Db Stuff
        self._db: DbManager = None
        self._dao_env: DaoEnvironment = None

        # Menu Bars
        self._environment_menu: QMenuBar = None
        self._image_menu: QMenuBar = None
        self._repository_menu: QMenuBar = None
        self._help_menu: QMenuBar = None

        self._init_db()
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle(Strings.APP_NAME)
        self.setWindowIcon(QIcon('assets/docker.svg'))
        menu_button = QPushButton(QIcon('assets/menu.svg'), "")
        menu_button.clicked.connect(self.open_env_connect_dialog)
        self.setCornerWidget(menu_button, Qt.TopLeftCorner)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.addTab(QWidget(), "Home")

    def _init_db(self):
        self._db = DbManager()
        self._dao_env = DaoEnvironment(conn=self._db.get_connection())

    def open_env_connect_dialog(self):
        env_connect_dialog = EnvConnectDialog(parent=self, dao=self._dao_env)
        env_connect_dialog.signals().accept_connect_signal.connect(self.connect_success)
        env_connect_dialog.open()

    @pyqtSlot(DEnvEnvironment, name=GeneralSignals.GENERAL_ACCEPT_CONNECT_SIGNAL)
    def connect_success(self, env: DEnvEnvironment = None):
        tab_window = DockerWindow(self, db=self._db, env=env)
        self._tabs.append(tab_window)
        index = self.addTab(tab_window, env.name)
        self.setTabEnabled(index + 1, True)

    def close_tab(self, index):
        tab = self.widget(index)
        if tab is not None:
            tab.deleteLater()
            tab.close()
        self.removeTab(index)
        self._tabs.remove(tab)

    def closeEvent(self, *args, **kwargs):
        """
        This function is called when this window is about to be closed
        :param args:
        :param kwargs:
        :return:
        """
        for tab in self._tabs:
            tab.closeEvent()

        self._tabs.clear()
