from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class MenuW(QWidget):
    """Главное меню: авторизация и регистрация."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Главное меню")
        self.resize(500, 300)

        layout = QVBoxLayout(self)

        title = QLabel("Добро пожаловать!")
        title.setStyleSheet("font-size: 20pt;")
        title.setObjectName("title")
        layout.addWidget(title)

        self.but_avt = QPushButton("Авторизоваться")
        self.but_reg = QPushButton("Зарегистрироваться")
        self.quit = QPushButton("Выход")

        layout.addWidget(self.but_avt)
        layout.addWidget(self.but_reg)
        layout.addWidget(self.quit)

    def closeEvent(self, event):
        """Если пользователь закрыл главное окно через крестик — завершаем приложение."""
        from PyQt6.QtWidgets import QApplication

        QApplication.instance().quit()
        event.accept()

