import sqlite3
from os.path import exists
from typing import Union


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
    def __init__(self) -> None:
        if not exists(_DB_FILE_NAME):
            self._init_db()
    
    def connection(self, func: callable) -> Union[list, None]:
        def wrapper(*args, **kwargs):
            connection = sqlite3.connect(_DB_FILE_NAME)

            result = func(*args, **kwargs, con=connection)

            connection.close()
            return result
        return wrapper

    # run only when file is not found in fs. This run sql script for create tables in db
    def _init_db(self) -> None:
        connection = sqlite3.connect(_DB_FILE_NAME)

        sql_script = _CREATE_SQL_SCRIPT
        connection.executescript(sql_script)
        connection.commit()

        connection.close()