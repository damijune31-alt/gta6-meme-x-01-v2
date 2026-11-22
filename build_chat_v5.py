#!/usr/bin/env python3
"""gta6-meme-x-01 v5 — Rockstar iMessage chat meme, rebuilt fresh in-session.

Canvas 1080x1350, black background. A fake chat with Rockstar Games:
promised Fall 2025, delayed to May 2026, delayed again to Nov 19 2026,
still typing after 13 years. Pink banner at the bottom with the real
make.fun ghost mark (fresh download from https://make.fun/press/mark-1024.png).

Usage:
    python3 build_chat_v5.py <ghost-png> [output-png]
Default ghost: ./mark-1024.png ; default output: ./meme.png
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
BG = (10, 10, 10)
GOLD = (245, 193, 0)
WHITE = (255, 255, 255)
GREY = (150, 150, 150)
GREEN = (52, 199, 89)
LEFT_BUBBLE = (38, 38, 40)      # #262628
RIGHT_BUBBLE = (11, 132, 255)   # #0B84FF
PINK = (233, 30, 99)
DIVIDER = (55, 55, 55)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
CHAT = 34          # chat bubble text size
TS = 24            # timestamp size
CAPTION = 28       # "typing for 13 years" size
MAX_BUBBLE = 688   # max bubble width


def font(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that all fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def bubble(draw, text, side, y):
    """Draw one chat bubble starting at y. Returns y just below it."""
    fnt = font(False, CHAT)
    lines = wrap(draw, text, fnt, MAX_BUBBLE - 56)
    line_h = 46
    text_w = max(draw.textlength(ln, font=fnt) for ln in lines)
    bw = int(text_w) + 56
    bh = len(lines) * line_h + 30
    if side == "left":
        x0 = 48
    else:
        x0 = 1032 - bw
    draw.rounded_rectangle([x0, y, x0 + bw, y + bh], radius=28,
                           fill=LEFT_BUBBLE if side == "left" else RIGHT_BUBBLE)
    ty = y + 15
    for ln in lines:
        draw.text((x0 + 28, ty), ln, font=fnt, fill=WHITE)
        ty += line_h
    return y + bh


def timestamp(draw, text, y):
    fnt = font(False, TS)
    tw = draw.textlength(text, font=fnt)
    draw.text(((W - tw) / 2, y), text, font=fnt, fill=(140, 140, 140))
    return y + 44


def typing_bubble(draw, y):
    """Grey bubble with three white dots. Returns y just below it."""
    x0, bw, bh = 48, 170, 66
    draw.rounded_rectangle([x0, y, x0 + bw, y + bh], radius=28, fill=LEFT_BUBBLE)
    cy = y + bh // 2
    for i in range(3):
        cx = x0 + 38 + i * 42
        draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=WHITE)
    return y + bh


def main():
    ghost_path = sys.argv[1] if len(sys.argv) > 1 else "./mark-1024.png"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "./meme.png"

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- header: gold R circle, name, online status, divider ----
    d.ellipse([60, 58, 132, 130], fill=GOLD)
    r_font = font(True, 54)
    r = "R"
    rb = d.textbbox((0, 0), r, font=r_font)
    rw, rh = rb[2] - rb[0], rb[3] - rb[1]
    d.text((96 - rw / 2 - rb[0], 94 - rh / 2 - rb[1]), r,
           font=r_font, fill=(0, 0, 0))
    d.text((150, 62), "Rockstar Games", font=font(True, 36), fill=WHITE)
    d.ellipse([151, 113, 169, 131], fill=GREEN)
    on_font = font(False, 24)
    ob = d.textbbox((0, 0), "online", font=on_font)
    d.text((178, 122 - (ob[3] - ob[1]) / 2 - ob[1]), "online",
           font=on_font, fill=GREY)
    d.line([(40, 158), (1040, 158)], fill=DIVIDER, width=2)

    # ---- chat flow ----
    y = 190
    y = timestamp(d, "Sep 17, 2013", y)
    y = bubble(d, "GTA VI is coming Fall 2025", "left", y) + 26
    y = bubble(d, "ok", "right", y) + 26
    y = timestamp(d, "May 2, 2025", y)
    y = bubble(d, "Sorry, delayed to May 2026", "left", y) + 26
    y = bubble(d, "any update?", "right", y) + 26
    y = timestamp(d, "Nov 2026", y)
    y = bubble(d, "Sorry again \u2014 Nov 19, 2026", "left", y) + 26
    y = bubble(d, "...", "right", y) + 26
    y = typing_bubble(d, y) + 26

    cap = "Rockstar has been typing for 13 years"
    cf = font(False, CAPTION)
    cw = d.textlength(cap, font=cf)
    d.text(((W - cw) / 2, y), cap, font=cf, fill=GREY)

    # ---- bottom banner: pink, ghost + PAID BY MY AI AGENT ----
    d.rounded_rectangle([98, 1100, 982, 1300], radius=18, fill=PINK)
    ghost = Image.open(ghost_path).convert("RGBA").resize((160, 160), Image.LANCZOS)
    img.paste(ghost, (128, 1120), ghost)
    d.ellipse([112, 1104, 304, 1296], outline=(15, 15, 15), width=6)
    d.text((330, 1128), "PAID BY MY AI AGENT", font=font(True, 30), fill=WHITE)
    d.text((330, 1172), "with a bounty payout it earned on",
           font=font(False, 22), fill=WHITE)
    d.text((330, 1206), "make.fun", font=font(True, 62), fill=WHITE)

    img.save(out_path)
    print(f"saved {out_path} {img.size}")
    # sanity: nothing drawn past the banner bottom, canvas exact
    assert img.size == (1080, 1350)


if __name__ == "__main__":
    main()
