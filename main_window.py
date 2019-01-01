import sys
import traceback
import docker
from PyQt5.QtCore import Qt,pyqtSlot
from docker.errors import DockerException
from collections import namedtuple

from daemon.view.daemon_list_widget import *

from image.view.image_list_widget import *
from image.view.image_detail_view import DockerImageDialog

from debug_console_widget import *

from db.db_connection import *


from strings import Strings
from util.log import Log
from signal.docker_connect_signal import DockerSignal


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

        self.image_list_widget: DockerImageListWidget = None
        self.image_detail_view: DockerImageDialog = None

        self.db = self.init_db()
        self.initUI()

    def initUI(self):
        self.debug = DebugConsoleWidget()
        self.setWindowTitle(Strings.APP_NAME)
        self.setWindowIcon(QIcon('assets/docker.svg'))
        self.setGeometry(self.top, self.left, self.width, self.height)

        # self.textEdit = QTextEdit()
        # self.setCentralWidget(self.textEdit)
        self.statusBar().showMessage(Strings.READY)
        self.file_menu = self.menuBar().addMenu(Strings.FILE_MENU)
        self.file_menu.addAction(QAction(Strings.ADD_ACTION, self))
        self.file_menu.addAction(QAction(Strings.OPEN_ACTION, self))
        self.file_menu.addAction(QAction(Strings.EXIT_ACTION, self, triggered=self.close))

        self.help_menu = self.menuBar().addMenu("Help")
        self.help_menu.addAction(QAction("About &Qt", self,statusTip="Show the Qt library's About box", triggered=QApplication.instance().aboutQt))
        self.help_menu.addAction(QAction("About Application", self, triggered=self.about))

        self.add_docker_daemons_view()
        self.image_list_widget = DockerImageListWidget()
        self.add_docker_images_view()
        self.add_debug_console(debug=self.debug)

    def init_db(self):
        db = DatabaseConnection()
        db.create_docker_daemon_table(drop_first=True)
        return db

    def dockAble(self):
        dock = QDockWidget("Images", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        # client = self.docker_connect()
        # if client is not None:
        #     print("Connected to " + client.__str__())
        #     print('====== Client Version Info =====')
        #     for key in client.version():
        #         print("{} = {}".format(key, client.version().get(key)))
        #     print('====== Disk Usage =====')
        #     for key in client.df():
        #         print("{} = {}".format(key, client.df().get(key)))
        #     print('====== Client Info =====')
        #     for key in client.info():
        #         print ("{} = {}".format(key, client.info().get(key)))
        #     print('====== Images =====')
        #     for key in client.images.list():
        #         print (key.attrs)
        #         print("Image = {}".format(key))
        #
        #     self.listwidget = QtWidgets.QListWidget(dock)
        #     self.imageList = []
        #     dialog = docker_image_view.DockerImageDialog()
        #     dialog.show()
        #     for image in client.images.list():
        #         self.imageList.append(image.__str__())

        #self.bluetooth_inquiry()
        #self.listwidget.addItems(self.imageList)

        #.setWidget(self.listwidget)
        #self.addDockWidget(Qt.RightDockWidgetArea, dock)

    def docker_connect(self, hostname="localhost", port=2376, version='auto'):
        client = None
        # signal = DockerSignal()
        # signal.connect_signal.connect(self.test)
        # res = signal.connect_signal.emit(2)

        base_url = "tcp://%s:%d" % (hostname, port)
        try:
            client = docker.DockerClient(base_url=base_url, version=version)
            self.debug.println("Connected!")
        except DockerException as e:
            print(e)
            self.debug.println(Strings.DOCKER_CANNOT_CONNECT % (hostname, port, version))
        return client

    def add_docker_daemons_view(self):
        dock = QDockWidget(Strings.DAEMONS, self)
        widget = DockerDaemonListWidget()
        for id, hostname, port in self.db.get_docker_daemons():
            item = DockerDaemonListWidgetItem()
            item.setText(str(id) + " - " + hostname + ':' + str(port))
            item.setData(Qt.UserRole, {'id': id,
                                       'hostname': hostname,
                                       'port': port})
            widget.addItem(item)
        widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        dock.setWidget(widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    def on_item_double_clicked(self, curr=None, prev=None):
        data = curr.data(Qt.UserRole)
        hostname = data['hostname']
        port = data['port']
        self.debug.println(Strings.DOCKER_TRY_CONNECT % (hostname, port))
        client = self.docker_connect(hostname, port)
        if client is not None:
            signal = DockerSignal()
            signal.refresh_images_signal.connect(self.refresh_images)
            signal.refresh_images_signal.emit(client.images.list())

    def on_image_clicked(self, item:DockerImageListWidgetItem = None):
        self.image_detail_view.setData(item.data(Qt.UserRole).attrs)
        self.image_detail_view.show()

    def add_docker_images_view(self):
        self.image_list_widget.itemClicked.connect(self.on_image_clicked)
        dock = QDockWidget(Strings.IMAGES, self)
        dock.setWidget(self.image_list_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.image_detail_view = DockerImageDialog()


    def add_debug_console(self, debug=None):
        dock = QDockWidget("Debug Console", self)
        dock.setWidget(debug)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)

    def about(self):
        QMessageBox.about(Strings.ABOUT, "Testing Qt's Capabilities")

    @pyqtSlot(list, name='docker_refresh_images_signal')
    def refresh_images(self, images=None):
        self.image_list_widget.clear()
        for image in images:
            item = DockerImageListWidgetItem()
            item.setText(str(image))
            item.setData(Qt.UserRole, image)
            self.image_list_widget.addItem(item)


fake_tb = namedtuple('fake_tb', ('tb_frame', 'tb_lasti', 'tb_lineno', 'tb_next'))


def excepthook(exec_type, exec_value, exec_tb):
    enriched_tb = _add_missing_frames(exec_tb)
    # Note: sys.__excepthook__(...) would not work here.
    # We need to use print_exception(...):
    traceback.print_exception(exec_type, exec_value, enriched_tb)


def _add_missing_frames(tb:fake_tb=None):
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

    window = MainWindow()
    window.show()
    app.setActiveWindow(window)
    sys.excepthook = excepthook
    sys.exit(app.exec_())


