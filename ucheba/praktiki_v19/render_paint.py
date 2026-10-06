#!/usr/bin/env python3
"""Paint-style sheets for practical works 1, 2, 5 — variant 19."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

BG = (255, 251, 240)
INK = (28, 28, 28)
RED = (196, 40, 40)
GREEN = (22, 122, 58)
BLUE = (28, 90, 168)
YELLOW = (255, 210, 70)
PAPER_Y = (255, 248, 210)
PAPER_B = (220, 236, 255)
PAPER_P = (238, 226, 255)
PAPER_G = (220, 245, 226)
PAPER_O = (255, 228, 180)
LINE = (50, 50, 50)
WHITE = (255, 255, 255)
W = 1200


def F(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size)


def comma(x, n=6):
    return f"{x:.{n}f}".replace(".", ",")


def txt(d, xy, s, size=26, fill=INK, bold=False, anchor="lt"):
    d.text(xy, s, font=F(size, bold), fill=fill, anchor=anchor)


def table(d, origin, col_w, row_h, headers, rows, fills, head=YELLOW, fsize=20):
    x0, y0 = origin
    x = x0
    for i, h in enumerate(headers):
        box = [x, y0, x + col_w[i], y0 + row_h]
        d.rectangle(box, fill=head, outline=LINE, width=3)
        txt(d, (x + col_w[i] / 2, y0 + row_h / 2), h, fsize, bold=True, anchor="mm")
        x += col_w[i]
    for r, row in enumerate(rows):
        x = x0
        y = y0 + (r + 1) * row_h
        last = r == len(rows) - 1
        for i, cell in enumerate(row):
            if last:
                fill = PAPER_O
            elif cell == "":
                fill = (242, 242, 242)
            else:
                fill = fills[i]
            box = [x, y, x + col_w[i], y + row_h]
            d.rectangle(box, fill=fill, outline=LINE, width=3)
            txt(d, (x + col_w[i] / 2, y + row_h / 2), cell, fsize - 1, bold=last, anchor="mm")
            x += col_w[i]


def new_im(h):
    return Image.new("RGB", (W, h), BG)


def stack(parts):
    h = sum(p.height for p in parts)
    out = Image.new("RGB", (W, h), BG)
    y = 0
    for p in parts:
        out.paste(p, (0, y))
        y += p.height
    return out


def banner(title, lines, fill=(40, 40, 40)):
    im = new_im(100 + 36 * len(lines))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 78], fill=fill)
    txt(d, (W / 2, 39), title, 32, (255, 255, 255), True, "mm")
    yy = 96
    for line in lines:
        txt(d, (40, yy), line, 24)
        yy += 36
    return im


def box_lines(title, lines, h, fill=WHITE, title_c=BLUE):
    im = new_im(h)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([40, 16, 1160, h - 16], radius=16, fill=fill, outline=LINE, width=3)
    txt(d, (60, 32), title, 24, title_c, True)
    yy = 78
    for line, kw in lines:
        txt(d, (60, yy), line, kw.get("size", 24), kw.get("fill", INK), kw.get("bold", False))
        yy += kw.get("gap", 40)
    return im


def sheet_pr1():
    parts = [
        banner(
            "Практика 1  ·  вариант 19  ·  погрешности",
            [
                "Задание 1:  X = √(c·d / b)",
                "Задание 2:  X = (a+b)² / (m·∛n − a)",
            ],
        )
    ]
    # task 1
    im = new_im(620)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 54], fill=YELLOW)
    txt(d, (W / 2, 27), "1.   X = √(c·d / b)", 28, bold=True, anchor="mm")
    txt(d, (40, 72), "b = 1,84 ± 0,06     c = 0,8345 ± 0,0004     d = 13,8 ± 0,3", 24)
    txt(d, (40, 118), "X = √(0,8345 · 13,8 / 1,84) = √6,25875 = 2,501749", 24, bold=True)
    txt(d, (40, 168), "ln X = ½ ln c + ½ ln d − ½ ln b", 24, BLUE, True)
    txt(d, (40, 214), "δX = ½ (Δc/c + Δd/d + Δb/b)", 24)
    txt(d, (40, 260), "  = ½ (0,0004/0,8345 + 0,3/13,8 + 0,06/1,84) = 0,027414", 24)
    txt(d, (40, 306), "ΔX = 0,027414 · 2,501749 = 0,06858", 24)
    d.rounded_rectangle([40, 370, 1160, 580], radius=16, fill=PAPER_G, outline=GREEN, width=4)
    txt(d, (60, 400), "ответ", 24, GREEN, True)
    txt(d, (60, 460), "X = 2,50  ±  0,07", 40, GREEN, True)
    parts.append(im)

    im = new_im(600)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 54], fill=(180, 220, 255))
    txt(d, (W / 2, 27), "2.   X = (a+b)² / (m · ∛n − a)", 26, bold=True, anchor="mm")
    txt(d, (40, 72), "a=9,37±0,04   b=3,108±0,003   m=0,46±0,02   n=15,2±0,4", 22)
    txt(d, (40, 116), "∛15,2 = 2,477125     знаменатель = 0,46·2,477125 − 9,37 = −8,230523", 22)
    txt(d, (40, 160), "(a+b)² = 12,478² = 155,700484     X = 155,700484 / (−8,230523) = −18,91745", 22, bold=True)
    txt(d, (40, 210), "u=a+b,  v=m·∛n−a,   Δu=0,043", 24, BLUE, True)
    txt(d, (40, 256), "Δv = ∛n·Δm + m/(3 n⅔)·Δn + Δa = 0,09954", 24)
    txt(d, (40, 302), "δX = 2·Δu/|u| + Δv/|v| = 0,01899     ΔX = 0,359", 24)
    d.rounded_rectangle([40, 370, 1160, 560], radius=16, fill=PAPER_G, outline=GREEN, width=4)
    txt(d, (60, 400), "ответ   (корень только от n, a снаружи)", 24, GREEN, True)
    txt(d, (60, 470), "X = −18,92  ±  0,36", 40, GREEN, True)
    parts.append(im)
    return stack(parts)


def sheet_pr2():
    def f(x):
        return 4 * x**3 - 2 * x**2 + 3 * x + 10

    parts = [
        banner(
            "Практика 2  ·  вариант 19  ·  хорды и касательные",
            [
                "1)  4x³ − 2x² + 3x + 10 = 0     ε = 0,01",
                "2)  2x² = 0,5ˣ + 2             ε = 0,001",
            ],
        )
    ]
    im = new_im(520)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 54], fill=YELLOW)
    txt(d, (W / 2, 27), "1. отделение корня + хорды", 28, bold=True, anchor="mm")
    txt(d, (40, 72), "f' = 12x² − 4x + 3 > 0 всегда  →  один действительный корень", 22)
    txt(d, (40, 112), "f(−2)= −36 < 0,   f(−1)= 1 > 0   →   ξ ∈ [−2; −1]", 24, bold=True)
    txt(d, (40, 158), "f''=24x−4 < 0 на отрезке.  f(−2)·f''(−2)>0  →  неподвижен a=−2", 22)
    txt(d, (40, 204), "xₙ₊₁ = xₙ − f(xₙ)·(xₙ − a) / (f(xₙ) − f(a))     x₀ = −1", 22, BLUE, True)
    headers = ["n", "xₙ", "f(xₙ)", "xₙ₊₁", "|Δx|"]
    col_w = [80, 220, 220, 220, 220]
    rows = [
        ["0", "−1,000000", "1,000000", "−1,027027", "0,027027"],
        ["1", "−1,027027", "0,476181", "−1,039729", "0,012702"],
        ["2", "−1,039729", "0,222805", "−1,045635", "0,005907 < ε"],
    ]
    table(d, (40, 250), col_w, 48, headers, rows, [WHITE] * 5)
    parts.append(im)

    im = new_im(420)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([40, 20, 1160, 180], radius=16, fill=PAPER_G, outline=GREEN, width=4)
    txt(d, (60, 50), "наименьший корень  ξ₁ = −1,046", 32, GREEN, True)
    txt(d, (60, 110), "Горнер:  4x² − 6,182541 x + 9,464684 = 0,   D < 0", 24)
    d.rounded_rectangle([40, 200, 1160, 380], radius=16, fill=WHITE, outline=LINE, width=3)
    txt(d, (60, 230), "остальные корни комплексные", 24, BLUE, True)
    txt(d, (60, 290), "ξ₂,₃  =  0,773  ±  1,330 i", 32, bold=True)
    parts.append(im)

    im = new_im(820)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 54], fill=PAPER_P)
    txt(d, (W / 2, 27), "2. график + касательные", 28, bold=True, anchor="mm")
    txt(d, (40, 70), "g(x) = 2x² − 0,5ˣ − 2 = 0     y₁=2x²   y₂=0,5ˣ+2", 22)
    headers = ["x", "2x²", "0,5ˣ+2", "g(x)"]
    col_w = [160, 220, 220, 220]
    rows = [
        ["−2", "8", "6", "+2"],
        ["−1,5", "4,5", "4,828", "−0,328"],
        ["−1", "2", "4", "−2"],
        ["0", "0", "3", "−3"],
        ["1", "2", "2,5", "−0,5"],
        ["1,5", "4,5", "2,354", "+2,146"],
        ["2", "8", "2,25", "+5,75"],
    ]
    table(d, (40, 110), col_w, 44, headers, rows, [WHITE, PAPER_Y, PAPER_B, PAPER_G], head=PAPER_P, fsize=20)
    txt(d, (40, 490), "знаки: [−2; −1,5] и [1; 1,5].  Меньший по | | — на [1; 1,5].", 22, bold=True)
    txt(d, (40, 534), "g(1,5)·g''(1,5)>0  →  x₀=1,5", 22)
    headers = ["n", "xₙ", "g", "g'", "xₙ₊₁", "|Δx|"]
    col_w = [70, 190, 180, 180, 190, 170]
    rows = [
        ["0", "1,500000", "2,146447", "6,245065", "1,156297", "0,343703"],
        ["1", "1,156297", "0,225383", "4,936178", "1,110638", "0,045660"],
        ["2", "1,110638", "0,003942", "4,763540", "1,109810", "0,000828"],
    ]
    table(d, (30, 580), col_w, 46, headers, rows, [WHITE] * 6, head=PAPER_P, fsize=18)
    parts.append(im)

    im = new_im(180)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([40, 20, 1160, 150], radius=16, fill=PAPER_G, outline=GREEN, width=4)
    txt(d, (60, 70), "ответ   ξ = 1,1098", 36, GREEN, True)
    parts.append(im)
    return stack(parts)


def sheet_pr5():
    parts = [
        banner(
            "Практика 5  ·  вариант 19  ·  интегралы",
            [
                "1) трапеции n=16    ∫ dx / √(2x²+0,7)     [1,4; 2]",
                "2) Симпсон n=8      ∫ lg(x²+0,8)/(x−1) dx   [2,5; 3,3]",
            ],
        )
    ]
    a, b, n = 1.4, 2.0, 16
    h = (b - a) / n
    xs = [a + i * h for i in range(n + 1)]
    ys = [1 / math.sqrt(2 * x * x + 0.7) for x in xs]
    s_end = ys[0] + ys[-1]
    s_mid = sum(ys[1:-1])
    I = h * (s_end / 2 + s_mid)

    im = new_im(1180)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 54], fill=YELLOW)
    txt(d, (W / 2, 27), "1. трапеции   n=16    h=(2−1,4)/16=0,0375", 26, bold=True, anchor="mm")
    headers = ["i", "x", "y края", "середина"]
    col_w = [90, 200, 300, 300]
    rows = []
    for i, (x, y) in enumerate(zip(xs, ys)):
        if i == 0 or i == n:
            rows.append([str(i), comma(x, 4), comma(y), ""])
        else:
            rows.append([str(i), comma(x, 4), "", comma(y)])
    rows.append(["Σ", "", comma(s_end), comma(s_mid)])
    table(d, (40, 70), col_w, 46, headers, rows, [WHITE, WHITE, PAPER_Y, PAPER_B], fsize=18)
    d.rounded_rectangle([40, 960, 1160, 1140], radius=16, fill=WHITE, outline=GREEN, width=4)
    txt(d, (60, 980), "I = h · ((y0+yn)/2 + Σ середин)", 24, BLUE, True)
    txt(d, (60, 1028), f"I = 0,0375 · ({comma(s_end)} / 2 + {comma(s_mid)}) = 0,237564", 24)
    txt(d, (60, 1084), "I ≈ 0,23756", 32, GREEN, True)
    parts.append(im)

    a2, b2, n2 = 2.5, 3.3, 8
    h2 = (b2 - a2) / (2 * n2)
    xs2 = [a2 + i * h2 for i in range(2 * n2 + 1)]
    ys2 = [math.log10(x * x + 0.8) / (x - 1) for x in xs2]
    s1 = ys2[0] + ys2[-1]
    s2 = sum(ys2[i] for i in range(1, 16, 2))
    s3 = sum(ys2[i] for i in range(2, 16, 2))
    I2 = (h2 / 3) * (s1 + 4 * s2 + 2 * s3)

    im = new_im(1220)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 54], fill=(180, 220, 255))
    txt(d, (W / 2, 27), "2. Симпсон   n=8    h=(3,3−2,5)/(2·8)=0,05     lg — десятичный", 24, bold=True, anchor="mm")
    txt(d, (40, 64), "после края ритм  4  2  4  2  …  4   края ×1", 22, RED, True)
    headers = ["i", "x", "края ×1", "нечёт ×4", "чёт ×2"]
    col_w = [80, 150, 240, 240, 240]
    m = 16
    rows = []
    for i, (x, y) in enumerate(zip(xs2, ys2)):
        if i == 0 or i == m:
            rows.append([str(i), comma(x, 2), comma(y), "", ""])
        elif i % 2 == 1:
            rows.append([str(i), comma(x, 2), "", comma(y), ""])
        else:
            rows.append([str(i), comma(x, 2), "", "", comma(y)])
    rows.append(["Σ", "", comma(s1), comma(s2), comma(s3)])
    table(d, (40, 104), col_w, 44, headers, rows, [WHITE, WHITE, PAPER_Y, PAPER_B, PAPER_P], head=(180, 220, 255), fsize=17)
    d.rounded_rectangle([40, 980, 1160, 1180], radius=16, fill=WHITE, outline=GREEN, width=4)
    txt(d, (60, 1000), "S = Σкр + 4·Σнеч + 2·Σчёт = 24,476159", 24, BLUE, True)
    txt(d, (60, 1050), "I = (0,05 / 3) · 24,476159    ← сначала скобка, потом ×", 24)
    txt(d, (60, 1110), "I ≈ 0,40794", 32, GREEN, True)
    parts.append(im)
    return stack(parts)


def main():
    files = [
        ("pr1_pogreshnosti.png", sheet_pr1()),
        ("pr2_korni.png", sheet_pr2()),
        ("pr5_integraly.png", sheet_pr5()),
    ]
    for name, im in files:
        p = OUT / name
        im.save(p, "PNG", optimize=True)
        print(p, im.size)


if __name__ == "__main__":
    main()
