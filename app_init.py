import sys
import os
import traceback

from PyQt5.Qt import QApplication, QSizePolicy
from PyQt5.QtWidgets import QMessageBox, QSpacerItem

from i18n import Strings
from util import Log
from main_window import MainWindow


def handle_exception(exec_type, exec_value, exec_traceback):
    if issubclass(exec_type, KeyboardInterrupt):
        sys.__excepthook__(exec_type, exec_value, exec_traceback)
        return

    file_name = os.path.split(exec_traceback.tb_frame.f_code.co_filename)[1]
    print(file_name)
    detail_error = ''
    for tb in traceback.extract_tb(exec_traceback):
        detail_error += '\n{}\n{}:{}\n'.format(str(tb.line), str(tb.filename), str(tb.lineno))
        print(exec_type, exec_value, file_name + ':' + str(exec_traceback.tb_lineno), tb)
        # Log.e(exec_type, exec_value, file_name + ':' + str(exec_traceback.tb_lineno), tb)

    Log.e(detail_error)

    traceback.print_exc(file=sys.stdout)

    tb = traceback.extract_tb(exec_traceback)
    msg = QMessageBox()

    msg.setIcon(QMessageBox.Critical)
    trace = traceback.format_exc()

    msg.setText(str(exec_type))
    msg.setInformativeText(str(tb[len(tb) - 1].line))
    msg.setWindowTitle(Strings.ERROR)
    msg.setDetailedText(detail_error)
    msg.setStandardButtons(QMessageBox.Ok)

    horizontal_spacer = QSpacerItem(512, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
    layout = msg.layout()
    layout.addItem(horizontal_spacer, layout.rowCount(), 0, 1, layout.columnCount())

    msg.exec_()


if __name__ == "__main__":
    Log.__init__(None)
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
