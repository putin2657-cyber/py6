import sys
import traceback

from PyQt6.QtWidgets import QApplication, QMessageBox

from oaip_web.oaip.auth_form import WidgetAvt
from edit_table import EditTableWindow
from main_menu import MenuW
from reg_form import WidgetReg
from user_menu import UserMenuW
from oaip_web.oaip.view_table import ViewTableWindow


def show_window(window):
    window.show()
    window.raise_()
    window.activateWindow()


class Control:
    """Переключение между окнами приложения."""

    def __init__(self):
        self.menu_form = MenuW()
        self.reg_form = WidgetReg()
        self.avt_form = WidgetAvt(on_success=self.open_user_menu)
        self.user_menu = UserMenuW()
        self.view_form = ViewTableWindow()
        self.edit_form = EditTableWindow()

        self.reg_form.quit.clicked.connect(self.open_menu)
        self.avt_form.quit.clicked.connect(self.open_menu)
        self.menu_form.but_avt.clicked.connect(self.open_avt)
        self.menu_form.but_reg.clicked.connect(self.open_reg)
        self.menu_form.quit.clicked.connect(self.close_app)

        self.user_menu.but_view.clicked.connect(self.open_view)
        self.user_menu.but_edit.clicked.connect(self.open_edit)
        self.user_menu.but_logout.clicked.connect(self.open_menu)

        self.view_form.btn_back.clicked.connect(self.back_to_user_menu)
        self.edit_form.btn_back.clicked.connect(self.back_to_user_menu)

        self.open_menu()

    def hide_all(self):
        self.menu_form.hide()
        self.reg_form.hide()
        self.avt_form.hide()
        self.user_menu.hide()
        self.view_form.hide()
        self.edit_form.hide()

    def open_menu(self):
        self.hide_all()
        show_window(self.menu_form)

    def open_avt(self):
        self.hide_all()
        show_window(self.avt_form)

    def open_reg(self):
        self.hide_all()
        show_window(self.reg_form)

    def open_user_menu(self, login):
        self.user_menu.set_login(login)
        self.hide_all()
        show_window(self.user_menu)

    def open_view(self):
        self.hide_all()
        show_window(self.view_form)

    def open_edit(self):
        self.hide_all()
        show_window(self.edit_form)

    def back_to_user_menu(self):
        self.hide_all()
        show_window(self.user_menu)

    def close_app(self):
        for window in (
            self.menu_form,
            self.reg_form,
            self.avt_form,
            self.user_menu,
            self.view_form,
            self.edit_form,
        ):
            window.close()
        QApplication.instance().quit()


def run_app():
    app = QApplication(sys.argv)
    app.setApplicationName("Управление пользователями")
    # Не завершать приложение автоматически при закрытии последнего окна:
    # мы управляем завершением вручную — приложение будет закрываться
    # только при нажатии кнопки "Выход" в главном меню или при закрытии
    # главного окна (реализовано в MenuW.closeEvent).
    app.setQuitOnLastWindowClosed(False)

    try:
        Control()
    except Exception:
        QMessageBox.critical(
            None,
            "Ошибка запуска",
            "Не удалось запустить приложение:\n\n"
            f"{traceback.format_exc()}\n\n"
            "Запускайте через main.py и интерпретатор .venv проекта.",
        )
        return 1

    return app.exec()


if __name__ == "__main__":
    sys.exit(run_app())
