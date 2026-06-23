from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QDialog, QLineEdit, QFormLayout
)

from oaip_web.oaip.connect_db import ConnectDB


class EditTableWindow(QMainWindow):
    """Форма 2: редактирование данных таблицы user."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактирование данных")
        self.resize(800, 600)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Редактировать")
        self.btn_delete = QPushButton("Удалить")
        self.btn_refresh = QPushButton("Обновить")
        self.btn_back = QPushButton("Назад")

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_back)
        layout.addLayout(btn_layout)

        self.btn_add.clicked.connect(self.add_record)
        self.btn_edit.clicked.connect(self.edit_record)
        self.btn_delete.clicked.connect(self.delete_record)
        self.btn_refresh.clicked.connect(self.load_data)

        self.db = None

    def _connect_db(self):
        if self.db:
            self.db.close()
        self.db = ConnectDB()
        return self.db.con is not None

    def showEvent(self, event):
        super().showEvent(event)
        self.load_data()

    def load_data(self):
        if not self._connect_db():
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных")
            return

        try:
            self.db.cur.execute("SELECT login, parol FROM user")
            rows = self.db.cur.fetchall()

            self.table.setRowCount(0)
            self.table.setColumnCount(2)
            self.table.setHorizontalHeaderLabels(["Login", "Parol"])

            if rows:
                self.table.setRowCount(len(rows))
                for i, (login, parol) in enumerate(rows):
                    self.table.setItem(i, 0, QTableWidgetItem(str(login)))
                    self.table.setItem(i, 1, QTableWidgetItem(str(parol)))
                self.table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных:\n{e}")

    def add_record(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить запись")
        layout = QFormLayout(dialog)

        login_input = QLineEdit()
        parol_input = QLineEdit()
        login_input.setPlaceholderText("Введите логин")
        parol_input.setPlaceholderText("Введите пароль")

        layout.addRow("Login", login_input)
        layout.addRow("Parol", parol_input)

        btn_box = QHBoxLayout()
        btn_ok = QPushButton("ОК")
        btn_cancel = QPushButton("Отмена")
        btn_box.addWidget(btn_ok)
        btn_box.addWidget(btn_cancel)
        layout.addRow(btn_box)

        btn_ok.clicked.connect(dialog.accept)
        btn_cancel.clicked.connect(dialog.reject)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        login = login_input.text().strip()
        parol = parol_input.text().strip()
        if not login or not parol:
            QMessageBox.warning(self, "Предупреждение", "Заполните все поля")
            return

        if not self._connect_db():
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных")
            return

        try:
            self.db.cur.execute(
                "INSERT INTO user (login, parol) VALUES (%s, %s)",
                (login, parol),
            )
            self.db.con.commit()
            self.load_data()
            QMessageBox.information(self, "Успех", "Запись добавлена")
        except Exception as e:
            self.db.con.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка добавления:\n{e}")

    def edit_record(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите строку для редактирования")
            return

        if self.table.item(current_row, 0) is None or self.table.item(current_row, 1) is None:
            QMessageBox.warning(self, "Ошибка", "Некорректные данные в строке")
            return

        current_login = self.table.item(current_row, 0).text()
        current_parol = self.table.item(current_row, 1).text()

        dialog = QDialog(self)
        dialog.setWindowTitle("Редактировать запись")
        layout = QFormLayout(dialog)

        login_input = QLineEdit(current_login)
        parol_input = QLineEdit(current_parol)

        layout.addRow("Login", login_input)
        layout.addRow("Пароль", parol_input)

        btn_box = QHBoxLayout()
        btn_ok = QPushButton("ОК")
        btn_cancel = QPushButton("Отмена")
        btn_box.addWidget(btn_ok)
        btn_box.addWidget(btn_cancel)
        layout.addRow(btn_box)

        btn_ok.clicked.connect(dialog.accept)
        btn_cancel.clicked.connect(dialog.reject)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        new_login = login_input.text().strip()
        new_parol = parol_input.text().strip()
        if not new_login or not new_parol:
            QMessageBox.warning(self, "Предупреждение", "Заполните все поля")
            return

        if not self._connect_db():
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных")
            return

        try:
            self.db.cur.execute(
                "UPDATE user SET login = %s, parol = %s WHERE login = %s",
                (new_login, new_parol, current_login),
            )
            self.db.con.commit()
            self.load_data()
            QMessageBox.information(self, "Успех", "Запись обновлена")
        except Exception as e:
            self.db.con.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка редактирования:\n{e}")

    def delete_record(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите строку для удаления")
            return

        if self.table.item(current_row, 0) is None:
            QMessageBox.warning(self, "Ошибка", "Некорректные данные в строке")
            return

        login = self.table.item(current_row, 0).text()
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            f"Удалить пользователя '{login}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        if not self._connect_db():
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных")
            return

        try:
            self.db.cur.execute("DELETE FROM user WHERE login = %s", (login,))
            self.db.con.commit()
            self.load_data()
            QMessageBox.information(self, "Успех", "Запись удалена")
        except Exception as e:
            self.db.con.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка удаления:\n{e}")

    def closeEvent(self, event):
        if self.db:
            self.db.close()
        event.accept()
