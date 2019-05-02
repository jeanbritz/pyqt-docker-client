from abc import abstractmethod

from PyQt5.QtCore import QObject, pyqtSignal


class UiItem(QObject):



    @abstractmethod
    def widget(self):
        pass

    @abstractmethod
    def set_value(self):
        pass

    @abstractmethod
    def get_value(self):
        pass

    def on_change(self, value):
        pass

    @abstractmethod
    def set_enabled(self, value: bool):
        pass

    @abstractmethod
    def is_enabled(self):
        pass
