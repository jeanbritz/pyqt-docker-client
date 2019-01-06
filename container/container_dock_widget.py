from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QDockWidget

from container import DockerContainerListWidget, DockerContainerListWidgetItem


class ContainerDockWidget(QDockWidget):

    def __init__(self, *__args):
        super().__init__(*__args)

        self._list_widget: DockerContainerListWidget = None
        self._current_selected_item: DockerContainerListWidgetItem = None
        self._init_ui()

    def _init_ui(self):
        self._list_widget = DockerContainerListWidget()
        self._list_widget.currentItemChanged.connect(self.on_container_clicked)
        self.setWidget(self._list_widget)

    def on_container_clicked(self, prev: DockerContainerListWidgetItem=None, next=None):
        self._current_selected_item = prev
        print(prev.data(Qt.UserRole))
        print(next)

    def list_widget(self):
        return self._list_widget



