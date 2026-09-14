"""Desenha o avatar flat do Claudinho (1024x1024 PNG)."""
from PIL import Image, ImageDraw

S = 2048  # canvas de desenho (downscale 4x = anti-aliasing)
img = Image.new("RGB", (S, S), (16, 38, 59))  # #10263B navy
d = ImageDraw.Draw(img)

NAVY2 = (23, 54, 85)     # circulo de fundo
TEAL = (30, 110, 104)    # camisa
SKIN = (232, 181, 139)
SKIN_SH = (200, 144, 96)
HAIR = (36, 24, 18)
WHITE = (250, 250, 248)
BROW = (36, 24, 18)
BLUSH = (230, 146, 131)

# fundo redondo
d.ellipse((104, 104, 1944, 1944), fill=NAVY2)
# torso
d.ellipse((352, 1640, 1696, 2560), fill=TEAL)
# pescoco
d.rounded_rectangle((912, 1420, 1136, 1800), radius=90, fill=SKIN)
# orelhas (antes da cabeca, pra espiar dos lados)
d.ellipse((664, 902, 740, 1064), fill=SKIN)
d.ellipse((1308, 902, 1384, 1064), fill=SKIN)
# cabeca
d.ellipse((704, 496, 1344, 1372), fill=SKIN)
# cabelo (meia-elipse superior, risca reta)
d.pieslice((672, 436, 1384, 1120), 180, 360, fill=HAIR)
# gola V branca
d.polygon(((846, 1734), (1024, 1924), (1202, 1734)), fill=WHITE)
# sobrancelhas
d.rounded_rectangle((834, 952, 992, 1004), radius=24, fill=BROW)
d.rounded_rectangle((1056, 952, 1214, 1004), radius=24, fill=BROW)
# olhos + brilho
d.ellipse((884, 1030, 952, 1098), fill=(29, 17, 9))
d.ellipse((1096, 1030, 1164, 1098), fill=(29, 17, 9))
d.ellipse((902, 1044, 926, 1068), fill=WHITE)
d.ellipse((1114, 1044, 1138, 1068), fill=WHITE)
# nariz
d.line((1024, 1048, 1024, 1152), fill=SKIN_SH, width=20)
d.ellipse((1008, 1132, 1040, 1164), fill=SKIN_SH)
# sorriso (arco inferior)
d.arc((872, 1090, 1176, 1298), 15, 165, fill=(122, 74, 43), width=26)
# blush
d.ellipse((788, 1174, 884, 1234), fill=BLUSH)
d.ellipse((1164, 1174, 1260, 1234), fill=BLUSH)

out = img.resize((512, 512), Image.LANCZOS)
out.save("/home/hermes/tools/claudinho-avatar.png", optimize=True)
import os
print("OK:", os.path.getsize("/home/hermes/tools/claudinho-avatar.png"), "bytes")
