# -*- coding: utf-8 -*-
"""Cartes d'unité — v3 : découpe de CHAQUE LIGNE selon les colonnes du tableau.

Le calque « Google traduit » pose une ligne visuelle = un seul bloc de texte, ce qui
entrelace les colonnes. Ici on reconstruit les colonnes à partir des bornes x des
libellés d'en-tête (لا. / المهارات / الأنشطة / المعرفة), puis on rend chaque cellule en
ordre logique arabe. Les lignes de compétences sont délimitées par les repères « n.n ».

Usage : .venv/bin/python work/fc_mk3.py P0 P1 out.md [--fullpage-img]
"""
import json, re, sys, unicodedata
import pymupdf

A, B, OUT = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
doc = pymupdf.open("work/ELE1204-froid-clim-N4.pdf")
RTL = lambda o: 0x0590 <= o <= 0x08FF or 0xFB50 <= o <= 0xFDFF or 0xFE70 <= o <= 0xFEFF
MIRROR = {")": "(", "(": ")", "[": "]", "]": "[", "{": "}", "}": "{", "<": ">", ">": "<"}

TERM = [
 (r"برامج التدريب المهني", "برامج التكوين المهني"), (r"برنامج التدريب المهني", "برنامج التكوين المهني"),
 (r"التدريب المهني", "التكوين المهني"), (r"التدريبية|التدريبى", "التكوينيّة"),
 (r"مؤسسة التدريب|مؤسسات التدريب|مركز التدريب|مراكز التدريب", "مؤسّسة التكوين"),
 (r"شركات التدريب", "المقاولات المُواكِبة"), (r"شركة التدريب", "المقاولة المُواكِبة"),
 (r"داخل الشركة|في الشركة|للشركة|الشركة", "المقاولة"),
 (r"المتدربين", "المتربّصين"), (r"المتدرب", "المتربّص"),
 (r"المدربين", "المُكوِّنين"), (r"المدرب", "المُكوِّن"),
 (r"مشرف التدريب", "مشرف التكوين"), (r"مدة التدريب", "مدّة التكوين"),
 (r"ساعات التدريب", "ساعات التكوين"), (r"خطة التدريب|خطة تدريب", "خُطّة التكوين"),
 (r"التدريب", "التكوين"),
]
REPAIR = [(r"\bخلل\b", "خلال"), (r"الساس", "الأساس"), (r"الاهداف|الهداف\b", "الأهداف"),
 (r"\bعل\b", "على"), (r"\bالملئمة\b", "الملائمة"), (r"\bاللمانية\b", "الألمانيّة"),
 (r"\bالتحادية\b", "الاتّحاديّة"), (r"\bالوليات\b", "الولايات"), (r"\bالا\b", "إلّا"),
 (r"\bالتي\b", "التي")]

def cls(c):
    o = ord(c)
    if RTL(o):
        return "R"
    if c == "\u0640":
        return "T"
    if c.isalpha():
        return "L"
    if c.isdigit() or c in "%\u2030\u00b0\u00b2\u00b3":
        return "D"
    return "N"

def tological(chars):
    seq = []
    for x0, x1, c in chars:
        k = cls(c)
        if k == "T":
            continue
        if k == "N":
            k = "R" if (seq and seq[-1][1] == "R") else "R"
        seq.append((c, k))
    groups = []
    for c, k in seq:
        if groups and groups[-1][1] == k:
            groups[-1][0] += c
        else:
            groups.append([c, k])
    def fix(t):
        o = []
        for ch in t:
            n = unicodedata.normalize("NFKC", ch)
            o.append(n[0] if len(n) == 1 and ord(ch) > 0xFB50 else n)
        return "".join(o)
    out = []
    for t, k in groups:
        if k == "R":
            t = fix(t[::-1])
            t = "".join(MIRROR.get(c, c) for c in t)
        out.append(t)
    out = out[::-1]
    s = "".join(out)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s+([،؛:.!?])", r"\1", s)
    return unicodedata.normalize("NFC", s).strip()

def clean(t):
    t = re.sub(r"\s+", " ", t or "").strip()
    for pat, rep in TERM + REPAIR:
        t = re.sub(pat, rep, t)
    return t

def page_lines(p):
    lines = []
    for b in p.get_text("rawdict")["blocks"]:
        if b["type"] != 0:
            continue
        for ln in b["lines"]:
            cs = []
            for sp in ln["spans"]:
                for ch in sp["chars"]:
                    if ch["c"] == "\n":
                        continue
                    bb = ch["bbox"]
                    cs.append((bb[0], bb[2], ch["c"], round(sp["size"], 1)))
            if not cs:
                continue
            cs.sort(key=lambda t: t[0])
            lines.append({"y0": ln["bbox"][1], "y1": ln["bbox"][3], "cs": cs,
                          "x0": min(c[0] for c in cs), "x1": max(c[1] for c in cs)})
    lines.sort(key=lambda l: (round(l["y0"], 1), l["x0"]))
    return lines

