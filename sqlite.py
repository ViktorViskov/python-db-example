import sqlite3
from typing import Union
from os.path import exists
from dataclasses import dataclass


# installing script
CREATE_SQL_SCRIPT = '''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255) NOT NULL,
        surname VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL
    );
'''

# model for user object
@dataclass
class User:
    id:int
    name:str
    surname:str
    email:str

class SQLiteContext:
    _file_name: str
    connection: sqlite3.Connection

    # service methods
    def __init__(self, db_file_name) -> None:
        self._file_name = db_file_name

        if not exists(self._file_name):
            self._init_db()

    def open_connection(self) -> None:
        self.connection = sqlite3.connect(self._file_name)

    def close_connection(self) -> None:
        self.connection.close()

    def _init_db(self) -> None:
        self.open_connection()

        sql_script = CREATE_SQL_SCRIPT
        self.connection.executescript(sql_script)
        self.connection.commit()

        self.close_connection()


class UserManager(SQLiteContext):
    # options
    db_file_name = "Some.db"
    table_name = "users"

    def __init__(self) -> None:
        super().__init__(self.db_file_name)

    # method for parsing user from db out data
    def _parse_user(self, db_out:list) -> Union[User, None]:
        '''IMPORTANT: Before use method you must check matching between order of arguments in data object and SQL query'''
        user = None

        if db_out:
            user = User(
                id=db_out[0], 
                name=db_out[1], 
                surname=db_out[2], 
                email=db_out[3])
            
        return user
    
    def add_user(self, u: User) -> None:
        self.open_connection()

        sql_querry = f'''
        INSERT INTO {self.table_name} (
            name,
            surname,
            email
        )
        VALUES (
            ?,
            ?,
            ?
        )
        '''

        self.connection.execute(
            sql_querry, (u.name, u.surname, u.email,))
        
        self.connection.commit()
        self.close_connection()

    def get_all_users(self) -> list[User]:
        self.open_connection()
        cursor = self.connection.cursor()

        cursor.execute(f"SELECT id, name, surname, email FROM {self.table_name}")
        rows = cursor.fetchall()

        return [self._parse_user(item) for item in rows]
    
    def get_user_by_id(self, id:int) -> Union[User, None]:
        self.open_connection()
        cursor = self.connection.cursor()

        cursor.execute(f"SELECT id, name, surname, email FROM {self.table_name} WHERE id = ?", (id,))
        out = cursor.fetchone()

        return self._parse_user(out)
    
    def update_user(self, u: User) -> None:
        self.open_connection()

        sql_querry = f'''
        UPDATE {self.table_name} 
        SET name = ?, surname = ?, email = ?
        WHERE id = ?;
        '''
        self.connection.execute(
            sql_querry, (u.name, u.surname, u.email, u.id,))
        
        self.connection.commit()
        self.close_connection()

    def delete_user(self, u: User) -> None:
        self.open_connection()

        sql_script = f'''
        DELETE FROM {self.table_name} WHERE id = ?;
        '''
        self.connection.execute(sql_script, (u.id,))

        self.connection.commit()
        self.close_connection()

