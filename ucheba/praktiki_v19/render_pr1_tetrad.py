#!/usr/bin/env python3
"""Практическая 1, вариант 19 — лист, который переписывают в тетрадь."""

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
W = 1280
STEP = 40
LEFT = 96


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
    d.line([(70, 0), (70, h)], fill=MARGIN, width=2)
    return im, d


def write(d, row, s, sz=21, fill=INK, bold=False):
    d.text((LEFT, row * STEP + 8), s, font=F(sz, bold), fill=fill)


def answer(d, row, s):
    y = row * STEP + 2
    d.rounded_rectangle(
        [LEFT - 16, y, W - 40, y + STEP + 10],
        radius=12,
        fill=(220, 245, 226),
        outline=GREEN,
        width=3,
    )
    d.text((LEFT, y + 6), s, font=F(28, True), fill=GREEN)


def sheet_z1():
    im, d = notebook(42)
    write(d, 1, "Практическая работа № 1", 28, bold=True)
    write(d, 2, "Тема: Погрешности вычислений          Вариант 19", 21)

    write(d, 4, "Задание 1", 24, BLUE, True)
    write(d, 5, "X = √(c · d / b)", 24, bold=True)
    write(d, 6, "b = 1,84 ± 0,06", 21)
    write(d, 7, "c = 0,8345 ± 0,0004", 21)
    write(d, 8, "d = 13,8 ± 0,3", 21)

    write(d, 10, "1. Значение", 22, BLUE, True)
    write(d, 11, "c · d = 0,8345 · 13,8 = 11,5161", 21)
    write(d, 12, "c · d / b = 11,5161 / 1,84 = 6,25875", 21)
    write(d, 13, "X = √6,25875 = 2,501749", 21, bold=True)

    write(d, 15, "2. Относительная погрешность", 22, BLUE, True)
    write(d, 16, "произведение:  δ*(c·d) = δ*c + δ*d", 21)
    write(d, 17, "частное:  δ*(c·d / b) = δ*c + δ*d + δ*b", 21)
    write(d, 18, "корень:  δ*X = (1/2) · (δ*c + δ*d + δ*b)", 21, bold=True)
    write(d, 19, "δ*c = 0,0004 / 0,8345 = 0,000479", 21)
    write(d, 20, "δ*d = 0,3 / 13,8 = 0,021739", 21)
    write(d, 21, "δ*b = 0,06 / 1,84 = 0,032609", 21)
    write(d, 22, "сумма = 0,054827", 21)
    write(d, 23, "δ*X = 0,054827 / 2 = 0,027414 ≈ 2,74%", 21, bold=True)

    write(d, 25, "3. Абсолютная погрешность", 22, BLUE, True)
    write(d, 26, "Δ*X = δ*X · |X| = 0,027414 · 2,501749 = 0,06858", 21)

    write(d, 28, "4. Запись ответа", 22, BLUE, True)
    write(d, 29, "Δ* с избытком: первая цифра 6 → одна значащая цифра → 0,07", 20)
    write(d, 30, "X до того же разряда (сотые). Правило II: отбрасываем 1 < 5", 20)
    write(d, 31, "2,501749 → 2,50", 21)
    write(d, 32, "Δокр = |2,501749 − 2,50| = 0,00175", 21)
    write(d, 33, "Δ* = 0,06858 + 0,00175 = 0,07033", 21)
    write(d, 34, "0,07033 > 0,07, одна цифра с избытком → 0,08", 21, bold=True)
    answer(d, 36, "X = 2,50 ± 0,08")
    return im.crop((0, 0, W, 38 * STEP))


def sheet_z2():
    im, d = notebook(50)
    write(d, 1, "Практическая работа № 1", 28, bold=True)
    write(d, 2, "Тема: Погрешности вычислений          Вариант 19", 21)

    write(d, 4, "Задание 2", 24, BLUE, True)
    write(d, 5, "X = (a + b)² / (m · ∛n − a)", 24, bold=True)
    write(d, 6, "корень только над n", 20, BLUE)
    write(d, 7, "a = 9,37 ± 0,04          b = 3,108 ± 0,003", 21)
    write(d, 8, "m = 0,46 ± 0,02          n = 15,2 ± 0,4", 21)

    write(d, 10, "1. Значение", 22, BLUE, True)
    write(d, 11, "a + b = 12,478          (a + b)² = 155,700484", 21)
    write(d, 12, "∛n = ∛15,2 = 2,477125", 21)
    write(d, 13, "m · ∛n = 0,46 · 2,477125 = 1,139477", 21)
    write(d, 14, "m · ∛n − a = 1,139477 − 9,37 = −8,230523", 21)
    write(d, 15, "X = 155,700484 / (−8,230523) = −18,91745", 21, bold=True)

    write(d, 17, "2. Относительная погрешность", 22, BLUE, True)
    write(d, 18, "сумма:  Δ*(a+b) = 0,04 + 0,003 = 0,043", 21)
    write(d, 19, "δ*(a+b) = 0,043 / 12,478 = 0,003446", 21)
    write(d, 20, "степень:  δ*((a+b)²) = 2 · 0,003446 = 0,006892", 21)
    write(d, 21, "δ*n = 0,4 / 15,2 = 0,026316", 21)
    write(d, 22, "корень:  δ*(∛n) = 0,026316 / 3 = 0,008772", 21)
    write(d, 23, "δ*m = 0,02 / 0,46 = 0,043478", 21)
    write(d, 24, "произведение:  δ*(m·∛n) = 0,043478 + 0,008772 = 0,052250", 20)
    write(d, 25, "Δ*(m·∛n) = 0,052250 · 1,139477 = 0,05954", 21)
    write(d, 26, "разность:  Δ* = 0,05954 + 0,04 = 0,09954", 21)
    write(d, 27, "δ* = 0,09954 / 8,230523 = 0,012094", 21)
    write(d, 28, "частное:  δ*X = 0,006892 + 0,012094 = 0,018986 ≈ 1,90%", 20, bold=True)

    write(d, 30, "3. Абсолютная погрешность", 22, BLUE, True)
    write(d, 31, "Δ*X = 0,018986 · 18,91745 = 0,35916", 21)

    write(d, 33, "4. Запись ответа", 22, BLUE, True)
    write(d, 34, "Δ* с избытком: первая цифра 3 → две значащие цифры → 0,36", 20)
    write(d, 35, "X до того же разряда (сотые). Правило I: отбрасываем 7 > 5", 20)
    write(d, 36, "−18,91745 → −18,92", 21)
    write(d, 37, "Δокр = |−18,91745 − (−18,92)| = 0,00255", 21)
    write(d, 38, "Δ* = 0,35916 + 0,00255 = 0,36171", 21)
    write(d, 39, "остаток после 0,36 не ноль → с избытком 0,37", 21, bold=True)
    answer(d, 41, "X = −18,92 ± 0,37")
    return im.crop((0, 0, W, 43 * STEP))


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
