#!/usr/bin/env python3
"""Практическая 2, вариант 19 — тетрадь + методички Жилкиной."""

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

PAPER = (252, 252, 244)
GRID = (214, 226, 236)
MARGIN = (214, 150, 150)
INK = (28, 28, 28)
GREEN = (22, 122, 58)
BLUE = (28, 90, 168)
LINE = (50, 50, 50)
WHITE = (255, 255, 255)
YELLOW = (255, 236, 170)
W = 1180
STEP = 38
LEFT = 84


def F(sz, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, sz)


def notebook(rows):
    h = (rows + 2) * STEP
    im = Image.new("RGB", (W, h), PAPER)
    d = ImageDraw.Draw(im)
    for x in range(0, W, STEP):
        d.line([(x, 0), (x, h)], fill=GRID, width=1)
    for y in range(0, h, STEP):
        d.line([(0, y), (W, y)], fill=GRID, width=1)
    d.line([(60, 0), (60, h)], fill=MARGIN, width=2)
    return im, d


def write(d, row, s, sz=22, fill=INK, bold=False):
    d.text((LEFT, row * STEP + 7), s, font=F(sz, bold), fill=fill)


def table(d, row, col_w, headers, rows, fsize=18, head=YELLOW):
    x0 = LEFT
    y0 = row * STEP
    rh = STEP
    x = x0
    for i, h in enumerate(headers):
        box = [x, y0, x + col_w[i], y0 + rh]
        d.rectangle(box, fill=head, outline=LINE, width=2)
        d.text(
            ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2),
            h,
            font=F(fsize, True),
            fill=INK,
            anchor="mm",
        )
        x += col_w[i]
    for r, rw in enumerate(rows):
        x = x0
        y = y0 + (r + 1) * rh
        for i, cell in enumerate(rw):
            box = [x, y, x + col_w[i], y + rh]
            d.rectangle(box, fill=WHITE, outline=LINE, width=2)
            d.text(
                ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2),
                cell,
                font=F(fsize),
                fill=INK,
                anchor="mm",
            )
            x += col_w[i]
    used = 1 + len(rows)
    return row + used


def graph_task2(path):
    xs = np.linspace(-2.3, 2.5, 400)
    fig, ax = plt.subplots(figsize=(5.6, 3.6), dpi=130)
    fig.patch.set_facecolor("#fcfcf4")
    ax.set_facecolor("#fffef8")
    ax.axhline(0, color="#222", lw=1.1)
    ax.axvline(0, color="#222", lw=1.0)
    ax.plot(xs, 2 * xs**2, color="#1c5aa8", lw=2.3, label="y = 2x²")
    ax.plot(xs, 0.5 * xs + 2, color="#c42828", lw=2.3, label="y = 0,5x+2")
    ax.plot([-0.8828], [1.5586], "o", color="#167a3a", ms=8)
    ax.plot([1.1328], [2.5664], "o", color="#777", ms=6)
    ax.annotate("ξ", xy=(-0.8828, 1.5586), xytext=(-2.05, 4.8),
                fontproperties=fpb, fontsize=12, color="#167a3a",
                arrowprops=dict(arrowstyle="->", color="#167a3a"))
    ax.set_xlim(-2.3, 2.5)
    ax.set_ylim(-0.3, 8)
    ax.grid(True, ls="--", alpha=0.35)
    ax.legend(prop=fp, loc="upper right", fontsize=9)
    ax.set_title("касательные", fontproperties=fp, fontsize=11)
    fig.tight_layout()
    fig.savefig(path, facecolor=fig.get_facecolor())
    plt.close()


