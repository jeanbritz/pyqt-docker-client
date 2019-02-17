from PyQt5.Qt import QIcon, Qt, QEvent, QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QDockWidget, QMessageBox

from environment.view import EnvConnectDialog, EnvConfigureDialog
from image import ImageDockWidget
from image.view import DockerImageDialog, ImagePullDialog
from network.view import NetworkDockWidget
from db import DbManager, DaoRegistry,DaoEnvironment
from core.toolbar import DefaultToolbar
from default_status_bar import DefaultStatusBar
from i18n import Strings
from container import ContainerConsoleDockWidget, ContainerDockWidget
from core.docker_manager import DockerManager
from core.auth import RepositoryLoginDialog
from qt_signal import GeneralSignals
from util import DebugConsole, LoadingDialog


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.top: int = 400
        self.left: int = 400
        self.width: int = 600
        self.height: int = 500

        self._debug_console: DebugConsole = None
        self._loading_dialog: LoadingDialog = None

        self.environment_menu: QMenuBar = None
        self.image_menu: QMenuBar = None
        self.repository_menu: QMenuBar = None
        self.help_menu: QMenuBar = None

        self.toolbar: DefaultToolbar = None
        self.status_bar: DefaultStatusBar = None

        self.image_dock_widget: ImageDockWidget = None
        self.image_detail_view: DockerImageDialog = None

        self.container_dock_widget: ContainerDockWidget = None
        self.container_console_widget: ContainerConsoleDockWidget = None

        self.network_dock_widget: NetworkDockWidget = None

        self.docker_manager: DockerManager = DockerManager()

        self.db: DbManager = None
        self.dao_env: DaoEnvironment = None
        self.dao_registry: DaoRegistry = None

        self.general_signals = GeneralSignals()
        self.docker_manager: DockerManager = DockerManager(general_signals=self.general_signals)

        self.env_configure_dialog: EnvConfigureDialog = None
        self.env_connect_dialog: EnvConnectDialog = None
        self.image_pull_dialog: ImagePullDialog = None
        self.login_dialog: RepositoryLoginDialog = None

        self.init_db()
        self.init_ui()

    def init_ui(self):
        self._debug_console = DebugConsole()

        self._loading_dialog = LoadingDialog(self)
        self.general_signals.show_loading_signal.connect(self.show_loading_dialog)

        self.setWindowTitle(Strings.APP_NAME)
        self.setWindowIcon(QIcon('assets/docker.svg'))
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.environment_menu = self.menuBar().addMenu(Strings.ENVIRONMENT_MENU)
        self.environment_menu.addAction(QAction(Strings.CONNECT_ACTION, self, triggered=self.open_env_connect_dialog))
        self.environment_menu.addAction(QAction(Strings.CONFIGURE_ACTION, self, triggered=self.open_env_config_dialog))

        self.image_menu = self.menuBar().addMenu(Strings.IMAGE_MENU)
        self.image_menu.addAction(QAction(Strings.PULL_ACTION, self, triggered=self.open_pull_image_dialog))

        self.repository_menu = self.menuBar().addMenu(Strings.REPOSITORY_MENU)
        self.repository_menu.addAction(QAction(Strings.LOGIN_ACTION, self, triggered=self.open_login_dialog))
        self.repository_menu.addAction(QAction(Strings.CONFIGURE_ACTION, self))

        self.help_menu = self.menuBar().addMenu("Help")
        self.help_menu.addAction(QAction("About &Qt", self,
                                         statusTip="Show the Qt library's About box",
                                         triggered=QApplication.instance().aboutQt))
        self.help_menu.addAction(QAction("About Application", self, triggered=self.about))

        self.init_toolbar()
        self.init_status_bar()

        self.add_docker_images_view()
        self.add_container_console_view()
        self.add_docker_container_view()

        self.add_docker_network_view()

        self.add_debug_console(debug=self._debug_console)

        self.container_dock_widget.list_widget().clicked.connect(self.on_container_clicked)

    def init_db(self):
        self.db = DbManager()
        self.dao_env = DaoEnvironment(conn=self.db.get_connection())
        self.dao_registry = DaoRegistry(conn=self.db.get_connection())

    def init_toolbar(self):
        self.toolbar = DefaultToolbar(self)
        self.toolbar.signals().clicked_signal.connect(self.docker_manager.on_toolbar_action)
        self.toolbar.signals().refresh_signal.connect(self.docker_manager.on_refresh_action)
        self.docker_manager.signals().status_change_signal.connect(self.toolbar.on_docker_manager_status_change)
        self.addToolBar(self.toolbar)

    def init_status_bar(self):
        self.status_bar = DefaultStatusBar(self)
        self.docker_manager.signals().status_change_signal.connect(self.status_bar.on_stats_update)
        self.setStatusBar(self.status_bar)

    def on_image_clicked(self, item = None):
        self.image_detail_view.set_data(item.data(Qt.UserRole).attrs)
        self.image_detail_view.show()

    def add_docker_images_view(self):
        self.image_dock_widget = ImageDockWidget(Strings.IMAGES, signals=self.general_signals)
        self.docker_manager.signals().refresh_images_signal.connect(self.image_dock_widget.list_widget().refresh_images)
        self.addDockWidget(Qt.RightDockWidgetArea, self.image_dock_widget)

        self.image_detail_view = DockerImageDialog()

    def add_docker_container_view(self):
        self.container_dock_widget = ContainerDockWidget(Strings.CONTAINERS, signals=self.general_signals, dialog=self.container_console_widget)
        self.docker_manager.signals().refresh_containers_signal.connect(self.container_dock_widget.list_widget()
                                                                        .refresh_containers)
        self.container_dock_widget.signals().dock_widget_selected_signal.connect(self.toolbar.on_dock_widget_focus)
        self.addDockWidget(Qt.RightDockWidgetArea, self.container_dock_widget)

    def add_docker_network_view(self):
        self.network_dock_widget = NetworkDockWidget(Strings.NETWORKS, signals=self.general_signals)
        self.docker_manager.signals().refresh_networks_signal.connect(self.network_dock_widget.list_widget()
                                                                      .refresh_networks)
        self.network_dock_widget.signals().dock_widget_selected_signal.connect(self.toolbar.on_dock_widget_focus)
        self.addDockWidget(Qt.RightDockWidgetArea, self.network_dock_widget)

    def add_container_console_view(self):
        self.container_console_widget = ContainerConsoleDockWidget("Work Area")
        self.setCentralWidget(self.container_console_widget)

    def add_debug_console(self, debug=None):
        dock = QDockWidget("Debug Console", self)
        dock.setWidget(debug)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)

    @pyqtSlot(bool, str, name=GeneralSignals.GENERAL_SHOW_LOADING_SIGNAL)
    def show_loading_dialog(self, show: bool = False, text: str = None):
        if show:
            self._loading_dialog.set_text(text)
            self._loading_dialog.open()
        else:
            self._loading_dialog.set_text(None)
            self._loading_dialog.close()

    def about(self):
        QMessageBox.about(self, Strings.ABOUT, "Learning Docker...")

    def open_pull_image_dialog(self):
        self.image_pull_dialog = ImagePullDialog(parent=self, docker_manager=self.docker_manager, db_connection=self.db)
        self.image_pull_dialog.open()

    def open_login_dialog(self):
        self.login_dialog = RepositoryLoginDialog(parent=self, docker_manager=self.docker_manager)
        self.login_dialog.open()

    def open_env_connect_dialog(self):
        self.env_connect_dialog = EnvConnectDialog(parent=self, dao=self.dao_env,
                                                   docker_manager=self.docker_manager)
        self.env_connect_dialog.open()

    def open_env_config_dialog(self):
        self.env_configure_dialog = EnvConfigureDialog(parent=self, dao=self.dao_env)
        self.env_configure_dialog.open()

    def closeEvent(self, *args, **kwargs):
        """
        This function is called when this window is about to be closed
        :param args:
        :param kwargs:
        :return:
        """
        self.docker_manager.close()

    def on_container_clicked(self, container):
        pass
