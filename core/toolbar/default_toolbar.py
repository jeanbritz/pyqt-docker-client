from PyQt5.QtCore import pyqtSlot, QVariant
from PyQt5.QtWidgets import QToolBar, QAction, QVBoxLayout, QDockWidget
from PyQt5.QtGui import QIcon

from core import ContainerClientModel, ClientModel
from core.docker_enum import ContainerStatus
from i18n import Strings
from qt_signal import GeneralSignals, ToolbarSignals
from core.docker_manager_service import ManagerStatus


class DefaultToolbar(QToolBar):

    def __init__(self, parent = None):
        super(DefaultToolbar, self).__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self._signals = ToolbarSignals()
        self._selected_model: ClientModel = None
        self._refresh_action: QAction = None
        self._play_action: QAction = None
        self._stop_action: QAction = None
        self._parent = parent
        self._init_ui()

    def _init_ui(self):
        self._refresh_action = QAction(QIcon("assets/refresh.svg"), Strings.REFRESH_ACTION, self)
        self._refresh_action.setEnabled(False)
        self.setToolTip(Strings.REFRESH_ACTION)
        self._play_action = QAction(QIcon("assets/play.svg"), Strings.PLAY_ACTION, self)
        self._play_action.setEnabled(False)
        self.setToolTip(Strings.PLAY_ACTION)
        self._stop_action = QAction(QIcon("assets/stop.svg"), Strings.STOP_ACTION, self)
        self._stop_action.setEnabled(False)
        self.setToolTip(Strings.STOP_ACTION)

        self.addAction(self._refresh_action)
        self.addAction(self._play_action)
        self.addAction(self._stop_action)
        self.actionTriggered[QAction].connect(self.on_action_clicked)

    def on_action_clicked(self, action: QAction):
        if action.text() != Strings.REFRESH_ACTION:
            self._signals.clicked_signal.emit(action, self._selected_model)
        else:
            self._signals.refresh_signal.emit()

    @pyqtSlot(QDockWidget, ClientModel, name=GeneralSignals.GENERAL_DOCK_WIDGET_SELECTED_SIGNAL)
    def on_dock_widget_focus(self, widget: QDockWidget, model: ClientModel):
        self._selected_model = model
        self._play_action.setEnabled(False)
        self._stop_action.setEnabled(False)
        if isinstance(model, ContainerClientModel):
            if model.state == ContainerStatus.EXITED.value:
                self._play_action.setEnabled(True)
            if model.state == ContainerStatus.RUNNING.value:
                self._stop_action.setEnabled(True)

    @pyqtSlot(ManagerStatus)
    def on_docker_manager_status_change(self, status):
        if status == ManagerStatus.CONNECTED:
            self._refresh_action.setEnabled(True)
        if status == ManagerStatus.DISCONNECTED:
            self.reset()

    def signals(self):
        return self._signals

    def reset(self):
        self._refresh_action.setEnabled(False)
        self._play_action.setEnabled(False)
        self._stop_action.setEnabled(False)
