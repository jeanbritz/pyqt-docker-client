from PyQt5.QtCore import QThread, pyqtSignal
from docker import DockerClient

from core import ContainerClientModel
from util import DebugConsole, Log
from core.docker_enum import Operation


class DockerOperationThread(QThread):

    def __init__(self, client=None, model=None, operation: Operation = None):
        QThread.__init__(self)
        self._client: DockerClient = client
        self._model = model
        self._operation: Operation = operation

    def __del__(self):
        self.wait()

    def set_operation(self, operation: Operation = None):
        self._operation = operation

    def run(self):
        if isinstance(self._model, ContainerClientModel):
            if self._operation == Operation.START_CONTAINER:
                self._client.api.start(self._model.id)
                DebugConsole.println("Container %s has %s" % (self._model.names, 'started'))
            if self._operation == Operation.STOP_CONTAINER:
                self._client.api.stop(self._model.id, timeout=120)
                DebugConsole.println("Container %s has %s" % (self._model.names, 'stopped'))

    def finished(self):
        Log.i("finished() called")


