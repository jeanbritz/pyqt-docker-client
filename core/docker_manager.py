import docker

from util.log import Log

from signal.docker_signal import DockerSignals
from docker.errors import DockerException


class DockerManager:

    DISCONNECTED = 0
    CONNECTED = 1

    def __init__(self):
        self._client: docker.DockerClient = None
        self._status = DockerManager.DISCONNECTED
        self._signals = DockerSignals()

    def connect(self, timeout=120, version='auto', env=None):
        kwargs = {'timeout': timeout, 'version': version, 'environment': env}
        try:
            self._client = docker.DockerClient.from_env(**kwargs)
            self._signals.connect_signal.emit()
            self._signals.refresh_images_signal.emit(self._client.images.list(all=True))
            self._signals.refresh_containers_signal.emit(self._client.containers.list(all=True))
            self._status = DockerManager.CONNECTED
        except DockerException as e:
            print(e)
            self._status = DockerManager.DISCONNECTED
            Log.e('Docker cannot connect')

    def disconnect(self):
        if self._client is not None:
            self._client.close()
            self._status = DockerManager.DISCONNECTED

    def status(self):
        return self._status

    def signals(self):
        return self._signals
