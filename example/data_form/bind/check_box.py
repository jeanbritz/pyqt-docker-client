from PyQt5.QtWidgets import QLineEdit, QCheckBox

from example.data_form.bind.ui_item import UiItem


class CheckBox(UiItem):

    def __init__(self, parent=None, signals=None):
        super(CheckBox, self).__init__()
        self._parent = parent
        self._signals = signals
        self._widget: QCheckBox = QCheckBox(parent)
        self._widget.stateChanged.connect(self.state_changed)

    def widget(self):
        return self._widget

    def set_value(self, value):
        if type(value) == bool:
            self._widget.setChecked(value)

    def get_value(self):
        return self._widget.isChecked()

    def set_enabled(self, value: bool):
        if type(value) == bool:
            self._widget.setEnabled(value)

    def is_enabled(self):
        self._widget.isEnabled()

    def state_changed(self, value):
        print("%s: State Changed [value: %s]" % (self.objectName(), value))
        self._signals.on_change_signal.emit(self.objectName(), str(value))
