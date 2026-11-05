# -*- coding: utf-8 -*-
"""Extracteur autonome pour la traduction AR du guide « Fabrication prototype veston ».

    python work/extract.py P0 P1 TAG          # ex : python work/extract.py 189 243 batch4

Produit (tout sous work/) :
  {TAG}_blocks.json   régions + lignes (avec police/taille/gras/couleur) par page
  {TAG}_extra.json    images « oubliées » (fusion/strip décoratif) récupérées une par une
  {TAG}_figs/*.jpg    vignettes découpées à la taille d'origine (200 dpi, jamais redimensionnées)
  skel/{TAG}_skeleton.txt  squelette de lecture pour la traduction

Contrairement à la v1 : le bandeau décoratif latéral n'est jamais fusionné avec les images,
et aucune image de contenu n'est écartée pour cause de « trop grande ».
"""
import fitz, json, os, sys, re
from PIL import Image

P0, P1, TAG = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "work", "source-VC-2019-veston.pdf")
FIG  = os.path.join(ROOT, "work", f"{TAG}_figs")
SKEL = os.path.join(ROOT, "work", "skel")
DPI  = 200
SC   = DPI / 72.0
os.makedirs(FIG, exist_ok=True); os.makedirs(SKEL, exist_ok=True)

doc = fitz.open(SRC)
ROM = re.compile(r"^\s*([IVXLCDM]+)\s*$")

