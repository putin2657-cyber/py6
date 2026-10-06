#!/usr/bin/env python3
"""Диаграммы взаимодействия процесса «Регистрация в системе».

Объекты — формы и другие части ИС (десктоп PyQt и веб Flask).
Запуск из корня репозитория: python3 docs/trp/build_diagrams.py
"""

from __future__ import annotations

import html
import math
import os
import signal
import subprocess
import time
from pathlib import Path

OUT = Path(__file__).resolve().parent
IMG = OUT / "images"

INK = "#1C2B39"
LINE = "#243140"
MUTED = "#4E6272"
LIFE = "#B7C3CE"
FORM_FILL = "#E7F0F8"
FORM_STROKE = "#1C4E7A"
CTRL_FILL = "#E7F4EA"
CTRL_STROKE = "#1E6B3A"
MOD_FILL = "#F3EEF8"
MOD_STROKE = "#5C3D86"
DB_FILL = "#E5F3EF"
DB_STROKE = "#1A6B58"
MSG_FILL = "#FBF3E6"
MSG_STROKE = "#8A5A12"
ACTOR = "#1C3D5A"
ALT_FILL = "#FFF8EE"
ALT_STROKE = "#8D6A2A"
SECTION = "#1F4E79"


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def text_width(text: str, size: float) -> float:
    width = 0.0
    for ch in text:
        if ch == " ":
            width += size * 0.33
        elif ch in ".,:;)(":
            width += size * 0.35
        elif "А" <= ch <= "я" or ch in "Ёё«»—":
            width += size * 0.62
        elif ch.isupper():
            width += size * 0.68
        else:
            width += size * 0.56
    return width


