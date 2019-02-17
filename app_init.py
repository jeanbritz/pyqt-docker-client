import sys
import os
import traceback

from PyQt5.Qt import QApplication, QSizePolicy
from PyQt5.QtWidgets import QMessageBox, QSpacerItem

from db import Upgrade
from i18n import Strings
from util import Log
from main_window import MainWindow


def handle_exception(exec_type, exec_value, exec_traceback):
    if issubclass(exec_type, KeyboardInterrupt):
        sys.__excepthook__(exec_type, exec_value, exec_traceback)
        return

    file_name = os.path.split(exec_traceback.tb_frame.f_code.co_filename)[1]
    detail_error = ''
    last_filename = None
    spacing = ''
    for tb in traceback.format_tb(exec_traceback, 10):
        pass
        # print(tb)
        #     if last_filename != tb.filename:
        #         detail_error += '[+] {} - {}:{}\n'.format(str(tb.line), str(tb.filename), str(tb.lineno))
        #         detail_error += spacing
        #         spacing += '\t'
        #     else:
        #         detail_error += spacing
        #         detail_error += '[-] {}:{}\n'.format(tb.line, tb.lineno)
        #     last_filename = tb.filename
        # for element in stack:
    traceback.print_exc()
    tb = traceback.extract_tb(exec_traceback)
    msg = QMessageBox()

    msg.setIcon(QMessageBox.Critical)
    trace = traceback.format_exc()

    msg.setText("Error has occurred")
    msg.setInformativeText(str(tb[len(tb) - 1].line))
    msg.setWindowTitle(Strings.ERROR)
    msg.setDetailedText(detail_error)
    msg.setStandardButtons(QMessageBox.Ok)

    horizontal_spacer = QSpacerItem(512, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
    layout = msg.layout()
    layout.addItem(horizontal_spacer, layout.rowCount(), 0, 1, layout.columnCount())

    msg.exec_()


def main():
    global app
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

    sys.excepthook = handle_exception
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