KEY = {"no": "لا.", "sk": "المهارات", "ac": "الأنشطة", "kn": "المعرفة"}
for pg in range(A, B + 1):
    p = doc[pg - 1]
    W, H = p.rect.width, p.rect.height
    lines = [l for l in page_lines(p)
             if "Translated" not in tological([(a, b, c) for a, b, c, _ in l["cs"]])]
    for l in lines:
        l["t"] = tological([(a, b, c) for a, b, c, _ in l["cs"]])
    # — bornes de colonnes : bandes d'en-tête (les libellés peuvent être sur 2 lignes)
    hits = {}
    for l in lines:
        if l["y0"] < 55 or l["y1"] > H - 55:
            continue
        for k, v in KEY.items():
            if v in l["t"]:
                hits.setdefault(k, []).append(l)
    best = None
    for k, ls in list(hits.items()):
        for ref in ls:
            band = [kk for kk, ll in hits.items() if any(abs(x["y0"] - ref["y0"]) < 34 for x in ll)]
            if best is None or len(band) > best[0]:
                best = (len(band), ref["y0"], band)
    if best is None or best[0] < 2:
        out = [f"#PAGE {pg}", "@SEC بطاقة وحدة"]
        for l in lines:
            if l["y0"] > H - 60 or l["y0"] < 40:
                continue
            t = clean(l["t"])
            if t:
                out.append("@P " + t)
        open(OUT, "a", encoding="utf-8").write("\n".join(out) + "\n"); continue
    kband = best[2]; hy = best[1]
    inband = {k: [l for l in hits[k] if abs(l["y0"] - hy) < 34] for k in kband}
    xr = {k: (min(l["x0"] for l in v), max(l["x1"] for l in v)) for k, v in inband.items()}
    order = sorted(xr, key=lambda k: xr[k][0])
    bounds = [(xr[order[i]][1] + xr[order[i + 1]][0]) / 2 for i in range(len(order) - 1)]
    ytop = max(l["y1"] for v in inband.values() for l in v)
    yhdr0 = min(l["y0"] for v in inband.values() for l in v)
    def colof(c):
        cx = (c[0] + c[1]) / 2
        for i, b in enumerate(bounds):
            if cx < b:
                return order[i]
        return order[-1]
    head = [l for l in lines if l["y0"] < yhdr0 - 3]
    body = [l for l in lines if l["y0"] > ytop and l["y1"] < H - 58]
    out = [f"#PAGE {pg}", "@SEC بطاقة وحدة"]
    # — bandeau supérieur (titre de l'unité, durée…)
    groups, cur, cy = [], [], None
    for l in head:
        if cy is not None and abs(l["y0"] - cy) > 7:
            groups.append(cur); cur = []
        cy = l["y0"]; cur.append(l)
    if cur:
        groups.append(cur)
    for g in groups:
        g = sorted(g, key=lambda l: -l["x0"])
        segs, cur = [], []
        for i, l in enumerate(g):
            if cur and (cur[-1]["x0"] - l["x1"]) > 55:
                segs.append(cur); cur = []
            cur.append(l)
        if cur:
            segs.append(cur)
        for sg in segs:
            t = clean(" ".join(l["t"] for l in sorted(sg, key=lambda l: -l["x0"])))
            if t:
                out.append("@P2 " + t)
    # — cellules : (ligne, colonne)
    cells = {}
    for l in body:
        per = {}
        for c in l["cs"]:
            per.setdefault(colof(c), []).append(c)
        for k, cs in per.items():
            t = tological([(a, b, ch) for a, b, ch, _ in cs])
            if t.strip():
                cells.setdefault((round(l["y0"], 1), k), []).append(t.strip())
    ys = sorted(set(k[0] for k in cells))
    # — segmentation en lignes de compétence : repère n.n dans la 1re colonne
    first = order[0]
    marks = []
    for y in ys:
        t = " ".join(cells.get((y, first), []))
        m = re.match(r"^\s*(\d+\.\d+)", t)
        if m:
            marks.append((y, m.group(1), t[m.end():].strip()))
    boundsy = [m[0] for m in marks] or ys[:1]
    boundsy = sorted(set(boundsy + [ys[-1] + 1]))
    # — liste des compétences repérées par « n.n » dans la colonne no
    marks = []
    for l in body:
        t = tological([(a, b, c) for a, b, c, _ in l["cs"] if colof((a, b, c)) == order[0]])
        m = re.match(r"^\s*(\d+\.\d+)", t)
        if m:
            marks.append((l["y0"], m.group(1).rstrip("."), t[m.end():].strip()))
    if marks:
        out.append("@H3 المهارات المهنيّة للوحدة")
    for y, num, tail in marks:
        # première ligne de la colonne « المهارات » à la même hauteur
        nxt = [m[0] for m in marks if m[0] > y + 3]
        hi = min(nxt, default=10 ** 6)
        seg_all = []
        for l in body:
            if y - 2 <= l["y0"] < hi - 2:
                seg = [c for c in l["cs"] if colof((c[0], c[1], c[2])) == "sk"]
                if seg:
                    t = tological([(a, b, ch) for a, b, ch, _ in seg])
                    if t.strip():
                        seg_all.append(t.strip())
        skt = " ".join(seg_all)
        t = clean(" ".join(x for x in (tail, skt) if x))
        t = re.sub(r"\s*\.\s*", "، ", t)
        if t:
            out.append(f"@U المهارة {num} — {t}")
    out.append("@TABEND")
    if 22 <= pg <= 65:
        wide = W > H
        out.append("@P4 الصورة المرجعيّة لصفحة الأصل (كما هي، مع النصّ العربيّ المُطبَع فوقها)")
        out.append(f"@IMG card_p{pg:02d} {26.5 if wide else 17.5}")
        out.append("@CAP بطاقة الوحدة كما وردت في صفحة الأصل (PDF %d). تُعتمد عند الشكّ، لأنّ صناديق ترجمة الآلة تقطع أطراف الأسطر داخل الخلايا." % pg)
    open(OUT, "a", encoding="utf-8").write("\n".join(out) + "\n")
print("ok", A, B)
