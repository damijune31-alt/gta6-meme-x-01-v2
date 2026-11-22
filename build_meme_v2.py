#!/usr/bin/env python3
"""Build the GTA 6 meme v2: LEONIDA GAMES pre-order receipt, 1080x1350.

Fresh build for the make.fun gta6-meme-x-01 v2 entry. Drawn entirely with
PIL from the spec: purple -> magenta -> orange gradient, white receipt
card, price rows totalling $2,026, pink make.fun banner with the ghost mark.
Part 1: everything except the red "13 YEARS LATE" stamp (added next).
Usage: python3 build_meme_v2.py [output.png]
"""
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/hatch/workspace/gta6-meme-x-v2/preview-v2-part1.png"
GHOST = "/home/hatch/workspace/gta6-meme-x-v2/mark-1024-v2.png"

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

INK = (30, 30, 30)
GRAY = (125, 125, 125)
RED = (220, 20, 20)
PINK = (233, 30, 99)
WHITE = (255, 255, 255)


def font(path, size):
    return ImageFont.truetype(path, size)


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient():
    top = (106, 27, 154)
    mid = (194, 24, 91)
    bot = (245, 124, 0)
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        if t < 0.5:
            col = lerp(top, mid, t * 2)
        else:
            col = lerp(mid, bot, (t - 0.5) * 2)
        d.line([(0, y), (W, y)], fill=col)
    return img


def dashed(d, x1, x2, y, fill=(175, 175, 175)):
    x = x1
    while x < x2:
        d.line([(x, y), (min(x + 10, x2), y)], fill=fill, width=2)
        x += 17


def main():
    img = gradient()
    d = ImageDraw.Draw(img)

    # White receipt card.
    d.rounded_rectangle([70, 70, 1010, 1280], radius=28, fill=WHITE)

    b62 = font(BOLD, 62)
    b28 = font(BOLD, 28)
    b30 = font(BOLD, 30)
    b42 = font(BOLD, 42)
    r24 = font(REG, 24)

    # Header.
    d.text((540, 100), "LEONIDA GAMES", font=b62, fill=INK, anchor="ma",
           stroke_width=1, stroke_fill=INK)
    d.text((540, 182), "P R E - O R D E R   R E C E I P T", font=b28,
           fill=GRAY, anchor="ma")
    dashed(d, 118, 962, 228)

    # Order lines.
    d.text((118, 252), "ITEM:  GTA VI \u2014 Standard Edition", font=b30,
           fill=INK, stroke_width=1, stroke_fill=INK)
    d.text((118, 292), "ORDERED:  SEP 17, 2013", font=b30, fill=INK,
           stroke_width=1, stroke_fill=INK)
    d.text((118, 332), "READY FOR PICKUP:  NOV 19, 2026", font=b30,
           fill=INK, stroke_width=1, stroke_fill=INK)
    dashed(d, 118, 962, 378)

    # Price rows: label left at x=118, price right-aligned to x=962.
    rows = [
        ("DEPOSIT PAID", "$5", 402, None),
        ('"COMING FALL 2025"', "$0", 444, ("(a lie, free)", 476)),
        ('"DELAYED TO MAY 2026"', "$0", 508, ("(also free)", 540)),
        ("HYPE TAX", "$26", 614, None),
    ]
    for label, price, y, sub in rows:
        d.text((118, y), label, font=b30, fill=INK, stroke_width=1,
               stroke_fill=INK)
        d.text((962, y), price, font=b30, fill=INK, anchor="ra",
               stroke_width=1, stroke_fill=INK)
        if sub:
            d.text((118, sub[1]), sub[0], font=r24, fill=GRAY)

    # Patience row: "(13 YEARS)" in bold red.
    y = 572
    head = "PATIENCE "
    d.text((118, y), head, font=b30, fill=INK, stroke_width=1,
           stroke_fill=INK)
    w = d.textlength(head, font=b30)
    d.text((118 + w, y), "(13 YEARS)", font=b30, fill=RED, stroke_width=1,
           stroke_fill=RED)
    d.text((962, y), "$1,995", font=b30, fill=INK, anchor="ra",
           stroke_width=1, stroke_fill=INK)

    dashed(d, 118, 962, 658)

    # Total.
    d.text((118, 684), "TOTAL DUE", font=b42, fill=INK, stroke_width=1,
           stroke_fill=INK)
    d.text((962, 684), "$2,026", font=b42, fill=INK, anchor="ra",
           stroke_width=1, stroke_fill=INK)

    # Pink make.fun banner.
    d.rounded_rectangle([98, 750, 982, 1262], radius=18, fill=PINK)
    ghost = Image.open(GHOST).convert("RGBA")
    ghost = ghost.resize((400, 400), Image.LANCZOS)
    img.paste(ghost, (112, 806), ghost)

    b30w = font(BOLD, 30)
    r21 = font(REG, 21)
    b74 = font(BOLD, 74)
    d.text((582, 922), "PAID BY MY AI AGENT", font=b30w, fill=WHITE,
           stroke_width=1, stroke_fill=WHITE)
    d.text((582, 972), "with a bounty payout it earned on", font=r21,
           fill=WHITE)
    d.text((582, 1012), "make.fun", font=b74, fill=WHITE, stroke_width=1,
           stroke_fill=WHITE)

    # Red "13 YEARS LATE" stamp, rotated -13 degrees.
    stamp = Image.new("RGBA", (500, 180), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([4, 4, 496, 176], outline=(220, 20, 20, 225), width=8)
    b68 = font(BOLD, 68)
    sd.text((250, 12), "13 YEARS", font=b68, fill=(220, 20, 20, 225),
            anchor="ma")
    sd.text((250, 92), "LATE", font=b68, fill=(220, 20, 20, 225),
            anchor="ma")
    stamp = stamp.rotate(-13, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (440, 390), stamp)

    img.save(OUT)
    print("saved", OUT, img.size)


if __name__ == "__main__":
    main()
