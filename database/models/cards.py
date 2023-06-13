# Python
import datetime
# Local
from database.core import Connection
from database.models.accounts import Account

class Card:
    # Object from db. Cards.
    id:int
    number: str 
    cvv: str
    date_end: datetime.datetime
    account: Account
    is_active: bool
    pin: str

    @staticmethod
    def create(number:str, cvv:str, date_end:datetime, account:str, is_active:bool, pin:str, conn:Connection):
        # Вставка новой записи в таблицу 'cards'.
        with conn.cursor() as cur:
            cur.execute(f"""
                    INSERT INTO accounts (number, owner, balance, type_)
                    VALUES ('{number}', '{cvv}', '{date_end}', '{account.id}','{is_active}', '{pin}')
                    """)
    @staticmethod
    def select(conn:Connection, request:str, filter_by:str = None, order_by:str = None): # Функция взятия значения из таблицы 'users'.
        result = f"SELECT {request} FROM cards"
        # Провериям есть ли условие.
        if filter_by:
            result += f" WHERE {filter_by}"
        if order_by:
            result += f" ORDER BY {order_by}"
        with conn.cursor() as cur:  # Получение курсора.
            cur.execute(result)  # Выполнение запроса.
            rows = cur.fetchall()  # Получение всех результатов.
            for row in rows:
                print(row)  # Вывод строки результата.
                
    @staticmethod
    def update(conn:Connection, column_name: str, new_value: str, filter_by: str):
        result = f"UPDATE cards SET {column_name} = '{new_value}' WHERE {filter_by}"
        with conn.cursor() as cur:
            cur.execute(result)

    @staticmethod
    def delete(conn:Connection, filter_by:str):
        result = f"DELETE FROM cards WHERE {filter_by}"
        with conn.cursor() as cur:
            cur.execute(result)
    
    @staticmethod
    def filter(conn: Connection, **kwargs:dict[str, any]) -> 'Card':
        condition: list[str] = []
        for i in kwargs:
            if isinstance(kwargs[i], str):
                condition.append(f"{i}='{kwargs[i]}'")
            condition.append(f'{i}={kwargs[i]}')
        res = f"""SELECT * FROM cards WHERE {condition}"""
        with conn.cursor() as cur:
            if len(condition) > 1:
                res += f""" AND {condition[1:]}"""
            cur.execute(res)
        return cur.fetchone()
            
    @staticmethod
    def all(conn:Connection):
        res = "SELECT * FROM cards"
        with conn.cursor() as cur:
            cur.execute(res)
            return cur.fetchall()
            
    @staticmethod
    def join(conn:Connection, table: str, **kwargs:dict[str,any]) -> 'Card':
        condition: list[str] = []
        for i in kwargs:
            condition.append(i)
        with conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM cards INNER JOIN {table} ON cards.{condition} = {table}.{condition} """)
            return cur.fetchone()