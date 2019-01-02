from PyQt5.QtCore import QObject, pyqtSignal


class GeneralSignals(QObject):

    GENERAL_DAEMON_SELECTED_SIGNAL = 'daemon_selected_signal'

    daemon_selected_signal = pyqtSignal(dict, name=GENERAL_DAEMON_SELECTED_SIGNAL)
