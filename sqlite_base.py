import sqlite3
from os.path import exists

# file where will be saved db
_DB_FILE_NAME = "Some.db"

# SQL installing script
_CREATE_SQL_SCRIPT = '''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255) NOT NULL,
        surname VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL
    );
'''

# class for represent base model for sqlite3 connection
class SQLiteBase:
    connection: sqlite3.Connection

    # service methods
    def __init__(self) -> None:
        if not exists(_DB_FILE_NAME):
            self._init_db()

    def open_connection(self) -> None:
        self.connection = sqlite3.connect(_DB_FILE_NAME)

    def close_connection(self) -> None:
        self.connection.close()

    # run only when file is not found in fs. This run sql script for create tables in db
    def _init_db(self) -> None:
        self.open_connection()

        sql_script = _CREATE_SQL_SCRIPT
        self.connection.executescript(sql_script)
        self.connection.commit()

        self.close_connection()