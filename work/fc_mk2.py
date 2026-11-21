# -*- coding: utf-8 -*-
"""Générateur v2 des « cartes d'unité » : découpe au MOT (pas au bloc), colonnes
délimitées par les libellés d'en-tête, lignes délimitées par les repères « لا. ».
C'est ce qui évite l'entrelacement des colonnes caused by the overlapping text boxes
of the Google-translated layer.

Usage : .venv/bin/python work/fc_mk2.py P0 P1 out.md [--json work/fc_blocks.json]
"""
import json, re, sys, unicodedata
import pymupdf

A, B, OUT = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
doc = pymupdf.open("work/ELE1204-froid-clim-N4.pdf")

TERM = [
 (r"برامج التدريب المهني", "برامج التكوين المهني"),
 (r"برنامج التدريب المهني", "برنامج التكوين المهني"),
 (r"التدريب المهنيّ", "التكوين المهني"),
 (r"التدريب المهني", "التكوين المهني"),
 (r"التدريبية|التدريبى", "التكوينيّة"),
 (r"مؤسسة التدريب|مؤسسات التدريب|مركز التدريب|مراكز التدريب|المؤسسة التكوينيّة", "مؤسّسة التكوين"),
 (r"شركة التدريب|شركات التدريب", "المقاولة المُواكِبة"),
 (r"داخل الشركة|في الشركة|للشركة", "داخل المقاولة المُواكِبة"),
 (r"المتدربين|المتدرب", "المتربّص"),
 (r"المدربين|المدرب", "المُكوِّن"),
 (r"مشرف التدريب|مشرف التكوين المهنيّ", "مشرف التكوين"),
 (r"مدة التدريب", "مدّة التكوين"),
 (r"ساعات التدريب", "ساعات التكوين"),
 (r"خطة التدريب|خطة تدريب", "خُطّة التكوين"),
 (r"التدريب", "التكوين"),
]
REPAIR = [
 (r"\bخلل\b", "خلال"), (r"الساس", "الأساس"), (r"الاهداف|الهداف\b", "الأهداف"),
 (r"\bعل\b", "على"), (r"\bالملئمة\b", "الملائمة"), (r"\bاللمانية\b", "الألمانيّة"),
 (r"\bالتحادية\b", "الاتّحاديّة"), (r"\bالوليات\b", "الولايات"),
 (r"مجإلّات|مجالت", "مجالت"), (r"إلّاستنشاق", "بالاستنشاق"), (r"إلّامتثال", "والامتثال"),
 (r"إلّاحتياطات", "الاحتياطات"), (r"الا", "إلّا"), (r"ً", ""),
]
def clean(t):
    t = re.sub(r"\s+", " ", t or "").strip()
    for pat, rep in TERM + REPAIR:
        t = re.sub(pat, rep, t)
    t = t.replace(" ،", "،").replace(" (", " (").replace("( ", "(").replace(" )", ")")
    return t.strip()

def isar(ch):
    o = ord(ch)
    return 0x0590 <= o <= 0x08FF or 0xFB50 <= o <= 0xFDFF or 0xFE70 <= o <= 0xFEFF

def fixw(w):
    """NFKC + remise en ordre logique des mots purement arabes (le PDF les pose en ordre visuel)."""
    n = unicodedata.normalize("NFKC", w).replace("\u0640", "")
    al = [c for c in n if not c.isspace()]
    if al and all(isar(c) or unicodedata.combining(c) for c in al):
        n = "".join(reversed(n))
        n = "".join({")": "(", "(": ")", "[": "]", "]": "["}.get(c, c) for c in n)
    return n

KKEY = {"no": r"^لا\.?$", "sk": r"المهارات", "ac": r"الأنشطة", "kn": r"المعرفة"}

def rtl_join(words):
    """words = [(x0,x1,w)] triés par y ; renvoie la ligne en ordre logique."""
    words = sorted(words, key=lambda t: -t[0])
    return " ".join(w for _, _, w in words)