def sheet_titul_z1a():
    im, d = notebook(34)
    write(d, 1, "Практическая работа № 2", 26, bold=True)
    write(d, 2, "Решение нелинейных уравнений", 22)
    write(d, 3, "Вариант  19", 22)

    write(d, 5, "Задание 1:", 24, BLUE, True)
    write(d, 6, "Отделить аналитически корни алгебраического уравнения.", 20)
    write(d, 7, "Уточнить наименьший по модулю корень методом хорд с точностью ε.", 20)
    write(d, 8, "Найти остальные корни, используя схему Горнера.", 20)
    write(d, 9, "4x³ − 2x² + 3x + 10 = 0          ε = 0,01", 24, bold=True)

    write(d, 11, "f(x)  =  4x³ − 2x² + 3x + 10", 22, bold=True)
    write(d, 12, "f'(x) =  12x² − 4x + 3", 22)
    write(d, 13, "f'(x) = 0:", 22, BLUE, True)
    write(d, 14, "12x² − 4x + 3 = 0", 22)
    write(d, 15, "D = 16 − 4·12·3 = 16 − 144 = −128 < 0", 22)
    write(d, 16, "критических точек нет,  f' > 0 всегда  →  f строго возрастает", 20)

    write(d, 18, "таблица знаков f(x)", 22, BLUE, True)
    r = table(
        d, 19,
        [140, 160, 160, 160, 160],
        ["x", "−∞", "−2", "−1", "+∞"],
        [["f(x)", "−", "−36", "+1", "+"]],
        fsize=20,
    )
    write(d, r + 1, "смена знака:   ξ ∈ [−2; −1]", 22, GREEN, True)
    write(d, r + 2, "единственный действительный = наименьший по модулю", 20)

    write(d, r + 4, "f''(x) = 24x − 4", 22, bold=True)
    write(d, r + 5, "таблица на концах отрезка", 22, BLUE, True)
    r = table(
        d, r + 6,
        [180, 220, 220],
        ["", "x = −2", "x = −1"],
        [
            ["f", "−36", "+1"],
            ["f'", "59", "19"],
            ["f''", "−52", "−28"],
            ["f · f''", "+  > 0", "−  < 0"],
        ],
        fsize=18,
    )
    write(d, r + 1, "f(a)·f''(a) > 0  →  неподвижен a = −2,   x₀ = b = −1", 21, GREEN, True)
    return im.crop((0, 0, W, (r + 3) * STEP))


def sheet_z1b():
    im, d = notebook(32)
    write(d, 1, "Задание 1  ·  хорды и Горнер", 24, BLUE, True)
    write(d, 2, "формула (4) методички, неподвижен a:", 20)
    write(d, 3, "xₙ₊₁ = xₙ − f(xₙ)·(xₙ − a) / (f(xₙ) − f(a))     x₀ = −1", 20, bold=True)
    write(d, 4, "a = −2,   f(a) = −36", 20)

    r = table(
        d, 6,
        [90, 210, 210, 220, 200],
        ["n", "xₙ", "f(xₙ)", "xₙ₊₁", "|Δx|"],
        [
            ["0", "−1,000000", "1,000000", "−1,027027", "0,027027"],
            ["1", "−1,027027", "0,476181", "−1,039729", "0,012702"],
            ["2", "−1,039729", "0,222805", "−1,045635", "0,005907"],
        ],
        fsize=17,
    )
    write(d, r + 1, "|xₙ₊₁ − xₙ| = 0,005907 ≤ 0,01  →  стоп", 21)
    write(d, r + 2, "ξ₁ = xₙ₊₁ = −1,046", 26, GREEN, True)

    write(d, r + 4, "схема Горнера   (деление на x − ξ,   ξ = −1,045635)", 20, BLUE, True)
    r = table(
        d, r + 5,
        [200, 180, 200, 200, 190],
        ["", "4", "−2", "3", "10"],
        [
            ["ξ · bᵢ₋₁", "—", "−4,182541", "6,464684", "−9,896608"],
            ["bᵢ", "4", "−6,182541", "9,464684", "0,103 ≈ 0"],
        ],
        fsize=16,
    )
    write(d, r + 1, "4x² − 6,182541 x + 9,464684 = 0", 21, bold=True)
    write(d, r + 2, "D = 38,224 − 151,435 = −113,21 < 0", 21)
    write(d, r + 3, "остальные корни комплексные", 21)
    write(d, r + 5, "ξ₂,₃ = 0,773 ± 1,330 i", 26, GREEN, True)
    write(d, r + 6, "наименьший по модулю действительный:   ξ₁ = −1,046", 20)
    return im.crop((0, 0, W, (r + 8) * STEP))


