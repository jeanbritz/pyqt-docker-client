from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from db.db_constant import DbConstant


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
            query.exec_(DbConstant.CREATE_TABLE_ENVIRONMENT % self.TABLE_NAME)
            query.exec_(DbConstant.CREATE_TABLE_ENVIRONMENT_SETTING % self.LINK_TABLE_NAME)
            query.finish()

    def list(self) -> dict:
        """
        Returns list of all environment plus their environment settings
        :return: dict - key is the environment name and the values are a dict of environment settings
        """
        result = {}
        query = QSqlQuery(self._conn)
        query.exec(DbConstant.SELECT_STAR % self.TABLE_NAME)
        rec = query.record()
        while query.next():
            env_id = query.value(rec.indexOf("env_id"))
            env_name = query.value(rec.indexOf("env_name"))
            env_values = self._list_env_values(env_id)
            result[env_name] = env_values
        return result

    def insert_env(self, name) -> int:
        """
        Insert environment record in table
        :param name: - Name of environment
        :return: Last insert's id columns value (primary key value)
        """
        query = QSqlQuery(self._conn)
        query.prepare(DbConstant.INSERT_ENVIRONMENT % self.TABLE_NAME)
        query.bindValue(":name", name)
        query.exec_()
        # Grab the last id before finish() is called, otherwise it is lost
        last_id = query.lastInsertId()
        query.finish()
        return last_id

    def insert_env_setting(self, env_id: int = None, setting: tuple = None):
        """
        Insert environment setting
        :param env_id: - Id of environment
        :param setting: - Tuple that is a name-value pair (e.g. ('DOCHER_HOST', 'tcp://localhost:2376'))
        :return: None
        """
        query = QSqlQuery(self._conn)
        query.prepare(DbConstant.INSERT_ENVIRONMENT_SETTING % self.LINK_TABLE_NAME)
        query.bindValue(":name", setting[0])
        query.bindValue(":value", setting[1])
        query.bindValue(":env_id", env_id)
        query.exec_()
        query.finish()

    def drop(self) -> None:
        """
        Drop all tables associated with this DAO
        :return: None
        """
        query = QSqlQuery(self._conn)
        query.exec_(DbConstant.DROP_TABLE % self.LINK_TABLE_NAME)
        query.exec_(DbConstant.DROP_TABLE % self.TABLE_NAME)

    def _list_env_values(self, env_id: int = None) -> dict:
        """
        Returns a dictionary of environmental settings for a specfic environment
        :param env_id: Environment's ID
        :return: dict - key - Environment Setting Name, value - Environment Setting Value
        """
        result = {}
        query = QSqlQuery(self._conn)
        query.prepare(DbConstant.SELECT_SETTINGS_BY_ENV % self.LINK_TABLE_NAME)
        query.bindValue(':env_id', env_id)
        query.exec_()
        rec = query.record()
        while query.next():
            name = query.value(rec.indexOf("es_name"))
            value = query.value(rec.indexOf("es_value"))
            result[name] = value
        return result
