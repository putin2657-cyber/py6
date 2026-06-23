from mysql.connector import connect, Error
import os


class ConnectDB:
    """Подключение к базе данных "услуги".

    Настоятельно рекомендуется задавать параметры подключения через
    переменные окружения (DB_HOST, DB_USER, DB_NAME, DB_PASSWORD) и не хранить
    пароли в репозитории.
    """

    def __init__(self):
        self.con = None
        self.cur = None
        self.connection()

    def connection(self):
        host = os.environ.get("DB_HOST", "localhost")
        user = os.environ.get("DB_USER", "root")
        db = os.environ.get("DB_NAME", "uslugi")
        password = os.environ.get("DB_PASSWORD")

        if not password:
            # Если пароль не задан в окружении, НЕ использовать "жёстко" записанные значения.
            # Выбрана стратегия: вывести предупреждение — лучше явно задать DB_PASSWORD.
            print("Warning: DB_PASSWORD not set in environment. Connection may fail or be insecure.")

        try:
            self.con = connect(
                user=user,
                host=host,
                database=db,
                password=password,
            )
            self.cur = self.con.cursor(buffered=True)
            print("Соединение установлено")
        except Error as e:
            print("Ошибка подключения:", e)

    def close(self):
        if self.cur:
            self.cur.close()
        if self.con and getattr(self.con, "is_connected", lambda: False)():
            self.con.close()
