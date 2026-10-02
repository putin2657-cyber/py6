#!/usr/bin/env python3
"""Практическая 2, вариант 19 — оформление как в тетради."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
fp = font_manager.FontProperties(fname=FONT)
fpb = font_manager.FontProperties(fname=FONTB)

BG = (255, 251, 240)
INK = (28, 28, 28)
GREEN = (22, 122, 58)
BLUE = (28, 90, 168)
RED = (196, 40, 40)
YELLOW = (255, 210, 70)
WHITE = (255, 255, 255)
LINE = (50, 50, 50)
PAPER_G = (220, 245, 226)
PAPER_B = (220, 236, 255)
PAPER_Y = (255, 248, 210)
W = 1240


def F(sz, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, sz)


def T(d, xy, s, sz=24, fill=INK, bold=False, anchor="lt"):
    d.text(xy, s, font=F(sz, bold), fill=fill, anchor=anchor)


def table(d, origin, col_w, rh, headers, rows, head=YELLOW, fsize=20, last=None):
    x0, y0 = origin
    x = x0
    for i, h in enumerate(headers):
        box = [x, y0, x + col_w[i], y0 + rh]
        d.rectangle(box, fill=head, outline=LINE, width=3)
        T(d, ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), h, fsize, bold=True, anchor="mm")
        x += col_w[i]
    for r, row in enumerate(rows):
        x = x0
        y = y0 + (r + 1) * rh
        fill_row = last if last and r == len(rows) - 1 else WHITE
        for i, cell in enumerate(row):
            box = [x, y, x + col_w[i], y + rh]
            d.rectangle(box, fill=fill_row, outline=LINE, width=3)
            T(d, ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), cell, fsize - 1, anchor="mm")
            x += col_w[i]
    return y0 + (len(rows) + 1) * rh


def header(d, title, subtitle=None):
    d.rectangle([0, 0, W, 86], fill=(40, 40, 40))
    T(d, (W / 2, 28), title, 30, (255, 255, 255), True, "mm")
    if subtitle:
        T(d, (W / 2, 62), subtitle, 22, (255, 255, 255), False, "mm")


def graph_task2(path):
    xs = np.linspace(-2.4, 2.6, 500)
    fig, ax = plt.subplots(figsize=(6.4, 4.2), dpi=140)
    fig.patch.set_facecolor("#fffbf0")
    ax.set_facecolor("#fffef8")
    ax.axhline(0, color="#222", lw=1.15)
    ax.axvline(0, color="#222", lw=1.05)
    ax.plot(xs, 2 * xs**2, color="#1c5aa8", lw=2.5, label="y = 2x²")
    ax.plot(xs, 0.5 * xs + 2, color="#c42828", lw=2.5, label="y = 0,5x + 2")
    ax.plot([-0.8828], [1.5586], "o", color="#167a3a", ms=9, zorder=5)
    ax.plot([1.1328], [2.5664], "o", color="#888", ms=7, zorder=5)
    ax.annotate(
        "ξ ≈ −0,883",
        xy=(-0.8828, 1.5586),
        xytext=(-2.25, 6.4),
        fontproperties=fpb,
        fontsize=11,
        color="#167a3a",
        arrowprops=dict(arrowstyle="->", color="#167a3a"),
    )
    ax.annotate(
        "≈ 1,13",
        xy=(1.1328, 2.5664),
        xytext=(1.35, 5.4),
        fontproperties=fp,
        fontsize=10,
        color="#555",
        arrowprops=dict(arrowstyle="->", color="#888"),
    )
    ax.axvspan(-1, 0, color="#167a3a", alpha=0.08)
    ax.set_xlim(-2.4, 2.6)
    ax.set_ylim(-0.4, 8.2)
    ax.set_xlabel("x", fontproperties=fp)
    ax.set_ylabel("y", fontproperties=fp)
    ax.grid(True, ls="--", alpha=0.38)
    ax.legend(prop=fp, loc="upper right", fontsize=10)
    ax.set_title("касательные", fontproperties=fp, fontsize=12)
    fig.tight_layout()
    fig.savefig(path, facecolor=fig.get_facecolor())
    plt.close()


def sheet_z1():
    im = Image.new("RGB", (W, 2680), BG)
    d = ImageDraw.Draw(im)
    header(d, "Практическая работа № 2", "Решение нелинейных уравнений   ·   Вариант 19")

    y = 110
    T(d, (40, y), "Задание 1", 28, BLUE, True)
    y += 46
    T(d, (40, y), "Отделить аналитически корни алгебраического уравнения.", 22)
    y += 34
    T(d, (40, y), "Уточнить наименьший по модулю корень уравнения методом хорд", 22)
    y += 34
    T(d, (40, y), "с точностью ε. Найти остальные корни, используя схему Горнера.", 22)
    y += 48
    d.rounded_rectangle([36, y, 1204, y + 64], radius=10, fill=PAPER_Y, outline=LINE, width=2)
    T(d, (56, y + 16), "4x³ − 2x² + 3x + 10 = 0              ε = 0,01", 26, bold=True)
    y += 88

    T(d, (40, y), "f(x)  =  4x³ − 2x² + 3x + 10", 24, bold=True)
    y += 40
    T(d, (40, y), "f'(x) =  12x² − 4x + 3", 24)
    y += 44
    T(d, (40, y), "f'(x) = 0:", 24, BLUE, True)
    y += 38
    T(d, (40, y), "12x² − 4x + 3 = 0", 24)
    y += 38
    T(d, (40, y), "D = (−4)² − 4·12·3 = 16 − 144 = −128 < 0", 24, bold=True)
    y += 40
    T(d, (40, y), "действительных корней f' нет  →  f строго возрастает, один корень", 22)
    y += 52

    T(d, (40, y), "таблица знаков f(x)", 24, BLUE, True)
    y += 40
    y = table(
        d,
        (80, y),
        [150, 190, 190, 190, 190],
        54,
        ["x", "−∞", "−2", "−1", "+∞"],
        [["f(x)", "−", "−36", "+1", "+"]],
        fsize=22,
    )
    y += 22
    T(d, (40, y), "смена знака только на [−2; −1]     ξ ∈ [−2; −1]", 24, GREEN, True)
    y += 36
    T(d, (40, y), "это единственный действительный корень = наименьший по модулю", 22)
    y += 50

    T(d, (40, y), "f''(x) = 24x − 4", 24, bold=True)
    y += 40
    T(d, (40, y), "для хорд неподвижен тот конец, где f · f'' > 0", 22)
    y += 40
    y = table(
        d,
        (80, y),
        [200, 300, 300],
        52,
        ["", "x = −2", "x = −1"],
        [
            ["f", "−36", "+1"],
            ["f'", "59", "19"],
            ["f''", "−52", "−28"],
            ["f · f''", "+  > 0", "−  < 0"],
        ],
        fsize=22,
    )
    y += 22
    T(d, (40, y), "неподвижен a = −2,   приближения со стороны b,   x₀ = −1", 24, GREEN, True)
    y += 44
    T(d, (40, y), "xₙ₊₁ = xₙ − f(xₙ)·(xₙ − a) / (f(xₙ) − f(a))", 24, BLUE, True)
    y += 44
    y = table(
        d,
        (40, y),
        [90, 250, 250, 250, 230],
        52,
        ["n", "xₙ", "f(xₙ)", "xₙ₊₁", "|Δx|"],
        [
            ["0", "−1,000000", "1,000000", "−1,027027", "0,027027"],
            ["1", "−1,027027", "0,476181", "−1,039729", "0,012702"],
            ["2", "−1,039729", "0,222805", "−1,045635", "0,005907"],
        ],
        fsize=20,
        last=(255, 228, 180),
    )
    y += 22
    T(d, (40, y), "|Δx| = 0,005907 < 0,01  →  стоп", 24)
    y += 44
    d.rounded_rectangle([40, y, 1200, y + 88], radius=14, fill=PAPER_G, outline=GREEN, width=4)
    T(d, (60, y + 26), "ξ₁ = −1,046", 34, GREEN, True)
    y += 112

    T(d, (40, y), "схема Горнера   (деление на x + 1,045635)", 24, BLUE, True)
    y += 40
    y = table(
        d,
        (60, y),
        [220, 190, 230, 230, 220],
        54,
        ["", "4", "−2", "3", "10"],
        [["−1,045635", "4", "−6,182541", "9,464684", "0,103 ≈ 0"]],
        fsize=20,
    )
    y += 28
    T(d, (40, y), "4x² − 6,182541 x + 9,464684 = 0", 24, bold=True)
    y += 40
    T(d, (40, y), "D = (−6,182541)² − 4·4·9,464684 = 38,224 − 151,435 = −113,21 < 0", 22)
    y += 38
    T(d, (40, y), "остальные корни комплексные", 24)
    y += 44
    d.rounded_rectangle([40, y, 1200, y + 130], radius=16, fill=PAPER_G, outline=GREEN, width=4)
    T(d, (60, y + 22), "ξ₂,₃ = 0,773 ± 1,330 i", 32, GREEN, True)
    T(d, (60, y + 78), "действительный наименьший по модулю:   ξ₁ = −1,046", 24)
    y += 150

    return im.crop((0, 0, W, y + 20))


def sheet_z2():
    gpath = OUT / "_tmp_g2.png"
    graph_task2(gpath)
    gim = Image.open(gpath).convert("RGB")
    gim = gim.resize((680, int(680 * gim.height / gim.width)), Image.Resampling.LANCZOS)

    im = Image.new("RGB", (W, 2100), BG)
    d = ImageDraw.Draw(im)
    header(d, "Задание 2   ·   графически + касательные", "Практическая работа № 2   ·   Вариант 19")

    y = 110
    T(d, (40, y), "Отделить графически корни. Уточнить наименьший по модулю", 22)
    y += 34
    T(d, (40, y), "корень уравнения методом касательных с точностью ε.", 22)
    y += 46
    d.rounded_rectangle([36, y, 1204, y + 64], radius=10, fill=PAPER_Y, outline=LINE, width=2)
    T(d, (56, y + 16), "2x² = 0,5x + 2              ε = 0,001", 26, bold=True)
    y += 86

    T(d, (40, y), "g(x)  =  2x² − 0,5x − 2  =  0", 24, bold=True)
    y += 40
    T(d, (40, y), "y₁ = 2x²     (парабола)          y₂ = 0,5x + 2     (прямая)", 24, BLUE, True)
    y += 40
    T(d, (40, y), "g'(x) = 4x − 0,5          g''(x) = 4", 24)
    y += 50

    im.paste(gim, (40, y))
    gx = 750
    gy = y + 20
    T(d, (gx, gy), "пересечения:", 24, BLUE, True)
    T(d, (gx, gy + 44), "ξ ∈ [−1; 0]", 26, GREEN, True)
    T(d, (gx, gy + 88), "и ещё  ξ ∈ [1; 2]", 22)
    T(d, (gx, gy + 136), "меньший по | |", 24)
    T(d, (gx, gy + 176), "на [−1; 0]", 26, GREEN, True)
    T(d, (gx, gy + 230), "берём этот отрезок", 22)

    y += gim.height + 28
    T(d, (40, y), "таблица на концах отрезка [−1; 0]", 24, BLUE, True)
    y += 40
    y = table(
        d,
        (80, y),
        [220, 300, 300],
        52,
        ["", "a = −1", "b = 0"],
        [
            ["g", "+0,5", "−2"],
            ["g'", "−4,5", "−0,5"],
            ["g''", "+4", "+4"],
            ["g · g''", "+  > 0", "−  < 0"],
        ],
        fsize=22,
    )
    y += 22
    T(d, (40, y), "g(a)·g''(a) > 0  →  x₀ = a = −1", 24, GREEN, True)
    y += 42
    T(d, (40, y), "xₙ₊₁ = xₙ − g(xₙ) / g'(xₙ)", 24, BLUE, True)
    y += 44
    y = table(
        d,
        (40, y),
        [90, 250, 250, 250, 230],
        52,
        ["n", "x", "g(x)", "g'(x)", "Δx"],
        [
            ["0", "−1,000000", "0,500000", "−4,500000", "+0,111111"],
            ["1", "−0,888889", "0,024691", "−4,055556", "+0,006088"],
            ["2", "−0,882801", "0,000074", "−4,031202", "+0,000018"],
        ],
        fsize=20,
        last=(255, 228, 180),
    )
    y += 22
    T(d, (40, y), "|Δx| = 0,000018 < 0,001  →  стоп", 24)
    y += 44
    d.rounded_rectangle([40, y, 1200, y + 96], radius=14, fill=PAPER_G, outline=GREEN, width=4)
    T(d, (60, y + 28), "Ответ:   ξ = −0,8828", 34, GREEN, True)
    y += 116
    gpath.unlink(missing_ok=True)
    return im.crop((0, 0, W, y + 16))


def main():
    z1 = sheet_z1()
    z2 = sheet_z2()
    p1 = OUT / "pr2_zadanie1.png"
    p2 = OUT / "pr2_zadanie2.png"
    z1.save(p1, "PNG", optimize=True)
    z2.save(p2, "PNG", optimize=True)
    print(p1, z1.size)
    print(p2, z2.size)


if __name__ == "__main__":
    main()
