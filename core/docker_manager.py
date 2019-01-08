from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtWidgets import QAction

from docker import DockerClient
from docker.models.resource import Model
from docker.models.containers import Container

from util import Log
from i18n import Strings

from qt_signal import DockerSignals, ToolbarSignals
from docker.errors import DockerException, APIError


class DockerManager(QObject):

    DISCONNECTED = 0
    CONNECTED = 1

    def __init__(self):
        super().__init__()
        self._client: DockerClient = None
        self._status = DockerManager.DISCONNECTED
        self._signals = DockerSignals()

    def init_env(self, timeout=120, version='auto', env=None):
        kwargs = {'timeout': timeout, 'version': version, 'environment': env}
        try:
            self._client = DockerClient.from_env(**kwargs)
            version = self._client.api.version()
            Log.i('Initialized communication using Docker Engine API version %s' % version['ApiVersion'])
            self._signals.connect_signal.emit()
            self._signals.refresh_images_signal.emit(self._client.images.list(all=True))
            self._signals.refresh_containers_signal.emit(self._client.containers.list(all=True))
            self._status = DockerManager.CONNECTED
        except DockerException as e:
            print(e)
            self._status = DockerManager.DISCONNECTED
            Log.e('Docker cannot connect')

    def close(self):
        if self._client is not None:
            self._client.close()
            self._status = DockerManager.DISCONNECTED

    def status(self):
        return self._status

    def signals(self):
        return self._signals

    def start_container(self, container: Container = None):
        if container is not None:
            self._client.api.start(container)

    @pyqtSlot(QAction, Model, name=ToolbarSignals.TOOLBAR_CLICKED_CONNECT_SIGNAL)
    def on_toolbar_action(self, action: QAction, model: Model):
        try:
            print('Action: %s, Model: %s' % (action, model))
            if isinstance(model, Container):
                if action.text() == Strings.PLAY_ACTION and model.status == 'exited':
                    value = self._client.api.start(model.id)
                    print(value)
        except APIError as e:
            print(e)
