from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QDockWidget

from image.view import DockerImageListWidget
from qt_signal import GeneralSignals


class ImageDockWidget(QDockWidget):

    def __init__(self, *__args, signals: GeneralSignals = None):
        super().__init__(*__args)

        self._signals = signals
        self._list_widget: DockerImageListWidget = None

        self._init_ui()

    def _init_ui(self):
        self._list_widget = DockerImageListWidget()
        self._list_widget.clicked.connect(self.on_click)
        self.setWidget(self._list_widget)

    def on_click(self, prev: QModelIndex = None, next: QModelIndex = None):
        self._signals.dock_widget_selected_signal.emit(self, prev.data(Qt.UserRole))

    def list_widget(self):
        return self._list_widget

    def signals(self):
        return self._signals
