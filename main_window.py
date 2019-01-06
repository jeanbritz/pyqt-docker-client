import sys
import traceback
from collections import namedtuple

from PyQt5.Qt import QIcon, Qt, QEvent, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QDockWidget, QMessageBox

from environment.view import EnvConnectDialog
from image.view import DockerImageListWidget, DockerImageListWidgetItem, DockerImageDialog
from debug_console_widget import DebugConsoleWidget
from db import DatabaseConnection
from toolbar import DefaultToolbar
from default_status_bar import DefaultStatusBar
from i18n import Strings
from util import Log
from container import DockerContainerListWidget, ContainerConsoleDockWidget, ContainerDockWidget
from core import DockerManager
from signal import GeneralSignals


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.top: int = 400
        self.left: int = 400
        self.width: int = 600
        self.height: int = 500

        self.debug: DebugConsoleWidget = None
        self.file_menu: QMenuBar = None
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

        self.daemon_connect_dialog: EnvConnectDialog = None

        self.init_db()
        self.init_ui()

        self.installEventFilter(self)

    def on_connect(self):
        self.debug.println('Connected!')

    def init_ui(self):
        self.debug = DebugConsoleWidget()
        self.setWindowTitle(Strings.APP_NAME)
        self.setWindowIcon(QIcon('assets/docker.svg'))
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.file_menu = self.menuBar().addMenu(Strings.FILE_MENU)
        # self.file_menu.addAction(QAction(Strings.ADD_ACTION, self))
        self.file_menu.addAction(QAction(Strings.CONNECT_ACTION, self, triggered=self.open_dialog))
        self.file_menu.addAction(QAction(Strings.EXIT_ACTION, self, triggered=self.close))

        self.help_menu = self.menuBar().addMenu("Help")
        self.help_menu.addAction(QAction("About &Qt", self,
                                         statusTip="Show the Qt library's About box",
                                         triggered=QApplication.instance().aboutQt))
        self.help_menu.addAction(QAction("About Application", self, triggered=self.about))

        self.add_docker_images_view()
        self.add_docker_container_view()
        self.add_container_console_view()

        self.add_debug_console(debug=self.debug)

        self.init_toolbar()
        self.init_status_bar()

    def init_db(self):
        self.db = DatabaseConnection()
        self.db.create_tables(drop_first=True)

    def init_toolbar(self):
        self.toolbar = DefaultToolbar(self)
        self.general_signals.daemon_selected_signal.connect(self.toolbar.on_daemon_selected)
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
        self.container_dock_widget = ContainerDockWidget(Strings.CONTAINERS)
        self.docker_manager.signals().refresh_containers_signal.connect(self.container_dock_widget.list_widget()
                                                                        .refresh_containers)
        self.addDockWidget(Qt.RightDockWidgetArea, self.container_dock_widget)

    def add_container_console_view(self):
        self.container_console_widget = ContainerConsoleDockWidget("Work Area")
        self.setCentralWidget(self.container_console_widget)

    def add_debug_console(self, debug=None):
        dock = QDockWidget("Debug Console", self)
        dock.setWidget(debug)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)

    def about(self):
        QMessageBox.about(Strings.ABOUT, "Testing Qt's Capabilities")

    def open_dialog(self):
        self.daemon_connect_dialog = EnvConnectDialog(parent=self, db_connection=self.db,
                                                      docker_manager=self.docker_manager)
        self.daemon_connect_dialog.open()

    def close(self):
        super().close(self)
        self.docker_manager.disconnect()

    def closeEvent(self, *args, **kwargs):
        """
        This function is called when this window is about to be closed
        :param args:
        :param kwargs:
        :return:
        """
        self.docker_manager.disconnect()

        def eventFilter(self, object: QObject = None, event: QEvent = None):
            super().eventFilter(object, event)
            print('Event %s, Object %s' % (event, object))
            return False



fake_tb = namedtuple('fake_tb', ('tb_frame', 'tb_lasti', 'tb_lineno', 'tb_next'))


def excepthook(exec_type, exec_value, exec_tb):
    enriched_tb = _add_missing_frames(exec_tb)
    # Note: sys.__excepthook__(...) would not work here.
    # We need to use print_exception(...):
    traceback.print_exception(exec_type, exec_value, enriched_tb)


def _add_missing_frames(tb: fake_tb = None):
    result = fake_tb(tb.tb_frame, tb.tb_lasti, tb.tb_lineno, tb.tb_next)
    frame = tb.tb_frame.f_back
    while frame:
        result = fake_tb(frame, tb.tb_lasti, tb.tb_lineno, tb.tb_next)
        frame = tb.tb_frame.f_back
    return result


if __name__ == "__main__":
    Log.__init__(None)
    Log.i('Starting GUI')
    app = QApplication(sys.argv)
    Log.i('Process ID %s' % app.applicationPid())

    app.setStyle('Fusion')
    app.focusWidget()
    window = MainWindow()
    app.setActiveWindow(window)
    window.show()

   # sys.excepthook = excepthook
    sys.exit(app.exec_())


