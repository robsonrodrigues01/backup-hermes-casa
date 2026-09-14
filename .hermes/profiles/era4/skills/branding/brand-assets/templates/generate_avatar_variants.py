#!/usr/bin/env python3
"""Gerador multiconceito de avatares 1:1 (1024px de saída) para foto de perfil.

Copia para um scratch path e edita as funções c1/c2/c3 antes de rodar.
Uso:
  uv venv /tmp/pxv && uv pip install --python /tmp/pxv/bin/python pillow
  PFP_OUT=/tmp/era4_pfp /tmp/pxv/bin/python generate_avatar_variants.py

Padrões usados (validados em produção no bot Claudemir/ERA 4.0):
- desenho em 2048×2048 (supersampling) + Lanczos para 1024×1024;
- gradientes: desenhar grid 512px e reescalar (bicubic);
- glow: camada RGBA com blur + alpha_composite (pass duplo intensifica);
- verificação embutida: thumbnail 64px + probes de pixel.
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

S, OUT = 2048, 1024
RES = getattr(Image, "Resampling", Image)
LANCZOS, BICUBIC = RES.LANCZOS, RES.BICUBIC
OUTDIR = os.environ.get("PFP_OUT", "/tmp/era4_pfp")
CYAN = (88, 233, 255)
os.makedirs(OUTDIR, exist_ok=True)


def diag_gradient(dark, light):
    n = 512
    bg = Image.new("RGB", (n, n))
    px = bg.load()
    for y in range(n):
        for x in range(n):
            t = (x + y) / (2 * (n - 1))
            px[x, y] = tuple(int(dark[i] + (light[i] - dark[i]) * t) for i in range(3))
    return bg.resize((S, S), BICUBIC).convert("RGBA")


def v_gradient(top, bottom):
    n = 512
    bg = Image.new("RGB", (n, n))
    px = bg.load()
    for y in range(n):
        t = y / (n - 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        for x in range(n):
            px[x, y] = c
    return bg.resize((S, S), BICUBIC).convert("RGBA")


def compose(base, layer, blur):
    return Image.alpha_composite(base, layer.filter(ImageFilter.GaussianBlur(blur)))


def save(img, name):
    final = img.convert("RGB").resize((OUT, OUT), LANCZOS)
    path = os.path.join(OUTDIR, name)
    final.save(path, "PNG", optimize=True)
    print("saved", path, final.size)
    return path


# Concept 1: robô amigável, gradiente indigo→violeta, visor ciano, circuitos
def c1():
    cx, cy = S // 2, S // 2
    img = diag_gradient((23, 14, 61), (96, 48, 170))
    halo = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse([cx - 740, cy - 740, cx + 740, cy + 740], fill=(155, 120, 255, 44))
    img = compose(img, halo, 260)

    circ_layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    cd = ImageDraw.Draw(circ_layer)
    LINE, NODE, w = (150, 130, 255, 58), (90, 230, 255, 92), 7

    def circuit(pts):
        cd.line(pts, fill=LINE, width=w, joint="curve")
        x, y = pts[-1]
        cd.ellipse([x - 17, y - 17, x + 17, y + 17], outline=NODE, width=5)
        cd.ellipse([x - 8, y - 8, x + 8, y + 8], fill=NODE)

    circuit([(120, 620), (430, 620), (430, 480), (700, 480)])
    circuit([(190, 270), (190, 430), (330, 430)])
    circuit([(1928, 800), (1720, 800), (1720, 960), (1560, 960)])
    circuit([(1868, 1560), (1868, 1340), (1700, 1340)])
    circuit([(200, 1790), (420, 1790), (420, 1620)])
    for (ax, ay) in [(300, 1120), (1755, 400), (1545, 1800), (455, 1520)]:
        L = 34
        cd.line([(ax - L, ay), (ax + L, ay)], fill=LINE, width=w)
        cd.line([(ax, ay - L), (ax, ay + L)], fill=LINE, width=w)
    for (dx, dy) in [(240, 900), (1640, 540), (240, 1350), (830, 200), (1440, 1870)]:
        r = 12
        cd.ellipse([dx - r, dy - r, dx + r, dy + r], fill=NODE)
    img = Image.alpha_composite(img, circ_layer.filter(ImageFilter.GaussianBlur(1.2)))

    body, shoulder, ear_col = (69, 78, 128, 255), (46, 51, 98, 255), (38, 44, 80, 255)
    panel, stem_col = (20, 24, 46, 255), (56, 63, 106, 255)
    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([cx - 575, 1545, cx + 575, S + 60], radius=230, fill=shoulder)
    gd.ellipse([cx - 34, 1786, cx + 34, 1854], fill=CYAN + (255,))
    d.rounded_rectangle([549, 830, 655, 1105], radius=34, fill=ear_col)
    d.rounded_rectangle([1393, 830, 1499, 1105], radius=34, fill=ear_col)
    d.line([(cx, 640), (cx, 470)], fill=stem_col, width=26)
    d.ellipse([cx - 13, 457, cx + 13, 483], fill=stem_col)
    gd.ellipse([cx - 40, 385, cx + 40, 465], fill=CYAN + (255,))
    d.rounded_rectangle([cx - 395, 600, cx + 395, 1330], radius=210, fill=body)
    d.rounded_rectangle([709, 703, 1339, 1237], radius=150, fill=panel)
    gd.ellipse([820, 1140, 1228, 1300], fill=(60, 200, 255, 60))
    for ex in (cx - 110, cx + 110):
        for _ in range(2):
            gd.rounded_rectangle([ex - 60, 843, ex + 60, 1067], radius=60, fill=CYAN + (170,))
    img = compose(img, glow, 46)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([cx - 156, 857, cx - 64, 1053], radius=46, fill=CYAN + (255,))
    d.rounded_rectangle([cx + 64, 857, cx + 156, 1053], radius=46, fill=CYAN + (255,))
    d.rounded_rectangle([cx - 85, 1164, cx + 85, 1192], radius=14, fill=(110, 225, 255, 150))
    d.ellipse([cx - 30, 395, cx + 30, 455], fill=CYAN + (255,))
    sheen = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sheen)
    sd.rounded_rectangle([669, 640, 1379, 900], radius=150, fill=(255, 255, 255, 14))
    img = compose(img, sheen, 40)
    return save(img, "c1_robo_amigavel.png")


# Concept 2: logo E4 dentro de silhueta de robô, azul-marinho + ciano neon
# (usa DejaVuSans-Bold, padrão Debian/Ubuntu; ajuste o path se o SO difere)
def c2():
    cx = S // 2
    img = v_gradient((6, 13, 38), (14, 30, 78))
    deco = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    dd = ImageDraw.Draw(deco)
    for k in range(4):
        r = 340 + 210 * k
        dd.arc([cx - r, 1100 - r, cx + r, 1100 + r], start=200 + 8 * k, end=250 + 14 * k,
               fill=(90, 230, 255, 40 - 7 * k), width=6)
        dd.arc([cx - r, 1100 - r, cx + r, 1100 + r], start=304 + 10 * k, end=352 + 8 * k,
               fill=(90, 230, 255, 36 - 7 * k), width=6)
    for (dx, dy), r in [((300, 300), 10), ((1748, 300), 10), ((300, 1700), 10), ((1748, 1700), 10),
                        ((420, 240), 7), ((1628, 240), 7), ((420, 1790), 7), ((1628, 1790), 7)]:
        dd.ellipse([dx - r, dy - r, dx + r, dy + r], fill=(90, 230, 255, 70))
    img = Image.alpha_composite(img, deco.filter(ImageFilter.GaussianBlur(0.8)))

    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.rounded_rectangle([600, 560, 1448, 1580], radius=230, outline=CYAN + (255,), width=30)
    g.rounded_rectangle([520, 940, 604, 1190], radius=42, fill=CYAN + (120,))
    g.rounded_rectangle([1444, 940, 1528, 1190], radius=42, fill=CYAN + (120,))
    g.line([(cx, 560), (cx, 410)], fill=CYAN + (255,), width=26)
    g.ellipse([cx - 48, 362, cx + 48, 458], fill=CYAN + (255,))
    g.line([cx - 118, 690, cx + 118, 690], fill=(90, 230, 255, 140), width=16)
    img = compose(img, glow, 42)
    img = Image.alpha_composite(img, glow)

    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 340)
    gap = 96
    wE = font.getbbox("E")[2]
    w4 = font.getbbox("4")[2]
    total = wE + gap + w4
    xE = cx - total // 2 + 40
    x4 = cx + wE + gap - total // 2 + 40
    tglow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    tg = ImageDraw.Draw(tglow)
    for i in (2, 1, 0):
        tg.text((xE, 1064), "E", font=font, fill=CYAN + (170,), anchor="mm", stroke_width=i)
        tg.text((x4, 1064), "4", font=font, fill=CYAN + (170,), anchor="mm", stroke_width=i)
    img = compose(img, tglow, 26)
    img = Image.alpha_composite(img, tglow)
    d = ImageDraw.Draw(img)
    for ex in (cx - 90, cx + 90):
        d.ellipse([ex - 16, 800, ex + 16, 832], fill=CYAN + (230,))
    return save(img, "c2_logo_e4.png")


# Concept 3: robôzinho chibi com headset acenando, fundo roxo + grid
def c3():
    cx = S // 2
    img = diag_gradient((109, 40, 217), (168, 85, 247))
    grid = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for x in range(0, S, 128):
        gd.line([(x, 0), (x, S)], fill=(255, 255, 255, 26), width=4)
        gd.line([(0, x), (S, x)], fill=(255, 255, 255, 26), width=4)
    img = Image.alpha_composite(img, grid)
    halo = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse([cx - 620, 900, cx + 620, 2140], fill=(255, 255, 255, 40))
    img = compose(img, halo, 300)

    D, B, C, PINK = (30, 27, 75, 255), (244, 246, 255, 255), (34, 211, 238, 255), (255, 170, 200, 90)
    d = ImageDraw.Draw(img)
    d.line([(760, 1650), (700, 1900)], fill=D, width=120)
    d.line([(760, 1650), (700, 1900)], fill=B, width=86)
    d.rounded_rectangle([748, 1500, 1300, 2136], radius=130, fill=B, outline=D, width=18)
    d.line([(1288, 1620), (1560, 1352)], fill=D, width=122)
    d.line([(1288, 1620), (1560, 1352)], fill=B, width=88)
    d.ellipse([1560 - 66, 1352 - 66, 1560 + 66, 1352 + 66], fill=B, outline=D, width=16)
    d.rounded_rectangle([640, 720, 1408, 1500], radius=240, fill=B, outline=D, width=18)
    d.ellipse([830 - 40, 1260 - 40, 830 + 40, 1260 + 40], fill=PINK)
    d.ellipse([1218 - 40, 1260 - 40, 1218 + 40, 1260 + 40], fill=PINK)
    d.ellipse([880 - 56, 1130 - 56, 880 + 56, 1130 + 56], fill=D)
    d.ellipse([1168 - 56, 1130 - 56, 1168 + 56, 1130 + 56], fill=D)
    d.ellipse([896 - 18, 1112 - 18, 896 + 18, 1112 + 18], fill=(255, 255, 255, 255))
    d.ellipse([1184 - 18, 1112 - 18, 1184 + 18, 1112 + 18], fill=(255, 255, 255, 255))
    d.arc([960, 1180, 1090, 1310], start=20, end=160, fill=D, width=18)
    d.arc([600, 640, 1448, 1560], start=182, end=358, fill=C, width=40)
    d.rounded_rectangle([540, 1000, 650, 1290], radius=44, fill=C, outline=D, width=16)
    d.rounded_rectangle([1398, 1000, 1508, 1290], radius=44, fill=C, outline=D, width=16)
    d.line([578, 1145, 612, 1145], fill=D, width=14)
    d.line([1436, 1145, 1470, 1145], fill=D, width=14)
    return save(img, "c3_chibi_headset.png")


if __name__ == "__main__":
    paths = [c1(), c2(), c3()]
    from PIL import Image as I
    for p in paths:
        im = I.open(p).convert("RGB")
        im.resize((64, 64), LANCZOS).save(p.replace(OUTDIR + "/", OUTDIR + "/thumb_"))
        print(p, "corner:", im.getpixel((8, 8)), "center:", im.getpixel((512, 512)))