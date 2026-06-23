
import re
from typing import Tuple


def validate_login(login: str) -> Tuple[bool, str]:
    """Проверяет логин.

    Требования:
    - минимум 3 символа
    - нет пробелов
    - хотя бы одна строчная английская буква (a-z)

    Возвращает (True, "") если OK, иначе (False, сообщение_об_ошибке).
    """
    if len(login) < 3:
        return False, "Логин должен содержать не менее 3 символов"
    if " " in login:
        return False, "Логин не должен содержать пробелов"
    if not re.search(r"[a-z]", login):
        return False, "Логин должен содержать хотя бы одну строчную английскую букву (a-z)"
    return True, ""


def validate_password(parol: str) -> Tuple[bool, str]:
    """Проверяет пароль.

    Требования:
    - минимум 6 символов
    - как минимум один специальный символ (не буква/цифра)

    Возвращает (True, "") если OK, иначе (False, сообщение_об_ошибке).
    """
    if len(parol) < 6:
        return False, "Пароль должен содержать не менее 6 символов"
    if not re.search(r"[^A-Za-z0-9]", parol):
        return False, "Пароль должен содержать хотя бы один специальный символ, например: _ - ! @ #"
    return True, ""

