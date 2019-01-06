from PyQt5.QtWidgets import QToolBar, QAction, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from util import Log
from i18n import Strings
from signal import GeneralSignals


class DefaultToolbar(QToolBar):

    def __init__(self, parent = None):
        super(DefaultToolbar, self).__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self._connect_action: QAction = None
        self.parent = parent
        self.init_ui()

        self.current_daemon: dict = None

    def init_ui(self):
        self._connect_action = QAction(QIcon("assets/play.svg"), Strings.CONNECT_ACTION, self)
        self._connect_action.setEnabled(False)
        self.addAction(self._connect_action)
        self.actionTriggered[QAction].connect(self.on_action_clicked)

    @pyqtSlot(dict, name=GeneralSignals.GENERAL_DAEMON_SELECTED_SIGNAL)
    def on_daemon_selected(self, daemon: dict = None):
        Log.i('Daemon selected')
        self._connect_action.setEnabled(True)
        self.current_daemon = daemon

    def on_action_clicked(self, action: QAction):
        Log.i('Clicked on %s' % action.text())
        if action.text() == Strings.CONNECT_ACTION:
            if self.current_daemon is not None:
                self.parent.docker_manager.connect(hostname=self.current_daemon['hostname'],
                                                   port=self.current_daemon['port'])
