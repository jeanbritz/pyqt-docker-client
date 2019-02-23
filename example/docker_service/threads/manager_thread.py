import time

from PyQt5.Qt import QObject, pyqtSlot
from example.docker_service.threads.manager_signals import ManagerSignals

from docker import DockerClient
from docker.errors import DockerException


class ManagerThread(QObject):

    DISCONNECTED = 0
    CONNECTED = 1
    ATTEMPT_CONNECT = 2
    RECONNECT = 3

    def __init__(self, env=None):
        super().__init__()
        self._env = env
        self._signals = ManagerSignals()
        self._stop = False
        self._client = None
        self._status = 0
        self._connect_retries = 0
        self._last_ping = 0

    @pyqtSlot()
    def run(self):
        print("Started Manager Thread")
        self._status = self.DISCONNECTED
        while self._stop is not True:
            if self._status == self.DISCONNECTED:
                print("Trying to contact Docker Daemon")
                # Try to connect
                try:
                    self.init_env(env=self._env)
                    self._last_ping = time.time()
                except DockerException as e:
                    print(e.args)
                    self._stop = True
                    self._change_status(self.DISCONNECTED)
            time.sleep(5)
            if self._status == self.CONNECTED:
                if self._ping():
                    print("Docker Daemon is responsive")

        self._close()
        print("Manager Stopped")

    def abort(self):
        self._stop = True

    def init_env(self, timeout=120, version='auto', env=None):
        kwargs = {'timeout': timeout, 'version': version, 'environment': env}
        self._client = DockerClient.from_env(**kwargs)
        print("Connected to Docker Daemon")
        self._change_status(self.CONNECTED)

    def _ping(self) -> bool:
        return self._client.ping()

    def _close(self):
        print("Closing Docker Daemon connection ...")
        if self._client:
            self._client.close()
        self._change_status(self.DISCONNECTED)

    def _change_status(self, status=None):
        self._status = status
        self._signals.status_change.emit(self._status)

    def signals(self):
        return self._signals
