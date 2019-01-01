from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class DatabaseConnection:

    def __init__(self):
        self._create_connection()

    def _create_connection(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('docker.db')
        if not self.db.open():
            QMessageBox.critical(None, "Cannot open database",
                                 "Unable to establish a database connection.\n"
                                 "This example needs SQLite support. Please read the Qt SQL "
                                 "driver documentation for information how to build it.\n\n"
                                 "Click Cancel to exit.",
                                 QMessageBox.Cancel)
            return None
        return True

    def create_docker_daemon_table(self, drop_first=False):
        query = QSqlQuery(self.db)
        if drop_first:
            query.exec_("drop table docker_daemons")

        query.exec_("create table docker_daemons(id int primary key, "
                    "hostname varchar(20), port integer )")
        query.exec_("insert into docker_daemons values (0, 'localhost', 2376)")
        return self.db.commit()

    def get_connection(self):
        return self.db

    def get_docker_daemons(self):
        result = []
        query = QSqlQuery(self.db)
        query.exec("select * from docker_daemons")
        rec = query.record()
        while query.next():
           result.append((query.value(rec.indexOf("id")),
                          query.value(rec.indexOf("hostname")),
                          query.value(rec.indexOf("port"))))
        return result