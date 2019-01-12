import os

from PyQt5.QtWidgets import QDialog, QLayout, QGroupBox, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QCheckBox,\
    QDialogButtonBox, QComboBox
from PyQt5.QtCore import Qt

from util import Log


class EnvConnectDialog(QDialog):

    def __init__(self, parent=None, db_connection=None, docker_manager=None):
        # super().__init__(parent=None, flags=(Qt.Window | Qt.WindowStaysOnTopHint))
        super(EnvConnectDialog, self).__init__(parent)
        self.setWindowIcon(parent.windowIcon())

        self._docker_manager = docker_manager
        self._main_layout: QLayout = None
        self._button_box: QDialogButtonBox = None

        self._env_combo_box: QComboBox = None
        self._env_host_text_box: QLabel = None
        self._api_version_combo_box: QComboBox = None

        self._use_tls_check_box: QCheckBox = None
        self._verify_host_check_box: QCheckBox = None
        self._cert_path_text_box: QLineEdit = None

        self._env_data = None
        self._api_version_data = None

        self._db_connection = db_connection
        self._init_ui()
        self._set_data()

    def _init_ui(self):
        self.setWindowTitle("Connect")
        self.setWindowModality(Qt.ApplicationModal)
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self._create_connection_group_box())
        self.main_layout.addWidget(self._create_ssl_group_box())
        self._button_box = self._create_button_box()
        self.main_layout.addWidget(self._button_box)
        self.setLayout(self.main_layout)

    def _set_data(self):
        self._env_data = self._db_connection.get_environments()
        self._api_version_data = self._db_connection.get_api_versions()
        for key in self._env_data:
            self._env_combo_box.addItem(key, self._env_data[key])
        for key in self._api_version_data:
            self._api_version_combo_box.addItem(key['name'], key['value'])

    def _create_connection_group_box(self):
        environment_group_box = QGroupBox("Environment")
        layout = QFormLayout()
        self._env_combo_box = QComboBox()
        self._env_combo_box.currentIndexChanged.connect(self.on_env_selection_change)
        self._env_combo_box.setCurrentIndex(0)
        layout.addRow(QLabel("Name"), self._env_combo_box)
        self._env_host_text_box = QLabel()
        layout.addRow(QLabel("Host"), self._env_host_text_box)
        self._api_version_combo_box = QComboBox()
        layout.addRow(QLabel("API Version"), self._api_version_combo_box)
        environment_group_box.setLayout(layout)
        return environment_group_box

    def _create_ssl_group_box(self):
        ssl_group_box = QGroupBox("TLS Details")
        layout = QFormLayout()
        self._use_tls_check_box = QCheckBox()
        self._use_tls_check_box.stateChanged.connect(self.on_use_tls_changed)
        self._verify_host_check_box = QCheckBox()
        self._verify_host_check_box.setEnabled(False)
        self._cert_path_text_box = QLineEdit()
        self._cert_path_text_box.setEnabled(False)
        layout.addRow(QLabel("Use TLS"), self._use_tls_check_box)
        layout.addRow(QLabel("Verify Host"), self._verify_host_check_box)
        layout.addRow(QLabel("Certificate Path"), self._cert_path_text_box)
        ssl_group_box.setLayout(layout)
        return ssl_group_box

    def _create_button_box(self):
        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        return button_box

    def on_env_selection_change(self, index):
        env = self._env_combo_box.currentData()
        try:
            self._env_host_text_box.setText(env['DOCKER_HOST'])
        except KeyError as e:
            self._env_host_text_box.setText("")

    def accept(self):
        env = self._env_data[self._env_combo_box.currentText()]
        Log.i('Loaded environment')
        version = self._api_version_combo_box.currentData()
        self._docker_manager.init_env(version=version, env=env)
        super().reject()

    def reject(self):
        super().reject()

    def on_use_tls_changed(self):
        self._verify_host_check_box.setEnabled(self._use_tls_check_box.isChecked())
        self._cert_path_text_box.setEnabled(self._use_tls_check_box.isChecked())