class SeqDiagram:
    def __init__(self, title: str, caption: str, participants: list[dict]):
        self.title = title
        self.caption = caption
        self.participants = participants
        self.col_w = 178
        self.margin_x = 28
        self.header_top = 64
        self.box_w = 158
        self.box_h = 76
        self.y = self.header_top + self.box_h + 26
        self.ops: list[tuple] = []
        self.fragments: list[dict] = []
        self.frag_stack: list[dict] = []
        self.activations: list[tuple] = []
        self._msg_y: dict[str, float] = {}

    @property
    def width(self) -> int:
        return int(self.margin_x * 2 + self.col_w * len(self.participants))

    def lx(self, key: str) -> float:
        for i, p in enumerate(self.participants):
            if p["id"] == key:
                return self.margin_x + i * self.col_w + self.col_w / 2
        raise KeyError(key)

    def mark(self, name: str) -> float:
        self._msg_y[name] = self.y
        return self.y

    def section(self, text: str) -> None:
        self.y += 6
        self.ops.append(("section", text, self.y))
        self.y += 24

    def msg(self, src: str, dst: str, text: str, kind: str = "sync", name: str | None = None) -> float:
        y = self.y
        self.ops.append(("msg", src, dst, text, kind, y))
        if name:
            self._msg_y[name] = y
        self.y += 46 if kind == "self" else 32
        return y

    def activate(self, who: str, y1: float, y2: float) -> None:
        self.activations.append((who, y1, y2))

    def alt_begin(self, guard: str, operator: str = "alt") -> None:
        self.y += 4
        frame = {
            "y1": self.y,
            "op": operator,
            "sections": [(self.y, guard)],
            "level": len(self.frag_stack),
        }
        self.frag_stack.append(frame)
        self.y += 28

    def alt_else(self, guard: str) -> None:
        self.y += 6
        self.frag_stack[-1]["sections"].append((self.y, guard))
        self.y += 24

    def alt_end(self) -> None:
        self.y += 8
        frame = self.frag_stack.pop()
        frame["y2"] = self.y
        self.fragments.append(frame)
        self.y += 6

    def note(self, who: str, text: str) -> None:
        self.ops.append(("note", who, text, self.y))
        lines = text.split("\n")
        self.y += 18 + 16 * len(lines)

    def _header(self, p: dict, i: int, top: float) -> str:
        cx = self.margin_x + i * self.col_w + self.col_w / 2
        x = cx - self.box_w / 2
        kind = p["kind"]
        parts: list[str] = []
        if kind == "actor":
            head_y = top + 16
            parts.append(
                f'<circle cx="{cx}" cy="{head_y}" r="11" fill="none" stroke="{ACTOR}" stroke-width="1.8"/>'
            )
            parts.append(
                f'<line x1="{cx}" y1="{head_y + 11}" x2="{cx}" y2="{head_y + 32}" stroke="{ACTOR}" stroke-width="1.8"/>'
            )
            parts.append(
                f'<line x1="{cx - 16}" y1="{head_y + 20}" x2="{cx + 16}" y2="{head_y + 20}" stroke="{ACTOR}" stroke-width="1.8"/>'
            )
            parts.append(
                f'<line x1="{cx}" y1="{head_y + 32}" x2="{cx - 14}" y2="{top + self.box_h - 16}" stroke="{ACTOR}" stroke-width="1.8"/>'
            )
            parts.append(
                f'<line x1="{cx}" y1="{head_y + 32}" x2="{cx + 14}" y2="{top + self.box_h - 16}" stroke="{ACTOR}" stroke-width="1.8"/>'
            )
            parts.append(
                f'<text x="{cx}" y="{top + self.box_h - 2}" text-anchor="middle" font-size="13" font-weight="650" fill="{INK}">{esc(p["name"])}</text>'
            )
            return "\n".join(parts)

        if kind == "db":
            fill, stroke = DB_FILL, DB_STROKE
            ry = 8
            body_top = top + ry
            body_h = self.box_h - ry * 2
            parts.append(
                f'<rect x="{x}" y="{body_top}" width="{self.box_w}" height="{body_h}" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>'
            )
            parts.append(
                f'<ellipse cx="{cx}" cy="{body_top}" rx="{self.box_w / 2}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>'
            )
            parts.append(
                f'<ellipse cx="{cx}" cy="{body_top + body_h}" rx="{self.box_w / 2}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>'
            )
            # side strokes hidden under ellipses: redraw upper arc only
            parts.append(
                f'<path d="M {x} {body_top} V {body_top + body_h}" fill="none" stroke="{stroke}" stroke-width="1.4"/>'
            )
            parts.append(
                f'<path d="M {x + self.box_w} {body_top} V {body_top + body_h}" fill="none" stroke="{stroke}" stroke-width="1.4"/>'
            )
        else:
            fill, stroke = {
                "form": (FORM_FILL, FORM_STROKE),
                "control": (CTRL_FILL, CTRL_STROKE),
                "module": (MOD_FILL, MOD_STROKE),
                "message": (MSG_FILL, MSG_STROKE),
            }[kind]
            parts.append(
                f'<rect x="{x}" y="{top}" width="{self.box_w}" height="{self.box_h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
            )

        parts.append(
            f'<text x="{cx}" y="{top + 20}" text-anchor="middle" font-size="11" fill="{MUTED}">«{esc(p["stereo"])}»</text>'
        )
        parts.append(
            f'<text x="{cx}" y="{top + 40}" text-anchor="middle" font-size="13.5" font-weight="650" fill="{INK}">{esc(p["name"])}</text>'
        )
        parts.append(
            f'<text x="{cx}" y="{top + 58}" text-anchor="middle" font-size="11" fill="{MUTED}">{esc(p["cls"])}</text>'
        )
        return "\n".join(parts)

    def render(self) -> str:
        bottom = self.y + 18
        footer = bottom + self.box_h + 36
        height = int(footer + 8)
        width = self.width
        chunks: list[str] = []
        chunks.append(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
        )
        chunks.append(
            """
<defs>
  <marker id="sync" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
    <path d="M 0 0 L 10 5 L 0 10 Z" fill="#243140"/>
  </marker>
  <marker id="reply" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
    <path d="M 1 1 L 9 5 L 1 9" fill="none" stroke="#4E6272" stroke-width="1.4"/>
  </marker>
</defs>
<style>
  text { font-family: Inter, "DejaVu Sans", "Liberation Sans", sans-serif; }
</style>
<rect width="100%" height="100%" fill="#ffffff"/>
"""
        )
        chunks.append(
            f'<text x="{width / 2}" y="28" text-anchor="middle" font-size="18" font-weight="700" fill="{INK}">{esc(self.title)}</text>'
        )
        chunks.append(
            f'<text x="{width / 2}" y="48" text-anchor="middle" font-size="12" fill="{MUTED}">ИС «Управление пользователями» · процесс «Регистрация»</text>'
        )

        # lifelines
        for i, _p in enumerate(self.participants):
            x = self.margin_x + i * self.col_w + self.col_w / 2
            y0 = self.header_top + self.box_h
            chunks.append(
                f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{bottom}" stroke="{LIFE}" stroke-width="1.2" stroke-dasharray="4 4"/>'
            )

        # fragment fills
        for fr in reversed(self.fragments):
            inset = 14 + fr["level"] * 18
            x = 10 + inset
            w = width - 20 - inset * 2
            h = fr["y2"] - fr["y1"]
            chunks.append(
                f'<rect x="{x}" y="{fr["y1"]}" width="{w}" height="{h}" rx="4" fill="{ALT_FILL}" fill-opacity="0.72" stroke="none"/>'
            )

        # activations
        for who, y1, y2 in self.activations:
            x = self.lx(who) - 5
            chunks.append(
                f'<rect x="{x}" y="{y1}" width="10" height="{max(8, y2 - y1)}" rx="1" fill="#1C3D5A" fill-opacity="0.9"/>'
            )

        # messages
        for op in self.ops:
            if op[0] == "section":
                _, text, y = op
                chunks.append(
                    f'<text x="{self.margin_x + 8}" y="{y}" font-size="12.5" font-weight="650" fill="{SECTION}">{esc(text)}</text>'
                )
            elif op[0] == "note":
                _, who, text, y = op
                lines = text.split("\n")
                tw = max(text_width(line, 12) for line in lines) + 22
                x = self.lx(who) + 16
                h = 14 + 16 * len(lines)
                chunks.append(
                    f'<rect x="{x}" y="{y}" width="{tw}" height="{h}" fill="#FFFBEA" stroke="#C4A24A" stroke-width="1"/>'
                )
                chunks.append(f'<polygon points="{x},{y} {x + 12},{y} {x},{y + 12}" fill="#C4A24A"/>')
                for n, line in enumerate(lines):
                    chunks.append(
                        f'<text x="{x + 12}" y="{y + 18 + n * 16}" font-size="12" fill="{INK}">{esc(line)}</text>'
                    )
            elif op[0] == "msg":
                _, src, dst, text, kind, y = op
                chunks.append(self._message(src, dst, text, kind, y))

        # fragment borders and guards
        for fr in self.fragments:
            inset = 14 + fr["level"] * 18
            x = 10 + inset
            w = width - 20 - inset * 2
            h = fr["y2"] - fr["y1"]
            chunks.append(
                f'<rect x="{x}" y="{fr["y1"]}" width="{w}" height="{h}" rx="4" fill="none" stroke="{ALT_STROKE}" stroke-width="1.3"/>'
            )
            op_w = text_width(fr["op"], 12) + 16
            chunks.append(
                f'<polygon points="{x},{fr["y1"]} {x + op_w},{fr["y1"]} {x + op_w + 8},{fr["y1"] + 11} {x + op_w},{fr["y1"] + 20} {x},{fr["y1"] + 20}" fill="{ALT_STROKE}"/>'
            )
            chunks.append(
                f'<text x="{x + 6}" y="{fr["y1"] + 14}" font-size="12" font-weight="700" fill="#ffffff">{esc(fr["op"])}</text>'
            )
            for index, (sy, guard) in enumerate(fr["sections"]):
                if index > 0:
                    chunks.append(
                        f'<line x1="{x}" y1="{sy}" x2="{x + w}" y2="{sy}" stroke="{ALT_STROKE}" stroke-width="1" stroke-dasharray="6 4"/>'
                    )
                chunks.append(
                    f'<text x="{x + op_w + 16}" y="{sy + 16}" font-size="12" fill="{ALT_STROKE}">[{esc(guard)}]</text>'
                )

        # headers on top and repeated at the bottom
        for i, p in enumerate(self.participants):
            chunks.append(self._header(p, i, self.header_top))
            chunks.append(self._header(p, i, bottom))

        chunks.append(
            f'<text x="{width / 2}" y="{footer - 8}" text-anchor="middle" font-size="13" fill="{INK}">{esc(self.caption)}</text>'
        )
        chunks.append("</svg>")
        self.height = height
        return "\n".join(chunks)

    def _message(self, src: str, dst: str, text: str, kind: str, y: float) -> str:
        x1 = self.lx(src)
        x2 = self.lx(dst)
        size = 12.5
        if kind == "self" or src == dst:
            x1 += 6
            path = f"M {x1} {y} H {x1 + 64} V {y + 20} H {x1 + 2}"
            label_x = x1 + 70
            label_y = y + 14
            anchor = "start"
            tw = text_width(text, size)
            bg = (
                f'<rect x="{label_x - 3}" y="{label_y - 12}" width="{tw + 8}" height="16" fill="#ffffff"/>'
            )
            line = (
                f'<path d="{path}" fill="none" stroke="{LINE}" stroke-width="1.25" marker-end="url(#sync)"/>'
            )
            label = (
                f'<text x="{label_x}" y="{label_y}" font-size="{size}" fill="{INK}">{esc(text)}</text>'
            )
            return bg + line + label

        color = LINE if kind == "sync" else MUTED
        marker = "sync" if kind == "sync" else "reply"
        dash = "" if kind == "sync" else ' stroke-dasharray="5 3.5"'
        # stop at activation edge
        if x2 > x1:
            x2 -= 6
            x1 += 6
        else:
            x2 += 6
            x1 -= 6
        mid = (x1 + x2) / 2
        tw = text_width(text, size)
        label_y = y - 6
        bg = (
            f'<rect x="{mid - tw / 2 - 4}" y="{label_y - 12}" width="{tw + 8}" height="16" fill="#ffffff" fill-opacity="0.92"/>'
        )
        line = (
            f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="1.25"{dash} marker-end="url(#{marker})"/>'
        )
        label = (
            f'<text x="{mid}" y="{label_y}" text-anchor="middle" font-size="{size}" fill="{INK}">{esc(text)}</text>'
        )
        return bg + line + label


