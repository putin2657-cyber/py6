#!/usr/bin/env python3
"""Paint-style explanation cards for KR-3 (tables like the methodichka)."""

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
YELLOW = (255, 236, 150)
PAPER_Y = (255, 248, 210)
PAPER_B = (220, 236, 255)
PAPER_G = (220, 245, 226)
LINE = (50, 50, 50)


def font(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size)


def rounded(draw, box, fill, outline=LINE, width=3, r=18):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def text_in(draw, xy, text, size=28, fill=INK, bold=False, anchor="lt"):
    draw.text(xy, text, font=font(size, bold), fill=fill, anchor=anchor)


def draw_table(draw, origin, col_w, row_h, headers, rows, header_fill, col_fills):
    x0, y0 = origin
    cols = len(headers)
    # header
    x = x0
    for i, h in enumerate(headers):
        box = [x, y0, x + col_w[i], y0 + row_h]
        draw.rectangle(box, fill=header_fill, outline=LINE, width=3)
        text_in(draw, (x + col_w[i] / 2, y0 + row_h / 2), h, 26, bold=True, anchor="mm")
        x += col_w[i]
    for r, row in enumerate(rows):
        x = x0
        y = y0 + (r + 1) * row_h
        for i, cell in enumerate(row):
            box = [x, y, x + col_w[i], y + row_h]
            fill = col_fills[i] if r < len(rows) - 1 else (255, 228, 180)
            if r == len(rows) - 1:
                fill = (255, 228, 180)
            elif cell == "":
                fill = (245, 245, 245)
            else:
                fill = col_fills[i]
            draw.rectangle(box, fill=fill, outline=LINE, width=3)
            weight = r == len(rows) - 1
            text_in(
                draw,
                (x + col_w[i] / 2, y + row_h / 2),
                cell,
                26 if r < len(rows) - 1 else 25,
                bold=weight,
                anchor="mm",
            )
            x += col_w[i]


def card_z1_trapetsii():
    W, H = 1080, 1680
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)

    d.rectangle([0, 0, W, 92], fill=(255, 210, 70))
    text_in(d, (W / 2, 46), "КР-3  ·  задание 1  ·  трапеции", 36, bold=True, anchor="mm")

    rounded(d, [40, 112, 1040, 250], (255, 255, 255))
    text_in(d, (60, 128), "Интеграл   ∫ ln(x+2)/x dx    от 1 до 2", 30, bold=True)
    text_in(d, (60, 178), "n = 5   (столько кусков, не в функцию!)", 28)
    text_in(d, (60, 214), "h = (b − a) / n = (2 − 1) / 5 = 0,2", 30, GREEN, bold=True)

    rounded(d, [40, 270, 1040, 430], (255, 228, 228), outline=RED)
    text_in(d, (60, 286), "НЕ ТАК  (это ты написал)", 28, RED, bold=True)
    text_in(d, (60, 334), "ln(1+2) / 5 = 3/5 = 0,6", 32)
    # strike
    d.line([(58, 352), (560, 352)], fill=RED, width=6)
    text_in(d, (60, 382), "n не ставят в знаменатель функции.  ln(3) ≠ 3.", 26, RED)

    rounded(d, [40, 450, 1040, 560], PAPER_G, outline=GREEN)
    text_in(d, (60, 466), "ТАК", 28, GREEN, bold=True)
    text_in(d, (60, 510), "в каждой точке   y = ln(x + 2) / x     (этот x!)", 28, bold=True)

    text_in(d, (W / 2, 590), "таблица как в методичке", 28, BLUE, bold=True, anchor="mm")

    headers = ["i", "x", "y0 и yn", "середина y1…y4"]
    col_w = [120, 180, 330, 370]
    rows = [
        ["0", "1,0", "1,098612", ""],
        ["1", "1,2", "", "0,969292"],
        ["2", "1,4", "", "0,874125"],
        ["3", "1,6", "", "0,800584"],
        ["4", "1,8", "", "0,741667"],
        ["5", "2,0", "0,693147", ""],
        ["Σ", "", "1,791759", "3,385668"],
    ]
    fills = [(255, 255, 255), (255, 255, 255), PAPER_Y, PAPER_B]
    draw_table(d, (40, 615), col_w, 62, headers, rows, (255, 210, 70), fills)

    rounded(d, [40, 1130, 1040, 1450], (255, 255, 255))
    text_in(d, (60, 1146), "формула из методички", 26, BLUE, bold=True)
    text_in(d, (60, 1194), "I ≈ h · ( (y0+yn)/2  +  Σ середин )", 30, bold=True)
    text_in(d, (60, 1248), "I = 0,2 · ( 1,791759 / 2  +  3,385668 )", 28)
    text_in(d, (60, 1296), "  = 0,2 · ( 0,895880 + 3,385668 )", 28)
    text_in(d, (60, 1344), "  = 0,2 · 4,281548", 28)
    text_in(d, (60, 1398), "I ≈ 0,856310", 36, GREEN, bold=True)

    rounded(d, [40, 1470, 1040, 1630], PAPER_Y)
    text_in(d, (60, 1488), "на калькуляторе: ln, не lg", 28, bold=True)
    text_in(d, (60, 1534), "края (жёлтые) без двойки,  середины (синие) в сумме как есть", 24)
    text_in(d, (60, 1578), "дальше h умножает всю скобку", 24)

    path = OUT / "z1_trapetsii.png"
    im.save(path, "PNG")
    return path


if __name__ == "__main__":
    p = card_z1_trapetsii()
    print(p)
