from mysql.connector import connect, Error


class ConnectDB:
    """Подключение к базе данных услуги."""

    def __init__(self):
        self.con = None
        self.cur = None
        self.connection()

    def connection(self):
        try:
            self.con = connect(
                user="root",
                host="localhost",
                db="услуги",
                password="[REDACTED]",
            )
            self.cur = self.con.cursor(buffered=True)
            print("Соединение установлено")
        except Error as e:
            print("Ошибка подключения:", e)

    def close(self):
        if self.cur:
            self.cur.close()
        if self.con and self.con.is_connected():
            self.con.close()
