from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QToolBar, QAction, QVBoxLayout, QDockWidget, QListWidgetItem
from PyQt5.QtGui import QIcon

from docker.models.resource import Model
from docker.models.containers import Container

from core import ContainerStatusEnum
from util import Log
from i18n import Strings
from qt_signal import GeneralSignals, ToolbarSignals


class DefaultToolbar(QToolBar):

    def __init__(self, parent = None):
        super(DefaultToolbar, self).__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self._signals = ToolbarSignals()
        self._selected_model: Model = None
        self._play_action: QAction = None
        self._parent = parent
        self._init_ui()

    def _init_ui(self):
        self._play_action = QAction(QIcon("assets/play.svg"), Strings.PLAY_ACTION, self)
        self._play_action.setEnabled(False)
        self.addAction(self._play_action)
        self.actionTriggered[QAction].connect(self.on_action_clicked)

    def on_action_clicked(self, action: QAction):
        Log.i('Clicked on %s' % action.text())
        self._signals.clicked_play_signal.emit(action, self._selected_model)

    @pyqtSlot(QDockWidget, Model, name=GeneralSignals.GENERAL_DOCK_WIDGET_SELECTED_SIGNAL)
    def on_dock_widget_focus(self, widget: QDockWidget, model: Model):
        print('Toolbar: Clicked on widget %s and item %s' % (widget, model))
        self._selected_model = model
        if isinstance(model, Container):
            print('Clicked on a container %s' % model)
            if model.status == ContainerStatusEnum.EXITED.value:
                self._play_action.setEnabled(True)

    def play_action(self):
        return self._play_action

    def signals(self):
        return self._signals
