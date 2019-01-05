from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from util.log import Log


class DatabaseConnection:

    def __init__(self):
        self._create_connection()

    def _create_connection(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('docker.db')
        Log.i("Database Driver: %s" % self.db.driverName())
        if not self.db.open():
            QMessageBox.critical(None, "Cannot open database",
                                 "Unable to establish a database connection.\n"
                                 "This example needs SQLite support. Please read the Qt SQL "
                                 "driver documentation for information how to build it.\n\n"
                                 "Click Cancel to exit.",
                                 QMessageBox.Cancel)
            return None
        return True

    def create_tables(self, drop_first=False):
        query = QSqlQuery(self.db)
        if drop_first:
            query.exec_("drop table docker_e_env")
            query.exec_("drop table docker_ev_env_setting")
            query.exec_("drop table docker_av_api_version")
            self.db.commit()

        query.exec_("create table docker_e_env("
                    "e_id int primary key, "
                    "e_name varchar(32))")
        query.exec_("insert into docker_e_env values (0, 'Docker VM')")

        query.exec_("create table docker_ev_env_setting("
                    "ev_name varchar(256),"
                    "ev_value varchar(1024),"
                    "e_id int,"
                    "primary key (e_id, ev_name))")
        query.exec_("insert into docker_ev_env_setting values ('DOCKER_HOST', 'tcp://localhost:2376', 0)")
        query.exec_("insert into docker_ev_env_setting values ('DOCKER_TLS_VERIFY', '', 0)")
        query.exec_("insert into docker_ev_env_setting values ('DOCKER_CERT_PATH', '', 0)")

        query.exec_("create table docker_av_api_version("
                    "av_name varchar(8),"
                    "av_value varchar(8))")
        query.exec_("insert into docker_av_api_version values ('Auto', 'auto')")

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

    def get_environments(self):
        result = {}
        query = QSqlQuery(self.db)
        query.exec("select * from docker_e_env")
        rec = query.record()
        while query.next():
            e_id = query.value(rec.indexOf("e_id"))
            env = query.value(rec.indexOf("e_name"))
            env_values = self._get_env_values(e_id)
            result[env] = env_values
        return result

    def _get_env_values(self, e_id=None):
        result = {}
        query = QSqlQuery(self.db)
        query.prepare("select * from docker_ev_env_setting where e_id = :env")
        query.bindValue(':env', e_id)
        query.exec_()
        rec = query.record()
        while query.next():
            name = query.value(rec.indexOf("ev_name"))
            value = query.value(rec.indexOf("ev_value"))
            result[name] = value
        return result

    def get_api_versions(self):
        result = []
        query = QSqlQuery(self.db)
        query.exec("select * from docker_av_api_version")
        rec = query.record()
        while query.next():
            result.append({'name': query.value(rec.indexOf('av_name')),
                           'value': query.value(rec.indexOf('av_value'))})
        return result