def desktop_participants() -> list[dict]:
    return [
        {"id": "user", "name": "Пользователь", "stereo": "", "cls": "", "kind": "actor"},
        {"id": "menu", "name": "Главное меню", "stereo": "форма", "cls": "MenuW", "kind": "form"},
        {"id": "ctrl", "name": "Контроллер окон", "stereo": "управление", "cls": "Control", "kind": "control"},
        {"id": "reg", "name": "Форма регистрации", "stereo": "форма", "cls": "WidgetReg", "kind": "form"},
        {"id": "val", "name": "Валидатор", "stereo": "модуль", "cls": "validators", "kind": "module"},
        {"id": "db", "name": "Подключение к БД", "stereo": "модуль", "cls": "ConnectDB", "kind": "module"},
        {"id": "mysql", "name": "База данных", "stereo": "хранилище", "cls": "uslugi.user", "kind": "db"},
        {"id": "msg", "name": "Окно сообщения", "stereo": "форма", "cls": "QMessageBox", "kind": "message"},
    ]


def build_main() -> SeqDiagram:
    d = SeqDiagram(
        "Диаграмма последовательности. Основной сценарий",
        "Рис. 1. Регистрация пользователя: успешное создание учётной записи и возврат в меню",
        desktop_participants(),
    )
    d.section("Открытие формы регистрации")
    d.msg("user", "menu", "1: нажать «Зарегистрироваться»")
    d.msg("menu", "ctrl", "1.1: but_reg.clicked")
    y_hide = d.msg("ctrl", "menu", "1.2: hide()")
    y_show = d.msg("ctrl", "reg", "1.3: show(), activateWindow()")
    d.activate("menu", y_hide - 8, y_hide + 10)
    d.activate("reg", y_show - 8, y_show + 10)
    d.msg("reg", "reg", "1.4: фокус на поле «Логин»", "self")

    d.section("Проверка данных и запись учётной записи")
    d.msg("user", "reg", "2: ввести логин и пароль")
    y_click = d.msg("user", "reg", "3: нажать «Зарегистрироваться»")
    y1 = d.msg("reg", "val", "3.1: validate_login(login)")
    y2 = d.msg("val", "reg", "3.2: (True, «»)", "reply")
    d.activate("val", y1 - 6, y2 + 4)
    y3 = d.msg("reg", "val", "3.3: validate_password(parol)")
    y4 = d.msg("val", "reg", "3.4: (True, «»)", "reply")
    d.activate("val", y3 - 6, y4 + 4)
    y5 = d.msg("reg", "db", "3.5: ConnectDB()")
    y6 = d.msg("db", "mysql", "3.6: CONNECT к uslugi")
    y7 = d.msg("mysql", "db", "3.7: соединение установлено", "reply")
    d.activate("mysql", y6 - 6, y7 + 4)
    d.msg("reg", "db", "3.8: execute(SELECT login WHERE login=%s)")
    y8 = d.msg("db", "mysql", "3.9: SELECT")
    y9 = d.msg("mysql", "db", "3.10: строк нет", "reply")
    d.activate("mysql", y8 - 6, y9 + 4)
    d.msg("db", "reg", "3.11: fetchone() = None", "reply")
    d.msg("reg", "db", "3.12: execute(INSERT login, parol)")
    d.msg("db", "mysql", "3.13: INSERT INTO user")
    d.msg("reg", "db", "3.14: commit()")
    y10 = d.msg("db", "mysql", "3.15: COMMIT")
    d.activate("mysql", y10 - 6, y10 + 10)
    y11 = d.msg("reg", "msg", "3.16: information «Вы зарегистрированы»")
    y12 = d.msg("msg", "user", "3.17: показать уведомление", "reply")
    d.activate("msg", y11 - 6, y12 + 4)
    d.msg("reg", "reg", "3.18: очистить поля логина и пароля", "self")
    y13 = d.msg("reg", "db", "3.19: close()")
    y14 = d.msg("db", "mysql", "3.20: закрыть соединение")
    d.activate("db", y5 - 6, y14 + 8)
    d.activate("reg", y_click - 6, y13 + 8)

    d.section("Возврат в главное меню")
    d.msg("user", "reg", "4: нажать «Назад»")
    d.msg("reg", "ctrl", "4.1: quit.clicked")
    d.msg("ctrl", "reg", "4.2: hide()")
    d.msg("ctrl", "menu", "4.3: show()")
    return d