for pg in range(A, B + 1):
    p = doc[pg - 1]
    H = p.rect.height; W = p.rect.width
    ws = []
    for x0, y0, x1, y1, w, bi, li, wi in p.get_text("words"):
        if w.strip().lower() in ("machine", "translated", "by", "google"):
            continue
        if y0 < 45 or y1 > H - 52:
            continue
        w = fixw(w)
        if not w.strip():
            continue
        ws.append({"x0": x0, "x1": x1, "cx": (x0 + x1) / 2, "y0": y0, "y1": y1, "w": w})
    # — ligne d'en-tête : la bande y la plus haute qui contient >= 2 mots-clés
    hits = {}
    for k, pat in KKEY.items():
        hits[k] = [w for w in ws if re.search(pat, w["w"]) and len(w["w"]) < 14]
    band = None
    for w in sorted([x for v in hits.values() for x in v], key=lambda t: t["y0"]):
        band = w["y0"]; break
    head = {}
    if band is not None:
        for k, lst in hits.items():
            cand = [w for w in lst if abs(w["y0"] - band) < 14]
            if cand:
                head[k] = {"x0": min(w["x0"] for w in cand), "x1": max(w["x1"] for w in cand),
                           "y": min(w["y0"] for w in cand)}
    cols = sorted(head, key=lambda k: (head[k]["x0"] + head[k]["x1"]) / 2)
    bnd = []
    for i in range(len(cols) - 1):
        bnd.append((head[cols[i]]["x1"] + head[cols[i + 1]]["x0"]) / 2.0)
    def col(w):
        if not cols:
            return "body"
        for i, b in enumerate(bnd):
            if w["cx"] < b:
                return cols[i]
        return cols[-1]
    for w in ws:
        w["col"] = col(w)
    below = [w for w in ws if band is None or w["y0"] > band + 26]
    above = [w for w in ws if band is not None and w["y1"] < band - 4]
    lines = [f"#PAGE {pg}", "@SEC بطاقة وحدة"]
    # — bloc du haut : titre de l'unité + durée
    if above:
        groups, cur, cy = [], [], None
        for w in sorted(above, key=lambda t: (round(t["y0"]), -t["x0"])):
            if cy is not None and abs(w["y0"] - cy) > 6:
                groups.append(cur); cur = []
            cy = w["y0"]; cur.append(w)
        if cur:
            groups.append(cur)
        for g in groups:
            t = clean(rtl_join([(x["x0"], x["x1"], x["w"]) for x in g]))
            if t:
                lines.append("@P2 " + t)
    # — lignes du tableau = repères « n.n » de la colonne no
    marks = sorted([w for w in below if w["col"] == "no" and re.match(r"^\d+\.\d+\.?$", w["w"])],
                   key=lambda w: w["y0"])
    ytop = min([w["y0"] for w in below], default=0)
    ybot = max([w["y1"] for w in below], default=0) + 0.5
    starts = [m["y0"] - 0.6 for m in marks] or [ytop]
    bounds = sorted(set([ytop] + starts + [ybot]))
    lines.append("@TABHDR لا.||المهارات المهنيّة||الأنشطة المهنيّة التي سيتم تغطيتها/أداؤها||المعرفة النظريّة والتقنيّات والتكنولوجيا اللازمة")
    def cell_lines(words):
        gs, cur, cy = [], [], None
        for w in sorted(words, key=lambda t: (round(t["y0"], 0), -t["x0"])):
            if cy is not None and abs(w["y0"] - cy) > 5:
                gs.append(cur); cur = []
            cy = w["y0"]; cur.append(w)
        if cur:
            gs.append(cur)
        return [rtl_join([(x["x0"], x["x1"], x["w"]) for x in g]) for g in gs]
    for i in range(len(bounds) - 1):
        lo, hi = bounds[i], bounds[i + 1]
        sel = [w for w in below if lo <= w["y0"] < hi]
        if not sel:
            continue
        num = marks[i]["w"].rstrip(".") if i < len(marks) and abs(marks[i]["y0"] - lo) < 2 else ""
        cs = []
        for k in ("no", "sk", "ac", "kn"):
            if k == "no":
                cs.append(num)
            else:
                ls = [clean(x) for x in cell_lines([w for w in sel if w["col"] == k])]
                ls = [x for x in ls if x and not re.match(r"^[\d.]+$", x)]
                # découpe sur les puces
                items = []
                buf = []
                for x in ls:
                    for piece in re.split(r"(?=\b•\b|•)", x):
                        piece = piece.strip(" •")
                        if not piece:
                            continue
                        buf.append(piece)
                    items.extend(buf); buf = []
                items = [re.sub(r"^\s*•\s*", "", it) for it in items if re.sub(r"^\s*•\s*", "", it)]
                cs.append("¦".join("• " + it for it in items) if items else ("¦".join("• " + x for x in ls) if ls else ""))
        if any(cs):
            lines.append("@ROW " + "||".join(cs))
    lines.append("@TABEND")
    open(OUT, "a", encoding="utf-8").write("\n".join(lines) + "\n")
print("ok", A, B)
