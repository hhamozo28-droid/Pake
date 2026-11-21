# -*- coding: utf-8 -*-
"""Préparation du module « ELE 1204 — Technicien en Froid et Climatisation N4 ».

Le PDF fourni est une traduction GOOGLE : le texte français d'origine a été effacé
de l'image de fond, la seule couche texte restante est l'arabe (formes de présentation,
ordre visuel, crochets miroir). Ce script :
  1. exporte par page   : image de fond brute (graphismes sans texte) -> work/fc/bg_pNN.jpg
                         rendu complet (graphismes + arabe en place)  -> work/fc/rd_pNN.jpg
  2. reconstruit le texte ARABE en ordre logique (tri des glyphes par x, runs LTR inversés)
  3. détecte les grilles de tableau dans l'image de fond (lignes sombres longues)
     et répartit les blocs de texte dans les cellules
Sorties : work/fc_blocks.json  +  work/fc_skel/pNN.txt  (brouillon de lecture)

Usage : .venv/bin/python work/fc_prep.py [P0 P1]
"""
import json, os, re, sys, unicodedata
import pymupdf
from PIL import Image

SRC = "work/ELE1204-froid-clim-N4.pdf"
DPI = 170
AR = r"^\s*[" + "\u0600-\u06ff" + "\ufb50-\ufdff\ufe70-\ufeff" + r"]"
RTL = lambda o: 0x0590 <= o <= 0x07FF or 0xFB50 <= o <= 0xFDFF or 0xFE70 <= o <= 0xFEFF or 0x0600 <= o <= 0x06FF
MIRROR = {")": "(", "(": ")", "[": "]", "]": "[", "{": "}", "}": "{", "<": ">", ">": "<"}
P0 = int(sys.argv[1]) if len(sys.argv) > 1 else 1
P1 = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9

os.makedirs("work/fc", exist_ok=True)
os.makedirs("work/fc_skel", exist_ok=True)

doc = pymupdf.open(SRC)


def norm(ch):
    if 0xFB50 <= ord(ch) <= 0xFDFF or 0xFE70 <= ord(ch) <= 0xFEFF:
        n = unicodedata.normalize("NFKC", ch)
        if n != ch:
            return n
    return ch


def cls(c):
    o = ord(c)
    if RTL(o):
        return "R"
    if c.isalpha():
        return "L"
    if c.isdigit() or c in "%\u2030\u066b\u00b0\u00b2\u00b3":
        return "D"
    if c == "\u0640":
        return "T"
    return "N"


def tological(chars):
    """chars = [(x0,x1,c)] posés de gauche à droite (ordre VISUEL du PDF).
    Rend l'ordre LOGIQUE : les suites arabes sont retournées (et leurs crochets mis
    en miroir), les nombres et les mots latins restent dans leur sens, puis l'ordre
    des groupes est inversé (RTL). Les neutres (ponctuation, espaces) suivent le groupe
    arabe précédent, comme en bidi."""
    seq = []
    for x0, x1, c in chars:
        k = cls(c)
        if k == "T":
            continue
        if k == "N":
            k = seq[-1][1] if seq and seq[-1][1] == "R" else "R"
        seq.append((c, k))
    groups = []
    for c, k in seq:
        if groups and groups[-1][1] == k:
            groups[-1][0] += c
        else:
            groups.append([c, k])
    def fix(s):
        o = []
        for ch in s:
            n = unicodedata.normalize("NFKC", ch)
            o.append(n[0] if len(n) == 1 and ord(ch) > 0xFB50 else n)
        return "".join(o)
    out = []
    for txt, k in groups:
        if k == "R":
            txt = fix(txt[::-1])
            txt = "".join(MIRROR.get(c, c) for c in txt)
        out.append(txt)
    out = out[::-1]
    s = "".join(out)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s+([،؛:.!?\u060c\u061b])", r"\1", s)
    s = re.sub(r"([،؛:\u060c\u061b])(?=\S)", r"\1 ", s)
    s = re.sub(r"\(\s+", "(", s); s = re.sub(r"\s+\)", ")", s)
    s = re.sub(r"\[\s+", "[", s); s = re.sub(r"\s+\]", "]", s)
    return unicodedata.normalize("NFC", s).strip()