def build_alt() -> SeqDiagram:
    d = SeqDiagram(
        "Диаграмма последовательности. Альтернативные сценарии",
        "Рис. 2. Отказы при регистрации: поля, формат, соединение, дубликат логина, ошибка SQL",
        desktop_participants(),
    )
    d.note(
        "reg",
        "Форма регистрации уже открыта.\nОткрытие — сообщения 1–1.4 на рис. 1.",
    )
    d.msg("user", "reg", "5: «Зарегистрироваться»")
    d.msg("reg", "reg", "5.1: снять пробелы по краям (strip)", "self")

    d.alt_begin("логин или пароль пустые")
    y1 = d.msg("reg", "msg", "5.2: warning «Заполните все поля»")
    y2 = d.msg("msg", "user", "5.3: показать предупреждение", "reply")
    d.activate("msg", y1 - 6, y2 + 4)
    d.alt_else("оба поля заполнены")
    ya = d.msg("reg", "val", "5.4: validate_login(login)")
    yb = d.msg("val", "reg", "5.5: (ok, сообщение)", "reply")
    d.activate("val", ya - 6, yb + 4)

    d.alt_begin("логин короче 3 символов, есть пробел или нет строчной a–z")
    y1 = d.msg("reg", "msg", "5.6: warning(текст валидатора)")
    y2 = d.msg("msg", "user", "5.7: показать предупреждение", "reply")
    d.activate("msg", y1 - 6, y2 + 4)
    d.alt_else("логин корректен")
    ya = d.msg("reg", "val", "5.8: validate_password(parol)")
    yb = d.msg("val", "reg", "5.9: (ok, сообщение)", "reply")
    d.activate("val", ya - 6, yb + 4)

    d.alt_begin("пароль короче 6 символов или нет спецсимвола")
    y1 = d.msg("reg", "msg", "5.10: warning(текст валидатора)")
    y2 = d.msg("msg", "user", "5.11: показать предупреждение", "reply")
    d.activate("msg", y1 - 6, y2 + 4)
    d.alt_else("пароль корректен")
    d.msg("reg", "db", "5.12: ConnectDB()")
    d.msg("db", "mysql", "5.13: CONNECT к uslugi")

    d.alt_begin("соединение не установлено (con = None)")
    y1 = d.msg("reg", "msg", "5.14: critical «Не удалось подключиться к базе данных»")
    y2 = d.msg("msg", "user", "5.15: показать ошибку", "reply")
    d.activate("msg", y1 - 6, y2 + 4)
    d.alt_else("соединение установлено")
    d.msg("reg", "db", "5.16: execute(SELECT login WHERE login=%s)")
    d.msg("db", "mysql", "5.17: SELECT")
    d.msg("mysql", "db", "5.18: результат", "reply")
    d.msg("db", "reg", "5.19: fetchone()", "reply")

    d.alt_begin("логин уже есть в user")
    y1 = d.msg("reg", "msg", "5.20: warning «Такой пользователь уже есть»")
    y2 = d.msg("msg", "user", "5.21: показать предупреждение", "reply")
    d.activate("msg", y1 - 6, y2 + 4)
    d.alt_else("логин свободен")
    d.note(
        "reg",
        "Дальше — основной сценарий рис. 1:\nINSERT, COMMIT, «Вы зарегистрированы», очистка полей.",
    )
    d.alt_end()

    d.alt_begin("исключение при запросе", operator="opt")
    d.msg("reg", "db", "5.22: rollback()")
    d.msg("db", "mysql", "5.23: ROLLBACK")
    y1 = d.msg("reg", "msg", "5.24: critical «Ошибка регистрации»")
    y2 = d.msg("msg", "user", "5.25: показать ошибку", "reply")
    d.activate("msg", y1 - 6, y2 + 4)
    d.alt_end()

    d.msg("reg", "db", "5.26: close()")
    d.msg("db", "mysql", "5.27: закрыть соединение")
    d.alt_end()  # connection
    d.alt_end()  # password
    d.alt_end()  # login
    d.alt_end()  # empty
    return d


