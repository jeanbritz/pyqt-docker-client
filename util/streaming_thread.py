from PyQt5.QtCore import QThread, pyqtSignal
from docker import DockerClient

from core import ContainerClientModel
from util import Log


class StreamingThread(QThread):

    def __init__(self, client=None, model=None, log_signal = None):
        QThread.__init__(self)
        self._client: DockerClient = client
        self._model = model
        self._log_signal = log_signal

    def __del__(self):
        self.wait()

    def run(self):
        if isinstance(self._model, ContainerClientModel):
            stream = self._client.api.logs(self._model.id, follow=True, stream=True)
            for line in stream:
                if self._log_signal:
                    self._log_signal.emit(line)

    def finished(self):
        Log.i("finished() called")


