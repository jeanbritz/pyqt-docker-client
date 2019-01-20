from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlDriver, QSqlError

"""
The QSqlQuery::exec() function returns a bool value that indicates if
the request has been successful. In your production code, always check
this value. You can further investigate the error
with QSqlQuery::lastError(). 
"""


class DbManager:

    def __init__(self):
        self._conn: QSqlDatabase = None
        self._driver: QSqlDriver = None

    def create(self) -> QSqlDatabase:
        """

        :return:
        """
        self._conn = QSqlDatabase.addDatabase("QSQLITE")
        self._conn.setDatabaseName("example.db")

        self._driver = self._conn.driver()
        print("Database Driver: %s" % self._conn.driverName())

        if not self._conn.open():
            QMessageBox.critical(None, "Cannot open database",
                                 "Unable to establish a database connection.\n"
                                 "This example needs SQLite support. Please read the Qt SQL "
                                 "driver documentation for information how to build it.\n\n"
                                 "Click Cancel to exit.",
                                 QMessageBox.Cancel)
            return None
        print("DB Connection established")
        return self._conn

    def get_connection(self):
        if self._conn is None:
            self._conn = QSqlDatabase.addDatabase('QSQLITE')
            self._conn.setDatabaseName("example.db")
            self._conn.open()
        return self._conn

    def close(self):
        if self._conn is not None:
            self._conn.close()

    def debug(self, query: QSqlQuery):
        if query.lastError().type() == QSqlError.NoError:
            print("Query OK: %s " % query.lastQuery())
        else:
            print("Query Error: %s [%s]" % (query.lastError().text(), query.lastQuery()))