def logical_line(chars):
    return tological(chars)


def page_chars(p):
    """list de lignes : {'y':,'x0':,'x1':,'chars':[(x0,x1,c)]}"""
    lines = []
    d = p.get_text("rawdict")
    for b in d["blocks"]:
        if b["type"] != 0:
            continue
        for ln in b["lines"]:
            cs = []
            for sp in ln["spans"]:
                for ch in sp["chars"]:
                    if ch["c"] in ("\n",):
                        continue
                    bb = ch["bbox"]
                    cs.append((bb[0], bb[2], ch["c"]))
            if not cs:
                continue
            cs.sort(key=lambda t: t[0])
            x0 = min(c[0] for c in cs); x1 = max(c[1] for c in cs)
            y0 = min(min(c for c in [t[0] for t in [ln["bbox"][1]]]) , 0) if False else ln["bbox"][1]
            lines.append({"y": ln["bbox"][1], "y1": ln["bbox"][3], "x0": x0, "x1": x1, "chars": cs,
                          "size": max((sp["size"] for sp in ln["spans"]), default=10)})
    return lines


def blocks_from_lines(lines, gap=9.0):
    """regroupe les lignes en paragraphes (même colonne, y contigus)"""
    lines = sorted(lines, key=lambda l: (round(l["y"], 1), l["x0"]))
    out = []
    for l in lines:
        placed = False
        for b in out:
            if abs(b["x0"] - l["x0"]) < 26 and 0 <= l["y"] - b["y1"] < gap and abs(l["x1"] - b["x1"]) < 130:
                b["lines"].append(l); b["y1"] = l["y1"]; b["x0"] = min(b["x0"], l["x0"]); b["x1"] = max(b["x1"], l["x1"])
                placed = True; break
        if not placed:
            out.append({"x0": l["x0"], "y0": l["y"], "x1": l["x1"], "y1": l["y1"], "lines": [l]})
    for b in out:
        b["text"] = "\n".join(logical_line(l["chars"]) for l in b["lines"])
        b["size"] = max(l["size"] for l in b["lines"])
    return out


