#!/usr/bin/env python3
"""Graphs + sign table for practical 2, variant 19 — as in the notebook example."""

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
YELLOW = (255, 210, 70)
LINE = (50, 50, 50)
WHITE = (255, 255, 255)
W = 1200


def F(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size)


def txt(d, xy, s, size=26, fill=INK, bold=False, anchor="lt"):
    d.text(xy, s, font=F(size, bold), fill=fill, anchor=anchor)


def plot_cubic(path: Path) -> Path:
    xs = np.linspace(-3.2, 1.6, 400)
    ys = 4 * xs**3 - 2 * xs**2 + 3 * xs + 10
    fig, ax = plt.subplots(figsize=(10.4, 6.2), dpi=140)
    fig.patch.set_facecolor("#fffbf0")
    ax.set_facecolor("#fffef8")
    ax.axhline(0, color="#222", lw=1.4)
    ax.axvline(0, color="#222", lw=1.2)
    ax.plot(xs, ys, color="#1c5aa8", lw=2.6, label="y = 4x³ − 2x² + 3x + 10")
    ax.plot([-2, -1], [-36, 1], "o", color="#c42828", ms=8, zorder=5)
    ax.annotate("f(−2)=−36", xy=(-2, -36), xytext=(-2.9, -22),
                fontproperties=fp, fontsize=12, color="#c42828",
                arrowprops=dict(arrowstyle="->", color="#c42828", lw=1.2))
    ax.annotate("f(−1)=1", xy=(-1, 1), xytext=(-0.3, 18),
                fontproperties=fp, fontsize=12, color="#c42828",
                arrowprops=dict(arrowstyle="->", color="#c42828", lw=1.2))
    ax.axvspan(-2, -1, color="#ffe28a", alpha=0.45)
    ax.plot([-1.046], [0], "o", color="#167a3a", ms=10, zorder=6)
    ax.annotate("ξ ≈ −1,046", xy=(-1.046, 0), xytext=(-2.6, 12),
                fontproperties=fpb, fontsize=13, color="#167a3a",
                arrowprops=dict(arrowstyle="->", color="#167a3a", lw=1.4))
    ax.set_xlim(-3.2, 1.6)
    ax.set_ylim(-45, 28)
    ax.set_xlabel("x", fontproperties=fp, fontsize=13)
    ax.set_ylabel("y", fontproperties=fp, fontsize=13)
    ax.set_title("Задание 1. График f(x)  ·  корень на [−2; −1]", fontproperties=fpb, fontsize=14)
    ax.grid(True, ls="--", alpha=0.45)
    ax.legend(prop=fp, loc="upper left")
    fig.tight_layout()
    fig.savefig(path, facecolor=fig.get_facecolor())
    plt.close()
    return path


def plot_two_curves(path: Path) -> Path:
    xs = np.linspace(-2.3, 2.5, 400)
    y1 = 2 * xs**2
    y2 = 0.5 * xs + 2
    fig, ax = plt.subplots(figsize=(10.4, 6.2), dpi=140)
    fig.patch.set_facecolor("#fffbf0")
    ax.set_facecolor("#fffef8")
    ax.axhline(0, color="#222", lw=1.3)
    ax.axvline(0, color="#222", lw=1.2)
    ax.plot(xs, y1, color="#1c5aa8", lw=2.6, label="y₁ = 2x²")
    ax.plot(xs, y2, color="#c42828", lw=2.6, label="y₂ = 0,5x + 2")
    # intersections
    pts = [(-0.8828, 2 * 0.8828**2), (1.1328, 2 * 1.1328**2)]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], "o", color="#167a3a", ms=9, zorder=5)
    ax.annotate("ξ ≈ −0,883\n(меньший по модулю)", xy=pts[0], xytext=(-2.15, 5.4),
                fontproperties=fpb, fontsize=12, color="#167a3a",
                arrowprops=dict(arrowstyle="->", color="#167a3a", lw=1.4))
    ax.annotate("≈ 1,133", xy=pts[1], xytext=(1.35, 5.2),
                fontproperties=fp, fontsize=12, color="#167a3a",
                arrowprops=dict(arrowstyle="->", color="#167a3a", lw=1.2))
    ax.axvspan(-1, 0, color="#ffe28a", alpha=0.4)
    ax.set_xlim(-2.3, 2.5)
    ax.set_ylim(-0.4, 9.2)
    ax.set_xlabel("x", fontproperties=fp, fontsize=13)
    ax.set_ylabel("y", fontproperties=fp, fontsize=13)
    ax.set_title("Задание 2. Графическое отделение  ·  y₁ = 2x²  и  y₂ = 0,5x+2",
                 fontproperties=fpb, fontsize=13)
    ax.grid(True, ls="--", alpha=0.45)
    ax.legend(prop=fp, loc="upper right")
    fig.tight_layout()
    fig.savefig(path, facecolor=fig.get_facecolor())
    plt.close()
    return path


