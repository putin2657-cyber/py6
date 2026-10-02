#!/usr/bin/env python3
"""KR-3 paint sheets: tables as in the methodichka, one PNG per variant."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "variants"
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
    s = f"{x:.{n}f}".replace(".", ",")
    return s


def comma_h(x):
    """Step h: 1 decimal if it is 0.1/0.2, else 4 decimals."""
    if abs(x * 10 - round(x * 10)) < 1e-9:
        return comma(x, 1)
    return comma(x, 4)


def comma_x(x):
    """Nodes: 1 decimal if it lands on tenths, else 4."""
    if abs(x * 10 - round(x * 10)) < 1e-9:
        return comma(x, 1)
    return comma(x, 4)


def txt(d, xy, s, size=26, fill=INK, bold=False, anchor="lt"):
    d.text(xy, s, font=F(size, bold), fill=fill, anchor=anchor)


def table(d, origin, col_w, row_h, headers, rows, fills, head=YELLOW, fsize=22):
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
            txt(
                d,
                (x + col_w[i] / 2, y + row_h / 2),
                cell,
                fsize - (2 if last else 0),
                bold=last,
                anchor="mm",
            )
            x += col_w[i]


def new_im(h):
    return Image.new("RGB", (W, h), BG)


def trap_data(f, a, b, n=5):
    h = (b - a) / n
    xs = [a + i * h for i in range(n + 1)]
    ys = [f(x) for x in xs]
    s_end = ys[0] + ys[-1]
    s_mid = sum(ys[1:-1])
    I = h * (s_end / 2 + s_mid)
    return h, xs, ys, s_end, s_mid, I


def simp_data(f, a, b, n=3):
    h = (b - a) / (2 * n)
    m = 2 * n
    xs = [a + i * h for i in range(m + 1)]
    ys = [f(x) for x in xs]
    s1 = ys[0] + ys[-1]
    s2 = sum(ys[i] for i in range(1, m, 2))
    s3 = sum(ys[i] for i in range(2, m, 2))
    I = (h / 3) * (s1 + 4 * s2 + 2 * s3)
    return h, xs, ys, s1, s2, s3, I


def euler_data(f, x0, y0, h, steps=3):
    rows = []
    x, y = x0, y0
    for i in range(steps):
        yp = f(x, y)
        pred = y + h * yp
        xn = x + h
        corr = f(xn, pred)
        dy = (h / 2) * (yp + corr)
        yn = y + dy
        rows.append(dict(i=i, x=x, y=y, yp=yp, pred=pred, xn=xn, corr=corr, dy=dy, yn=yn))
        x, y = xn, yn
    return rows, y


def adams_data(f, xs, ys):
    h = xs[1] - xs[0]
    yps = [f(x, y) for x, y in zip(xs, ys)]
    ts = [h * yp for yp in yps]
    dt = [ts[i + 1] - ts[i] for i in range(3)]
    d2 = [dt[i + 1] - dt[i] for i in range(2)]
    d3 = d2[1] - d2[0]
    dy3 = ts[3] + 0.5 * dt[2] + (5 / 12) * d2[1] + (3 / 8) * d3
    y4 = ys[3] + dy3
    x4 = xs[3] + h
    return dict(h=h, yps=yps, ts=ts, dt=dt, d2=d2, d3=d3, dy3=dy3, x4=x4, y4=y4)


def section_trap(title, flabel, f, a, b, n=5):
    h, xs, ys, s_end, s_mid, I = trap_data(f, a, b, n)
    im = new_im(820)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 58], fill=YELLOW)
    txt(d, (W / 2, 29), title, 28, bold=True, anchor="mm")
    txt(d, (40, 78), flabel, 26, bold=True)
    txt(d, (40, 118), f"n = {n}    h = (b−a)/n = ({comma_x(b)}−{comma_x(a)})/{n} = {comma_h(h)}", 24, GREEN, True)
    headers = ["i", "x", "y0 и yn", "середина"]
    col_w = [90, 180, 280, 300]
    rows = []
    for i, (x, y) in enumerate(zip(xs, ys)):
        if i == 0 or i == n:
            rows.append([str(i), comma_x(x), comma(y), ""])
        else:
            rows.append([str(i), comma_x(x), "", comma(y)])
    rows.append(["Σ", "", comma(s_end), comma(s_mid)])
    table(d, (40, 165), col_w, 52, headers, rows, [WHITE, WHITE, PAPER_Y, PAPER_B])
    d.rounded_rectangle([40, 600, 1160, 790], radius=16, fill=WHITE, outline=LINE, width=3)
    txt(d, (60, 618), "I ≈ h · ((y0+yn)/2 + Σ середин)", 24, BLUE, True)
    txt(d, (60, 662), f"I = {comma_h(h)} · ({comma(s_end)} / 2  +  {comma(s_mid)})", 24)
    txt(d, (60, 704), f"  = {comma_h(h)} · ({comma(s_end/2)} + {comma(s_mid)}) = {comma_h(h)} · {comma(s_end/2 + s_mid)}", 24)
    txt(d, (60, 748), f"I ≈ {comma(I)}", 32, GREEN, True)
    return im, I


def section_simp(title, flabel, f, a, b, n=3):
    h, xs, ys, s1, s2, s3, I = simp_data(f, a, b, n)
    im = new_im(920)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 58], fill=(180, 220, 255))
    txt(d, (W / 2, 29), title, 28, bold=True, anchor="mm")
    txt(d, (40, 74), flabel, 26, bold=True)
    txt(d, (40, 114), f"В методичке h = (b−a)/(2n) !   n={n}  →  2n={2*n} шагов", 24, RED, True)
    txt(d, (40, 152), f"h = ({comma_x(b)}−{comma_x(a)})/{2*n} = {comma_h(h)}", 26, GREEN, True)
    headers = ["i", "x", "края y0,y2n", "нечёт (×4)", "чёт (×2)"]
    col_w = [80, 170, 240, 240, 240]
    m = 2 * n
    rows = []
    for i, (x, y) in enumerate(zip(xs, ys)):
        if i == 0 or i == m:
            rows.append([str(i), comma_x(x), comma(y), "", ""])
        elif i % 2 == 1:
            rows.append([str(i), comma_x(x), "", comma(y), ""])
        else:
            rows.append([str(i), comma_x(x), "", "", comma(y)])
    rows.append(["Σ", "", comma(s1), comma(s2), comma(s3)])
    table(d, (40, 200), col_w, 48, headers, rows, [WHITE, WHITE, PAPER_Y, PAPER_B, PAPER_P], head=(180, 220, 255), fsize=20)
    d.rounded_rectangle([40, 680, 1160, 890], radius=16, fill=WHITE, outline=LINE, width=3)
    txt(d, (60, 698), "I ≈ (h/3) · (Σкрая + 4·Σнечёт + 2·Σчёт)", 24, BLUE, True)
    txt(d, (60, 744), f"I = {comma_h(h)}/3 · ({comma(s1)} + 4·{comma(s2)} + 2·{comma(s3)})", 23)
    inner = s1 + 4 * s2 + 2 * s3
    txt(d, (60, 786), f"  = {comma(h/3)} · {comma(inner)}", 24)
    txt(d, (60, 832), f"I ≈ {comma(I)}", 32, GREEN, True)
    return im, I


def section_euler(title, flabel, f, x0, y0, h, steps=3):
    rows_d, yfin = euler_data(f, x0, y0, h, steps)
    im = new_im(620)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 58], fill=PAPER_G)
    txt(d, (W / 2, 29), title, 26, bold=True, anchor="mm")
    txt(d, (40, 72), flabel, 24, bold=True)
    txt(d, (40, 108), "прогноз = y + h·y'     коррекция = f(x+h, прогноз)     Δy = (h/2)(y' + корр.)", 20, BLUE, True)
    headers = ["i", "x", "y", "y'", "прогноз", "x след", "корр.", "Δy"]
    col_w = [70, 110, 160, 160, 160, 110, 160, 150]
    rows = []
    for r in rows_d:
        rows.append(
            [
                str(r["i"]),
                comma_x(r["x"]),
                comma(r["y"]),
                comma(r["yp"]),
                comma(r["pred"]),
                comma_x(r["xn"]),
                comma(r["corr"]),
                comma(r["dy"]),
            ]
        )
    last = rows_d[-1]
    rows.append(["", comma_x(last["xn"]), comma(last["yn"]), "", "", "", "", ""])
    table(d, (20, 150), col_w, 50, headers, rows, [WHITE] * 8, head=PAPER_G, fsize=18)
    d.rounded_rectangle([40, 510, 1160, 590], radius=14, fill=WHITE, outline=GREEN, width=4)
    txt(d, (60, 548), f"ответ:  y({comma_x(last['xn'])}) ≈ {comma(last['yn'])}", 30, GREEN, True, anchor="lm")
    return im, last["yn"]


def section_adams(title, flabel, f, xs, ys):
    ad = adams_data(f, xs, ys)
    im = new_im(780)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 58], fill=PAPER_P)
    txt(d, (W / 2, 29), title, 26, bold=True, anchor="mm")
    txt(d, (40, 72), flabel, 24, bold=True)
    txt(d, (40, 108), f"h = {comma_h(ad['h'])}    t = h·y'    Δy = t + (1/2)Δt + (5/12)Δ²t + (3/8)Δ³t", 20, BLUE, True)
    headers = ["i", "x", "y", "Δy", "y'", "t", "Δt", "Δ²t", "Δ³t"]
    col_w = [70, 110, 150, 140, 140, 140, 130, 130, 130]
    # build 5 rows like methodichka
    ts, dt, d2, d3 = ad["ts"], ad["dt"], ad["d2"], ad["d3"]
    yps = ad["yps"]
    table_rows = []
    # i=0
    table_rows.append(
        [
            "0",
            comma_x(xs[0]),
            comma(ys[0]),
            "",
            comma(yps[0]),
            comma(ts[0]),
            comma(dt[0]),
            comma(d2[0]),
            comma(d3),
        ]
    )
    table_rows.append(
        [
            "1",
            comma_x(xs[1]),
            comma(ys[1]),
            "",
            comma(yps[1]),
            comma(ts[1]),
            comma(dt[1]),
            comma(d2[1]),
            "",
        ]
    )
    table_rows.append(
        [
            "2",
            comma_x(xs[2]),
            comma(ys[2]),
            "",
            comma(yps[2]),
            comma(ts[2]),
            comma(dt[2]),
            "",
            "",
        ]
    )
    table_rows.append(
        [
            "3",
            comma_x(xs[3]),
            comma(ys[3]),
            comma(ad["dy3"]),
            comma(yps[3]),
            comma(ts[3]),
            "",
            "",
            "",
        ]
    )
    table_rows.append(
        [
            "4",
            comma_x(ad["x4"]),
            comma(ad["y4"]),
            "",
            "",
            "",
            "",
            "",
            "",
        ]
    )
    table(d, (10, 150), col_w, 48, headers, table_rows, [WHITE] * 9, head=PAPER_P, fsize=17)
    d.rounded_rectangle([40, 470, 1160, 740], radius=16, fill=WHITE, outline=LINE, width=3)
    txt(d, (60, 490), "шаг с диагонали (как в методичке):", 22, BLUE, True)
    txt(d, (60, 532), f"Δy₃ = t₃ + ½·Δt₂ + 5/12·Δ²t₁ + 3/8·Δ³t₀", 22)
    txt(
        d,
        (60, 574),
        f"Δy₃ = {comma(ts[3])} + 0,5·{comma(dt[2])} + (5/12)·{comma(d2[1])} + (3/8)·{comma(d3)}",
        20,
    )
    txt(d, (60, 616), f"Δy₃ = {comma(ad['dy3'])}", 24, bold=True)
    txt(d, (60, 662), f"y₄ = y₃ + Δy₃ = {comma(ys[3])} + {comma(ad['dy3'])}", 24)
    txt(d, (60, 706), f"y({comma_x(ad['x4'])}) ≈ {comma(ad['y4'])}", 30, GREEN, True)
    return im, ad["y4"]


def stack(parts):
    h = sum(p.height for p in parts)
    out = Image.new("RGB", (W, h), BG)
    y = 0
    for p in parts:
        out.paste(p, (0, y))
        y += p.height
    return out


def header(name, lines):
    im = new_im(160 + 34 * len(lines))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 80], fill=(40, 40, 40))
    txt(d, (W / 2, 40), name, 34, (255, 255, 255), True, "mm")
    yy = 100
    for line in lines:
        txt(d, (40, yy), line, 24)
        yy += 36
    return im


VARIANTS = []


def add(slug, name, lines, builders):
    VARIANTS.append(dict(slug=slug, name=name, lines=lines, builders=builders))


# --- variants from photos + original KR ---

add(
    "var1",
    "Вариант 1  (бланк, который решали)",
    [
        "1 трапеции n=5   ∫ ln(x+2)/x dx  [1; 2]",
        "2 Симпсон n=3    ∫ (x³−8) dx     [3,0; 3,6]",
        "3 Эйлер–Коши     y' = 2y − x² , y(0)=2 , [0; 0,3] h=0,1",
        "4 Адамс          y' = y + x·y , y(0,8)=?   старт 1,0; 1,2; 1,5; 1,8",
    ],
    lambda: [
        section_trap("1. Трапеции", "y = ln(x+2) / x     ln — натуральный", lambda x: math.log(x + 2) / x, 1, 2),
        section_simp("2. Симпсон (параболы)", "y = x³ − 8", lambda x: x**3 - 8, 3.0, 3.6),
        section_euler("3. Эйлер–Коши", "y' = 2y − x² ,  y(0)=2 ,  h=0,1", lambda x, y: 2 * y - x * x, 0.0, 2.0, 0.1),
        section_adams("4. Адамс", "y' = y(1+x)   найти y(0,8)", lambda x, y: y * (1 + x), [0.0, 0.2, 0.4, 0.6], [1.0, 1.2, 1.5, 1.8]),
    ],
)

add(
    "var_ex",
    "Вариант с фото:  e²ˣ / (x+5)",
    [
        "1 трапеции n=5   ∫ e^{2x}/(x+5) dx  [0; 1]",
        "2 Симпсон n=3    ∫ (x³+1) dx        [0,4; 1,2]",
        "3 Эйлер–Коши     y' = 2x + y² , y(0)=1 , [0; 0,3] h=0,1",
        "4 Адамс          y' = x² − y , y(2,8)=?  старт y(2)=0; 0,4; 0,6; 0,8",
    ],
    lambda: [
        section_trap("1. Трапеции", "y = e^{2x} / (x+5)", lambda x: math.exp(2 * x) / (x + 5), 0, 1),
        section_simp("2. Симпсон", "y = x³ + 1", lambda x: x**3 + 1, 0.4, 1.2),
        section_euler("3. Эйлер–Коши", "y' = 2x + y² ,  y(0)=1 ,  h=0,1", lambda x, y: 2 * x + y * y, 0.0, 1.0, 0.1),
        section_adams("4. Адамс", "y' = x² − y   найти y(2,8)", lambda x, y: x * x - y, [2.0, 2.2, 2.4, 2.6], [0.0, 0.4, 0.6, 0.8]),
    ],
)

add(
    "var_ln",
    "Вариант с фото:  ln(x+2)/x  (другой 2–4)",
    [
        "1 трапеции n=5   ∫ ln(x+2)/x dx  [1; 2]",
        "2 Симпсон n=3    ∫ (x³+2) dx     [1,2; 1,8]",
        "3 Эйлер–Коши     y' = x² − 2y , y(0)=1 , [0; 0,3] h=0,1",
        "4 Адамс          y' = x² + y , y(0,8)=?  старт 2,0; 2,4; 2,8; 2,9",
    ],
    lambda: [
        section_trap("1. Трапеции", "y = ln(x+2) / x", lambda x: math.log(x + 2) / x, 1, 2),
        section_simp("2. Симпсон", "y = x³ + 2", lambda x: x**3 + 2, 1.2, 1.8),
        section_euler("3. Эйлер–Коши", "y' = x² − 2y ,  y(0)=1 ,  h=0,1", lambda x, y: x * x - 2 * y, 0.0, 1.0, 0.1),
        section_adams("4. Адамс", "y' = x² + y   найти y(0,8)", lambda x, y: x * x + y, [0.0, 0.2, 0.4, 0.6], [2.0, 2.4, 2.8, 2.9]),
    ],
)

add(
    "var8",
    "Вариант 8  (бланк)",
    [
        "1 трапеции n=5  радианы   ∫ cos(2x)/x dx  [6; 7]",
        "2 Симпсон n=3            ∫ (2x³−1) dx    [1,0; 1,6]",
        "3 Эйлер–Коши             y' = 2x² + y , y(0)=1 , [0; 0,3] h=0,1",
        "4 Адамс                  y' = x²·y , y(1,8)=?  старт 1,0; 1,3; 1,8; 2,1",
    ],
    lambda: [
        section_trap("1. Трапеции  (радианы!)", "y = cos(2x) / x     калькулятор в RAD", lambda x: math.cos(2 * x) / x, 6, 7),
        section_simp("2. Симпсон", "y = 2x³ − 1", lambda x: 2 * x**3 - 1, 1.0, 1.6),
        section_euler("3. Эйлер–Коши", "y' = 2x² + y ,  y(0)=1 ,  h=0,1", lambda x, y: 2 * x * x + y, 0.0, 1.0, 0.1),
        section_adams("4. Адамс", "y' = x² · y   найти y(1,8)", lambda x, y: (x * x) * y, [1.0, 1.2, 1.4, 1.6], [1.0, 1.3, 1.8, 2.1]),
    ],
)

add(
    "var5",
    "Вариант B-5  (тетрадь)",
    [
        "1 трапеции n=5  радианы   ∫ sin(x)/(x+3) dx  [1; 2]",
        "2 Симпсон n=3            ∫ (x³+5) dx        [0,4; 1,0]",
        "3 Эйлер–Коши             y' = y² − x y , y(0)=2 , [0; 0,3] h=0,1",
        "4 Адамс                  y' = y − x y , y(0,8)=?  старт 2,0; 2,2; 2,7; 3,0",
    ],
    lambda: [
        section_trap("1. Трапеции  (радианы!)", "y = sin(x) / (x+3)", lambda x: math.sin(x) / (x + 3), 1, 2),
        section_simp("2. Симпсон", "y = x³ + 5", lambda x: x**3 + 5, 0.4, 1.0),
        section_euler("3. Эйлер–Коши", "y' = y² − x y ,  y(0)=2 ,  h=0,1", lambda x, y: y * y - x * y, 0.0, 2.0, 0.1),
        section_adams("4. Адамс", "y' = y(1 − x)   найти y(0,8)", lambda x, y: y - x * y, [0.0, 0.2, 0.4, 0.6], [2.0, 2.2, 2.7, 3.0]),
    ],
)

add(
    "var3b",
    "Вариант 3В  (тетрадь)",
    [
        "1 трапеции n=5  радианы   ∫ cos(x)/(x+2) dx  [0; 1]",
        "2 Симпсон n=3            ∫ (x³+3) dx        [0,0; 0,6]",
        "3 Эйлер–Коши             y' = y² − 2x , y(0)=1 , [0; 0,3] h=0,1",
        "4 Адамс                  y' = x y + x² , y(0,8)=?  старт 1,0; 1,5; 1,7; 2,0",
    ],
    lambda: [
        section_trap("1. Трапеции  (радианы!)", "y = cos(x) / (x+2)", lambda x: math.cos(x) / (x + 2), 0, 1),
        section_simp("2. Симпсон", "y = x³ + 3", lambda x: x**3 + 3, 0.0, 0.6),
        section_euler("3. Эйлер–Коши", "y' = y² − 2x ,  y(0)=1 ,  h=0,1", lambda x, y: y * y - 2 * x, 0.0, 1.0, 0.1),
        section_adams("4. Адамс", "y' = x y + x²   найти y(0,8)", lambda x, y: x * y + x * x, [0.0, 0.2, 0.4, 0.6], [1.0, 1.5, 1.7, 2.0]),
    ],
)

add(
    "var22",
    "Вариант 22  (бланк)",
    [
        "1 трапеции n=5   ∫ eˣ / x² dx   [1; 2]",
        "2 Симпсон n=3    ∫ (x³−1) dx    [2,1; 2,7]",
        "3 Эйлер–Коши     y' = 2x² − y , y(0)=2 , [0; 0,3] h=0,1",
        "4 Адамс          y' = x + x·y , y(1,8)=?  старт 2,0; 2,5; 3,2; 4,3",
    ],
    lambda: [
        section_trap("1. Трапеции", "y = eˣ / x²", lambda x: math.exp(x) / (x * x), 1, 2),
        section_simp("2. Симпсон", "y = x³ − 1", lambda x: x**3 - 1, 2.1, 2.7),
        section_euler("3. Эйлер–Коши", "y' = 2x² − y ,  y(0)=2 ,  h=0,1", lambda x, y: 2 * x * x - y, 0.0, 2.0, 0.1),
        section_adams("4. Адамс", "y' = x(1+y)   найти y(1,8)", lambda x, y: x + x * y, [1.0, 1.2, 1.4, 1.6], [2.0, 2.5, 3.2, 4.3]),
    ],
)


def answers_sheet(answers):
    h = 90 + 70 * len(answers) + 80
    im = new_im(h)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 80], fill=(40, 40, 40))
    txt(d, (W / 2, 40), "КР-3  ·  ответы по вариантам", 32, (255, 255, 255), True, "mm")
    headers = ["вариант", "1 трапеции", "2 Симпсон", "3 Эйлер-К.", "4 Адамс"]
    col_w = [340, 200, 200, 200, 200]
    rows = []
    for name, ans, _path, _sz in answers:
        short = name.split("  (")[0]
        rows.append([short, comma(ans[0]), comma(ans[1]), comma(ans[2]), comma(ans[3])])
    table(d, (30, 100), col_w, 52, headers, rows, [PAPER_Y, WHITE, PAPER_B, PAPER_G, PAPER_P], fsize=18)
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    answers = []
    for v in VARIANTS:
        parts = [header(v["name"], v["lines"])]
        ans = []
        for im, val in v["builders"]():
            parts.append(im)
            ans.append(val)
        sheet = stack(parts)
        path = OUT / f"{v['slug']}.png"
        sheet.save(path, "PNG", optimize=True)
        answers.append((v["name"], ans, path, sheet.size))
        print(path, sheet.size, [comma(a) for a in ans])
    cheat = answers_sheet(answers)
    cp = OUT / "otvety.png"
    cheat.save(cp, "PNG")
    print(cp)
    return answers


if __name__ == "__main__":
    main()