def web_participants() -> list[dict]:
    return [
        {"id": "user", "name": "Пользователь", "stereo": "", "cls": "", "kind": "actor"},
        {"id": "menu", "name": "Главное меню", "stereo": "форма", "cls": "menu.html", "kind": "form"},
        {"id": "reg", "name": "Форма регистрации", "stereo": "форма", "cls": "register.html", "kind": "form"},
        {"id": "app", "name": "Веб-приложение", "stereo": "модуль", "cls": "Flask /register", "kind": "control"},
        {"id": "val", "name": "Валидатор", "stereo": "модуль", "cls": "validators", "kind": "module"},
        {"id": "db", "name": "Подключение к БД", "stereo": "модуль", "cls": "ConnectDB", "kind": "module"},
        {"id": "mysql", "name": "База данных", "stereo": "хранилище", "cls": "uslugi.user", "kind": "db"},
        {"id": "login", "name": "Форма авторизации", "stereo": "форма", "cls": "login.html", "kind": "form"},
    ]


def build_web() -> SeqDiagram:
    d = SeqDiagram(
        "Диаграмма последовательности. Веб-регистрация",
        "Рис. 4. Тот же процесс на формах Flask: при успехе — переход к форме авторизации",
        web_participants(),
    )
    d.section("Открытие формы")
    d.msg("user", "menu", "1: ссылка «Регистрация»")
    d.msg("menu", "app", "1.1: GET /register")
    d.msg("app", "reg", "1.2: render_template(register.html)")
    d.msg("reg", "user", "1.3: страница регистрации", "reply")

    d.section("Ввод и отправка")
    d.msg("user", "reg", "2: ввести логин и пароль")
    d.msg("reg", "reg", "2.1: подсветить правила пароля", "self")
    d.note("reg", "Подсветка не блокирует отправку.\nРешение принимает веб-приложение.")
    y = d.msg("user", "reg", "3: «Зарегистрироваться»")
    d.msg("reg", "app", "3.1: POST /register (login, parol)")
    d.activate("app", y + 32, 0)  # placeholder, fixed below
    app_from = y + 32

    d.alt_begin("логин или пароль пустые")
    d.msg("app", "reg", "3.2: redirect /register, flash «Заполните все поля»")
    d.alt_else("поля заполнены, логин не прошёл validate_login")
    d.msg("app", "val", "3.3: validate_login(login)")
    d.msg("val", "app", "3.4: (False, сообщение)", "reply")
    d.msg("app", "reg", "3.5: redirect /register, flash(сообщение)")
    d.alt_else("логин корректен, пароль не прошёл validate_password")
    d.msg("app", "val", "3.6: validate_password(parol)")
    d.msg("val", "app", "3.7: (False, сообщение)", "reply")
    d.msg("app", "reg", "3.8: redirect /register, flash(сообщение)")
    d.alt_else("логин и пароль корректны")
    d.msg("app", "db", "3.9: ConnectDB()")
    d.msg("db", "mysql", "3.10: CONNECT к uslugi")
    d.alt_begin("нет соединения")
    d.msg("app", "reg", "3.11: redirect /register, flash «Ошибка подключения…»")
    d.alt_else("соединение есть")
    d.msg("app", "db", "3.12: execute(SELECT id WHERE login=%s)")
    d.msg("db", "mysql", "3.13: SELECT")
    d.msg("mysql", "db", "3.14: результат", "reply")
    d.msg("db", "app", "3.15: fetchone()", "reply")
    d.alt_begin("логин уже есть")
    d.msg("app", "reg", "3.16: снова register.html, flash «Такой пользователь уже есть»")
    d.alt_else("логин свободен")
    d.msg("app", "db", "3.17: execute(INSERT login, parol)")
    d.msg("db", "mysql", "3.18: INSERT INTO user")
    d.msg("app", "db", "3.19: commit()")
    d.msg("db", "mysql", "3.20: COMMIT")
    d.msg("app", "login", "3.21: redirect /login, flash «Вы зарегистрированы»")
    d.msg("login", "user", "3.22: форма входа и уведомление", "reply")
    d.alt_end()
    d.alt_begin("исключение при запросе", operator="opt")
    d.msg("app", "db", "3.23: rollback()")
    d.msg("db", "mysql", "3.24: ROLLBACK")
    d.msg("app", "reg", "3.25: register.html, flash «Ошибка регистрации»")
    d.alt_end()
    d.msg("app", "db", "3.26: close()")
    d.alt_end()
    d.alt_end()

    # activation of the web app covers the POST handling
    d.activations = [(who, y1, y2) for who, y1, y2 in d.activations if y2 != 0]
    d.activate("app", app_from - 6, d.y - 16)
    return d


