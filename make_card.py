# -*- coding: utf-8 -*-
"""Generate a printable business-card PNG (1050x600, ~300dpi) with a QR code.
Re-run after deploying to point the QR at your live site:
    python make_card.py "https://<username>.github.io"
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
    ("Email",   "hoangngan6486@gmail.com"),
    ("Phone",   "+84 98 136 1339"),
    ("Phone TW","+886 973 908 284"),
    ("LinkedIn","in/nguyen-hoang-thanh-ngan"),
]
# What the QR points to. Pass a URL as the 1st arg to override.
QR_URL     = sys.argv[1] if len(sys.argv) > 1 else "https://www.linkedin.com/in/nguyen-hoang-thanh-ngan-58604b340/"
QR_CAPTION = "SCAN ME"
QR_SUB     = "Open my profile"
AVATAR     = os.path.join(BASE, "assets", "avatar.jpg")
OUT        = os.path.join(BASE, "namecard.png")

# ---- palette (sky) ----
INK   = (15, 43, 70)
MUTED = (86, 122, 151)
BRAND = (2, 132, 199)
SKY_T = (150, 205, 240)
SKY_B = (247, 251, 255)
PANEL = (255, 255, 255)
LINE  = (206, 226, 240)

W, H = 1050, 600

def font(names, size):
    for n in names:
        p = os.path.join("C:\\Windows\\Fonts", n)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

F_NAME  = font(["segoeuib.ttf", "arialbd.ttf"], 40)
F_ROLE  = font(["seguisb.ttf", "segoeui.ttf", "arial.ttf"], 24)
F_ORG   = font(["segoeui.ttf", "arial.ttf"], 18)
F_TAG   = font(["seguisb.ttf", "arialbd.ttf"], 17)
F_LAB   = font(["seguisb.ttf", "arialbd.ttf"], 17)
F_VAL   = font(["segoeui.ttf", "arial.ttf"], 20)
F_CAP   = font(["segoeuib.ttf", "arialbd.ttf"], 22)
F_SUB   = font(["segoeui.ttf", "arial.ttf"], 16)

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

# ---- background gradient ----
img = Image.new("RGB", (W, H), SKY_B)
d = ImageDraw.Draw(img)
for y in range(H):
    t = (y / H) ** 0.85
    c = tuple(int(SKY_T[i] + (SKY_B[i] - SKY_T[i]) * t) for i in range(3))
    d.line([(0, y), (W, y)], fill=c)

# soft sun glow top-left
glow = Image.new("L", (W, H), 0)
ImageDraw.Draw(glow).ellipse((-160, -220, 320, 260), fill=70)
img.paste(Image.new("RGB", (W, H), (255, 250, 230)), (0, 0), glow)

# ---- right QR panel ----
px0, py0, px1, py1 = 700, 50, 1012, 550
d.rounded_rectangle((px0, py0, px1, py1), radius=26, fill=PANEL, outline=LINE, width=2)

qr = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=10, border=1)
qr.add_data(QR_URL); qr.make(fit=True)
qim = qr.make_image(fill_color=INK, back_color="white").convert("RGB")
QS = 250
qim = qim.resize((QS, QS), Image.NEAREST)
qcx = (px0 + px1) // 2
img.paste(qim, (qcx - QS // 2, 150))
d.text((qcx, 430), QR_CAPTION, font=F_CAP, fill=BRAND, anchor="mm")
d.text((qcx, 462), QR_SUB,    font=F_SUB, fill=MUTED, anchor="mm")

# ---- avatar ----
av_size = 150
try:
    av = ImageOps.fit(Image.open(AVATAR).convert("RGB"), (av_size, av_size), Image.LANCZOS)
    ss = av_size * 4
    m = Image.new("L", (ss, ss), 0)
    ImageDraw.Draw(m).ellipse((0, 0, ss, ss), fill=255)
    m = m.resize((av_size, av_size), Image.LANCZOS)
    d.ellipse((52, 52, 52 + av_size + 8, 52 + av_size + 8), fill=PANEL)  # ring
    img.paste(av, (56, 56), m)
except Exception as e:
    d.ellipse((56, 56, 56 + av_size, 56 + av_size), fill=BRAND)

# ---- name / role / org (right of avatar) ----
tx = 228
name_lines = wrap(d, NAME, F_NAME, 430)
y = 60 if len(name_lines) > 1 else 78
for ln in name_lines:
    d.text((tx, y), ln, font=F_NAME, fill=INK); y += 48
d.text((tx, y + 2), ROLE, font=F_ROLE, fill=BRAND); y += 36
for ln in wrap(d, ORG, F_ORG, 440):
    d.text((tx, y), ln, font=F_ORG, fill=MUTED); y += 24

# ---- tagline chip ----
ty = 250
tw = d.textlength(TAGLINE, font=F_TAG)
d.rounded_rectangle((56, ty, 56 + tw + 36, ty + 38), radius=19, fill=(224, 242, 254))
d.text((74, ty + 19), TAGLINE, font=F_TAG, fill=BRAND, anchor="lm")

# ---- contact ----
cy = 322
for lab, val in CONTACT:
    d.text((56, cy), lab, font=F_LAB, fill=BRAND)
    d.text((198, cy - 2), val, font=F_VAL, fill=INK)
    cy += 46

# ---- footer note ----
d.text((56, 556 - 8), "Scan the code to view my digital card & save my contact.",
       font=F_SUB, fill=MUTED, anchor="lb")

img.save(OUT, "PNG")
print("Saved:", OUT, "| QR ->", QR_URL)
