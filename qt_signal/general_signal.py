from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QDockWidget

from docker.models.resource import Model


class GeneralSignals(QObject):

    GENERAL_DOCK_WIDGET_SELECTED_SIGNAL = 'dock_widget_selected_signal'

    dock_widget_selected_signal = pyqtSignal(QDockWidget, Model, name=GENERAL_DOCK_WIDGET_SELECTED_SIGNAL)
