
from PyQt5.Qt import QObject, pyqtSignal


class ManagerSignals(QObject):

    error = pyqtSignal(str)
    status_change = pyqtSignal(int)
