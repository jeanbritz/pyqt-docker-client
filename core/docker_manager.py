from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtWidgets import QAction

from docker import DockerClient
from docker.models.resource import Model
from docker.models.containers import Container

from core import ContainerClientModel
from core.docker_enum import Operation
from util import Log, DockerOperationThread, DebugConsole
from i18n import Strings
from qt_signal import DockerSignals, ToolbarSignals
from docker.errors import DockerException, APIError


class DockerManager(QObject):

    DISCONNECTED = 0
    CONNECTED = 1

    def __init__(self, general_signals=None):
        super().__init__()
        self._client: DockerClient = None
        self._status = DockerManager.DISCONNECTED
        self._signals = DockerSignals()
        self._general_signals = general_signals

    def init_env(self, timeout=120, version='auto', env=None):
        kwargs = {'timeout': timeout, 'version': version, 'environment': env}
        try:
            self._client = DockerClient.from_env(**kwargs)
            version = self._client.api.version()
            DebugConsole.println('Environment loaded for %s' % env['DOCKER_HOST'])
            Log.i('Initialized communication using Docker Engine API version %s' % version['ApiVersion'])
            self._change_status(DockerManager.CONNECTED)
            self.refresh_all()

        except DockerException as e:
            print("DockerManager :: %s" % e)
            self._change_status(DockerManager.DISCONNECTED)
            DebugConsole.println('Docker Client could not load environment')
            Log.e('Docker Client could not load environment')

    def close(self):
        if self._client is not None:
            self._client.close()
            self._change_status(DockerManager.DISCONNECTED)

    def _change_status(self, status):
        self._status = status
        # Broadcast the status change
        self._signals.status_change_signal.emit(self._status)

    def status(self):
        return self._status

    def signals(self):
        return self._signals

    def refresh_all(self):
        self._signals.refresh_images_signal.emit(self._client.api.images(all=True))
        self._signals.refresh_containers_signal.emit(self._client.api.containers(all=True))
        self._signals.refresh_networks_signal.emit(self._client.networks.list())

    def login(self, username=None, password=None, reauth=False, registry=None):
        try:
            result = self._client.api.login(username=username, password=password, reauth=reauth, registry=registry)
            print('Result = %s' % result)
            return result
        except APIError as e:
            return e.explanation

    def log(self, container: Container = None):
        logs = container.logs(**{'stream': True})
        return logs

    def stop_container(self, model: ContainerClientModel = None, timeout=120):
        self._general_signals.show_loading_signal.emit(True, 'Stopping %s ...' % model.names)
        #self.log(model)
        result = self._client.api.stop(model.id, timeout=timeout)
        print('DockerManager :: Container Stop Result %s' % result)
        self._signals.refresh_containers_signal.emit(self._client.api.containers(all=True))
        self._general_signals.show_loading_signal.emit(False, '')

    def pull_image(self, repository='hub.docker.com', tag=None):
        if tag is not None:
            try:
                for line in self._client.api.pull(repository=repository, tag=tag, stream=True):
                    print(line)
            except APIError as e:
                print(e)
            self._signals.refresh_images_signal.emit(self._client.images.list(all=True))

    @pyqtSlot(name=ToolbarSignals.TOOLBAR_REFRESH_SIGNAL)
    def on_refresh_action(self):
        self.refresh_all()

    @pyqtSlot(QAction, Model, name=ToolbarSignals.TOOLBAR_CLICKED_SIGNAL)
    def on_toolbar_action(self, action: QAction, model: Model = None):
        try:

            if isinstance(model, ContainerClientModel):
                if action.text() == Strings.PLAY_ACTION and model.state == 'exited':
                    self._client.api.start(model.id)
                if action.text() == Strings.STOP_ACTION and model.state == 'running':
                    thread = DockerOperationThread(docker_manager=self, model=model, operation=Operation.STOP_CONTAINER)
                    thread.start()

                self._signals.refresh_containers_signal.emit(self._client.api.containers(all=True))
        except APIError as e:
            print("DockerManager :: API Error :: %s" % e)
