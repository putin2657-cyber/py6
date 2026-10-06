#!/usr/bin/env python3
"""Чертежи DFD и IDEF0 для задания по интернет-магазину."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager, patheffects
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = Path(__file__).resolve().parent
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font_manager.fontManager.addfont(FONT)
font_manager.fontManager.addfont(FONT_BOLD)
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False

INK = "#222222"
BLUE = "#1f4e79"
GREEN = "#2e5d34"


def _save(fig, name: str) -> Path:
    path = OUT / name
    fig.savefig(path, dpi=170, bbox_inches="tight", facecolor="white", pad_inches=0.28)
    plt.close(fig)
    return path


def _wrap(text: str, width: int) -> str:
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = w if not cur else f"{cur} {w}"
        if len(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return "\n".join(lines)


def _txt(ax, x, y, text, size=8.2, weight="normal", color="#1a1a1a", ha="center", va="center"):
    ax.text(x, y, text, fontsize=size, fontweight=weight, color=color, ha=ha, va=va, linespacing=1.22, zorder=6)


def entity(ax, x, y, w, h, title):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, lw=1.55, ec="#2b2b2b", fc="#f6e7b8", zorder=3))
    _txt(ax, x, y, _wrap(title, 16), size=8.7, weight="bold")
    return x, y, w, h


def process(ax, x, y, w, h, num, title):
    ax.add_patch(
        FancyBboxPatch(
            (x - w / 2, y - h / 2),
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.16",
            lw=1.55,
            ec=BLUE,
            fc="#d7e8f7",
            zorder=3,
        )
    )
    ax.add_patch(Rectangle((x - w / 2, y + h / 2 - 0.40), 0.52, 0.40, lw=1.15, ec=BLUE, fc=BLUE, zorder=4))
    _txt(ax, x - w / 2 + 0.26, y + h / 2 - 0.20, str(num), size=8.3, weight="bold", color="white")
    _txt(ax, x + 0.06, y - 0.04, _wrap(title, 18), size=8.0, weight="bold")
    return x, y, w, h


def store(ax, x, y, w, h, title):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, lw=1.55, ec=GREEN, fc="#dcefd8", zorder=3))
    ax.plot([x - w / 2 + 0.15, x - w / 2 + 0.15], [y - h / 2, y + h / 2], color=GREEN, lw=1.55, zorder=4)
    _txt(ax, x + 0.05, y, _wrap(title, 16), size=8.0, weight="bold")
    return x, y, w, h


def edge(box, side: str, t: float = 0.5, extra: float = 0.0):
    x, y, w, h = box
    if side == "L":
        return (x - w / 2 - extra, y + (t - 0.5) * h * 0.7)
    if side == "R":
        return (x + w / 2 + extra, y + (t - 0.5) * h * 0.7)
    if side == "T":
        return (x + (t - 0.5) * w * 0.7, y + h / 2 + extra)
    if side == "B":
        return (x + (t - 0.5) * w * 0.7, y - h / 2 - extra)
    raise ValueError(side)


def poly(ax, pts, text="", off=(0.0, 0.0), size=7.1, longest=True):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=INK, lw=1.18, zorder=2, solid_capstyle="round")
    ax.add_patch(
        FancyArrowPatch(
            pts[-2],
            pts[-1],
            arrowstyle="-|>",
            mutation_scale=12.5,
            lw=1.18,
            color=INK,
            zorder=3,
            shrinkA=0,
            shrinkB=0,
        )
    )
    if not text:
        return
    if longest and len(pts) > 2:
        segs = list(zip(pts[:-1], pts[1:]))
        (a, b) = max(segs, key=lambda s: abs(s[0][0] - s[1][0]) + abs(s[0][1] - s[1][1]))
    else:
        a, b = pts[0], pts[-1]
        if len(pts) >= 2:
            a, b = pts[-2], pts[-1]
    mx, my = (a[0] + b[0]) / 2 + off[0], (a[1] + b[1]) / 2 + off[1]
    t = ax.text(mx, my, _wrap(text, 20), fontsize=size, ha="center", va="center", color="#111", zorder=5, linespacing=1.12)
    t.set_path_effects([patheffects.withStroke(linewidth=3.8, foreground="white")])


def curve(ax, p1, p2, text="", rad=0.0, off=(0.0, 0.0), size=7.2):
    ax.add_patch(
        FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=13, lw=1.18, color=INK, connectionstyle=f"arc3,rad={rad}", zorder=2)
    )
    if not text:
        return
    mx, my = (p1[0] + p2[0]) / 2 + off[0], (p1[1] + p2[1]) / 2 + off[1]
    t = ax.text(mx, my, _wrap(text, 20), fontsize=size, ha="center", va="center", zorder=5, linespacing=1.12)
    t.set_path_effects([patheffects.withStroke(linewidth=3.6, foreground="white")])


def legend_dfd(ax, x, y):
    entity(ax, x, y, 2.15, 0.68, "Внешняя сущность")
    process(ax, x + 2.95, y, 2.35, 0.82, "N", "Процесс")
    store(ax, x + 5.9, y, 2.35, 0.68, "D Хранилище")


def draw_context() -> Path:
    fig, ax = plt.subplots(figsize=(15.4, 10.8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11.15)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.text(8, 10.55, "Контекстная DFD  (уровень 0)", ha="center", va="center", fontsize=16, fontweight="bold")
    ax.text(8, 10.08, "Система интернет-магазина", ha="center", va="center", fontsize=12, color="#333")

    sys = (8.0, 5.45, 4.9, 2.45)
    ax.add_patch(
        FancyBboxPatch(
            (sys[0] - sys[2] / 2, sys[1] - sys[3] / 2),
            sys[2],
            sys[3],
            boxstyle="round,pad=0.03,rounding_size=0.32",
            lw=2.0,
            ec=BLUE,
            fc="#d7e8f7",
            zorder=3,
        )
    )
    _txt(ax, 8.0, 6.15, "0", size=13, weight="bold", color=BLUE)
    _txt(ax, 8.0, 5.35, "Система\nинтернет-магазина", size=11.2, weight="bold")

    buyer = entity(ax, 1.65, 5.45, 2.55, 1.12, "Покупатель")
    staff = entity(ax, 8.0, 8.65, 3.15, 1.05, "Сотрудник магазина")
    ship = entity(ax, 14.35, 5.45, 2.6, 1.12, "Служба доставки")
    boss = entity(ax, 8.0, 1.72, 2.75, 1.05, "Руководитель")

    curve(ax, edge(buyer, "R", 0.72), edge(sys, "L", 0.72), "Состав заказа", off=(0.0, 0.28))
    curve(ax, edge(buyer, "R", 0.22), edge(sys, "L", 0.18), "Оплата", rad=-0.08, off=(0.0, -0.30))
    curve(ax, edge(sys, "L", 0.95), edge(buyer, "R", 0.95), "Стоимость, способ доставки,\nстатус / отказ", rad=0.16, off=(-0.05, 0.50), size=6.9)

    curve(ax, edge(sys, "T", 0.62), edge(staff, "B", 0.62), "Информация о заказе", off=(1.55, 0.0))
    curve(ax, edge(staff, "B", 0.32), edge(sys, "T", 0.32), "Статус подготовки товаров", off=(-1.85, 0.0), size=7.0)

    curve(ax, edge(sys, "R", 0.5), edge(ship, "L", 0.5), "Заявка на доставку", off=(0.05, 0.28))

    curve(ax, edge(boss, "T", 0.68), edge(sys, "B", 0.68), "Запрос отчёта", off=(1.28, 0.0))
    curve(ax, edge(sys, "B", 0.28), edge(boss, "T", 0.28), "Отчёт о продажах", off=(-1.38, 0.0))

    legend_dfd(ax, 2.35, 0.52)
    return _save(fig, "dfd_context.png")


def draw_level1() -> Path:
    fig, ax = plt.subplots(figsize=(20.4, 13.0))
    ax.set_xlim(0, 22.4)
    ax.set_ylim(0, 13.85)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.text(11.2, 13.5, "DFD первого уровня", ha="center", va="center", fontsize=16, fontweight="bold")
    ax.text(
        11.2,
        13.08,
        "Декомпозиция процесса 0 «Система интернет-магазина»  •  5 процессов, 2 хранилища",
        ha="center",
        va="center",
        fontsize=10.4,
        color="#333",
    )

    # верхний конвейер: покупатель — 1 — 2 — 3 — 4 — доставка
    buyer = entity(ax, 1.65, 10.55, 2.5, 1.08, "Покупатель")
    p1 = process(ax, 5.55, 10.55, 2.62, 1.38, "1", "Проверить наличие товаров")
    p2 = process(ax, 9.55, 10.55, 2.62, 1.38, "2", "Зарегистрировать заказ")
    p3 = process(ax, 13.55, 10.55, 2.62, 1.38, "3", "Рассчитать стоимость и принять оплату")
    p4 = process(ax, 17.55, 10.55, 2.62, 1.38, "4", "Подготовить и передать в доставку")
    ship = entity(ax, 21.05, 10.55, 2.4, 1.08, "Служба доставки")

    d1 = store(ax, 5.55, 6.85, 2.62, 1.02, "D1  Товары")
    d2 = store(ax, 11.55, 6.85, 2.9, 1.02, "D2  Заказы")

    staff = entity(ax, 1.65, 4.55, 2.5, 1.08, "Сотрудник магазина")
    p5 = process(ax, 11.55, 2.15, 2.9, 1.38, "5", "Сформировать отчёт о продажах")
    boss = entity(ax, 17.55, 2.15, 2.62, 1.08, "Руководитель")

    # ряд процессов
    poly(ax, [edge(buyer, "R", 0.72), edge(p1, "L", 0.72)], "Состав заказа", off=(0.0, 0.24))
    poly(ax, [edge(p1, "L", 0.22), edge(buyer, "R", 0.22)], "Отказ / нет товара", off=(0.0, -0.26), size=6.7)
    poly(ax, [edge(p1, "R", 0.5), edge(p2, "L", 0.5)], "Проверенный заказ", off=(0.0, 0.24), size=6.8)
    poly(ax, [edge(p2, "R", 0.5), edge(p3, "L", 0.5)], "Зарегистрированный заказ", off=(0.0, 0.24), size=6.6)
    poly(ax, [edge(p3, "R", 0.5), edge(p4, "L", 0.5)], "Оплаченный заказ", off=(0.0, 0.24), size=6.8)
    poly(ax, [edge(p4, "R", 0.5), edge(ship, "L", 0.5)], "Заявка на доставку", off=(0.0, 0.24), size=6.8)

    # подтверждение покупателю над конвейером
    poly(
        ax,
        [edge(p2, "T", 0.35), (9.55, 12.28), (1.65, 12.28), edge(buyer, "T", 0.5)],
        "Подтверждение, стоимость, способ доставки",
        off=(-2.4, -0.34),
        size=6.8,
    )

    # оплата: слева вниз и к P3 снизу
    poly(
        ax,
        [edge(buyer, "B", 0.35), (1.65, 8.95), (13.55, 8.95), edge(p3, "B", 0.35)],
        "Оплата",
        off=(3.6, 0.24),
        size=7.2,
    )

    # P1 <-> D1
    poly(ax, [edge(p1, "B", 0.32), edge(d1, "T", 0.32)], "Запрос наличия", off=(-1.22, 0.0), size=6.7)
    poly(ax, [edge(d1, "T", 0.72), edge(p1, "B", 0.72)], "Остатки и цены", off=(1.18, 0.0), size=6.7)

    # P2 -> D2
    poly(ax, [edge(p2, "B", 0.45), (9.55, 7.36), edge(d2, "T", 0.22)], "Данные заказа", off=(-0.15, 0.22), size=6.8)

    # P3 <-> D2
    poly(ax, [edge(d2, "T", 0.55), (12.1, 9.86), edge(p3, "B", 0.72)], "Сумма заказа", off=(0.95, 0.0), size=6.6)
    poly(ax, [edge(p3, "B", 0.18), (13.05, 8.15), (13.05, 7.36), edge(d2, "R", 0.55)], "Статус «оплачен»", off=(1.25, 0.0), size=6.6)

    # P4 -> D2 статус
    poly(ax, [edge(p4, "B", 0.5), (17.55, 6.85), edge(d2, "R", 0.5)], "Статус «в доставку»", off=(0.15, -0.28), size=6.6)

    # сотрудник
    poly(
        ax,
        [edge(p2, "B", 0.18), (8.45, 9.62), (8.45, 4.55), edge(staff, "R", 0.72)],
        "Информация о заказе",
        off=(0.15, -1.35),
        size=6.7,
    )
    poly(
        ax,
        [edge(staff, "R", 0.22), (17.55, 4.15), edge(p4, "B", 0.18)],
        "Статус подготовки",
        off=(5.8, 0.24),
        size=6.7,
    )

    # отчёт
    poly(ax, [edge(d2, "B", 0.5), edge(p5, "T", 0.5)], "Данные продаж", off=(1.15, 0.0), size=6.8)
    poly(ax, [edge(boss, "L", 0.72), edge(p5, "R", 0.72)], "Запрос отчёта", off=(0.0, 0.24), size=6.8)
    poly(ax, [edge(p5, "R", 0.22), edge(boss, "L", 0.22)], "Отчёт о продажах", off=(0.0, -0.26), size=6.8)

    legend_dfd(ax, 1.9, 0.7)
    _txt(ax, 16.3, 0.7, "Внешние потоки совпадают\nс контекстной DFD.", size=7.6, color="#444", ha="left")
    return _save(fig, "dfd_uroven1.png")


def draw_idef0() -> Path:
    fig, ax = plt.subplots(figsize=(16.4, 11.3))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11.15)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")

    ax.text(8, 10.62, "Диаграмма IDEF0  A-0", ha="center", va="center", fontsize=16, fontweight="bold")
    ax.text(
        8,
        10.18,
        "Контекстная диаграмма функции «Обработать заказ покупателя»",
        ha="center",
        va="center",
        fontsize=11,
        color="#333",
    )

    ax.add_patch(Rectangle((0.42, 0.42), 15.16, 9.42, fill=False, lw=1.0, edgecolor="#777"))
    ax.text(0.62, 9.58, "Узел: A-0", fontsize=9, ha="left", va="center", color="#444")
    ax.text(15.35, 0.62, "A-0", fontsize=9, ha="right", va="center", color="#444")

    bx, by, bw, bh = 5.55, 3.95, 4.9, 3.15
    ax.add_patch(Rectangle((bx, by), bw, bh, lw=2.45, ec="black", fc="white", zorder=3))
    _txt(ax, bx + bw / 2, by + bh / 2 + 0.12, "Обработать заказ\nпокупателя", size=13.2, weight="bold")
    ax.text(bx + bw - 0.18, by + 0.16, "A0", fontsize=11, ha="right", va="bottom", fontweight="bold")

    left, right, top, bottom = bx, bx + bw, by + bh, by

    def arrow(a, b):
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=14, lw=1.35, color=INK, zorder=2))

    ax.text(0.72, 7.42, "Входы (I)", fontsize=9, fontweight="bold", color=BLUE, ha="left")
    arrow((1.55, 6.42), (left, 6.42))
    ax.text(1.45, 6.64, "Заказ покупателя\n(выбранные товары)", fontsize=8.1, ha="right", va="bottom")
    arrow((1.55, 5.22), (left, 5.22))
    ax.text(1.45, 5.44, "Оплата", fontsize=8.1, ha="right", va="bottom")
    arrow((1.55, 4.32), (left, 4.32))
    ax.text(1.45, 4.14, "Статус подготовки\nтоваров сотрудником", fontsize=7.7, ha="right", va="top")

    ax.text(8.0, 9.62, "Управление (C)", fontsize=9, fontweight="bold", color=BLUE, ha="center")
    arrow((6.25, 9.22), (6.25, top))
    ax.text(6.25, 9.28, "Прайс, правила\nналичия и резерва", fontsize=7.8, ha="center", va="bottom")
    arrow((8.0, 9.22), (8.0, top))
    ax.text(8.0, 9.28, "Условия и тарифы\nдоставки", fontsize=7.8, ha="center", va="bottom")
    arrow((9.75, 9.22), (9.75, top))
    ax.text(9.75, 9.28, "Регламент обработки\nи оплаты заказа", fontsize=7.8, ha="center", va="bottom")

    ax.text(15.28, 7.62, "Выходы (O)", fontsize=9, fontweight="bold", color=BLUE, ha="right")
    arrow((right, 6.62), (14.4, 6.62))
    ax.text(14.5, 6.84, "Стоимость, способ доставки,\nподтверждение / отказ", fontsize=7.7, ha="left", va="bottom")
    arrow((right, 5.38), (14.4, 5.38))
    ax.text(14.5, 5.60, "Заявка в службу доставки", fontsize=7.9, ha="left", va="bottom")
    arrow((right, 4.28), (14.4, 4.28))
    ax.text(14.5, 4.10, "Учётные данные заказа\n(для отчёта о продажах)", fontsize=7.7, ha="left", va="top")

    ax.text(8.0, 1.22, "Механизмы (M)", fontsize=9, fontweight="bold", color=BLUE, ha="center")
    # стрелки СНИЗУ ВВЕРХ в нижнюю грань блока
    arrow((6.55, 2.42), (6.55, bottom))
    ax.text(6.55, 2.28, "ИС интернет-магазина\n(каталог, заказы)", fontsize=7.9, ha="center", va="top")
    arrow((9.4, 2.42), (9.4, bottom))
    ax.text(9.4, 2.28, "Сотрудник магазина", fontsize=7.9, ha="center", va="top")

    ax.text(
        8.0,
        0.70,
        "ICOM: слева — входы, сверху — управление, справа — выходы, снизу — механизмы (стрелки входят снизу вверх).",
        ha="center",
        va="center",
        fontsize=8.0,
        color="#555",
    )
    return _save(fig, "idef0_a-0.png")


if __name__ == "__main__":
    for fn in (draw_context, draw_level1, draw_idef0):
        print(fn())
