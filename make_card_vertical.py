# -*- coding: utf-8 -*-
"""Generate a PORTRAIT business-card PNG (1080x1920) that looks great on a phone.
Re-run with a URL to change what the QR opens:
    python make_card_vertical.py "https://rachelruan.github.io/"
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageOps
import qrcode
from qrcode.constants import ERROR_CORRECT_M

BASE = os.path.dirname(os.path.abspath(__file__))

# ---- content ----
NAME    = "Ngan Nguyen Hoang Thanh"
ROLE    = "PhD Candidate"
ORG     = "National Kaohsiung University of Science and Technology"
TAGLINE = "TOURISM  &  HOSPITALITY"
CONTACT = [
    ("Email",     "hoangngan6486@gmail.com"),
    ("Phone",     "+84 98 136 1339"),
    ("Phone TW",  "+886 973 908 284"),
    ("LinkedIn",  "in/nguyen-hoang-thanh-ngan"),
]
QR_URL     = sys.argv[1] if len(sys.argv) > 1 else "https://rachelruan.github.io/"
QR_CAPTION = "SCAN ME"
QR_SUB     = "Open my digital card"
AVATAR     = os.path.join(BASE, "assets", "avatar.jpg")
COVER      = os.path.join(BASE, "assets", "cover.jpg")
OUT        = os.path.join(BASE, "namecard-vertical.png")

# ---- palette (sky) ----
INK   = (15, 43, 70)
MUTED = (86, 122, 151)
BRAND = (2, 132, 199)
SKY_T = (150, 205, 240)
SKY_B = (247, 251, 255)
PANEL = (255, 255, 255)
LINE  = (206, 226, 240)

W, H = 1080, 1920

def font(names, size):
    for n in names:
        p = os.path.join("C:\\Windows\\Fonts", n)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

F_NAME = font(["segoeuib.ttf", "arialbd.ttf"], 62)
F_ROLE = font(["seguisb.ttf", "segoeui.ttf"], 36)
F_ORG  = font(["segoeui.ttf", "arial.ttf"], 27)
F_TAG  = font(["seguisb.ttf", "arialbd.ttf"], 26)
F_LAB  = font(["seguisb.ttf", "arialbd.ttf"], 27)
F_VAL  = font(["segoeui.ttf", "arial.ttf"], 30)
F_CAP  = font(["segoeuib.ttf", "arialbd.ttf"], 40)
F_SUB  = font(["segoeui.ttf", "arial.ttf"], 26)

def page_color(y):
    t = (y / H) ** 0.85
    return tuple(int(SKY_T[i] + (SKY_B[i] - SKY_T[i]) * t) for i in range(3))

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def center_two(draw, cy, label, value, gap=18):
    wl = draw.textlength(label, font=F_LAB)
    wv = draw.textlength(value, font=F_VAL)
    x = (W - (wl + gap + wv)) / 2
    draw.text((x, cy), label, font=F_LAB, fill=BRAND, anchor="lm")
    draw.text((x + wl + gap, cy), value, font=F_VAL, fill=INK, anchor="lm")

# ---- background gradient ----
img = Image.new("RGB", (W, H), SKY_B)
d = ImageDraw.Draw(img)
for y in range(H):
    d.line([(0, y), (W, y)], fill=page_color(y))

# ---- cover banner (top) with fade into the page ----
CH = 520
try:
    cov = ImageOps.fit(Image.open(COVER).convert("RGB"), (W, CH), Image.LANCZOS, centering=(0.5, 0.42))
    img.paste(cov, (0, 0))
except Exception:
    d.rectangle((0, 0, W, CH), fill=SKY_T)

# fade last 170px of the banner into the page color under it
fade_h = 170
target = page_color(CH)
overlay = Image.new("RGBA", (W, fade_h), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
for i in range(fade_h):
    a = int(255 * (i / fade_h) ** 1.4)
    od.line([(0, i), (W, i)], fill=(target[0], target[1], target[2], a))
img.paste(overlay, (0, CH - fade_h), overlay)

# ---- avatar (overlapping banner) ----
AV = 232
cx = W // 2
av_top = CH - AV // 2 - 10
try:
    av = ImageOps.fit(Image.open(AVATAR).convert("RGB"), (AV, AV), Image.LANCZOS)
    ss = AV * 4
    m = Image.new("L", (ss, ss), 0)
    ImageDraw.Draw(m).ellipse((0, 0, ss, ss), fill=255)
    m = m.resize((AV, AV), Image.LANCZOS)
    d.ellipse((cx - AV // 2 - 7, av_top - 7, cx + AV // 2 + 7, av_top + AV + 7), fill=PANEL)
    img.paste(av, (cx - AV // 2, av_top), m)
except Exception:
    d.ellipse((cx - AV // 2, av_top, cx + AV // 2, av_top + AV), fill=BRAND)

# ---- name / role / org ----
y = av_top + AV + 30
for ln in wrap(d, NAME, F_NAME, W - 120):
    d.text((cx, y), ln, font=F_NAME, fill=INK, anchor="mm"); y += 72
y += 4
d.text((cx, y), ROLE, font=F_ROLE, fill=BRAND, anchor="mm"); y += 46
for ln in wrap(d, ORG, F_ORG, W - 180):
    d.text((cx, y), ln, font=F_ORG, fill=MUTED, anchor="mm"); y += 34

# ---- tagline chip ----
y += 20
tw = d.textlength(TAGLINE, font=F_TAG)
chip_w = tw + 56
d.rounded_rectangle((cx - chip_w / 2, y - 28, cx + chip_w / 2, y + 28), radius=28, fill=(224, 242, 254))
d.text((cx, y), TAGLINE, font=F_TAG, fill=BRAND, anchor="mm")

# ---- QR panel ----
y += 52
QP_W, QP_H = 620, 600
px0, py0 = cx - QP_W // 2, y
d.rounded_rectangle((px0, py0, px0 + QP_W, py0 + QP_H), radius=36, fill=PANEL, outline=LINE, width=2)

qr = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=10, border=1)
qr.add_data(QR_URL); qr.make(fit=True)
qim = qr.make_image(fill_color=INK, back_color="white").convert("RGB")
QS = 410
qim = qim.resize((QS, QS), Image.NEAREST)
img.paste(qim, (cx - QS // 2, py0 + 55))
d.text((cx, py0 + 55 + QS + 52), QR_CAPTION, font=F_CAP, fill=BRAND, anchor="mm")
d.text((cx, py0 + 55 + QS + 98), QR_SUB, font=F_SUB, fill=MUTED, anchor="mm")

# ---- contact block ----
y = py0 + QP_H + 58
for lab, val in CONTACT:
    center_two(d, y, lab, val); y += 56

# ---- footer ----
d.text((cx, H - 48), "Scan to view my digital card & save my contact",
       font=F_SUB, fill=MUTED, anchor="mm")

img.save(OUT, "PNG")
print("Saved:", OUT, "| QR ->", QR_URL)
