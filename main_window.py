from PyQt5.Qt import QIcon, Qt, QEvent, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QDockWidget, QMessageBox

from environment.view import EnvConnectDialog
from image.view import DockerImageListWidget, DockerImageListWidgetItem, DockerImageDialog, ImagePullDialog
from debug_console_widget import DebugConsoleWidget
from db import DatabaseConnection
from core.toolbar import DefaultToolbar
from default_status_bar import DefaultStatusBar
from i18n import Strings
from container import DockerContainerListWidget, ContainerConsoleDockWidget, ContainerDockWidget
from core import DockerManager
from core.auth import DockerLoginDialog
from qt_signal import GeneralSignals


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.top: int = 400
        self.left: int = 400
        self.width: int = 600
        self.height: int = 500

        self.debug: DebugConsoleWidget = None
        self.file_menu: QMenuBar = None
        self.image_menu: QMenuBar = None
        self.help_menu: QMenuBar = None

        self.toolbar: DefaultToolbar = None
        self.status_bar: DefaultStatusBar = None

        self.image_list_widget: DockerImageListWidget = None
        self.image_detail_view: DockerImageDialog = None

        self.container_dock_widget: DockerContainerListWidget = None
        self.container_console_widget: ContainerConsoleDockWidget = None

        self.docker_manager: DockerManager = DockerManager()
        self.db: DatabaseConnection = None

        self.general_signals = GeneralSignals()

        self.env_connect_dialog: EnvConnectDialog = None
        self.image_pull_dialog: ImagePullDialog = None
        self.login_dialog: DockerLoginDialog = None

        self.init_db()
        self.init_ui()



    def on_connect(self):
        self.debug.println('Connected!')

    def init_ui(self):
        self.debug = DebugConsoleWidget()
        self.setWindowTitle(Strings.APP_NAME)
        self.setWindowIcon(QIcon('assets/docker.svg'))
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.file_menu = self.menuBar().addMenu(Strings.FILE_MENU)
        self.file_menu.addAction(QAction(Strings.LOGIN_ACTION, self, triggered=self.open_login_dialog))
        self.file_menu.addAction(QAction(Strings.CONNECT_ACTION, self, triggered=self.open_env_connect_dialog))
        self.file_menu.addAction(QAction(Strings.EXIT_ACTION, self, triggered=self.close))

        self.image_menu = self.menuBar().addMenu(Strings.IMAGE_MENU)
        self.image_menu.addAction(QAction(Strings.PULL_ACTION, self,triggered=self.open_pull_image_dialog))

        self.help_menu = self.menuBar().addMenu("Help")
        self.help_menu.addAction(QAction("About &Qt", self,
                                         statusTip="Show the Qt library's About box",
                                         triggered=QApplication.instance().aboutQt))
        self.help_menu.addAction(QAction("About Application", self, triggered=self.about))

        self.init_toolbar()
        self.init_status_bar()

        self.add_docker_images_view()
        self.add_docker_container_view()
        self.add_container_console_view()

        self.add_debug_console(debug=self.debug)

    def init_db(self):
        self.db = DatabaseConnection()
        self.db.create_tables(drop_first=True)

    def init_toolbar(self):
        self.toolbar = DefaultToolbar(self)
        self.toolbar.signals().clicked_signal.connect(self.docker_manager.on_toolbar_action)
        self.addToolBar(self.toolbar)

    def init_status_bar(self):
        self.status_bar = DefaultStatusBar(self)
        self.docker_manager.signals().connect_signal.connect(self.status_bar.on_stats_update)
        self.setStatusBar(self.status_bar)

    def on_image_clicked(self, item:DockerImageListWidgetItem = None):
        self.image_detail_view.set_data(item.data(Qt.UserRole).attrs)
        self.image_detail_view.show()

    def add_docker_images_view(self):
        self.image_list_widget = DockerImageListWidget()
        self.image_list_widget.itemClicked.connect(self.on_image_clicked)
        self.docker_manager.signals().refresh_images_signal.connect(self.image_list_widget.refresh_images)
        dock = QDockWidget(Strings.IMAGES, self)
        dock.setWidget(self.image_list_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.image_detail_view = DockerImageDialog()

    def add_docker_container_view(self):
        self.container_dock_widget = ContainerDockWidget(Strings.CONTAINERS, signals=self.general_signals)
        self.docker_manager.signals().refresh_containers_signal.connect(self.container_dock_widget.list_widget()
                                                                        .refresh_containers)
        self.container_dock_widget.signals().dock_widget_selected_signal.connect(self.toolbar.on_dock_widget_focus)
        self.addDockWidget(Qt.RightDockWidgetArea, self.container_dock_widget)

    def add_container_console_view(self):
        self.container_console_widget = ContainerConsoleDockWidget("Work Area")
        self.setCentralWidget(self.container_console_widget)

    def add_debug_console(self, debug=None):
        dock = QDockWidget("Debug Console", self)
        dock.setWidget(debug)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)

    def about(self):
        QMessageBox.about(self, Strings.ABOUT, "Learning Docker...")

    def open_pull_image_dialog(self):
        self.image_pull_dialog = ImagePullDialog(parent=self, docker_manager=self.docker_manager)
        self.image_pull_dialog.open()

    def open_login_dialog(self):
        self.login_dialog = DockerLoginDialog(parent=self, docker_manager=self.docker_manager)
        self.login_dialog.open()

    def open_env_connect_dialog(self):
        self.env_connect_dialog = EnvConnectDialog(parent=self, db_connection=self.db,
                                                   docker_manager=self.docker_manager)
        self.env_connect_dialog.open()

    def close(self):
        super().close(self)
        self.docker_manager.close()

    def closeEvent(self, *args, **kwargs):
        """
        This function is called when this window is about to be closed
        :param args:
        :param kwargs:
        :return:
        """
        self.docker_manager.close()

    def eventFilter(self, obj: QObject = None, event: QEvent = None):
        # super().eventFilter(object, event)
        # if event.type() == QEven:
        print('Event %s, Object %s' % (event.type(), obj.thread()))
            # return False
        return False
