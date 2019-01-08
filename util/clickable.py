from PyQt5.QtCore import QObject, pyqtSignal, QEvent
from PyQt5.QtWidgets import QDockWidget


def create_clickable_dock_widget(widget: QDockWidget):

    class Filter(QObject):

        clicked = pyqtSignal(QObject)

        def eventFilter(self, obj: QObject, event: QEvent):
           # print('obj: %s, event: %s' % (obj, event))
            if obj == widget or obj == widget.widget():
                if event.type() == QEvent.MouseButtonRelease:
                    self.clicked.emit(obj, widget)
                    return True
            return False

    _filter = Filter(widget)
    widget.installEventFilter(_filter)
    return _filter.clicked
