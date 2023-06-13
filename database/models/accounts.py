# Python

# Local
from database.core import Connection

class Account:
    # Object from db. Accounts.
    id: int
    number: str 
    owner: str
    balance: str
    type_: str

    @staticmethod
    def create(number:str, owner:str, balance:str, type_:str, conn:Connection):
        # Вставка новой записи в таблицу 'accounts'.
        with conn.cursor() as cur:
            cur.execute(f"""
                    INSERT INTO accounts (number, owner, balance, type_)
                    VALUES ('{number}', '{owner.id}', '{balance}', '{type_}')
                    """)
    @staticmethod
    def select(conn:Connection, request:str, filter_by:str = None, order_by:str = None): # Функция взятия значения из таблицы 'users'.
        result = f"SELECT {request} FROM accounts"
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
        result = f"UPDATE accounts SET {column_name} = '{new_value}' WHERE {filter_by}"
        with conn.cursor() as cur:
            cur.execute(result)

    @staticmethod
    def delete(conn:Connection, filter_by:str):
        result = f"DELETE FROM accounts WHERE {filter_by}"
        with conn.cursor() as cur:
            cur.execute(result)

    @staticmethod
    def filter(conn: Connection, **kwargs:dict[str, any]) -> 'Account':
        condition: list[str] = []
        for i in kwargs:
            if isinstance(kwargs[i], str):
                condition.append(f"{i}='{kwargs[i]}'")
            condition.append(f'{i}={kwargs[i]}')
        res = f"""SELECT * FROM accounts WHERE {condition}"""
        with conn.cursor() as cur:
            if len(condition) > 1:
                res += f""" AND {condition[1:]}"""
            cur.execute(res)
        return cur.fetchone()
            
    @staticmethod
    def all(conn:Connection):
        res = "SELECT * FROM accounts"
        with conn.cursor() as cur:
            cur.execute(res)
            return cur.fetchall()
            
    @staticmethod
    def join(conn:Connection, table: str, **kwargs:dict[str,any]) -> 'Account':
        condition: list[str] = []
        for i in kwargs:
            condition.append(i)
        with conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM accounts INNER JOIN {table} ON accounts.{condition} = {table}.{condition} """)
            return cur.fetchone()