# -*- coding: utf-8 -*-
"""Découpe des figures du module froid/clim à partir des pages rendues.

Fichier de spécification (TSV, une figure par ligne) :
    page  x0  y0  x1  y1  nom
coordonnées en points PDF (origine en haut à gauche). Sorties : work/batchfc_figs/<nom>.jpg
Usage : .venv/bin/python work/fc_crop.py work/fc_crops.tsv
"""
import os, sys
from PIL import Image
SRC = "work/fc/rd_p%02d.jpg"
OUT = "work/batchfc_figs"
SCALE = 170 / 72.0
os.makedirs(OUT, exist_ok=True)
spec = sys.argv[1] if len(sys.argv) > 1 else "work/fc_crops.tsv"
n = 0
for line in open(spec, encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    f = line.split()
    pg, x0, y0, x1, y1, name = int(f[0]), *[float(v) for v in f[1:5]], f[5]
    im = Image.open(SRC % pg)
    box = [int(v * SCALE) for v in (x0, y0, x1, y1)]
    box = [max(0, box[0]), max(0, box[1]), min(im.width, box[2]), min(im.height, box[3])]
    im.crop(box).save(f"{OUT}/{name}.jpg", quality=88, optimize=True)
    print(name, box, "->", round((box[2]-box[0])/SCALE, 1), "x", round((box[3]-box[1])/SCALE, 1), "pt")
    n += 1
print("figures:", n)
