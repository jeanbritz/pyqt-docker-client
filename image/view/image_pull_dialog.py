import os

from PyQt5.QtWidgets import QDialog, QLayout, QGroupBox, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QCheckBox,\
    QDialogButtonBox, QComboBox
from PyQt5.QtCore import Qt


class ImagePullDialog(QDialog):

    def __init__(self, parent=None, docker_manager=None):
        # super().__init__(parent=None, flags=(Qt.Window | Qt.WindowStaysOnTopHint))
        super(ImagePullDialog, self).__init__(parent)
        self.setWindowIcon(parent.windowIcon())

        self._docker_manager = docker_manager
        self._main_layout: QLayout = None
        self._button_box: QDialogButtonBox = None

        self._image_tag_text_box: QLineEdit = None

        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("Connect")
        self.setWindowModality(Qt.ApplicationModal)
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self._create_repository_group_box())
        self._button_box = self._create_button_box()
        self.main_layout.addWidget(self._button_box)
        self.setLayout(self.main_layout)

    def _create_repository_group_box(self):
        repository_group_box = QGroupBox("Repository")
        layout = QFormLayout()
        self._image_tag_text_box = QLineEdit()
        layout.addRow(QLabel("Tag"), self._image_tag_text_box)
        repository_group_box.setLayout(layout)
        return repository_group_box

    def _create_button_box(self):
        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        return button_box

    # def on_repo_selection_change(self, index):
    #     env = self._env_combo_box.currentData()
    #     try:
    #         self._image_tag_text_box.setText(env['DOCKER_HOST'])
    #     except KeyError as e:
    #         self._image_tag_text_box.setText("")

    def accept(self):
        tag = self._image_tag_text_box.text()
        self._docker_manager.pull_image(tag=tag)
        super().reject()

    def reject(self):
        super().reject()

    def on_use_tls_changed(self):
        self._verify_host_check_box.setEnabled(self._use_tls_check_box.isChecked())
        self._cert_path_text_box.setEnabled(self._use_tls_check_box.isChecked())
