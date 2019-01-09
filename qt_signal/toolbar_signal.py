from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QAction

from docker.models.resource import Model


class ToolbarSignals(QObject):

    TOOLBAR_CLICKED_SIGNAL = 'toolbar_clicked_signal'

    clicked_signal = pyqtSignal(QAction, Model, name=TOOLBAR_CLICKED_SIGNAL)
