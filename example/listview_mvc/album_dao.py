from PyQt5.QtSql import QSqlQuery
from example.listview_mvc import Album, DbManager


class AlbumDao:
    TABLE_NAME = 'albums'

    def __init__(self, dbm: DbManager = None) -> None:
        super().__init__()
        self._dbm: DbManager = dbm
        self._conn = dbm.get_connection()

    def init(self) -> bool:
        """
        Initialise Albums table.
        It creates the table if it does not exists yet
        :return: bool - initialization was successful, else false if initialization were unsuccessful
        """
        if self.TABLE_NAME not in self._conn.tables():
            query = QSqlQuery(self._conn)
            return query.exec_("create table %s (id integer primary key autoincrement, name text)" % self.TABLE_NAME)

        return True

    def create_album(self, album: Album) -> Album:
        """
        Creates a new album entry into the table
        :param album: Data to be inserted as an entry into the table
        :return: Newly inserted album entry
        """
        query = QSqlQuery(self._conn)
        query.prepare("insert into %s (name) values (:name)" % self.TABLE_NAME)
        query.bindValue(":name", album.name)
        query.exec_() # Bound values are replaced with proper values and executed
        self._dbm.debug(query)
        # Grab the last id before finish() is called, otherwise it is lost
        last_id = query.lastInsertId()
        album._id = last_id
        query.finish()
        return album

    def albums(self) -> list:
        """
        Returns list of all albums
        :return: list of albums
        """
        result = []
        query = QSqlQuery(self._conn)
        query.exec("select * from %s" % self.TABLE_NAME)
        self._dbm.debug(query)
        rec = query.record()
        while query.next():
            album = Album()
            album._id = query.value(rec.indexOf("id"))
            album._name = query.value(rec.indexOf("name"))
            result.append(album)
        return result

    def read_album(self, album_id: int) -> Album:
        pass

    def update_album(self, album: Album) -> bool:
        """
        Updates existing entry of Album record
        :param album: Record with updated data
        :return: bool - true if operation was successful, else false if operation was unsuccessful
        """
        query = QSqlQuery(self._conn)
        query.prepare("update %s set name = :name where id = :id" % self.TABLE_NAME)
        query.bindValue(":name", album.name)
        query.bindValue(":id", album.id)
        result = query.exec_()  # Bound values are replaced with proper values and executed
        self._dbm.debug(query)
        query.finish()
        return result

    def delete_album(self, album) -> bool:
        """
        Deletes a specific album
        :param album: Album to delete (needs the id to be specified at least)
        :return: bool - true - operation was successful, else operation unsuccessful
        """
        query = QSqlQuery(self._conn)
        query.prepare("delete from %s where id = :id" % self.TABLE_NAME)
        query.bindValue(":id", album.id)
        result = query.exec_()  # Bound values are replaced with proper values and executed
        self._dbm.debug(query)
        query.finish()
        return result

    def drop(self) -> bool:
        """
        Drop all tables associated with this DAO
        :return: bool - true if operation was successful else false if operation was unsuccessful
        """
        query = QSqlQuery(self._conn)
        return query.exec_("drop table %s" % self.TABLE_NAME)
