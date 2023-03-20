from typing import Union

from data_models import User
from mysql_base import MySQLBase


class DbUserManager(MySQLBase):
    # options
    table_name = "users"

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
        cursor = connection.cursor()

        sql_querry = f'''
        INSERT INTO {self.table_name} (
            name,
            surname,
            email
        )
        VALUES (
            %s,
            %s,
            %s
        )
        '''

        cursor.execute(
            sql_querry, (u.name, u.surname, u.email,))
        connection.commit()

        cursor.close()
        connection.close()

    def get_all_users(self) -> list[User]:
        connection = self.open_connection()
        cursor = connection.cursor()

        cursor.execute(f"SELECT id, name, surname, email FROM {self.table_name}")
        rows = cursor.fetchall()
        
        cursor.close()
        connection.close()
        return [self._parse_user(item) for item in rows]
    
    def get_user_by_id(self, id:int) -> Union[User, None]:
        connection = self.open_connection()
        cursor = connection.cursor()

        cursor.execute(f"SELECT id, name, surname, email FROM {self.table_name} WHERE id = %s", (id,))
        out = cursor.fetchone()

        connection.close()
        return self._parse_user(out)
    
    def update_user(self, u: User) -> None:
        connection = self.open_connection()
        cursor = connection.cursor()

        sql_querry = f'''
        UPDATE {self.table_name} 
        SET name = %s, surname = %s, email = %s
        WHERE id = %s;
        '''
        cursor.execute(
            sql_querry, (u.name, u.surname, u.email, u.id,))
        connection.commit()
        
        cursor.close()
        connection.close()

    def delete_user(self, u: User) -> None:
        connection = self.open_connection()
        cursor = connection.cursor()

        sql_script = f'''
        DELETE FROM {self.table_name} WHERE id = %s;
        '''
        cursor.execute(sql_script, (u.id,))
        connection.commit()

        cursor.close()
        connection.close()

