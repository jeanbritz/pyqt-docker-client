from datetime import datetime
import time
import enum

from PyQt5.Qt import QObject, pyqtSlot, pyqtSignal

from docker import DockerClient
from docker.errors import DockerException, APIError


class Manager(QObject):

    def __init__(self, env=None):
        super().__init__()
        self._env = env
        self._signals = ManagerSignals()
        self._stop = False
        self._client = None
        self._status = ManagerStatus.DISCONNECTED
        self._connect_retries = 0
        self._last_ping = 0

    @pyqtSlot()
    def run(self):
        print("Started Manager")
        while self._stop is not True:
            if self._status == ManagerStatus.DISCONNECTED:
                print("Trying to contact Docker Daemon")
                # Try to connect
                try:
                    self.init_env(env=self._env)
                    self._last_ping = datetime.now()
                except DockerException as e:
                    print(e.args)
                    self._stop = True
                    self._change_status(ManagerStatus.DISCONNECTED)
            time.sleep(5)
            if self._status == ManagerStatus.CONNECTED:
                diff = (datetime.now() - self._last_ping).total_seconds()
                if diff > 30:
                    try:
                        if self._ping():
                            self._last_ping = datetime.now()
                            print("Docker Daemon is responsive")
                    except APIError as e:
                        print(e)
                        print("Docker Daemon became unresponsive")
                        self._change_status(ManagerStatus.DISCONNECTED)

        self._close()
        print("Manager Stopped")

    def abort(self):
        self._stop = True

    def init_env(self, timeout=120, version='auto', env=None):
        kwargs = {'timeout': timeout, 'version': version, 'environment': env}
        self._client = DockerClient.from_env(**kwargs)
        print("Connected to Docker Daemon")
        self._change_status(ManagerStatus.CONNECTED)

    def _ping(self) -> bool:
        return self._client.ping()

    def _close(self):
        print("Closing Docker Daemon connection")
        if self._client:
            self._client.close()
        self._change_status(ManagerStatus.DISCONNECTED)

    def _change_status(self, status=None):
        self._status = status
        self._signals.status_change.emit(self._status)

    def signals(self):
        return self._signals


class ManagerStatus(enum.Enum):

    DISCONNECTED = 'Disconnected'
    CONNECTED = 'Connected'
    ATTEMPT_CONNECT = 'Attempt to connect'
    RECONNECT = 'Reconnect'


class ManagerSignals(QObject):

    error = pyqtSignal(str)
    status_change = pyqtSignal(ManagerStatus)
