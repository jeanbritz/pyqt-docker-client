from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from db.db_constant import DbConstant


class DaoRegistry:
    TABLE_NAME = 'd_reg_registry'

    def __init__(self, conn: QSqlDatabase = None) -> None:
        super().__init__()
        self._conn = conn

    def init(self) -> None:
        """
        Initialise Registry table.
        It creates the table if it does not exists yet
        :return: None
        """
        if self.TABLE_NAME not in self._conn.tables():
            query = QSqlQuery(self._conn)
            query.exec_(DbConstant.CREATE_TABLE_REGISTRY % self.TABLE_NAME)

    def insert_registry(self, name, hostname) -> int:
        """
        Insert registry record into table
        :param name: - Name of registry
        :param hostname: - Hostname of registry (e.g. localhost:5000)
        :return: Last insert's id columns value (primary key value)

        insert into docker_reg_registry values (0, 'Local VM', 'localhost:5000')
        """
        query = QSqlQuery(self._conn)
        query.prepare(DbConstant.INSERT_REGISTRY % self.TABLE_NAME)
        query.bindValue(":name", name)
        query.bindValue(":hostname", hostname)
        query.exec_()
        # Grab the last id before finish() is called, otherwise it is lost
        last_id = query.lastInsertId()
        query.finish()
        return last_id

    def list(self) -> dict:
        """
        Returns list of all registries
        :return: dict - key is the registry name and value is the hostname
        """
        result = {}
        query = QSqlQuery(self._conn)
        query.exec(DbConstant.SELECT_STAR % self.TABLE_NAME)
        rec = query.record()
        while query.next():
            # reg_id = query.value(rec.indexOf("reg_id"))
            reg_name = query.value(rec.indexOf("reg_name"))
            reg_hostname = query.value(rec.indexOf("reg_hostname"))
            result[reg_name] = reg_hostname
        return result

    def drop(self) -> None:
        """
        Drop all tables associated with this DAO
        :return: None
        """
        query = QSqlQuery(self._conn)
        query.exec_(DbConstant.DROP_TABLE % self.TABLE_NAME)