def box(cx: float, cy: float, w: float, h: float, title: str, stereo: str, cls: str, fill: str, stroke: str) -> str:
    x, y = cx - w / 2, cy - h / 2
    return "\n".join(
        [
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>',
            f'<text x="{cx}" y="{cy - 16}" text-anchor="middle" font-size="11" fill="{MUTED}">«{esc(stereo)}»</text>',
            f'<text x="{cx}" y="{cy + 4}" text-anchor="middle" font-size="14" font-weight="700" fill="{INK}">{esc(title)}</text>',
            f'<text x="{cx}" y="{cy + 22}" text-anchor="middle" font-size="11" fill="{MUTED}">{esc(cls)}</text>',
        ]
    )


def actor_box(cx: float, cy: float) -> str:
    return "\n".join(
        [
            f'<circle cx="{cx}" cy="{cy - 28}" r="12" fill="none" stroke="{ACTOR}" stroke-width="1.8"/>',
            f'<line x1="{cx}" y1="{cy - 16}" x2="{cx}" y2="{cy + 8}" stroke="{ACTOR}" stroke-width="1.8"/>',
            f'<line x1="{cx - 18}" y1="{cy - 4}" x2="{cx + 18}" y2="{cy - 4}" stroke="{ACTOR}" stroke-width="1.8"/>',
            f'<line x1="{cx}" y1="{cy + 8}" x2="{cx - 14}" y2="{cy + 28}" stroke="{ACTOR}" stroke-width="1.8"/>',
            f'<line x1="{cx}" y1="{cy + 8}" x2="{cx + 14}" y2="{cy + 28}" stroke="{ACTOR}" stroke-width="1.8"/>',
            f'<text x="{cx}" y="{cy + 48}" text-anchor="middle" font-size="14" font-weight="700" fill="{INK}">Пользователь</text>',
        ]
    )


def cylinder(cx: float, cy: float, w: float, h: float, title: str, stereo: str, cls: str) -> str:
    x = cx - w / 2
    ry = 9
    top = cy - h / 2 + ry
    body_h = h - ry * 2
    return "\n".join(
        [
            f'<rect x="{x}" y="{top}" width="{w}" height="{body_h}" fill="{DB_FILL}" stroke="{DB_STROKE}" stroke-width="1.5"/>',
            f'<ellipse cx="{cx}" cy="{top}" rx="{w / 2}" ry="{ry}" fill="{DB_FILL}" stroke="{DB_STROKE}" stroke-width="1.5"/>',
            f'<ellipse cx="{cx}" cy="{top + body_h}" rx="{w / 2}" ry="{ry}" fill="{DB_FILL}" stroke="{DB_STROKE}" stroke-width="1.5"/>',
            f'<path d="M {x} {top} V {top + body_h}" fill="none" stroke="{DB_STROKE}" stroke-width="1.5"/>',
            f'<path d="M {x + w} {top} V {top + body_h}" fill="none" stroke="{DB_STROKE}" stroke-width="1.5"/>',
            f'<text x="{cx}" y="{cy - 14}" text-anchor="middle" font-size="11" fill="{MUTED}">«{esc(stereo)}»</text>',
            f'<text x="{cx}" y="{cy + 4}" text-anchor="middle" font-size="14" font-weight="700" fill="{INK}">{esc(title)}</text>',
            f'<text x="{cx}" y="{cy + 22}" text-anchor="middle" font-size="11" fill="{MUTED}">{esc(cls)}</text>',
        ]
    )