GRID_L={}
def grid_from_image(path, W, H):
    """Détecte les traits de tableau dans l'image de fond : rendues binaires puis
    moyennées par ligne / par colonne (redimensionnement 1xN)."""
    im = Image.open(path).convert("L")
    w, h = im.size
    bi = im.point(lambda v: 255 if v < 150 else 0)
    rows = bi.resize((1, h), Image.BILINEAR)
    cols = bi.resize((w, 1), Image.BILINEAR)
    ry = [255 - rows.getpixel((0, y)) for y in range(h)]
    cx = [255 - cols.getpixel((x, 0)) for x in range(w)]
    def peaks(v, frac, minlen):
        thr = int(255 * frac); run = []; res = []
        for i, a in enumerate(v):
            if a > thr:
                run.append(i)
            else:
                if len(run) >= minlen:
                    res.append((run[0] + run[-1]) // 2)
                run = []
        if len(run) >= minlen:
            res.append((run[0] + run[-1]) // 2)
        return res
    hl = peaks(ry, 0.42, 6)          # traits horizontaux
    vl = peaks(cx, 0.28, 4)          # traits verticaux
    sc = (W / w, H / h)
    hl = [y * sc[1] for y in hl]; vl = [x * sc[0] for x in vl]
    GRID_L["h"]=hl; GRID_L["v"]=vl
    if len(hl) < 2 or len(vl) < 2:
        return []
    cells = []
    for i in range(len(hl) - 1):
        for j in range(len(vl) - 1):
            r0, r1 = hl[i], hl[i + 1]; c0, c1 = vl[j], vl[j + 1]
            if r1 - r0 < 9 or c1 - c0 < 22:
                continue
            cells.append({"r": i, "c": j, "rect": [c0, r0, c1, r1]})
    return cells


out = []
for pno in range(doc.page_count):
    if not (P0 <= pno + 1 <= P1):
        continue
    p = doc[pno]
    W, H = p.rect.width, p.rect.height
    bgj = f"work/fc/bg_p{pno+1:02d}.jpg"; rdj = f"work/fc/rd_p{pno+1:02d}.jpg"
    if not os.path.exists(bgj):
        ims = p.get_images(full=True)
        for im in ims:
            b = doc.extract_image(im[0])
            if b["width"] > 700:
                open(bgj, "wb").write(b["image"]); break
    if not os.path.exists(rdj):
        pix = p.get_pixmap(dpi=DPI)
        pix.pil_save(rdj, quality=82, optimize=True)
    allchars = []
    for b in p.get_text("rawdict")["blocks"]:
        if b["type"] != 0:
            continue
        for ln in b["lines"]:
            for sp in ln["spans"]:
                for ch in sp["chars"]:
                    bb = ch["bbox"]
                    if ch["c"] == "\n":
                        continue
                    allchars.append({"x0": round(bb[0], 1), "x1": round(bb[2], 1), "y0": round(bb[1], 1),
                                     "y1": round(bb[3], 1), "c": ch["c"], "sz": round(sp["size"], 1)})
    CUR_CHARS = allchars
    lines = page_chars(p)
    # on exclut le pied d'une ligne d'eau « Machine Translated by Google »
    lines = [l for l in lines if "Translated" not in "".join(c for _, _, c in l["chars"])]
    blks = blocks_from_lines(lines)
    cells = grid_from_image(bgj, W, H) if os.path.exists(bgj) else []
    for b in blks:
        b["cell"] = None
        cx = (b["x0"] + b["x1"]) / 2; cy = (b["y0"] + b["y1"]) / 2
        for c in cells:
            x0, y0, x1, y1 = c["rect"]
            if x0 - 1 <= cx <= x1 + 1 and y0 - 2 <= cy <= y1 + 2:
                c["text"] = (c.get("text", "") + "\n" + b["text"]).strip(); c["rect"] = [round(v, 1) for v in c["rect"]]
                b["cell"] = (c["r"], c["c"]); break
    for c in cells:
        c.setdefault("text", "")
    out.append({"page": pno + 1, "w": round(W, 1), "h": round(H, 1), "landscape": W > H,
                "hlines": [round(v, 1) for v in GRID_L.get("h", [])], "vlines": [round(v, 1) for v in GRID_L.get("v", [])],
                "blocks": [{"x0": round(b["x0"], 1), "y0": round(b["y0"], 1), "x1": round(b["x1"], 1),
                            "y1": round(b["y1"], 1), "size": round(b["size"], 1), "cell": b["cell"],
                            "text": b["text"]} for b in blks],
                "chars": CUR_CHARS, "grid": cells, "nrows": (max(c["r"] for c in cells) + 1) if cells else 0,
                "ncols": (max(c["c"] for c in cells) + 1) if cells else 0})

json.dump(out, open("work/fc_blocks.json", "w"), ensure_ascii=False, indent=1)

for pg in out:
    fn = f"work/fc_skel/p{pg['page']:02d}.txt"
    L = [f"=== PDF p{pg['page']}  {'paysage' if pg['landscape'] else 'portrait'} {pg['w']}x{pg['h']} | grille {pg['nrows']}x{pg['ncols']} ==="]
    if pg["grid"]:
        rows = {}
        for c in pg["grid"]:
            rows.setdefault(c["r"], {})[c["c"]] = c["text"].replace("\n", " ")
        for r in sorted(rows):
            L.append(f"ligne {r}: " + " || ".join(rows[r].get(k, "") for k in sorted(rows[r])))
    for b in sorted(pg["blocks"], key=lambda b: (b["y0"], b["x0"])):
        if b["cell"] is None:
            L.append(f"[{b['y0']:.0f},{b['x0']:.0f}-{b['x1']:.0f} s{b['size']:.0f}] {b['text']}")
    open(fn, "w", encoding="utf-8").write("\n".join(L) + "\n")
print("pages:", len(out), "->", "work/fc_blocks.json", "work/fc_skel/")
