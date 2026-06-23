from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)

from oaip_web.oaip.connect_db import ConnectDB
from oaip_web.oaip.validators import validate_login, validate_password


class WidgetAvt(QWidget):
    """Форма авторизации."""

    def __init__(self, on_success=None, parent=None):
        super().__init__(parent)
        self.on_success = on_success
        self.setWindowTitle("Авторизация")
        self.resize(500, 300)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Авторизация"))

        form = QFormLayout()
        self.login = QLineEdit()
        self.login.setPlaceholderText("Введите логин")
        self.parol = QLineEdit()
        self.parol.setPlaceholderText("Введите пароль")
        self.parol.setEchoMode(QLineEdit.EchoMode.Password)

        form.addRow("Логин", self.login)
        form.addRow("Пароль", self.parol)
        layout.addLayout(form)

        self.vvod = QPushButton("Авторизировать")
        self.quit = QPushButton("Назад")
        layout.addWidget(self.vvod)
        layout.addWidget(self.quit)

        self.vvod.clicked.connect(self.vvod_clicked)
        self.current_login = ""

    def showEvent(self, event):
        """При показе формы — ставим фокус на поле логина."""
        super().showEvent(event)
        self.login.setFocus()

    def closeEvent(self, event):
        """При попытке закрыть форму — прячем её вместо полного закрытия приложения.

        Главный выход остаётся через главное меню или крестик главного окна.
        """
        self.hide()
        event.ignore()

    def vvod_clicked(self):
        login = self.login.text().strip()
        parol = self.parol.text().strip()

        if not login or not parol:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        # Валидация формата логина и пароля перед обращением к БД
        ok, msg = validate_login(login)
        if not ok:
            QMessageBox.warning(self, "Ошибка", msg)
            return

        ok, msg = validate_password(parol)
        if not ok:
            QMessageBox.warning(self, "Ошибка", msg)
            return

        db = ConnectDB()
        if not db.con:
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных")
            return

        try:
            db.cur.execute(
                "SELECT login, parol FROM user WHERE login = %s AND parol = %s",
                (login, parol),
            )
            user = db.cur.fetchone()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка авторизации:\n{e}")
            db.close()
            return

        db.close()

        if user:
            self.current_login = login
            QMessageBox.information(self, "Уведомление", "Вы авторизировались")
            if self.on_success:
                self.on_success(login)
        else:
            QMessageBox.warning(self, "Ошибка", "Некорректный логин или пароль")


if __name__ == "__main__":
    import sys

    from control_win import run_app

    sys.exit(run_app())
