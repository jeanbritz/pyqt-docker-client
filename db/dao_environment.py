from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from db.db_constant import DbConstant
from environment.model import DEnvEnvironment, DEsEnvSetting


class DaoEnvironment:

    TABLE_NAME = 'd_env_environment'
    LINK_TABLE_NAME = "d_es_env_setting"

    def __init__(self, conn: QSqlDatabase = None) -> None:
        super().__init__()
        self._conn = conn

    def init(self):
        """
        Initialise Environment table.
        It creates the table if it does not exists yet
        :return: None
        """
        if self.TABLE_NAME not in self._conn.tables():
            query = QSqlQuery(self._conn)
            a = query.exec_(DbConstant.CREATE_TABLE_ENVIRONMENT % self.TABLE_NAME)
            b = query.exec_(DbConstant.CREATE_TABLE_ENVIRONMENT_SETTING % self.LINK_TABLE_NAME)
            query.finish()
            return a and b
        return True

    def environments(self) -> list:
        """
        Returns list of all environment plus their environment settings
        :return: dict - key is the environment name and the values are a dict of environment settings
        """
        result = []
        query = QSqlQuery(self._conn)
        query.exec(DbConstant.SELECT_STAR % self.TABLE_NAME)
        rec = query.record()
        while query.next():
            env_id = query.value(rec.indexOf("env_id"))
            env_name = query.value(rec.indexOf("env_name"))
            env_settings = self.environment_settings(DEnvEnvironment(_id=env_id))
            result.append(DEnvEnvironment(_id=env_id, name=env_name, settings=env_settings))
        return result

    def create_env(self, env: DEnvEnvironment = None) -> DEnvEnvironment:
        """
        Create environment record in table
        :param env: - Name of environment
        :return: Environment Model Object
        """
        if env is not None:
            query = QSqlQuery(self._conn)
            query.prepare(DbConstant.INSERT_ENVIRONMENT % self.TABLE_NAME)
            query.bindValue(":name", env.name)
            query.exec_()
            # Grab the last id before finish() is called, otherwise it is lost
            last_id = query.lastInsertId()
            query.finish()
            return DEnvEnvironment(_id=last_id, name=env.name)

    def update_env(self, env: DEnvEnvironment) -> bool:
        """
        Update existing Environment record in table
        :param env: - Reference to existing Environment record
        :return: true - update was succeesful, false - update was unsuccessful
        """

        query = QSqlQuery(self._conn)
        query.prepare("update %s set env_name = :name where env_id = :id" % self.TABLE_NAME)
        query.bindValue(":name", env.name)
        query.bindValue(":id", env.id)
        result = query.exec_()
        query.finish()
        return result

    def delete_env(self, env: DEnvEnvironment) -> bool:
        """
        Deletes Environment record in table
        :param env: Reference to Environment reocrd
        :return: true - delete was successful, false - delete was unsuccessful
        """
        query = QSqlQuery(self._conn)
        query.prepare("delete from %s where env_id = :id" % self.TABLE_NAME)
        query.bindValue(":id", env.id)
        result = query.exec_()
        query.finish()
        return result

    def create_env_setting(self, env: DEnvEnvironment = None, setting: tuple = None) -> DEsEnvSetting:
        """
        Create environment setting
        :param env: - Reference of environment
        :param setting: - Tuple that is a name-value pair (e.g. ('DOCKER_HOST', 'tcp://localhost:2376'))
        :return: Environment Setting Model Object
        """
        query = QSqlQuery(self._conn)
        query.prepare(DbConstant.INSERT_ENVIRONMENT_SETTING % self.LINK_TABLE_NAME)
        query.bindValue(":name", setting[0])
        query.bindValue(":value", setting[1])
        query.bindValue(":env_id", env.id)
        success = query.exec_()
        query.finish()

        if success:
            return DEsEnvSetting(env_id=env.id, name=setting[0], value=setting[1])

    def drop(self) -> None:
        """
        Drop all tables associated with this DAO
        :return: None
        """
        query = QSqlQuery(self._conn)
        query.exec_(DbConstant.DROP_TABLE % self.LINK_TABLE_NAME)
        query.exec_(DbConstant.DROP_TABLE % self.TABLE_NAME)

    def environment_settings(self, env: DEnvEnvironment = None) -> list:
        """
        Returns a dictionary of environmental settings for a specific environment
        :param env: Environment Reference
        :return: List of Environment Settings
        """
        result = []
        query = QSqlQuery(self._conn)
        query.prepare(DbConstant.SELECT_SETTINGS_BY_ENV % self.LINK_TABLE_NAME)
        query.bindValue(':env_id', env.id)
        query.exec_()
        rec = query.record()
        while query.next():
            name = query.value(rec.indexOf("es_name"))
            value = query.value(rec.indexOf("es_value"))
            result.append(DEsEnvSetting(env_id=env.id, name=name, value=value))
        return result
