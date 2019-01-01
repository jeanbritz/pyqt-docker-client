from PyQt5.QtCore import QObject, pyqtSignal


class DockerSignal(QObject):

    disconnect_signal = pyqtSignal()
    connect_signal = pyqtSignal(int, name='docker_connect_signal')

    refresh_images_signal = pyqtSignal(list, name="docker_refresh_images_signal")