from PyQt5.QtWidgets import QLineEdit

from example.data_form.bind.ui_item import UiItem


class TextBox(UiItem):

    def __init__(self, parent=None, signals=None):
        super(TextBox, self).__init__()
        self._signals = signals
        self._widget: QLineEdit = QLineEdit(parent)
        self._widget.textChanged.connect(self.text_changed)

    def widget(self):
        return self._widget

    def set_value(self):
        pass

    def get_value(self):
        return self._widget.text()

    def set_enabled(self, value: bool):
        pass

    def is_enabled(self):
        pass

    def set_mode(self, mode):
        if mode == 'password':
            self._widget.setEchoMode(QLineEdit.Password)

    def text_changed(self, value):
        print("%s: State Changed [value: %s]" % (self.objectName(), value))
        self._signals.on_change_signal.emit(self.objectName(), value)