def header_block() -> Image.Image:
    im = Image.new("RGB", (W, 980), BG)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 78], fill=(40, 40, 40))
    txt(d, (W / 2, 39), "Практика 2  ·  вариант 19  ·  графики и знаки", 30, (255, 255, 255), True, "mm")

    d.rectangle([0, 78, W, 132], fill=YELLOW)
    txt(d, (W / 2, 105), "Задание 1. Аналитическое отделение", 26, bold=True, anchor="mm")

    txt(d, (40, 150), "f(x) = 4x³ − 2x² + 3x + 10", 26, bold=True)
    txt(d, (40, 196), "f'(x) = 12x² − 4x + 3", 24)
    txt(d, (40, 240), "D = 16 − 144 = −128 < 0   →   действительных критических точек нет", 24, BLUE, True)
    txt(d, (40, 286), "f'(x) > 0 всегда, f строго возрастает, один действительный корень", 24)

    # sign table
    txt(d, (40, 340), "таблица знаков f(x)", 24, BLUE, True)
    headers = ["x", "−∞", "−2", "−1", "+∞"]
    vals = ["f(x)", "−", "−36", "+1", "+"]
    col_w = [140, 180, 180, 180, 180]
    x0, y0, rh = 80, 390, 56
    for i, h in enumerate(headers):
        box = [x0 + sum(col_w[:i]), y0, x0 + sum(col_w[: i + 1]), y0 + rh]
        d.rectangle(box, fill=YELLOW, outline=LINE, width=3)
        txt(d, ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), h, 22, bold=True, anchor="mm")
    fills = [YELLOW, (255, 228, 228), (255, 228, 228), (220, 245, 226), (220, 245, 226)]
    for i, h in enumerate(vals):
        box = [x0 + sum(col_w[:i]), y0 + rh, x0 + sum(col_w[: i + 1]), y0 + 2 * rh]
        d.rectangle(box, fill=fills[i], outline=LINE, width=3)
        txt(d, ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), h, 22, bold=True, anchor="mm")

    # arrows under sign change
    d.polygon([(x0 + 140 + 180 + 90, y0 + 2 * rh + 18),
               (x0 + 140 + 180 + 70, y0 + 2 * rh + 48),
               (x0 + 140 + 180 + 110, y0 + 2 * rh + 48)], fill=GREEN)
    txt(d, (x0 + 80, y0 + 2 * rh + 70), "смена знака на [−2; −1]  →  сюда хорды, это единственный ξ", 24, GREEN, True)

    d.rounded_rectangle([40, 640, 1160, 940], radius=16, fill=WHITE, outline=LINE, width=3)
    txt(d, (60, 660), "контрольные точки для графика", 22, BLUE, True)
    pts = [(-3, -119), (-2, -36), (-1.5, -12.5), (-1, 1), (0, 10), (1, 15)]
    yy = 710
    for x, y in pts:
        txt(d, (70, yy), f"x = {str(x).replace('.', ',')}     f = {str(y).replace('.', ',')}", 22)
        yy += 36
    return im


def main():
    g1 = plot_cubic(OUT / "_tmp_cubic.png")
    g2 = plot_two_curves(OUT / "_tmp_two.png")
    top = header_block()
    im1 = Image.open(g1).convert("RGB")
    im2 = Image.open(g2).convert("RGB")
    # scale graphs to width W
    def fit(im):
        r = W / im.width
        return im.resize((W, int(im.height * r)), Image.Resampling.LANCZOS)

    im1, im2 = fit(im1), fit(im2)
    cap = Image.new("RGB", (W, 90), BG)
    d = ImageDraw.Draw(cap)
    txt(d, (W / 2, 45), "Задание 2. Две линии — точки пересечения и есть корни", 26, bold=True, anchor="mm")

    h = top.height + im1.height + cap.height + im2.height + 20
    out = Image.new("RGB", (W, h), BG)
    y = 0
    for part in (top, im1, cap, im2):
        out.paste(part, (0, y))
        y += part.height
    dest = OUT / "pr2_grafiki.png"
    out.save(dest, "PNG", optimize=True)
    g1.unlink(missing_ok=True)
    g2.unlink(missing_ok=True)
    print(dest, out.size)


if __name__ == "__main__":
    main()
