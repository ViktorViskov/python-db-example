from typing import Union

from data_models import User
from sqlite_base import SQLiteBase


class DbUserManager(SQLiteBase):
    # options
    table_name = "users"

    def __init__(self) -> None:
        super().__init__()

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
        connection = self.open_connection()

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

        connection.execute(
            sql_querry, (u.name, u.surname, u.email,))
        
        connection.commit()
        connection.close()

    def get_all_users(self) -> list[User]:
        connection = self.open_connection()
        cursor = connection.cursor()

        cursor.execute(f"SELECT id, name, surname, email FROM {self.table_name}")
        rows = cursor.fetchall()
        
        connection.close()
        return [self._parse_user(item) for item in rows]
    
    def get_user_by_id(self, id:int) -> Union[User, None]:
        connection = self.open_connection()
        cursor = connection.cursor()

        cursor.execute(f"SELECT id, name, surname, email FROM {self.table_name} WHERE id = ?", (id,))
        out = cursor.fetchone()

        connection.close()
        return self._parse_user(out)
    
    def update_user(self, u: User) -> None:
        connection = self.open_connection()

        sql_querry = f'''
        UPDATE {self.table_name} 
        SET name = ?, surname = ?, email = ?
        WHERE id = ?;
        '''
        connection.execute(
            sql_querry, (u.name, u.surname, u.email, u.id,))
        
        connection.commit()
        connection.close()

    def delete_user(self, u: User) -> None:
        connection = self.open_connection()

        sql_script = f'''
        DELETE FROM {self.table_name} WHERE id = ?;
        '''
        connection.execute(sql_script, (u.id,))

        connection.commit()
        connection.close()

