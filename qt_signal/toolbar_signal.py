from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QAction

from core import ClientModel


class ToolbarSignals(QObject):

    TOOLBAR_CLICKED_SIGNAL = 'toolbar_clicked_signal'
    TOOLBAR_REFRESH_SIGNAL = 'toolbar_refresh_signal'

    clicked_signal = pyqtSignal(QAction, ClientModel, name=TOOLBAR_CLICKED_SIGNAL)
    refresh_signal = pyqtSignal(name=TOOLBAR_REFRESH_SIGNAL)
