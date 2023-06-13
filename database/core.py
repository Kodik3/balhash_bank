import psycopg2

class Connection:
    # Connection with PostgreSQL.

    def __new__(cls, *args, **kwargs):
        # Проверяем, существует ли уже экземпляр класса Connection в атрибуте 'instance'
        if not hasattr(cls, 'instance'):
        # Если экземпляр не существует, создаем новый экземпляр класса
            cls.instance = super(Connection, cls).__new__(cls)
        # Возвращаем экземпляр класса
        return cls.instance

    def __init__(self, host: str, port: int, user: str, password: str, dbname: str) -> None:
        # Инициализация параметров подключения
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.conn = None
        try:
            # Установление подключения к базе данных
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                dbname=self.dbname
            )
            self.conn.autocommit = True
            print('[SUCCESS] Connection is successful!')
        except Exception as e:
            print(e)
            print("[ERROR] CONNECTION ERROR!")
            
    def create_tables(self):
        try:
            with self.conn.cursor() as cur:
                # Создание таблиц в базе данных, если они еще не существуют
                cur.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS users(
                        id SERIAL PRIMARY KEY,
                        first_name VARCHAR(200) NOT NULL,
                        last_name VARCHAR(200) NOT NULL,
                        date_of_birth DATE NOT NULL,
                        iin VARCHAR(12) UNIQUE NOT NULL CHECK(LENGTH(iin)=12),
                        phone_number VARCHAR(10) UNIQUE NOT NULL CHECK(LENGTH(phone_number)=10)
                    );
                    CREATE TABLE IF NOT EXISTS accounts(
                        id SERIAL PRIMARY KEY,
                        number VARCHAR(20) UNIQUE NOT NULL CHECK(LENGTH(number)=20),
                        owner_id INTEGER NOT NULL UNIQUE REFERENCES users(id),
                        balance DECIMAL CHECK(balance > -3000) DEFAULT(0),
                        type VARCHAR(4)
                    );
                    CREATE TABLE IF NOT EXISTS cards(
                        id SERIAL PRIMARY KEY,
                        number VARCHAR(16) UNIQUE NOT NULL CHECK(LENGTH(number)=16),
                        account_id INTEGER NOT NULL REFERENCES accounts(id),
                        cvv VARCHAR(3) UNIQUE NOT NULL CHECK(LENGTH(cvv)=3),
                        date_end DATE DEFAULT(NOW() + INTERVAL '3 YEAR'),
                        is_active BOOLEAN DEFAULT('true'),
                        pin VARCHAR(4) NOT NULL CHECK(LENGTH(pin)=4)
                    );
                    '''
                )
        except:
            print("[ERROR] CAN't CREATE TABLES!")
    
    def cursor(self):
        # Получение курсора для выполнения запросов
        return self.conn.cursor()

