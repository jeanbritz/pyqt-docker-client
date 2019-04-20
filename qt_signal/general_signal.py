from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QDockWidget

from core import ClientModel
from environment.model import DEnvEnvironment


class GeneralSignals(QObject):

    GENERAL_DOCK_WIDGET_SELECTED_SIGNAL = 'dock_widget_selected_signal'
    GENERAL_SHOW_LOADING_SIGNAL = 'show_loading_signal'
    GENERAL_STOP_DOCKER_SERVICE_SIGNAL = 'stop_docker_service_signal'
    GENERAL_ACCEPT_CONNECT_SIGNAL = 'accept_connect_signal'

    stop_docker_service_signal = pyqtSignal()
    dock_widget_selected_signal = pyqtSignal(QDockWidget, ClientModel, name=GENERAL_DOCK_WIDGET_SELECTED_SIGNAL)
    show_loading_signal = pyqtSignal(bool, str, name=GENERAL_SHOW_LOADING_SIGNAL)
    accept_connect_signal = pyqtSignal(DEnvEnvironment, name= GENERAL_ACCEPT_CONNECT_SIGNAL)
