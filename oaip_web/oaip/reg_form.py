from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)

from oaip_web.oaip.connect_db import ConnectDB
from oaip_web.oaip.validators import validate_login, validate_password


class WidgetReg(QWidget):
    """Форма регистрации."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Регистрация")
        self.resize(500, 300)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Регистрация"))

        form = QFormLayout()
        self.login = QLineEdit()
        self.login.setPlaceholderText("Придумайте логин")
        # Убедимся, что ввод логина виден (нормальный режим отображения)
        self.login.setEchoMode(QLineEdit.EchoMode.Normal)
        # Включаем кнопку очистки поля для удобства
        try:
            self.login.setClearButtonEnabled(True)
        except Exception:
            pass
        self.parol = QLineEdit()
        self.parol.setPlaceholderText("Придумайте пароль")
        self.parol.setEchoMode(QLineEdit.EchoMode.Password)
        try:
            self.parol.setClearButtonEnabled(True)
        except Exception:
            pass

        form.addRow("Логин", self.login)
        form.addRow("Пароль", self.parol)
        layout.addLayout(form)

        self.vvod = QPushButton("Зарегистрироваться")
        self.quit = QPushButton("Назад")
        layout.addWidget(self.vvod)
        layout.addWidget(self.quit)

        self.vvod.clicked.connect(self.vvod_clicked)

    def showEvent(self, event):
        """При показе формы — ставим фокус на поле логина."""
        super().showEvent(event)
        self.login.setFocus()

    def closeEvent(self, event):
        """При попытке закрыть форму — прячем её вместо полного закрытия приложения."""
        self.hide()
        event.ignore()

    def vvod_clicked(self):
        login = self.login.text().strip()
        parol = self.parol.text().strip()

        if not login or not parol:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        # Валидация логина/пароля перед регистрацией
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
            db.cur.execute("SELECT login FROM user WHERE login = %s", (login,))
            exists = db.cur.fetchone()

            if exists:
                QMessageBox.warning(self, "Ошибка", "Такой пользователь уже есть")
            else:
                db.cur.execute(
                    "INSERT INTO user (login, parol) VALUES (%s, %s)",
                    (login, parol),
                )
                db.con.commit()
                QMessageBox.information(self, "Уведомление", "Вы зарегистрированы")
                self.login.clear()
                self.parol.clear()
        except Exception as e:
            db.con.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка регистрации:\n{e}")
        finally:
            db.close()


if __name__ == "__main__":
    import sys

    from oaip_web.oaip.control_win import run_app

    sys.exit(run_app())
