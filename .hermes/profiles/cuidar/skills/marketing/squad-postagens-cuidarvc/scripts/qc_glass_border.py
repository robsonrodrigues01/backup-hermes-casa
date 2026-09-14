#!/usr/bin/env python
"""qc_glass_border.py — verifica borda de painel glass por PIXELS (visão falha em linhas <=3px).
Uso: python3 qc_glass_border.py <card.png> <y0-do-box> [coluna]
Saída: brilho máximo por linha em y0-4..y0+8; pico >180 em y0±2 = borda branca PRESENTE.
Linguagem glass oficial do cuidar.vc — ver references/glass-card-notas.md."""
import sys
from PIL import Image

path, y0 = sys.argv[1], int(sys.argv[2])
col = int(sys.argv[3]) if len(sys.argv) > 3 else 540
img = Image.open(path).convert("RGB")
peaks = []
for dy in range(-4, 9):
    y = y0 + dy
    if 0 <= y < img.height:
        b = max(img.getpixel((col, y)))
        peaks.append((dy, b))
        print(f"y0{dy:+d}: brilho {b}")
near = [b for dy, b in peaks if abs(dy) <= 2]
print("BORDA PRESENTE" if near and max(near) > 180
      else "BORDA AUSENTE: aumentar width (3px) e/ou alpha (230) do outline em glass()")