def rom2int(s):
    v = {"I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000}
    t = p = 0
    for ch in reversed(s):
        n = v[ch]; t += n if n >= p else -n; p = max(p, n)
    return t

def grow(r, dx, dy=None):
    dy = dx if dy is None else dy
    return fitz.Rect(r.x0 - dx, r.y0 - dy, r.x1 + dx, r.y1 + dy)

def overlap(a, b):
    r = fitz.Rect(a); r.intersect(fitz.Rect(b)); return r

def cluster(rects, gap=6.0):
    """fusionne les rectangles qui se touchent (grilles d'images, planches), jamais au-delà de la page."""
    rs = [fitz.Rect(r) for r in rects]
    changed = True
    while changed:
        changed = False
        out = []
        while rs:
            cur = rs.pop()
            merged = True
            while merged:
                merged = False
                for i, r in enumerate(rs):
                    g = grow(cur, gap)
                    if g.intersects(r):
                        cur |= r; rs.pop(i); merged = True; changed = True
            out.append(cur)
        rs = out
    return rs

pages_out, extra_out, skel = [], [], []
for pno in range(P0 - 1, min(P1, doc.page_count)):
    page = doc[pno]
    prec = page.rect
    n = pno + 1
    skel.append(f"\n=== PDF p{n} ===")

    # ---------- lignes de texte (avec typographie) ----------
    raw = page.get_text("dict")
    lines = []
    for blk in raw.get("blocks", []):
        if blk.get("type") != 0:
            continue
        for ln in blk.get("lines", []):
            spans = ln.get("spans", [])
            txt = "".join(s["text"] for s in spans).strip()
            if not txt:
                continue
            bb = fitz.Rect(ln["bbox"])
            sz = max(s["size"] for s in spans)
            bold = any((s["flags"] & 16) or "Bold" in s["font"] or "bold" in s["font"] for s in spans)
            col = spans[0]["color"]
            lines.append({"text": txt, "x0": round(bb.x0, 1), "x1": round(bb.x1, 1),
                          "y0": round(bb.y0, 1), "y1": round(bb.y1, 1),
                          "size": round(sz, 1), "bold": bool(bold), "color": col, "reg": None})
    # numéro de page imprimée (pied de page)
    printed = None
    for L in lines:
        if L["y0"] > prec.height * 0.90 and (L["text"].isdigit() or ROM.match(L["text"])):
            printed = int(L["text"]) if L["text"].isdigit() else rom2int(ROM.match(L["text"]).group(1))
            break

    # ---------- images ----------
    rects = []
    for info in page.get_image_info(xrefs=True):
        try:
            r = fitz.Rect(info["bbox"])
        except Exception:
            continue
        if r.is_empty or r.width < 4 or r.height < 4:
            continue
        rects.append(r)

    # --- aires dessinées (tableaux vectoriels) : uniquement des « cellules » ---
    cells = []
    for item in page.get_drawings():
        try:
            r = fitz.Rect(item["rect"])
        except Exception:
            continue
        if r.is_empty:
            continue
        # filets pleine largeur / pleine hauteur : ne jamais les faire cluster
        if (r.width > 0.55 * prec.width and r.height < 14) or (r.height > 0.55 * prec.height and r.width < 14):
            continue
        if r.get_area() > 0.45 * prec.get_area():
            continue
        if r.width < 6 and r.height < 6:
            continue
        cells.append(r)
    vec = []
    for c in cluster(cells, gap=1.5):
        if c.width < 60 or c.height < 40:
            continue
        if c.get_area() > 0.72 * prec.get_area():
            continue
        vec.append(c)
    rects.extend(vec)
    def decorative(r):
        """bandeau latéral / filets : pleine hauteur mais très étroits, ou minuscules."""
        full_h = r.height > 0.95 * prec.height
        full_w = r.width > 0.95 * prec.width
        if (full_h and r.width < 0.35 * prec.width) or (full_w and r.height < 0.06 * prec.height):
            return True
        return r.width < 24 and r.height < 24          # petites icônes / puces décoratives

    kept, dropped = [], []
    for r in rects:
        (dropped if decorative(r) else kept).append(r)

    clusters = []
    for c in cluster(kept, gap=4.0):
        c = c & prec
        if c.width > 18 and c.height > 18:
            clusters.append(c)
    # un cluster qui avalerait la page entière est un artefact de cadre : on le remplace par ses images
    fixed = []
    for c in clusters:
        if c.get_area() > 0.78 * prec.get_area():
            parts = [r & prec for r in kept if c.contains(r) or overlap(c, r).get_area() > 0.4 * max(r.get_area(), 1)]
            parts = [p for p in parts if p.width > 18 and p.height > 18 and p.get_area() <= 0.78 * prec.get_area()]
            fixed.extend(parts if parts else [])
        else:
            fixed.append(c)
    # dédoublonnage
    clusters = []
    for c in fixed:
        if not any(overlap(c, d).get_area() > 0.85 * min(c.get_area(), d.get_area()) for d in clusters):
            clusters.append(c)
    clusters.sort(key=lambda c: (round(c.y0), c.x0))

    regions = []
    for i, c in enumerate(clusters, 1):
        rid = f"p{n:03d}_r{i}"
        px = int(c.width * SC); py = int(c.height * SC)
        zoom = min(2.5, max(0.5, 1600.0 / max(px, 1)))
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom * SC, zoom * SC), clip=c, alpha=False)
        png = os.path.join(FIG, rid + ".png")
        jpg = os.path.join(FIG, rid + ".jpg")
        pix.save(png)
        im = Image.open(png).convert("RGB"); im.save(jpg, quality=88, optimize=True)
        os.remove(png)
        inside = [L for L in lines
                  if c.contains(fitz.Point((L["x0"] + L["x1"]) / 2, (L["y0"] + L["y1"]) / 2))]
        for L in inside:
            L["reg"] = rid
        kind = "fig"
        if inside:
            short = sum(1 for L in inside if len(L["text"]) < 26)
            kind = "tab" if (len(inside) >= 6 and short >= 0.5 * len(inside)) else "mixed"
        regions.append({"id": rid, "kind": kind,
                        "x0": round(c.x0, 1), "y0": round(c.y0, 1),
                        "x1": round(c.x1, 1), "y1": round(c.y1, 1),
                        "w_pt": round(c.width, 1), "h_pt": round(c.height, 1),
                        "px": [im.size[0], im.size[1]]})
        skel.append(f"  [img] {rid} {regions[-1]['kind']} {round(c.width)}x{round(c.height)}pt "
                    f"@({round(c.x0)},{round(c.y0)}) lignes={len(inside)}")

    # ---------- images « oubliées » (celles du bandeau + toute image non couverte) ----------
    def covered(r):
        m = grow(r, -2)
        for c in clusters:
            if c.contains(m) or overlap(c, m).get_area() > 0.55 * max(m.get_area(), 1):
                return True
        return False

    k = 0
    for r in kept + dropped:
        if covered(r):
            continue
        if r.width < 12 and r.height < 12:
            continue
        k += 1
        rid = f"p{n:03d}_d{k}"
        pix = page.get_pixmap(matrix=fitz.Matrix(200 / 72, 200 / 72), clip=r, alpha=False)
        png = os.path.join(FIG, rid + ".png"); jpg = os.path.join(FIG, rid + ".jpg")
        pix.save(png); im = Image.open(png).convert("RGB"); im.save(jpg, quality=88, optimize=True)
        os.remove(png)
        rec = {"page": n, "id": rid, "clip": [round(v, 1) for v in (r.x0, r.y0, r.x1, r.y1)],
               "w_pt": round(r.width, 1), "h_pt": round(r.height, 1),
               "px": [im.size[0], im.size[1]]}
        extra_out.append(rec)
        skel.append(f"  [rec] {rid} {round(r.width)}x{round(r.height)}pt @({round(r.x0)},{round(r.y0)})")

    skel.append(f"  [printed] {printed}   [lines] {len(lines)}   [regions] {len(regions)}")
    for L in sorted(lines, key=lambda x: (round(x["y0"]), x["x0"])):
        fl = "B" if L["bold"] else " "
        skel.append(f"    {L['y0']:>6.1f} {L['x0']:>6.1f} {L['size']:>4.1f}{fl} {L['reg'] or '   '} | {L['text'][:150]}")
    pages_out.append({"page": n, "printed": printed, "regions": regions, "lines": lines})

json.dump({"pages": pages_out}, open(os.path.join(ROOT, "work", f"{TAG}_blocks.json"), "w"), ensure_ascii=False)
json.dump(extra_out, open(os.path.join(ROOT, "work", f"{TAG}_extra.json"), "w"), ensure_ascii=False)
open(os.path.join(ROOT, "work", "skel", f"{TAG}_skeleton.txt"), "w", encoding="utf-8").write("\n".join(skel))
nj = sum(1 for f in os.listdir(FIG) if f.endswith(".jpg"))
print(f"{TAG}: pages={len(pages_out)} regions={sum(len(p['regions']) for p in pages_out)} "
      f"images_récupérées={len(extra_out)} fichiers={nj} lignes={sum(len(p['lines']) for p in pages_out)}")
