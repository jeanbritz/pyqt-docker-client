
from PyQt5.Qt import QItemSelectionModel
from PyQt5.QtWidgets import QDialog, QListView, QPushButton, QHBoxLayout, QVBoxLayout, QDesktopWidget
from environment.model import EnvironmentListModel


class EnvConfigureDialog(QDialog):

    def __init__(self, parent=None, dao=None):
        super(EnvConfigureDialog, self).__init__(parent)
        self.setWindowTitle("Environments")
        self._dao = dao
        self._init_ui()

    def _init_ui(self):
        """
        Initialize UI components
        :return:
        """

        self.list_view = QListView()
        self.list_model = EnvironmentListModel(dao=self._dao)
        self.list_selection_model = QItemSelectionModel(self.list_model)

        self.list_view.setModel(self.list_model)
        self.list_view.setSelectionModel(self.list_selection_model)

        btn_add = QPushButton('Add', self)
        btn_edit = QPushButton('Edit', self)
        btn_delete = QPushButton('Delete', self)

        list_layout = QHBoxLayout()
        list_layout.addStretch(1)
        list_layout.addWidget(self.list_view)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(btn_add)
        buttons_layout.addWidget(btn_edit)
        buttons_layout.addWidget(btn_delete)

        main_layout = QVBoxLayout()
        main_layout.addLayout(list_layout)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
