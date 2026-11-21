# -*- coding: utf-8 -*-
"""Génère un brouillon .md (balisage build_fc) pour les pages « cartes d'unité »
à partir de work/fc_blocks.json : colonnes détectées par les libellés d'en-tête,
lignes par regroupement vertical, puces séparées par « ¦ ».

Usage : .venv/bin/python work/fc_mk.py P0 P1 work/fcar/D_cards.md
"""
import json, re, sys, unicodedata

A, B, OUT = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
BLK = {p["page"]: p for p in json.load(open("work/fc_blocks.json"))}

TERM = [
 (r"برامج التدريب المهني", "برامج التكوين المهني"),
 (r"برنامج التدريب المهني", "برنامج التكوين المهني"),
 (r"برنامج التدريب\b", "برنامج التكوين"),
 (r"التدريب المهني", "التكوين المهني"),
 (r"التدريبية", "التكوينيّة"),
 (r"التدريبى", "التكويني"),
 (r"مؤسسة التدريب|مؤسسات التدريب|مركز التدريب|مراكز التدريب", "مؤسّسة التكوين"),
 (r"شركة التدريب|شركات التدريب|داخل الشركة|في الشركة", "داخل المقاولة المُواكِبة"),
 (r"المتدربين|المتدرب", "المتربّص"),
 (r"المدربين|المدرب", "المُكوِّن"),
 (r"مشرف التدريب", "مشرف التكوين"),
 (r"مدة التدريب", "مدّة التكوين"),
 (r"ساعات التدريب", "ساعات التكوين"),
 (r"خطة التدريب|خط تدريب|خطة تدريب", "خُطّة التكوين"),
 (r"تنظيم التدريب|عملية التدريب", "تنظيم التكوين"),
 (r"التدريب النظري", "التكوين النظري"),
 (r"التدريب", "التكوين"),
 (r"المهني(?!ة|ا)", "المهنيّ"),
]
REPAIR = [
 (r"\bخلل\b", "خلال"),
 (r"التعليمي(?!ـ)", "التربوي"),
 (r"\bالملئمة\b", "الملائمة"),
 (r"\bاللمانية\b", "الألمانيّة"),
 (r"\bالتحادية\b", "الاتّحاديّة"),
 (r"\bالوليات\b", "الولايات"),
 (r"الساس", "الأساس"),
 (r"الاهداف|الهداف\b", "الأهداف"),
 (r"\bعل\b", "على"),
 (r"الا", "إلّا"),
]

def clean(t):
    t = re.sub(r"\s+", " ", t or "").strip()
    for pat, rep in TERM + REPAIR:
        t = re.sub(pat, rep, t)
    t = t.replace("؛", "؛").replace(" ،", "،").replace("( ", "(").replace(" )", ")")
    return t.strip()

def cells(text):
    parts = [p.strip(" -•\u06d4") for p in re.split(r"[•]", text)]
    parts = [clean(p) for p in parts if clean(p)]
    return parts

HDRS = {"no": r"^\s*لا\.?\s*$", "sk": r"المهارات", "ac": r"الأنشطة", "kn": r"المعرفة"}
MARK = re.compile(r"^(\d+\.\d+)\s*$")

for pg in range(A, B + 1):
    P = BLK.get(pg)
    if not P:
        continue
    W, H = P["w"], P["h"]
    blks = [b for b in P["blocks"] if b["text"].strip()]
    blks = [b for b in blks if b["y0"] < H - 55 and b["y0"] > 45]
    for b in blks:
        b["text"] = b["text"].replace("\n", " ")
        b["cx"] = (b["x0"] + b["x1"]) / 2
    head = {}
    for k, pat in HDRS.items():
        hit = [b for b in blks if re.search(pat, b["text"]) and len(b["text"]) < 95]
        if hit:
            head[k] = min(hit, key=lambda b: b["x0"])
    cols = sorted(head, key=lambda k: head[k]["cx"])
    # bornes de colonnes = milieux entre centres des en-têtes
    lim = []
    for i in range(len(cols) - 1):
        lim.append((head[cols[i]]["cx"] + head[cols[i + 1]]["cx"]) / 2.0)
    def col(b):
        if not cols:
            return "ac"
        for i, l in enumerate(lim):
            if b["cx"] < l:
                return cols[i]
        return cols[-1]
    for b in blks:
        b["col"] = col(b)
    ytop = min([b["y1"] for b in head.values()], default=None)
    body = [b for b in blks if ytop is None or (b["y0"] > ytop + 2 and b["col"] != "hdr")]
    pre = [b for b in blks if ytop is not None and b["y1"] < ytop - 2]
    body = [b for b in body if b not in pre]
    # lignes = segments délimités par les repères de la colonne « لا. »
    marks = sorted([b for b in body if b["col"] == "no" and MARK.match(b["text"])], key=lambda b: b["y0"])
    cuts = [m["y0"] for m in marks] or [min([b["y0"] for b in body], default=0)]
    ybot = max([b["y1"] for b in body], default=0) + 1
    bounds = sorted(set([min([b["y0"] for b in body], default=0)] + cuts + [ybot]))
    rows = []
    for i in range(len(bounds) - 1):
        lo, hi = bounds[i], bounds[i + 1]
        r = {}
        for b in body:
            if lo - 3 <= b["y0"] < hi - 3 or (i == len(bounds) - 2 and b["y0"] >= lo - 3):
                r.setdefault(b["col"], []).append(b)
        for k in r:
            r[k].sort(key=lambda b: (round(b["y0"]), b["x0"]))
        rows.append((marks[i]["text"].strip() if i - 0 < len(marks) and i < len(marks) else "", r))
    lines = [f"#PAGE {pg}", "@SEC بطاقة وحدة"]
    for b in sorted(pre, key=lambda b: (round(b["y0"]), -b["cx"])):
        t = clean(b["text"])
        if t:
            lines.append("@P2 " + t)
    lines.append("@TABHDR لا.||المهارات المهنيّة||الأنشطة المهنيّة التي سيتم تغطيتها/أداؤها||المعرفة النظريّة والتقنيّات والتكنولوجيا اللازمة")
    for num, r in rows:
        cs = []
        for k in ("no", "sk", "ac", "kn"):
            txt = " ".join(b["text"] for b in r.get(k, []))
            if k == "no":
                cs.append(num or clean(txt))
            else:
                ps = cells(txt)
                cs.append("¦".join(("• " + p) for p in ps) if ps else "")
        if any(cs):
            lines.append("@ROW " + "||".join(cs))
    lines.append("@TABEND")
    open(OUT, "a", encoding="utf-8").write("\n".join(lines) + "\n")
print("généré", A, "-", B, "->", OUT)
