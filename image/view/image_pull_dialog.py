import os

from PyQt5.QtWidgets import QDialog, QLayout, QGroupBox, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QCheckBox,\
    QDialogButtonBox, QComboBox
from PyQt5.QtCore import Qt


class ImagePullDialog(QDialog):

    def __init__(self, parent=None, docker_manager=None, db_connection=None):
        # super().__init__(parent=None, flags=(Qt.Window | Qt.WindowStaysOnTopHint))
        super(ImagePullDialog, self).__init__(parent)
        self.setWindowIcon(parent.windowIcon())

        self._db_connection = db_connection
        self._docker_manager = docker_manager
        self._main_layout: QLayout = None
        self._button_box: QDialogButtonBox = None

        self._image_tag_text_box: QLineEdit = None

        self._registry_data: dict = None

        self._init_ui()
        self._set_data()

    def _init_ui(self):
        self.setWindowTitle("Pull Image")
        self.setWindowModality(Qt.ApplicationModal)
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self._create_registry_group_box())
        self._button_box = self._create_button_box()
        self.main_layout.addWidget(self._button_box)
        self.setLayout(self.main_layout)

    def _create_registry_group_box(self):
        repository_group_box = QGroupBox("Registry")
        layout = QFormLayout()
        self._registry_combo_box = QComboBox()
        self._registry_combo_box.currentIndexChanged.connect(self.on_registry_selection_change)
        self._registry_combo_box.setCurrentIndex(0)
        self._image_tag_text_box = QLineEdit()
        layout.addRow(QLabel("Name"), self._registry_combo_box)
        layout.addRow(QLabel("Tag"), self._image_tag_text_box)
        repository_group_box.setLayout(layout)
        return repository_group_box

    def _create_button_box(self):
        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        return button_box

    def on_registry_selection_change(self, index):
        pass

    def _set_data(self):
        self._registry_data = self._db_connection.get_registries()

        for key in self._registry_data:
            self._registry_combo_box.addItem(key['name'], key['hostname'])

    def accept(self):
        tag = self._image_tag_text_box.text()
        registry = self._registry_combo_box.currentData()

        print("ImagePullDialog :: accept :: Tag %s, Registry %s" % (tag, registry))
        # self._docker_manager.pull_image(tag=tag)
        super().reject()

    def reject(self):
        super().reject()