# Python
import datetime
# Local
from database.core import Connection

class User:
    # Object from db. User.
    id: int
    first_name: str
    last_name: str
    date_of_birth: datetime.datetime
    iin: str
    phone_number: str
    
    @staticmethod
    def create(first_name: str, last_name: str, date_of_birth: datetime, iin: str, phone_number: str, conn: Connection):
        # Вставка новой записи в таблицу 'users'.
        with conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO users (first_name, last_name, date_of_birth, iin, phone_number)
                VALUES ('{first_name}', '{last_name}', '{date_of_birth}', '{iin}', '{phone_number}')
                """)

    @staticmethod
    def select(conn:Connection, request:str = "*", filter_by:str = None, order_by:str = None, join_table:str = None, column_join:str = None): # Функция взятия значения из таблицы 'users'.
        result = f"SELECT {request} FROM users"
        # Провериям есть ли условие.
        if filter_by:
            result += f" WHERE {filter_by}"
        if order_by:
            result += f" ORDER BY {order_by}"
        if join_table and column_join:
            result += f" INNER JOIN {join_table} ON users.{column_join} = {join_table}.{column_join}"
        with conn.cursor() as cur:
            cur.execute(result)
            rows = cur.fetchall()
            for row in rows:
                print(row)
                
    @staticmethod
    def update(conn:Connection, column_name: str, new_value: str, filter_by: str):
        result = f"UPDATE users SET {column_name} = '{new_value}' WHERE {filter_by}"
        with conn.cursor() as cur:
            cur.execute(result)

    @staticmethod
    def delete(conn:Connection, filter_by:str):
        result = f"DELETE FROM users WHERE {filter_by}"
        with conn.cursor() as cur:
            cur.execute(result)

    @staticmethod
    def get(conn:Connection, **kwargs:dict[str, any]) -> "User":
        condition: list[str] = []
        for i in kwargs:
            if isinstance(kwargs[i], str):
                condition.append(f"{i}='{kwargs[i]}'")
            condition.append(f'{i}={kwargs[i]}')
        with conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM users WHERE {' AND '.join(condition)}""")
        return cur.fetchone()

    @staticmethod
    def filter(conn: Connection, **kwargs:dict[str, any]) -> 'User':
        condition: list[str] = []
        for i in kwargs:
            if isinstance(kwargs[i], str):
                condition.append(f"{i}='{kwargs[i]}'")
            condition.append(f'{i}={kwargs[i]}')
        res = f"""SELECT * FROM users WHERE {condition}"""
        with conn.cursor() as cur:
            if len(condition) > 1:
                res += f""" AND {condition[1:]}"""
            cur.execute(res)
        return cur.fetchall()
            
    @staticmethod
    def all(conn:Connection):
        res = "SELECT * FROM users"
        with conn.cursor() as cur:
            cur.execute(res)
            return cur.fetchall()
            
    @staticmethod
    def join(conn:Connection, table: str, **kwargs:dict[str,any]) -> 'User':
        condition: list[str] = []
        for i in kwargs:
            condition.append(i)
        with conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM users INNER JOIN {table} ON users.{condition} = {table}.{condition} """)
            return cur.fetchall()
            