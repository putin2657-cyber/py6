from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox
)

from connect_db import ConnectDB


class ViewTableWindow(QMainWindow):
    """Форма 1: просмотр всех данных из таблицы user."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Просмотр данных")
        self.resize(800, 600)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.btn_refresh = QPushButton("Обновить")
        self.btn_back = QPushButton("Назад")
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_back)
        layout.addLayout(btn_layout)

        self.btn_refresh.clicked.connect(self.load_data)
        self.db = None

    def showEvent(self, event):
        super().showEvent(event)
        self.load_data()

    def load_data(self):
        if self.db:
            self.db.close()

        self.db = ConnectDB()
        if not self.db.con:
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

    def closeEvent(self, event):
        if self.db:
            self.db.close()
        event.accept()
