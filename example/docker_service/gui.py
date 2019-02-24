import sys

from PyQt5.Qt import QApplication, QVBoxLayout, QPushButton, QWidget, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QLabel
from example.docker_service.manager_thread import Manager, ManagerStatus


class MainWindow(QMainWindow):

    signal_stop_worker = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()

        self.top: int = 400
        self.left: int = 400
        self.width: int = 600
        self.height: int = 500

        self.setGeometry(self.top, self.left, self.width, self.height)

        self.layout = QVBoxLayout()
        self.btn_start = QPushButton()
        self.btn_start.clicked.connect(self.start_manager)
        self.btn_start.setText("Start")
        self.btn_stop = QPushButton()
        self.btn_stop.clicked.connect(self.stop_manager)
        self.btn_stop.setText("Stop")
        self.status_label = QLabel()

        self.layout.addWidget(self.btn_start)
        self.layout.addWidget(self.btn_stop)
        self.layout.addWidget(self.status_label)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.manager_thread = None
        self.manager_worker = None

    @pyqtSlot(ManagerStatus)
    def manager_status_change(self, status):
        self.status_label.setText(status.value)

    def stop_manager(self):
        self.signal_stop_worker.emit()

    def start_manager(self):
        self.manager_thread = QThread()
        env = {'DOCKER_CERT_PATH': '',
               'DOCKER_HOST': 'tcp://10.0.0.17:2375',
               'DOCKER_TLS_VERIFY': ''}
        self.manager_worker = Manager(env=env)
        self.manager_thread.setObjectName("Manager Thread")
        self.manager_worker.signals().status_change.connect(self.manager_status_change)
        self.signal_stop_worker.connect(self.manager_worker.abort)
        self.manager_worker.moveToThread(self.manager_thread)
        self.manager_thread.started.connect(self.manager_worker.run)
        self.manager_thread.start()


def main():
    global app

    print('Starting GUI')
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    app.setActiveWindow(window)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
