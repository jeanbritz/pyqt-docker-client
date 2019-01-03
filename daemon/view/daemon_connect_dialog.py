from PyQt5.QtWidgets import QDialog, QLayout, QGroupBox, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QSpinBox,\
    QDialogButtonBox


class DaemonConnectDialog(QDialog):

    def __init__(self, parent=None):
        # super().__init__(parent=None, flags=(Qt.Window | Qt.WindowStaysOnTopHint))
        super(DaemonConnectDialog, self).__init__(parent)

        self.main_layout: QLayout = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Connect to Docker Deamon")
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.create_form_group_box())
        self.main_layout.addWidget(self.create_button_box())
        self.setLayout(self.main_layout)

    def create_form_group_box(self):
        form_group_box = QGroupBox("Form Layout")
        layout = QFormLayout()
        layout.addRow(QLabel("Hostname"), QLineEdit())
        layout.addRow(QLabel("Port"), QSpinBox())
        form_group_box.setLayout(layout)
        return form_group_box

    def create_button_box(self):
        return QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
