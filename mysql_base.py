from mysql.connector import connect
from mysql.connector import MySQLConnection
from mysql.connector import ProgrammingError


# DB connection configs
_DB_HOST = "address"
_DB_LOGIN = "login"
_DB_PASSWORD = "password"
_DB_NAME = "dbname"

# SQL installing script
_CREATE_SQL_SCRIPT = '''
    CREATE TABLE users (
        id INTEGER AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        surname VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
    );
'''

class MySQLBase:

    # constructor
    def __init__(self):
        self._init_db()

    # create connection
    def open_connection(self) -> MySQLConnection:
        return connect(host = _DB_HOST, user = _DB_LOGIN, passwd = _DB_PASSWORD, database = _DB_NAME)
    
    # init db
    def _init_db(self) -> None:
        try:
            connection = self.open_connection()
            connection.close()
        except ProgrammingError as e:
            if e.errno == 1049:
                # create db
                connection = connect(host = _DB_HOST, user = _DB_LOGIN, passwd = _DB_PASSWORD)
                cursor = connection.cursor()

                cursor.execute(f"CREATE DATABASE {self.db}")

                cursor.close()
                connection.close()

                # create tables
                connection = self.open_connection()
                cursor = connection.cursor()

                cursor.execute(_CREATE_SQL_SCRIPT)

                cursor.close()
                connection.close()
