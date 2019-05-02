from PyQt5.QtCore import QObject, pyqtSignal


class DataFormSignals(QObject):
    on_change_signal = pyqtSignal(str, str, name="on_change")
