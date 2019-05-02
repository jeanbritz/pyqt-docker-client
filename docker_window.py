from PyQt5.Qt import QIcon, Qt, QThread, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QMenuBar, QAction, QDockWidget, QMessageBox, QMainWindow
from docker.errors import APIError

from core import ClientModel, ContainerClientModel
from core.docker_enum import ContainerStatus, Operation
from environment.view import EnvConnectDialog, EnvConfigureDialog
from image.view.image_dock_widget import ImageDockWidget
from image.view import DockerImageDialog, ImagePullDialog
from network.view import NetworkDockWidget
from db import DbManager, DaoRegistry, DaoEnvironment
from core.toolbar import DockerToolbar
from docker_status_bar import DockerStatusBar
from i18n import Strings
from container import WorkAreaDockWidget, ContainerDockWidget
from core.docker_service import DockerService
from core.auth import RepositoryLoginDialog
from qt_signal import GeneralSignals, ToolbarSignals
from qt_signal.docker_signal import DockerSignals
from util import DebugConsole, LoadingDialog
from environment.model import DEnvEnvironment
from util.operation_thread import DockerOperationThread


class DockerWindow(QMainWindow):

    def __init__(self, parent=None, db: DbManager = None, env: DEnvEnvironment = None):
        super(DockerWindow, self).__init__(parent)
        QThread.currentThread().setObjectName('Docker Window')

        self._db = db
        self._env = env

        # Toolbar
        self._toolbar: DockerToolbar = None

        # Status
        self._status_bar: DockerStatusBar = None

        self._debug_console: DebugConsole = None
        self._loading_dialog: LoadingDialog = None

        self.image_detail_view: DockerImageDialog = None

        self.container_console_widget: WorkAreaDockWidget = None

        self._docker_service: DockerService = DockerService()

        # DAO
        self._dao_env: DaoEnvironment = None
        self._dao_registry: DaoRegistry = None

        self.general_signals = GeneralSignals()
        self.docker_signals = DockerSignals()

        self.threads = []
        self._dock_widgets = {}

        self.env_configure_dialog: EnvConfigureDialog = None
        self.env_connect_dialog: EnvConnectDialog = None
        self.image_pull_dialog: ImagePullDialog = None
        self.login_dialog: RepositoryLoginDialog = None

        self._init_dao()
        self._init_ui()
        self.start_docker_service(env=self._env)

    def _init_dao(self):
        self._dao_env = DaoEnvironment(conn=self._db.get_connection())
        self._dao_registry = DaoRegistry(conn=self._db.get_connection())

    def _init_toolbar(self):
        self._toolbar = DockerToolbar(self)
        self._docker_service.signals().status_change_signal.connect(self._toolbar.on_status_change)
        self._toolbar.signals().refresh_signal.connect(self._docker_service.refresh_all)
        self._toolbar.signals().clicked_signal.connect(self.on_toolbar_action)
        self.addToolBar(self._toolbar)

    def _init_status_bar(self):
        self._status_bar = DockerStatusBar(self)
        self._docker_service.signals().status_change_signal.connect(self._status_bar.on_change)
        self.setStatusBar(self._status_bar)

    def _init_ui(self):
        self._debug_console = DebugConsole()
        self._init_toolbar()
        self._init_status_bar()
        self._loading_dialog = LoadingDialog(self)
        self.general_signals.show_loading_signal.connect(self.show_loading_dialog)



        self.environment_menu = self.menuBar().addMenu(Strings.ENVIRONMENT_MENU)
        # self.environment_menu.addAction(QAction(Strings.CONNECT_ACTION, self, triggered=self.open_env_connect_dialog))
        # self.environment_menu.addAction(QAction(Strings.CONFIGURE_ACTION, self, triggered=self.open_env_config_dialog))

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

        self._add_dock_widgets()
        self.add_debug_console(debug=self._debug_console)





    def on_image_clicked(self, item = None):
        self.image_detail_view.set_data(item.data(Qt.UserRole).attrs)
        self.image_detail_view.show()

    def _add_dock_widgets(self):
        dock_widget = ImageDockWidget(Strings.IMAGES, signals=self.general_signals)
        self._docker_service.signals().refresh_signal.connect(dock_widget.list_widget().refresh_images)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget)
        self._dock_widgets[Strings.IMAGES] = dock_widget

        dock_widget = ContainerDockWidget(Strings.CONTAINERS, signals=self.general_signals)
        self._docker_service.signals().refresh_signal.connect(dock_widget.list_widget().refresh_containers)
        dock_widget.signals().dock_widget_selected_signal.connect(self._toolbar.on_dock_widget_focus)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget)
        self._dock_widgets[Strings.CONTAINERS] = dock_widget

        dock_widget = NetworkDockWidget(Strings.NETWORKS, signals=self.general_signals)
        self._docker_service.signals().refresh_signal.connect(dock_widget.list_widget().refresh_networks)
        dock_widget.signals().dock_widget_selected_signal.connect(self._toolbar.on_dock_widget_focus)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget)
        self._dock_widgets[Strings.NETWORKS] = dock_widget

        self.general_signals.dock_widget_selected_signal.connect(self.on_dock_widget_focus)

    def set_container_work_area_view(self, client=None, model=None):
        self.container_console_widget = WorkAreaDockWidget("Work Area", client=client, model=model)

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
        self.image_pull_dialog = ImagePullDialog(parent=self, docker_manager=self._docker_service, db_connection=self.db)
        self.image_pull_dialog.open()

    def open_login_dialog(self):
        self.login_dialog = RepositoryLoginDialog(parent=self, docker_manager=self._docker_service)
        self.login_dialog.open()

    def open_env_config_dialog(self):
        self.env_configure_dialog = EnvConfigureDialog(parent=self, dao=self._dao_env)
        self.env_configure_dialog.open()

    @pyqtSlot(QDockWidget, ClientModel, name=GeneralSignals.GENERAL_DOCK_WIDGET_SELECTED_SIGNAL)
    def on_dock_widget_focus(self, widget: QDockWidget, model: ClientModel):
        if isinstance(model, ContainerClientModel):
            self.set_container_work_area_view(client=self._docker_service.client(), model=model)

    @pyqtSlot(DEnvEnvironment, name=DockerSignals.DOCKER_START_SERVICE_SIGNAL)
    def start_docker_service(self, env=None):
        self._docker_service.init_env(env=env)
        thread = QThread()
        thread.setObjectName("Docker Service for %s" % env.name)
        self._docker_service.moveToThread(thread)
        thread.started.connect(self._docker_service.run)
        thread.start()
        self.threads.append(thread)

    @pyqtSlot(QAction, ClientModel, name=ToolbarSignals.TOOLBAR_CLICKED_SIGNAL)
    def on_toolbar_action(self, action: QAction, model: ClientModel = None):
        thread = DockerOperationThread(client=self._docker_service.client(), model=model)
        try:
            if isinstance(model, ContainerClientModel):
                if action.text() == Strings.PLAY_ACTION and model.state == ContainerStatus.EXITED:
                    thread.set_operation(Operation.START_CONTAINER)
                if action.text() == Strings.STOP_ACTION and model.state == ContainerStatus.RUNNING:
                    thread.set_operation(Operation.STOP_CONTAINER)
            thread.start()
        except APIError as e:
            print("DockerManager :: API Error :: %s" % e)

    def close(self):
        super().close()
        self._docker_service.abort()

