from PyQt5.QtCore import QObject, pyqtSignal


class DockerSignals(QObject):

    DOCKER_CONNECT_SIGNAL = 'docker_connect_signal'
    DOCKER_DISCONNECT_SIGNAL = 'docker_disconnect_signal'
    DOCKER_REFRESH_IMAGES_SIGNAL = 'docker_refresh_images_signal'
    DOCKER_REFRESH_CONTAINERS_SIGNAL = 'docker_refresh_containers_signal'

    disconnect_signal = pyqtSignal(name=DOCKER_DISCONNECT_SIGNAL)
    connect_signal = pyqtSignal(name=DOCKER_CONNECT_SIGNAL)
    refresh_images_signal = pyqtSignal(list, name=DOCKER_REFRESH_IMAGES_SIGNAL)
    refresh_containers_signal = pyqtSignal(list, name=DOCKER_REFRESH_CONTAINERS_SIGNAL)
