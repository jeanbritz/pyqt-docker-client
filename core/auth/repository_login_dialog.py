from PyQt5.QtWidgets import QDialog, QLayout, QGroupBox, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QCheckBox,\
    QDialogButtonBox, QMessageBox
from PyQt5.QtCore import Qt

from i18n import Strings


class RepositoryLoginDialog(QDialog):

    def __init__(self, parent=None, db_connection=None, docker_manager=None):
        # super().__init__(parent=None, flags=(Qt.Window | Qt.WindowStaysOnTopHint))
        super(RepositoryLoginDialog, self).__init__(parent)
        self.setWindowIcon(parent.windowIcon())

        self._docker_manager = docker_manager
        self._main_layout: QLayout = None
        self._button_box: QDialogButtonBox = None

        self._username_text_box: QLineEdit = None
        self._password_text_box: QLineEdit = None
        self._email_text_box: QLineEdit = None

        self._reauth_check_box: QCheckBox = None

        # self._db_connection = db_connection
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("Repository Login")
        self.setWindowModality(Qt.ApplicationModal)
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self._create_credentials_group_box())
        self._button_box = self._create_button_box()
        self.main_layout.addWidget(self._button_box)
        self.setLayout(self.main_layout)

    def _create_credentials_group_box(self):
        group_box = QGroupBox("Credentials")
        layout = QFormLayout()
        self._username_text_box = QLineEdit()
        layout.addRow(QLabel("Username"), self._username_text_box)
        self._password_text_box = QLineEdit()
        self._password_text_box.setEchoMode(QLineEdit.Password)
        layout.addRow(QLabel("Password"), self._password_text_box)
        self._reauth_check_box = QCheckBox()
        layout.addRow(QLabel("Re-authenticate"), self._reauth_check_box)
        group_box.setLayout(layout)
        return group_box

    def _create_button_box(self):
        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        return button_box

    def accept(self):
        username: str = self._username_text_box.text()
        password: str = self._password_text_box.text()
        reauth: bool = self._reauth_check_box.isChecked()

        result = self._docker_manager.login(username=username, password=password,
                                   reauth=reauth)
        error = QMessageBox()

        if isinstance(result, str):
            error.setIcon(QMessageBox.Critical)
            error.setWindowTitle(Strings.ERROR)
            error.setText(result)

        if isinstance(result, dict):
            error.setIcon(QMessageBox.Information)
            error.setWindowTitle(Strings.INFO)
            error.setText(result['Status'])

        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
        super().reject()

    def reject(self):
        super().reject()

