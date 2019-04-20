import sys
import traceback

from PyQt5.Qt import QApplication, QSizePolicy
from PyQt5.QtWidgets import QMessageBox, QSpacerItem

from db import Upgrade
from i18n import Strings
from main_window import MainWindow
from util import Log


def handle_exception(exec_type, exec_value, exec_traceback):
    if issubclass(exec_type, KeyboardInterrupt):
        sys.__excepthook__(exec_type, exec_value, exec_traceback)
        return
    detail_error = ''
    print("============= UNHANDLED EXCEPTION =============")
    for line in traceback.format_exception(exec_type, exec_value, exec_traceback):
        detail_error += line
    print(detail_error)
    print("===============================================")

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)

    msg.setText("Error has occurred. See logs for more details")
    msg.setInformativeText(exec_value.__repr__())
    msg.setWindowTitle(Strings.ERROR)
    msg.setStandardButtons(QMessageBox.Ok)

    horizontal_spacer = QSpacerItem(512, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
    layout = msg.layout()
    layout.addItem(horizontal_spacer, layout.rowCount(), 0, 1, layout.columnCount())

    msg.exec_()


def main():
    global app
    global threads

    Log.__init__(None)
    Log.i("Performing DB Init")
    upgrade = Upgrade()
    upgrade.upgrade()

    Log.i('Starting GUI')
    app = QApplication(sys.argv)
    Log.i('Process ID %s' % app.applicationPid())

    app.setStyle('Fusion')
    app.focusWidget()
    window = MainWindow()
    app.setActiveWindow(window)
    window.show()

    threads = []

    sys.excepthook = handle_exception
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
