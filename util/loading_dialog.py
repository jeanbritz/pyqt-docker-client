from PyQt5.QtWidgets import QDialog, QHBoxLayout, QDialogButtonBox, QLabel
from PyQt5.Qt import Qt


class LoadingDialog(QDialog):

    def __init__(self, parent=None):
        # super().__init__(parent=None, flags=(Qt.Window | Qt.WindowStaysOnTopHint))
        super(LoadingDialog, self).__init__(parent)
        if parent:
            self.setWindowIcon(parent.windowIcon())
            self.setWindowTitle(parent.windowTitle())

        self._text_label: QLabel = QLabel('Loading...')
        self._main_layout: QHBoxLayout = None
        self._button_box: QDialogButtonBox = None
        self._init_ui()

    def _init_ui(self):
        self._main_layout = QHBoxLayout()
        #loading = QPixmap('assets/loading.svg')
        #label = QLabel()
        #label.setPixmap(loading)
        #self._main_layout.addWidget(label)
        self._main_layout.addWidget(self._text_label)
        self._button_box = QDialogButtonBox(QDialogButtonBox.Cancel)
        self._main_layout.addWidget(self._button_box)
        self.setLayout(self._main_layout)

    def set_text(self, text):
        if text:
            self._text_label.setText(text)
        else:
            self._text_label.setText("Loading...")