def sheet_z2():
    gpath = OUT / "_tmp_g2.png"
    graph_task2(gpath)
    gim = Image.open(gpath).convert("RGB")
    gim = gim.resize((480, int(480 * gim.height / gim.width)), Image.Resampling.LANCZOS)

    im, d = notebook(40)
    write(d, 1, "Задание 2:", 24, BLUE, True)
    write(d, 2, "Отделить графически корни. Уточнить наименьший по модулю", 20)
    write(d, 3, "корень уравнения методом касательных с точностью ε.", 20)
    write(d, 4, "2x² = 0,5x + 2          ε = 0,001", 24, bold=True)

    write(d, 6, "g(x) = 2x² − 0,5x − 2 = 0", 22, bold=True)
    write(d, 7, "y₁ = 2x²          y₂ = 0,5x + 2", 22)
    write(d, 8, "g'(x) = 4x − 0,5          g''(x) = 4", 22)

    write(d, 10, "точки для графика", 20, BLUE, True)
    table(
        d, 11,
        [120, 140, 160, 140],
        ["x", "2x²", "0,5x+2", "g(x)"],
        [
            ["−2", "8", "1", "7"],
            ["−1", "2", "1,5", "0,5"],
            ["0", "0", "2", "−2"],
            ["1", "2", "2,5", "−0,5"],
            ["2", "8", "3", "5"],
        ],
        fsize=17,
    )
    im.paste(gim, (670, 9 * STEP))
    write(d, 18, "ξ ∈ [−1; 0]   и   ξ ∈ [1; 2]", 21)
    write(d, 19, "меньший по | |  на  [−1; 0]", 22, GREEN, True)

    write(d, 21, "таблица на концах [−1; 0]", 21, BLUE, True)
    r = table(
        d, 22,
        [180, 220, 220],
        ["", "a = −1", "b = 0"],
        [
            ["g", "+0,5", "−2"],
            ["g'", "−4,5", "−0,5"],
            ["g''", "+4", "+4"],
            ["g · g''", "+  > 0", "−  < 0"],
        ],
        fsize=18,
    )
    write(d, r + 1, "g(a)·g''(a) > 0  →  x₀ = a = −1", 21, GREEN, True)
    write(d, r + 2, "xₙ₊₁ = xₙ − g(xₙ)/g'(xₙ)", 21, bold=True)

    r = table(
        d, r + 4,
        [90, 210, 210, 210, 200],
        ["n", "x", "g(x)", "g'(x)", "Δx"],
        [
            ["0", "−1,000000", "0,500000", "−4,500000", "+0,111111"],
            ["1", "−0,888889", "0,024691", "−4,055556", "+0,006088"],
            ["2", "−0,882801", "0,000074", "−4,031202", "+0,000018"],
        ],
        fsize=17,
    )
    write(d, r + 1, "|Δx| = 0,000018 ≤ 0,001  →  стоп", 21)
    write(d, r + 2, "ξ = −0,8828", 26, GREEN, True)
    gpath.unlink(missing_ok=True)
    return im.crop((0, 0, W, (r + 4) * STEP))


def main():
    a = sheet_titul_z1a()
    b = sheet_z1b()
    c = sheet_z2()
    files = [
        (OUT / "pr2_zadanie1a.png", a),
        (OUT / "pr2_zadanie1b.png", b),
        (OUT / "pr2_zadanie2.png", c),
    ]
    # one long z1 for convenience
    z1 = Image.new("RGB", (W, a.height + b.height), PAPER)
    z1.paste(a, (0, 0))
    z1.paste(b, (0, a.height))
    files.append((OUT / "pr2_zadanie1.png", z1))
    for p, im in files:
        im.save(p, "PNG", optimize=True)
        print(p, im.size)


if __name__ == "__main__":
    main()
