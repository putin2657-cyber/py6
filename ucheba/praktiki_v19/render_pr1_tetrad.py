#!/usr/bin/env python3
"""Практическая 1, вариант 19 — по методичкам: действия и верные цифры."""

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
W = 1240
STEP = 42
LEFT = 92


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
    d.line([(68, 0), (68, h)], fill=MARGIN, width=2)
    return im, d


def write(d, row, s, sz=22, fill=INK, bold=False):
    d.text((LEFT, row * STEP + 8), s, font=F(sz, bold), fill=fill)


def answer(d, row, s):
    y = row * STEP + 4
    d.rounded_rectangle(
        [LEFT - 16, y, W - 48, y + STEP + 8],
        radius=12,
        fill=(220, 245, 226),
        outline=GREEN,
        width=3,
    )
    d.text((LEFT, y + 8), s, font=F(28, True), fill=GREEN)


def sheet_z1():
    im, d = notebook(40)
    write(d, 1, "Практическая работа № 1", 28, bold=True)
    write(d, 2, "Тема:  Погрешности вычислений", 22)
    write(d, 3, "Вариант  19", 22)

    write(d, 5, "Задание 1", 26, BLUE, True)
    write(d, 6, "X  =  √( c · d  /  b )", 26, bold=True)
    write(d, 8, "b  =  1,84  ±  0,06", 22)
    write(d, 9, "c  =  0,8345  ±  0,0004", 22)
    write(d, 10, "d  =  13,8  ±  0,3", 22)

    write(d, 12, "Значение", 22, BLUE, True)
    write(d, 13, "c · d  =  0,8345 · 13,8  =  11,5161", 22)
    write(d, 14, "c · d / b  =  11,5161 / 1,84  =  6,25875", 22)
    write(d, 15, "X  =  √6,25875  =  2,501749", 22, bold=True)

    write(d, 17, "Погрешность по действиям", 22, BLUE, True)
    write(d, 18, "произведение:   δ*(c·d)  =  δ*c + δ*d", 22)
    write(d, 19, "частное:   δ*(c·d / b)  =  δ*c + δ*d + δ*b", 22)
    write(d, 20, "корень:   δ*X  =  (1/2) · (δ*c + δ*d + δ*b)", 22, bold=True)

    write(d, 22, "δ*c  =  0,0004 / 0,8345  =  0,000479", 22)
    write(d, 23, "δ*d  =  0,3 / 13,8  =  0,021739", 22)
    write(d, 24, "δ*b  =  0,06 / 1,84  =  0,032609", 22)
    write(d, 25, "сумма  =  0,054827", 22)
    write(d, 26, "δ*X  =  0,054827 / 2  =  0,027414", 22, bold=True)
    write(d, 27, "δ*X  ≈  2,74 %", 22, bold=True)
    write(d, 29, "Δ*X  =  δ*X · |X|  =  0,027414 · 2,501749  =  0,06858", 22)

    write(d, 31, "Верные цифры:  Δ*X ≤ 0,1  и  Δ*X > 0,01  →  две", 22)
    write(d, 32, "Округление до 2,5.  Правило II: отбрасываем 0 < 5", 22)
    write(d, 33, "Δокр  =  |2,501749 − 2,5|  =  0,00175", 22)
    write(d, 34, "Δ*  =  Δ*X + Δокр  =  0,06858 + 0,00175  =  0,07033", 22)
    answer(d, 36, "X  =  2,5  ±  0,071")
    return im.crop((0, 0, W, 38 * STEP))


def sheet_z2():
    im, d = notebook(52)
    write(d, 1, "Практическая работа № 1", 28, bold=True)
    write(d, 2, "Тема:  Погрешности вычислений", 22)
    write(d, 3, "Вариант  19", 22)

    write(d, 5, "Задание 2", 26, BLUE, True)
    write(d, 6, "X  =  (a + b)²  /  ( m · ∛n  −  a )", 24, bold=True)
    write(d, 7, "корень только над n", 20, BLUE)

    write(d, 8, "a = 9,37 ± 0,04     b = 3,108 ± 0,003", 22)
    write(d, 9, "m = 0,46 ± 0,02     n = 15,2 ± 0,4", 22)

    write(d, 11, "Значение", 22, BLUE, True)
    write(d, 12, "a + b  =  12,478          (a + b)²  =  155,700484", 22)
    write(d, 13, "∛n  =  ∛15,2  =  2,477125", 22)
    write(d, 14, "m · ∛n  =  0,46 · 2,477125  =  1,139477", 22)
    write(d, 15, "m · ∛n − a  =  1,139477 − 9,37  =  −8,230523", 22)
    write(d, 16, "X  =  155,700484 / (−8,230523)  =  −18,91745", 22, bold=True)

    write(d, 18, "Погрешность по действиям", 22, BLUE, True)
    write(d, 19, "сумма:   Δ*(a+b)  =  Δ*a + Δ*b  =  0,043", 22)
    write(d, 20, "δ*(a+b)  =  0,043 / 12,478  =  0,003446", 22)
    write(d, 21, "степень:   δ*((a+b)²)  =  2 · 0,003446  =  0,006892", 22)

    write(d, 23, "δ*n  =  0,4 / 15,2  =  0,026316", 22)
    write(d, 24, "корень:   δ*(∛n)  =  0,026316 / 3  =  0,008772", 22)
    write(d, 25, "δ*m  =  0,02 / 0,46  =  0,043478", 22)
    write(d, 26, "произведение:   δ*(m·∛n)  =  0,043478 + 0,008772  =  0,052250", 21)
    write(d, 27, "Δ*(m·∛n)  =  0,052250 · 1,139477  =  0,05954", 22)
    write(d, 28, "разность:   Δ*(m·∛n − a)  =  0,05954 + 0,04  =  0,09954", 22)
    write(d, 29, "δ*(m·∛n − a)  =  0,09954 / 8,230523  =  0,012094", 22)

    write(d, 31, "частное:   δ*X  =  0,006892 + 0,012094  =  0,018986", 22, bold=True)
    write(d, 32, "δ*X  ≈  1,90 %", 22, bold=True)
    write(d, 33, "Δ*X  =  0,018986 · 18,91745  =  0,35916", 22)

    write(d, 35, "Верные цифры:  Δ*X ≤ 1  и  Δ*X > 0,1  →  две", 22)
    write(d, 36, "Округление до −19.  Правило I: отбрасываем 9 > 5", 22)
    write(d, 37, "Δокр  =  |−18,91745 − (−19)|  =  0,08255", 22)
    write(d, 38, "Δ*  =  0,35916 + 0,08255  =  0,44171", 22)
    answer(d, 40, "X  =  −19  ±  0,442")
    return im.crop((0, 0, W, 42 * STEP))


def main():
    z1 = sheet_z1()
    z2 = sheet_z2()
    p1 = OUT / "pr1_zadanie1.png"
    p2 = OUT / "pr1_zadanie2.png"
    z1.save(p1, "PNG", optimize=True)
    z2.save(p2, "PNG", optimize=True)
    print(p1, z1.size)
    print(p2, z2.size)


if __name__ == "__main__":
    main()