def _overlaps(a: tuple[float, float, float, float], b: tuple[float, float, float, float], pad: float = 4) -> bool:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return not (ax + aw + pad <= bx or bx + bw + pad <= ax or ay + ah + pad <= by or by + bh + pad <= ay)


def _label_at(x: float, y: float, lines: list[str]) -> tuple[str, tuple[float, float, float, float]]:
    size = 12
    tw = max(text_width(line, size) for line in lines)
    th = 16 * len(lines) + 10
    rect = (x, y, tw + 14, th)
    parts = [
        f'<rect x="{x}" y="{y}" width="{tw + 14}" height="{th}" rx="4" fill="#ffffff" stroke="#D5DEE6" stroke-width="1"/>'
    ]
    for i, line in enumerate(lines):
        parts.append(
            f'<text x="{x + 7}" y="{y + 17 + i * 16}" font-size="{size}" fill="{INK}">{esc(line)}</text>'
        )
    return "\n".join(parts), rect


def build_communication() -> tuple[str, int, int]:
    """Коммуникация успешного сценария. Номера сообщений совпадают с рис. 1."""
    width, height = 1560, 980
    rects = {
        "user": (48, 118, 120, 132),
        "menu": (300, 140, 200, 86),
        "ctrl": (690, 140, 230, 86),
        "val": (48, 500, 200, 86),
        "reg": (360, 500, 240, 86),
        "db": (760, 500, 230, 86),
        "mysql": (1140, 488, 200, 110),
        "msg": (360, 800, 240, 86),
    }

    def center(key: str) -> tuple[float, float]:
        x, y, w, h = rects[key]
        return x + w / 2, y + h / 2

    def edge(src: str, dst: str) -> tuple[float, float, float, float]:
        sx, sy = center(src)
        tx, ty = center(dst)
        dx, dy = tx - sx, ty - sy
        sw, sh = rects[src][2] / 2, rects[src][3] / 2
        dw, dh = rects[dst][2] / 2, rects[dst][3] / 2

        def hit(cx: float, cy: float, hw: float, hh: float, ox: float, oy: float) -> tuple[float, float]:
            adx, ady = abs(ox), abs(oy)
            scale_x = hw / adx if adx else 1e9
            scale_y = hh / ady if ady else 1e9
            scale = min(scale_x, scale_y)
            return cx + ox * scale, cy + oy * scale

        x1, y1 = hit(sx, sy, sw, sh, dx, dy)
        x2, y2 = hit(tx, ty, dw, dh, -dx, -dy)
        return x1, y1, x2, y2

    pairs = [
        ("user", "menu"),
        ("menu", "ctrl"),
        ("ctrl", "reg"),
        ("user", "reg"),
        ("reg", "val"),
        ("reg", "db"),
        ("db", "mysql"),
        ("reg", "msg"),
    ]
    labels = {
        ("user", "menu"): (188, 78, ["1: «Зарегистрироваться»"]),
        ("menu", "ctrl"): (520, 104, ["1.1: but_reg.clicked"]),
        ("ctrl", "reg"): (500, 328, ["1.3: show(), activateWindow()", "4.1: quit.clicked", "4.2: hide()"]),
        ("user", "reg"): (188, 292, ["2: ввести логин и пароль", "3: «Зарегистрироваться»", "4: «Назад»"]),
        ("menu", "extra"): (430, 248, ["1.2: hide() главного меню", "4.3: show() главного меню"]),
        ("reg", "val"): (48, 612, ["3.1: validate_login(login)", "3.2: (True, «»)", "3.3: validate_password(parol)", "3.4: (True, «»)"]),
        ("reg", "db"): (660, 648, ["3.5: ConnectDB()", "3.8: SELECT login", "3.11: fetchone() = None", "3.12: INSERT INTO user", "3.14: commit()", "3.19: close()"]),
        ("db", "mysql"): (1020, 352, ["3.6: CONNECT к uslugi", "3.7: соединение установлено", "3.9 / 3.13: SELECT / INSERT", "3.15: COMMIT", "3.20: закрыть соединение"]),
        ("reg", "msg"): (640, 812, ["3.16: «Вы зарегистрированы»", "3.18: очистить поля логина и пароля"]),
        ("msg", "user"): (40, 400, ["3.17: показать уведомление"]),
        ("self", "reg"): (620, 456, ["1.4: фокус на «Логин»"]),
    }

    label_rects: list[tuple[str, tuple[float, float, float, float]]] = []
    label_svg: list[str] = []
    for key, (x, y, lines) in labels.items():
        svg, rect = _label_at(x, y, lines)
        label_svg.append(svg)
        label_rects.append((f"{key[0]}-{key[1]}", rect))

    for name, rect in label_rects:
        for oname, orect in rects.items():
            if _overlaps(rect, orect):
                print(f"OVERLAP label {name} x object {oname} {rect} vs {orect}")
        for name2, rect2 in label_rects:
            if name < name2 and _overlaps(rect, rect2):
                print(f"OVERLAP label {name} x label {name2}")

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<defs><marker id="to-user" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 Z" fill="#7E91A3"/></marker></defs>',
        '<style>text { font-family: Inter, "DejaVu Sans", "Liberation Sans", sans-serif; }</style>',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="{width / 2}" y="34" text-anchor="middle" font-size="18" font-weight="700" fill="{INK}">Диаграмма коммуникации. Основной сценарий</text>',
        f'<text x="{width / 2}" y="56" text-anchor="middle" font-size="12" fill="{MUTED}">ИС «Управление пользователями» · процесс «Регистрация» · номера сообщений совпадают с рис. 1</text>',
    ]
    for src, dst in pairs:
        x1, y1, x2, y2 = edge(src, dst)
        parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#7E91A3" stroke-width="1.35"/>'
        )
    # 3.17 идёт от окна сообщения к пользователю в обход валидатора
    parts.append(
        '<path d="M 360 843 H 22 V 190 H 48" fill="none" stroke="#7E91A3" stroke-width="1.35" marker-end="url(#to-user)"/>'
    )

    rx, ry, rw, rh = rects["reg"]
    sx, sy = rx + rw - 6, ry + 16
    parts.append(
        f'<path d="M {sx} {sy} h 26 v 24 h -20" fill="none" stroke="{LINE}" stroke-width="1.2"/>'
    )
    parts.append(
        f'<polygon points="{sx - 2},{sy + 24} {sx + 8},{sy + 20} {sx + 8},{sy + 28}" fill="{LINE}"/>'
    )

    ux, uy, uw, uh = rects["user"]
    parts.append(actor_box(ux + uw / 2, uy + 58))
    parts.append(box(*center("menu"), rects["menu"][2], rects["menu"][3], "Главное меню", "форма", "MenuW", FORM_FILL, FORM_STROKE))
    parts.append(box(*center("ctrl"), rects["ctrl"][2], rects["ctrl"][3], "Контроллер окон", "управление", "Control", CTRL_FILL, CTRL_STROKE))
    parts.append(box(*center("val"), rects["val"][2], rects["val"][3], "Валидатор", "модуль", "validators", MOD_FILL, MOD_STROKE))
    parts.append(box(*center("reg"), rects["reg"][2], rects["reg"][3], "Форма регистрации", "форма", "WidgetReg", FORM_FILL, FORM_STROKE))
    parts.append(box(*center("db"), rects["db"][2], rects["db"][3], "Подключение к БД", "модуль", "ConnectDB", MOD_FILL, MOD_STROKE))
    parts.append(cylinder(*center("mysql"), rects["mysql"][2], rects["mysql"][3], "База данных", "хранилище", "uslugi.user"))
    parts.append(box(*center("msg"), rects["msg"][2], rects["msg"][3], "Окно сообщения", "форма", "QMessageBox", MSG_FILL, MSG_STROKE))
    parts.extend(label_svg)
    parts.append(
        f'<text x="{width / 2}" y="{height - 16}" text-anchor="middle" font-size="13" fill="{INK}">Рис. 3. Диаграмма коммуникации (кооперации) успешной регистрации</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts), width, height

def write_svg(name: str, svg: str, width: int, height: int) -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    svg_path = IMG / f"{name}.svg"
    svg_path.write_text(svg, encoding="utf-8")
    html_path = Path("/tmp") / f"{name}.html"
    html_path.write_text(
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        "<style>html,body{margin:0;padding:0;background:#fff;overflow:hidden;}</style></head><body>"
        + svg
        + "</body></html>",
        encoding="utf-8",
    )
    png_path = IMG / f"{name}.png"
    if png_path.exists():
        png_path.unlink()
    profile = Path("/tmp") / f"chrome-{name}"
    proc = subprocess.Popen(
        [
            "google-chrome",
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--hide-scrollbars",
            "--no-first-run",
            "--disable-extensions",
            "--disable-background-networking",
            "--force-device-scale-factor=2",
            f"--user-data-dir={profile}",
            f"--window-size={width},{height}",
            "--default-background-color=FFFFFFFF",
            f"--screenshot={png_path}",
            html_path.as_uri(),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    deadline = time.time() + 45
    last_size = -1
    stable = 0
    while time.time() < deadline:
        if png_path.exists():
            size = png_path.stat().st_size
            if size > 1000 and size == last_size:
                stable += 1
                if stable >= 3:
                    break
            else:
                stable = 0
            last_size = size
        time.sleep(0.25)
    else:
        os.killpg(proc.pid, signal.SIGKILL)
        raise RuntimeError(f"screenshot failed for {name}")
    os.killpg(proc.pid, signal.SIGKILL)
    proc.wait(timeout=5)
    print(f"{name}: {width}x{height} -> {png_path.stat().st_size} bytes")


def main() -> None:
    diagrams = {
        "seq-register-main": build_main(),
        "seq-register-alt": build_alt(),
        "seq-register-web": build_web(),
    }
    for name, diagram in diagrams.items():
        svg = diagram.render()
        write_svg(name, svg, diagram.width, diagram.height)
    svg, width, height = build_communication()
    write_svg("comm-register-main", svg, width, height)


if __name__ == "__main__":
    main()
