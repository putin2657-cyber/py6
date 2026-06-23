import sys


def main():
    try:
        from PyQt6.QtWidgets import QApplication, QMessageBox
    except ModuleNotFoundError:
        print(
            "PyQt6 не установлен для текущего Python.\n"
            "В PyCharm выберите интерпретатор:\n"
            "PythonProject6/.venv/bin/python"
        )
        return 1

    from oaip_web.oaip.control_win import run_app

    return run_app()


if __name__ == "__main__":
    sys.exit(main())
