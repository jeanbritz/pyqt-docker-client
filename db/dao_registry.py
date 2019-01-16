from PyQt5.QtSql import QSqlDatabase, QSqlQuery


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
            query.exec_("create table " + self.TABLE_NAME + "("
                        "reg_id int primary key, "
                        "reg_name varchar(32),"
                        "reg_hostname varchar(128))")

    def insert_registry(self, name, hostname) -> int:
        """
        Insert registry record into table
        :param name: - Name of registry
        :param hostname: - Hostname of registry (e.g. localhost:5000)
        :return: Last insert's id columns value (primary key value)

        insert into docker_reg_registry values (0, 'Local VM', 'localhost:5000')
        """
        query = QSqlQuery(self._conn)
        query.prepare("insert into " + self.TABLE_NAME + " (reg_name, reg_hostname) values (:name, :hostname)")
        query.bindValue(":name", name)
        query.bindValue(":hostname", hostname)
        query.exec()
        return query.lastInsertId()

    def list(self) -> dict:
        """
        Returns list of all registries
        :return: dict - key is the registry name and value is the hostname
        """
        result = {}
        query = QSqlQuery(self._conn)
        query.exec("select * from " + self.TABLE_NAME)
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
        query.exec_("drop table " + self.TABLE_NAME)
