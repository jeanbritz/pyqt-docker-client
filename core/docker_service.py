from datetime import datetime
import enum
import time


from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject
from PyQt5.QtWidgets import QAction

from docker import DockerClient
from docker.models.resource import Model
from docker.models.containers import Container

from core import ContainerClientModel, DockerEntity
from util import Log
from i18n import Strings
from qt_signal import ToolbarSignals
from docker.errors import DockerException, APIError
from requests.exceptions import ConnectionError


class DockerService(QObject):

    def __init__(self):
        super().__init__()
        self._client: DockerClient = None
        self._status = ManagerStatus.DISCONNECTED
        self._signals = ManagerSignals()
        self._last_ping = 0
        self._stop = False
        self._kwargs = {}
        self._env = None

    @pyqtSlot()
    def run(self):
        Log.i("Manager Started [%s]" % self._env.name)
        while self._stop is not True:
            if self._status == ManagerStatus.DISCONNECTED:
                self._connect()
            time.sleep(2)
            if self._status == ManagerStatus.CONNECTED:
                diff = (datetime.now() - self._last_ping).total_seconds()
                if diff > 30:
                    try:
                        if self._ping():
                            self._last_ping = datetime.now()
                            Log.i("Docker Daemon is responsive")
                    except APIError as e:
                        Log.e(e)
                        Log.i("Docker Daemon became unresponsive")
                        self._change_status(ManagerStatus.DISCONNECTED)

        self._close()
        Log.i("Manager stopped")

    def init_env(self, env=None):
        """
        Initialize environment variables
        :param env: DEnvEnvironment Object
        :return:
        """
        self._last_ping = 0
        self._stop = False
        self._env = env
        self._kwargs = {'timeout': 120, 'version': 'auto', 'environment': env.settings_to_dict}

    def _ping(self):
        """
        Ping the Docker Daemon
        :return:
        """
        try:
            return self._client.ping()
        except ConnectionError as e:
            Log.e(e)
            Log.i("Docker Daemon became unresponsive")
            self._change_status(ManagerStatus.DISCONNECTED)
            return False

    def _connect(self):
        try:
            Log.i("Attempt to contact Docker Daemon")
            self._change_status(ManagerStatus.ATTEMPT_CONNECT)
            self._client = DockerClient.from_env(**self._kwargs)
            self._last_ping = datetime.now()
            Log.i("Connected to Docker Daemon")
            self._change_status(ManagerStatus.CONNECTED)
            self.refresh_all()
        except DockerException as e:
            Log.e(e)
            self._stop = True
            self._change_status(ManagerStatus.DISCONNECTED)

    def _close(self):
        """
        Close connection to Docker Daemon
        :return:
        """
        if self._client is not None:
            self._client.close()
            self._change_status(ManagerStatus.DISCONNECTED)

    def _change_status(self, status):
        """
        Broadcasts Docker Service status change
        :param status:
        :return:
        """
        self._status = status
        # Broadcast the status change
        self._signals.status_change_signal.emit(self._status)

    def status(self):
        return self._status

    def signals(self):
        return self._signals

    def abort(self):
        """
        Abort the Docker Service to continue
        :return:
        """
        self._stop = True

    def refresh_all(self):
        self._signals.refresh_signal.emit(DockerEntity.IMAGE, self._client.api.images(all=True))
        self._signals.refresh_signal.emit(DockerEntity.CONTAINER, self._client.api.containers(all=True))
        self._signals.refresh_signal.emit(DockerEntity.NETWORK, self._client.networks.list())

    def login(self, username=None, password=None, reauth=False, registry=None):
        try:
            result = self._client.api.login(username=username, password=password, reauth=reauth, registry=registry)
            return result
        except APIError as e:
            return e.explanation

    def log(self, container: Container = None):
        logs = container.logs(**{'stream': True})
        return logs

    def stop_container(self, model: ContainerClientModel = None, timeout=120):
        self._general_signals.show_loading_signal.emit(True, 'Stopping %s ...' % model.names)
        result = self._client.api.stop(model.id, timeout=timeout)
        Log.i('Container Stop Result %s' % result)
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
                    pass
                    # thread = DockerOperationThread(docker_manager=self, model=model, operation=Operation.STOP_CONTAINER)
                    # thread.start()

                self._signals.refresh_containers_signal.emit(self._client.api.containers(all=True))
        except APIError as e:
            print("DockerManager :: API Error :: %s" % e)


class ManagerStatus(enum.Enum):

    DISCONNECTED = 'Disconnected'
    CONNECTED = 'Connected'
    ATTEMPT_CONNECT = 'Attempt to connect'
    RECONNECT = 'Reconnect'


class ManagerSignals(QObject):

    error = pyqtSignal(str)
    status_change_signal = pyqtSignal(ManagerStatus)
    refresh_signal = pyqtSignal(DockerEntity, list, name='docker_refresh_signal')
