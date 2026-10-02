#!/usr/bin/env python3
"""Практическая 1, вариант 19 — оформление как в тетради с фото."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (252, 252, 244)
GRID = (214, 226, 236)
MARGIN = (214, 150, 150)
INK = (28, 28, 28)
GREEN = (22, 122, 58)
BLUE = (28, 90, 168)
W = 1100
STEP = 40
LEFT = 88


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
    d.line([(64, 0), (64, h)], fill=MARGIN, width=2)
    return im, d


def write(d, row, s, sz=24, fill=INK, bold=False):
    d.text((LEFT, row * STEP + 7), s, font=F(sz, bold), fill=fill)


def sheet_z1():
    im, d = notebook(28)
    write(d, 1, "Практическая работа № 1", 26, bold=True)
    write(d, 2, "Тема:  Погрешности вычислений", 24)
    write(d, 3, "Вариант  19", 24)

    write(d, 5, "Задание 1:", 26, BLUE, True)
    write(d, 6, "X  =  √(c · d / b)", 28, bold=True)

    write(d, 8, "b  =  1,84  ±  0,066", 24)
    write(d, 9, "c  =  0,8345  ±  0,0004", 24)
    write(d, 10, "d  =  13,8  ±  0,3", 24)

    write(d, 12, "X  =  √(0,8345 · 13,8 / 1,84)  =  √6,25875  =  2,501749", 22, bold=True)

    write(d, 14, "δX  =  ½ δc  +  ½ δd  +  ½ δb  =", 24)
    write(d, 15, "     =  Δc/(2|c|)  +  Δd/(2|d|)  +  Δb/(2|b|)  =", 24)
    write(d, 16, "     =  0,0004/(2·0,8345)  +  0,3/(2·13,8)  +  0,066/(2·1,84)  =", 21)
    write(d, 17, "     =  0,000240  +  0,010870  +  0,017935  =  0,029044", 22)

    write(d, 19, "≈  2,9 %", 24, bold=True)

    write(d, 21, "ΔX  =  0,029044 · 2,501749  =  0,07266", 24)
    write(d, 22, "округляем ΔX с избытком:   0,08", 24)
    write(d, 23, "X округляем до того же знака", 22)

    write(d, 25, "X  =  2,50  ±  0,08", 30, GREEN, True)
    return im.crop((0, 0, W, 27 * STEP))


def sheet_z2():
    im, d = notebook(38)
    write(d, 1, "Практическая работа № 1", 26, bold=True)
    write(d, 2, "Тема:  Погрешности вычислений", 24)
    write(d, 3, "Вариант  19", 24)

    write(d, 5, "Задание 2:", 26, BLUE, True)
    write(d, 6, "X  =  (a + b)²  /  (m · ∛(n − a))", 26, bold=True)

    write(d, 8, "a  =  9,37  ±  0,04", 24)
    write(d, 9, "b  =  3,108  ±  0,003", 24)
    write(d, 10, "m  =  0,46  ±  0,02", 24)
    write(d, 11, "n  =  15,2  ±  0,4", 24)

    write(d, 13, "n − a  =  15,2 − 9,37  =  5,83", 24)
    write(d, 14, "∛(n − a)  =  ∛5,83  =  1,799794", 24)
    write(d, 15, "a + b  =  12,478      (a + b)²  =  155,700484", 24)
    write(d, 16, "m · ∛(n − a)  =  0,46 · 1,799794  =  0,827905", 24)
    write(d, 17, "X  =  155,700484 / 0,827905  =  188,06556", 24, bold=True)

    write(d, 19, "δX  =  2 δ(a+b)  +  δm  +  (1/3) δ(n−a)  =", 24)
    write(d, 20, "     =  2 Δ(a+b)/|a+b|  +  Δm/|m|  +  (1/3) Δ(n−a)/|n−a|", 22)
    write(d, 21, "Δ(a+b)  =  0,04 + 0,003  =  0,043", 24)
    write(d, 22, "Δ(n−a)  =  0,4 + 0,04  =  0,44", 24)
    write(d, 23, "     =  2·0,043/12,478  +  0,02/0,46  +  (1/3)·0,44/5,83  =", 21)
    write(d, 24, "     =  0,006892  +  0,043478  +  0,025157  =  0,075528", 22)

    write(d, 26, "≈  7,6 %", 24, bold=True)

    write(d, 28, "ΔX  =  0,075528 · 188,06556  =  14,204", 24)
    write(d, 29, "округляем ΔX с избытком:   15", 24)
    write(d, 30, "X округляем до единиц (тот же знак)", 22)

    write(d, 32, "X  =  188  ±  15", 30, GREEN, True)
    return im.crop((0, 0, W, 34 * STEP))


def main():
    p1 = OUT / "pr1_zadanie1.png"
    p2 = OUT / "pr1_zadanie2.png"
    z1 = sheet_z1()
    z2 = sheet_z2()
    z1.save(p1, "PNG", optimize=True)
    z2.save(p2, "PNG", optimize=True)
    print(p1, z1.size)
    print(p2, z2.size)


if __name__ == "__main__":
    main()
