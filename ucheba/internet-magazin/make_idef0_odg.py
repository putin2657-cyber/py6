#!/usr/bin/env python3
"""Рисует диаграмму IDEF0 A-0 через LibreOffice Draw (UNO) и сохраняет .odg."""

from __future__ import annotations

import os
import sys
import time
import traceback

import uno
from com.sun.star.awt import Point, Size
from com.sun.star.beans import PropertyValue

# Константы UNO (чтобы не импортировать enum до соединения с soffice)
FILL_NONE, FILL_SOLID = 0, 1
LINE_NONE, LINE_SOLID = 0, 1
ALIGN_LEFT, ALIGN_RIGHT, ALIGN_CENTER = 0, 1, 3
VALIGN_TOP, VALIGN_CENTER, VALIGN_BOTTOM = 0, 1, 2

OUT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "IDEF0_A-0.odg")
)


def cm(v: float) -> int:
    """Сантиметры → 1/100 мм (единицы LibreOffice)."""
    return int(round(v * 1000))


def pv(name, value):
    p = PropertyValue()
    p.Name = name
    p.Value = value
    return p


def connect(retries: int = 40):
    local = uno.getComponentContext()
    resolver = local.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local
    )
    url = "uno:socket,host=127.0.0.1,port=2002;urp;StarOffice.ComponentContext"
    last = None
    for _ in range(retries):
        try:
            return resolver.resolve(url)
        except Exception as exc:
            last = exc
            time.sleep(0.35)
    raise RuntimeError(f"Не удалось подключиться к LibreOffice: {last}")


def add_rect(doc, page, x, y, w, h, line_width=80, fill=None):
    sh = doc.createInstance("com.sun.star.drawing.RectangleShape")
    page.add(sh)
    sh.setPosition(Point(cm(x), cm(y)))
    sh.setSize(Size(cm(w), cm(h)))
    sh.LineColor = 0x000000
    sh.LineWidth = line_width
    sh.LineStyle = LINE_SOLID
    if fill is None:
        sh.FillStyle = FILL_NONE
    else:
        sh.FillStyle = FILL_SOLID
        sh.FillColor = fill
    return sh


def add_line(doc, page, x1, y1, x2, y2, arrow="end", width=55):
    sh = doc.createInstance("com.sun.star.drawing.LineShape")
    page.add(sh)
    sh.setPosition(Point(cm(x1), cm(y1)))
    sh.setSize(Size(cm(x2 - x1), cm(y2 - y1)))
    sh.LineColor = 0x000000
    sh.LineWidth = width
    sh.LineStyle = LINE_SOLID
    if arrow in ("end", "both"):
        sh.LineEndName = "Arrow"
        sh.LineEndWidth = 280
        sh.LineEndCenter = False
    if arrow == "both":
        sh.LineStartName = "Arrow"
        sh.LineStartWidth = 280
    return sh


def add_text(
    doc,
    page,
    x,
    y,
    w,
    h,
    text,
    size=12,
    bold=False,
    color=0x000000,
    align=ALIGN_CENTER,
    valign=VALIGN_CENTER,
):
    sh = doc.createInstance("com.sun.star.drawing.TextShape")
    page.add(sh)
    sh.setPosition(Point(cm(x), cm(y)))
    sh.setSize(Size(cm(w), cm(h)))
    sh.FillStyle = FILL_NONE
    sh.LineStyle = LINE_NONE
    sh.String = text
    sh.CharFontName = "Liberation Sans"
    sh.CharHeight = size
    sh.CharColor = color
    sh.CharWeight = 150 if bold else 100
    sh.ParaAdjust = align
    sh.TextVerticalAdjust = valign
    loc = uno.createUnoStruct("com.sun.star.lang.Locale")
    loc.Language = "ru"
    loc.Country = "RU"
    sh.CharLocale = loc
    sh.TextAutoGrowHeight = False
    sh.TextLeftDistance = 40
    sh.TextRightDistance = 40
    sh.TextUpperDistance = 20
    sh.TextLowerDistance = 20
    return sh


