from PyQt5.QtCore import QObject, pyqtSignal, QVariant

from docker.models.containers import Container
from environment.model import DEnvEnvironment


class DockerSignals(QObject):

    DOCKER_STATUS_CHANGE_SIGNAL = 'docker_status_change_signal'
    DOCKER_REFRESH_IMAGES_SIGNAL = 'docker_refresh_images_signal'
    DOCKER_REFRESH_CONTAINERS_SIGNAL = 'docker_refresh_containers_signal'
    DOCKER_REFRESH_NETWORKS_SIGNAL = 'docker_refresh_networks_signal'

    DOCKER_START_CONTAINER_SIGNAL = 'docker_start_container_signal'

    DOCKER_START_SERVICE_SIGNAL = 'docker_start_service_signal'

    status_change_signal = pyqtSignal(QVariant, name=DOCKER_STATUS_CHANGE_SIGNAL)
    refresh_images_signal = pyqtSignal(list, name=DOCKER_REFRESH_IMAGES_SIGNAL)
    refresh_containers_signal = pyqtSignal(list, name=DOCKER_REFRESH_CONTAINERS_SIGNAL)
    refresh_networks_signal = pyqtSignal(list, name=DOCKER_REFRESH_NETWORKS_SIGNAL)

    start_container_signal = pyqtSignal(Container, name=DOCKER_START_CONTAINER_SIGNAL)

    start_docker_service = pyqtSignal(DEnvEnvironment, name=DOCKER_START_SERVICE_SIGNAL)
