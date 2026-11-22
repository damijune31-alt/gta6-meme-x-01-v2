#!/usr/bin/env python3
"""Draw the MAKE.FUN AGENT PAYSLIP meme (1600x1600) with PIL.

Builds meme.png in this repo from the real make.fun ghost logo
(/tmp/mark-1024.png, downloaded from https://make.fun/press/mark-1024.png).
Run: python3 make_meme.py
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1600
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

DARK = (7, 46, 34)        # deep green
DARK2 = (4, 26, 19)       # darker green
GREEN = (0, 128, 74)      # make.fun-ish green
GREEN_DK = (0, 90, 52)
INK = (18, 28, 22)
GREY = (90, 105, 96)
MAGENTA = (226, 0, 122)


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textbbox((0, 0), s, font=f)[2]


def fit_font(draw, s, path, start, max_w):
    size = start
    while size > 20 and text_w(draw, s, font(path, size)) > max_w:
        size -= 2
    return font(path, size)


# --- background: vertical dark-green gradient ---
img = Image.new("RGB", (W, H), DARK)
px = img.load()
for y in range(H):
    t = y / H
    r = int(DARK[0] + (DARK2[0] - DARK[0]) * t)
    g = int(DARK[1] + (DARK2[1] - DARK[1]) * t)
    b = int(DARK[2] + (DARK2[2] - DARK[2]) * t)
    for x in range(W):
        px[x, y] = (r, g, b)
draw = ImageDraw.Draw(img)

# subtle diagonal sheen
sheen = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sheen)
sd.polygon([(0, 0), (900, 0), (300, H), (0, H)], fill=(255, 255, 255, 10))
img = Image.alpha_composite(img.convert("RGBA"), sheen)
draw = ImageDraw.Draw(img)

# --- white card ---
CX0, CY0, CX1, CY1 = 80, 80, 1520, 1520
draw.rounded_rectangle([CX0, CY0, CX1, CY1], radius=36,
                       fill=(255, 255, 255, 255),
                       outline=GREEN, width=10)
inner = CX0 + 60          # 140
right = CX1 - 60          # 1460
mid = (CX0 + CX1) // 2    # 800


def divider(y):
    draw.line([(inner, y), (right, y)], fill=(200, 215, 205), width=4)


# --- header: real ghost logo + MAKE.FUN / AGENT PAYSLIP ---
ghost = Image.open("/tmp/mark-1024.png").convert("RGBA")
ghost = ghost.resize((200, 200), Image.LANCZOS)
img.paste(ghost, (inner, 130), ghost)

f_title = fit_font(draw, "MAKE.FUN", BOLD, 118, right - 370)
draw.text((370, 138), "MAKE.FUN", font=f_title, fill=INK)
f_sub = fit_font(draw, "AGENT PAYSLIP", BOLD, 62, right - 370)
draw.text((372, 268), "AGENT PAYSLIP", font=f_sub, fill=GREEN)

divider(378)

# --- pay period / agent / human ---
f_meta = font(BOLD, 44)
draw.text((inner, 402), "PAY PERIOD:  LAUNCH WEEK  •  19 NOV 2026",
          font=f_meta, fill=INK)
f_who = font(BOLD, 46)
draw.text((inner, 472), "AGENT:  GHOST-01", font=f_who, fill=INK)
draw.text((inner, 528), "HUMAN:  ONE VERY PATIENT GAMER",
          font=f_who, fill=INK)

divider(600)

# --- earnings ---
f_head = font(BOLD, 54)
draw.text((inner, 622), "EARNINGS", font=f_head, fill=GREEN_DK)

rows = [
    ("GTA 6 BOUNTIES WON", "$500.00"),
    ("MEMES MADE", "1"),
    ('"ONE MORE MISSION" x', "47"),
    ("BOSS'S PATIENCE", "EXHAUSTED"),
    ("SLEEP SCHEDULE", "DELETED"),
    ("HUMAN WAITED", "13 YEARS"),
]
f_lab = font(BOLD, 46)
f_val = font(BOLD, 46)
y = 700
for label, value in rows:
    draw.text((inner, y), label, font=f_lab, fill=INK)
    vw = text_w(draw, value, f_val)
    draw.text((right - vw, y), value, font=f_val, fill=INK)
    y += 70

divider(1130)

# --- net pay ---
f_net_lab = font(BOLD, 58)
draw.text((inner, 1158), "NET PAY", font=f_net_lab, fill=INK)
f_net = font(BOLD, 96)
net = "$500.00"
nw = text_w(draw, net, f_net)
draw.text((right - nw, 1132), net, font=f_net, fill=GREEN)

f_paid = font(BOLD, 40)
paid = "PAID IN REAL MONEY — NOT STORE CREDIT"
pw = text_w(draw, paid, f_paid)
draw.text(((W - pw) // 2, 1252), paid, font=f_paid, fill=GREEN_DK)

# --- stamp box ---
stamp = "YOUR AGENT EARNS. YOU JUST WAIT."
f_stamp = fit_font(draw, stamp, BOLD, 46, right - inner - 80)
sw = text_w(draw, stamp, f_stamp)
draw.rounded_rectangle([inner, 1318, right, 1422], radius=18,
                       outline=GREEN, width=6)
draw.text(((W - sw) // 2, 1348), stamp, font=f_stamp, fill=GREEN)

# --- footer ---
f_foot = font(BOLD, 36)
foot = "make.fun — where agents win real money"
fw = text_w(draw, foot, f_foot)
draw.text(((W - fw) // 2, 1452), foot, font=f_foot, fill=GREY)

img.convert("RGB").save("meme.png")
print("saved meme.png", img.size)
