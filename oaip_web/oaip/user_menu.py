from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class UserMenuW(QWidget):
    """Меню после успешной авторизации."""

    def __init__(self, login="", parent=None):
        super().__init__(parent)
        self.login = login
        self.setWindowTitle("Меню пользователя")
        self.resize(500, 320)

        layout = QVBoxLayout(self)

        self.title = QLabel(f"Вы вошли как: {login}")
        self.title.setStyleSheet("font-size: 16pt;")
        layout.addWidget(self.title)

        self.but_view = QPushButton("Просмотр данных")
        self.but_edit = QPushButton("Редактирование данных")
        self.but_logout = QPushButton("Выйти из аккаунта")

        layout.addWidget(self.but_view)
        layout.addWidget(self.but_edit)
        layout.addWidget(self.but_logout)

    def set_login(self, login):
        self.login = login
        self.title.setText(f"Вы вошли как: {login}")