def main() -> int:
    ctx = connect()
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    doc = desktop.loadComponentFromURL("private:factory/sdraw", "_blank", 0, ())
    try:
        doc.SpellOnline = False
    except Exception:
        pass
    page = doc.getDrawPages().getByIndex(0)

    # A4 альбомная
    page.Width = cm(29.70)
    page.Height = cm(21.00)

    # Заголовок
    add_text(
        doc, page, 1.0, 0.25, 27.7, 0.7,
        "Диаграмма IDEF0  A-0",
        size=20, bold=True,
    )
    add_text(
        doc, page, 1.0, 0.90, 27.7, 0.55,
        "Контекстная диаграмма функции «Обработать заказ покупателя»",
        size=12, bold=False, color=0x333333,
    )

    # Рамка узла
    add_rect(doc, page, 0.55, 1.55, 28.60, 18.90, line_width=35)
    add_text(doc, page, 0.70, 1.60, 4.5, 0.45, "Узел: A-0", size=10, align=ALIGN_LEFT, color=0x444444)
    add_text(doc, page, 24.5, 19.85, 4.4, 0.40, "A-0", size=10, align=ALIGN_RIGHT, color=0x444444)

    # Блок A0
    box_x, box_y, box_w, box_h = 11.15, 7.85, 7.40, 5.30
    box = add_rect(doc, page, box_x, box_y, box_w, box_h, line_width=110)
    add_text(
        doc, page, box_x, box_y + 1.15, box_w, 2.4,
        "Обработать заказ\nпокупателя",
        size=18, bold=True,
    )
    add_text(
        doc, page, box_x + box_w - 1.35, box_y + box_h - 0.70, 1.20, 0.55,
        "A0", size=14, bold=True, align=ALIGN_RIGHT, valign=VALIGN_BOTTOM,
    )

    blue = 0x1F4E79
    box_l, box_r = box_x, box_x + box_w
    box_t, box_b = box_y, box_y + box_h

    # --- Входы (слева → в блок) ---
    add_text(doc, page, 0.70, 5.35, 4.2, 0.45, "Входы (I)", size=11, bold=True, color=blue, align=ALIGN_LEFT)
    add_line(doc, page, 2.10, 8.55, box_l, 8.55)
    add_text(doc, page, 0.65, 7.40, 4.9, 1.00, "Заказ покупателя\n(выбранные товары)", size=11, align=ALIGN_RIGHT, valign=VALIGN_BOTTOM)
    add_line(doc, page, 2.10, 10.50, box_l, 10.50)
    add_text(doc, page, 0.65, 9.45, 4.9, 0.90, "Оплата", size=11, align=ALIGN_RIGHT, valign=VALIGN_BOTTOM)
    add_line(doc, page, 2.10, 12.20, box_l, 12.20)
    add_text(doc, page, 0.65, 12.25, 4.9, 0.95, "Статус подготовки\nтоваров сотрудником", size=10, align=ALIGN_RIGHT, valign=VALIGN_TOP)

    # --- Управление (сверху вниз в блок) ---
    add_text(doc, page, 19.6, 1.58, 8.8, 0.40, "Управление (C)", size=11, bold=True, color=blue, align=ALIGN_LEFT)
    cx = [box_x + 1.05, box_x + box_w / 2, box_x + box_w - 1.05]
    add_line(doc, page, cx[0], 3.55, cx[0], box_t)
    add_text(doc, page, cx[0] - 1.20, 1.95, 2.40, 1.50, "Прайс, правила\nналичия и резерва", size=9)
    add_line(doc, page, cx[1], 3.55, cx[1], box_t)
    add_text(doc, page, cx[1] - 1.20, 1.95, 2.40, 1.50, "Условия и тарифы\nдоставки", size=9)
    add_line(doc, page, cx[2], 3.55, cx[2], box_t)
    add_text(doc, page, cx[2] - 1.20, 1.95, 2.40, 1.50, "Регламент\nобработки и оплаты", size=9)

    # --- Выходы (из блока вправо) ---
    add_text(doc, page, 23.4, 5.35, 5.3, 0.45, "Выходы (O)", size=11, bold=True, color=blue, align=ALIGN_RIGHT)
    add_line(doc, page, box_r, 8.55, 26.85, 8.55)
    add_text(doc, page, 21.55, 7.20, 7.4, 1.20, "Стоимость, способ доставки,\nподтверждение / отказ", size=10, align=ALIGN_LEFT, valign=VALIGN_BOTTOM)
    add_line(doc, page, box_r, 10.50, 26.85, 10.50)
    add_text(doc, page, 21.55, 9.45, 7.4, 0.90, "Заявка в службу доставки", size=11, align=ALIGN_LEFT, valign=VALIGN_BOTTOM)
    add_line(doc, page, box_r, 12.20, 26.85, 12.20)
    add_text(doc, page, 21.55, 12.25, 7.4, 1.05, "Учётные данные заказа\n(для отчёта о продажах)", size=10, align=ALIGN_LEFT, valign=VALIGN_TOP)

    # --- Механизмы (снизу вверх в блок) ---
    add_text(doc, page, 10.5, 18.95, 8.7, 0.40, "Механизмы (M)", size=11, bold=True, color=blue)
    mx1 = box_x + 1.55
    mx2 = box_x + box_w - 1.55
    add_line(doc, page, mx1, 16.85, mx1, box_b)
    add_text(doc, page, mx1 - 2.30, 16.90, 4.6, 1.15, "ИС интернет-магазина\n(каталог, заказы)", size=10, valign=VALIGN_TOP)
    add_line(doc, page, mx2, 16.85, mx2, box_b)
    add_text(doc, page, mx2 - 2.30, 16.90, 4.6, 1.15, "Сотрудник магазина", size=10, valign=VALIGN_TOP)

    add_text(
        doc, page, 1.2, 19.95, 22.5, 0.40,
        "ICOM: слева — входы, сверху — управление, справа — выходы, снизу — механизмы (стрелки входят снизу вверх).",
        size=9, color=0x555555,
    )

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    url = uno.systemPathToFileUrl(OUT)
    doc.storeAsURL(url, (pv("FilterName", "draw8"), pv("Overwrite", True)))
    doc.close(True)
    print(OUT)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        traceback.print_exc()
        raise SystemExit(1)
