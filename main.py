# Python
# from decouple import config
import datetime
# Local
from database.core import Connection
from env import *
# Models
from database.models.users import User
from database.models.accounts import Account
from database. models.cards import Card

# Connection
my_connection: Connection = Connection(
    host     = DB_HOST,
    port     = DB_PORT,
    user     = DB_USER,
    password = DB_PASSWORD,
    dbname   = DB_NAME
)


if __name__ == "__main__":
    # Создание таблиц.
    my_connection.create_tables()
    # Создание нового пользователя.
    # User.create(
    #     conn=my_connection,
    #     first_name='Bob',
    #     last_name='Bisics',
    #     date_of_birth=datetime.datetime(year=2005, month=11, day=21),
    #     iin="198276456122",
    #     phone_number='8732323733'
    # )
    # # Обновление значения
    # User.update(conn=my_connection, column_name='first_name', new_value='Sohn', filter_by='id = 1')
    # # Вывод данных из таблицы 'users'.
    # User.select(conn=my_connection,)
    User.filter(conn=my_connection, where="id = 1")
    # User.get(conn=my_connection,id = 1)