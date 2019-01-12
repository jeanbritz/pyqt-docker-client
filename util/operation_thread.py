from PyQt5.QtCore import QThread, pyqtSignal

from core import ContainerClientModel
from util import DebugConsole
from core.docker_enum import Operation


class DockerOperationThread(QThread):

    def __init__(self, docker_manager=None, model=None, operation: Operation=None):
        QThread.__init__(self)
        self._docker_manager = docker_manager
        self._model = model
        self._operation: Operation = operation

    def __del__(self):
        self.wait()

    def run(self):
        if isinstance(self._model, ContainerClientModel):
            if self._operation == Operation.STOP_CONTAINER:
                self._docker_manager.stop_container(self._model, timeout=120)
                DebugConsole.println("Container %s has %s" % (self._model.names, 'stopped'))

    def finished(self):
        print("DockerOperationThread :: finished() called")


