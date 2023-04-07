import sqlite3
from sqlite3 import Connection
from os.path import exists


# file where will be saved db
_DB_FILE_NAME = "sqlite.db"

# SQL installing script
with open("install_sqlite.sql", "r") as file:
    _CREATE_SQL_SCRIPT = file.read()

# class for represent base model for sqlite3 connection
class SQLiteBase:

    # service methods
    def __init__(self) -> None:
        if not exists(_DB_FILE_NAME):
            self._init_db()

    def open_connection(self) -> Connection:
        return sqlite3.connect(_DB_FILE_NAME)

    # run only when file is not found in fs. This run sql script for create tables in db
    def _init_db(self) -> None:
        connection = self.open_connection()

        connection.executescript(_CREATE_SQL_SCRIPT)
        connection.commit()

        connection.close()