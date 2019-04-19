
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QTabWidget
from PyQt5.QtCore import Qt


class ConfigDialog(QDialog):

    def __init__(self, parent=None,):
        super(ConfigDialog, self).__init__(parent)

        self._config_button_box = None
        self._config_tab_widget = None
v
    def _init_ui(self):
        self._config_button_box = QDialogButtonBox(self)
        self._config_button_box.setOrientation(Qt.Horizontal)
        self._config_button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self._config_tab_widget = QTabWidget(self)
