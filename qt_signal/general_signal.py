from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QDockWidget

from core import ClientModel


class GeneralSignals(QObject):

    GENERAL_DOCK_WIDGET_SELECTED_SIGNAL = 'dock_widget_selected_signal'
    GENERAL_SHOW_LOADING_SIGNAL = 'show_loading_signal'

    dock_widget_selected_signal = pyqtSignal(QDockWidget, ClientModel, name=GENERAL_DOCK_WIDGET_SELECTED_SIGNAL)
    show_loading_signal = pyqtSignal(bool, str, name=GENERAL_SHOW_LOADING_SIGNAL)
