from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QLabel, QCheckBox, QVBoxLayout, QGroupBox

from example.data_form.bind.check_box import CheckBox
from example.data_form.bind.text_box import TextBox
from example.data_form.signals import DataFormSignals


class DataForm(QWidget):

    def __init__(self, config: list = None, grouping: list = None):
        super(QWidget, self).__init__()
        self._config = config
        self._grouping_config = grouping
        self._group_layouts = {}
        self._widgets = {}
        self._signals = DataFormSignals()
        self._signals.on_change_signal.connect(self.on_change)

    def draw(self):
        for group in self._grouping_config:
            self._group_layouts[group['name']] = QFormLayout()
        _layout = QVBoxLayout()
        for i in range(len(self._config)):
            _label = self._config[i]['label']
            _type = self._config[i]['type']
            _bind = self._config[i]['bind']
            _group = self._config[i]['group']
            _enabled = True
            if 'enabled' in self._config[i].keys():
                pass# _enabled = self.parse_bool(self._config[i]['enabled'])

            _input = None
            if _type in ('text', 'string'):
                _input = TextBox(parent=self, signals=self._signals)
            if _type == 'password':
                _input = TextBox(parent=self, signals=self._signals)
                _input.set_mode(_type)
            if _type in ('boolean', 'bool'):
                _input = CheckBox(parent=self, signals=self._signals)
            if _input is not None:
                _input.setObjectName(_bind)
                if type(_enabled) is bool:
                    _input.set_enabled(_enabled)
                self._widgets[_bind] = _input.widget()
            if _group:
                self._group_layouts[_group].addRow(QLabel(_label), _input.widget())
        for group in self._group_layouts:
            _group_widget = QGroupBox(group)
            _group_widget.setLayout(self._group_layouts[group])
            _layout.addWidget(_group_widget)
        self.setLayout(_layout)
        print(self.get_data())

    def get_data(self):
        data = []
        for bind in self._widgets:
            data.append({bind: self._widgets[bind].text()})
        return data

    def parse_bool(s):
        if s:
            return s.lower() in ("yes", "true", "t", "1")
        return False

    # @pyqtSlot(str, str, name="on_change")
    def on_change(self, bind, value):
        print("On Change - bind:%s, value:%s" % (bind, value))
