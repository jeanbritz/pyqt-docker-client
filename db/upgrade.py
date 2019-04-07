from PyQt5.QtSql import QSqlError

from db import DbManager, DaoEnvironment, DaoRegistry
from environment.model import DEnvEnvironment
from util import Log


class Upgrade:

    def __init__(self) -> None:
        super().__init__()

        self._db_manager = DbManager()
        # Create database if it does not exists yet (Currently working just with SQLite3 database)
        self._conn = self._db_manager.create()

        # Creating DAO objects
        self._dao_environment = DaoEnvironment(self._conn)
        self._dao_registry = DaoRegistry(self._conn)

    def upgrade(self):
        """
        Upgrade script for now
        :return:
        """
        try:
            Log.i("Upgrade Started")
            self._dao_environment.drop()

            self._dao_environment.init()
            self.handle_sql_error(self._conn.lastError())

            # Insert Local VM environment
            env = self._dao_environment.create_env(DEnvEnvironment(name='Local VM'))
            if env is not None:
                self._dao_environment.create_env_setting(env, ('DOCKER_HOST', 'tcp://10.0.0.13:2375'))
                self._dao_environment.create_env_setting(env, ('DOCKER_TLS_VERIFY', ''))
                self._dao_environment.create_env_setting(env, ('DOCKER_CERT_PATH', ''))

            # Insert Linux environment
            env = self._dao_environment.create_env(DEnvEnvironment(name='Linux'))
            if env is not None:
                self._dao_environment.create_env_setting(env, ('DOCKER_HOST', 'unix:///var/run/docker.sock'))
                self._dao_environment.create_env_setting(env, ('DOCKER_TLS_VERIFY', ''))
                self._dao_environment.create_env_setting(env, ('DOCKER_CERT_PATH', ''))

            self._dao_registry.drop()
            self._dao_registry.init()

            # Insert Local Docker Registry entry
            registry_id = self._dao_registry.insert_registry('Local VM', 'localhost:5000')

            # Commit all changes to database

            self.handle_sql_error(self._conn.lastError())
        except QSqlError as e:
            self.handle_sql_error(e)
        # Close database connection
        self._conn.close()

    def handle_sql_error(self, error: QSqlError = None):
        """
        Types:
        ConnectionError = 1
        NoError = 0
        StatementError = 2
        TransactionError = 3
        UnknownError = 4
        :param error:
        :return:
        """
        if error is not None:
            if error.type() == QSqlError.NoError:
                pass
            elif error.type() == QSqlError.ConnectionError:
                Log.e("SQL Error [Connection Error] - %s" % error.text())
            elif error.type() == QSqlError.StatementError:
                Log.e("SQL Error [Statement Error] - %s" % error.text())
            elif error.type() == QSqlError.TransactionError:
                Log.e("SQL Error [Transaction Error] - %s" % error.text())
            else:
                Log.e("SQL Error [Unknown Error] - %s" % error.text())
