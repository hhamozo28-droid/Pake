# -*- coding: utf-8 -*-
"""معاينة PDF للنصّ العربيّ (صفحة PDF لكلّ صفحة أصل).
يقرأ نفس ملفات work/ar*/*.md التي يبني منها build.py / build_all.py ملفّ الوورد،
ويُخرج ملفّ PDF مقابلًا لتنظيمها: العنوان، الفقرات، القوائم، الجداول، والصور في مواضعها.
يستعمل Story من PyMuPDF مع خطّ Amiri (تشكيل الحروف العربية صحيح عبر HarfBuzz).

الاستعمال:  .venv/bin/python work/pdf_preview.py            # كامل 1–243
            .venv/bin/python work/pdf_preview.py 100 140    # نطاق صفحات الأصل
"""
import os, re, glob, html, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
ARDIRS = ["work/ar", "work/ar2", "work/ar3", "work/ar4"]
FIGS = "work/all_figs"
OUTPDF = os.environ.get("OUTPDF", "traduction/معاينة-كامل-1-243.pdf")
P0 = int(sys.argv[1]) if len(sys.argv) > 1 else 1
P1 = int(sys.argv[2]) if len(sys.argv) > 2 else 243

CSS = """
@font-face{font-family:amiri;src:url(work/fonts/Amiri-Regular.ttf);}
@font-face{font-family:amiri;src:url(work/fonts/Amiri-Bold.ttf);font-weight:bold;}
html{font-size:10pt;}
body{font-family:amiri; direction:rtl; text-align:right; line-height:1.55; margin:0;}
h1.pg{font-size:11pt; color:#7a7a7a; text-align:center; margin:0 0 6pt 0; font-weight:normal;}
h1{font-size:17pt; margin:10pt 0 6pt 0; color:#1F3864;}
h2{font-size:14pt; margin:9pt 0 5pt 0; color:#1F3864;}
h3{font-size:12.5pt; margin:8pt 0 4pt 0;}
h4{font-size:11.5pt; margin:7pt 0 3pt 0;}
p{margin:0 0 4pt 0; text-align:justify;}
.c{text-align:center;}
.lbl{font-weight:bold; margin:6pt 0 2pt 0;}
.note{color:#a00000; font-size:9pt; text-align:right;}
.cap{color:#404040; font-size:9pt; text-align:center; margin:1pt 0 6pt 0;}
.f{text-align:center; font-size:11pt; margin:5pt 0;}
ul,ol{margin:2pt 0 5pt 14pt; padding:0;}
li{margin:0 0 2pt 0;}
table{border-collapse:collapse; width:100%; margin:4pt 0 7pt 0; font-size:9pt;}
th,td{border:0.5pt solid #8c8c8c; padding:2.5pt 4pt; text-align:right; vertical-align:top;}
th{background:#dce6f1; font-weight:bold;}
img{display:block; margin:5pt auto;}
.hard{page-break-after:always;}
"""

def esc(t):
    t = html.escape(t or "", quote=False)
    return t.replace("||", "\x00")

PREV = "work/prev_figs"
os.makedirs(PREV, exist_ok=True)

def small(p):
    """Version réduite de la figure pour garder l'aperçu léger (<=760 px de large)."""
    out = f"{PREV}/{os.path.basename(p)}"
    if os.path.exists(out):
        return out
    try:
        from PIL import Image
        im = Image.open(p)
        if im.width > 760:
            im = im.resize((760, int(im.height * 760 / im.width)), Image.LANCZOS)
        im.convert("RGB").save(out, "JPEG", quality=68, optimize=True)
        return out
    except Exception:
        return p

def img_tag(fid, w_cm=None):
    for ext in (".jpg", ".png"):
        p = f"{FIGS}/{fid}{ext}"
        if os.path.exists(p):
            p = small(p)
            st = f" style='width:{min(float(w_cm),16.5):.2f}cm'" if w_cm else ""
            return f"<img src='{p}'{st}>"
    return f"<p class='note'>[صورة غير متوفّرة في المعاينة: {html.escape(str(fid))}]</p>"

def render(md_files):
    """Retourne une liste de fragments HTML, un par page d'origine."""
    pages, cur = [], None
    tbl = None
    for fn in md_files:
        for raw in open(fn, encoding="utf-8").read().split("\n"):
            line = raw.rstrip()
            m = re.match(r"^#PAGE\s+(\d+)", line)
            if m:
                pg = int(m.group(1))
                if cur is not None:
                    pages.append((prev, "\n".join(cur)))
                prev = pg
                cur = [] if P0 <= pg <= P1 else None
                continue
            if cur is None:
                continue
            mm = re.match(r"^@(\w+)\s*(.*)$", line)
            if not mm:
                if line.strip():
                    cur.append("<p>%s</p>" % esc(line).replace("\x00", " "))
                continue
            tag, rest = mm.group(1), mm.group(2).strip()
            cells = [c.strip() for c in rest.split("||")] if rest else []
            if tag in ("SEC", "HEAD"):
                continue
            elif tag == "TOC":
                cur.append("<h2>الفهرس</h2><p class='note'>(يُبنى جدول المحتويات في ملفّ الوورد تلقائيًّا؛ "
                           "هذه المعاينة تُظهر التسلسل حسب صفحات الأصل.)</p>")
            elif tag in ("TITLE",):
                cur.append("<h1 class='c'>%s</h1>" % esc(rest))
            elif tag in ("TITLES", "DATE"):
                cur.append("<p class='c'>%s</p>" % esc(rest))
            elif tag in ("H1", "H2", "H3", "H4"):
                cur.append("<%s>%s</%s>" % ("h"+tag[1], esc(rest), "h"+tag[1]))
            elif tag in ("P",):
                cur.append("<p>%s</p>" % esc(rest).replace("\x00", " "))
            elif tag == "P2":
                cur.append("<p style='font-weight:bold'>%s</p>" % esc(rest))
            elif tag == "P3":
                cur.append("<p style='font-size:9pt'>%s</p>" % esc(rest))
            elif tag == "P4":
                cur.append("<p class='lbl'>%s</p>" % esc(rest))
            elif tag in ("U", "U2"):
                cur.append("<ul><li>%s</li></ul>" % esc(rest).replace("\x00", " "))
            elif tag in ("N1", "N2"):
                cur.append("<ol><li>%s</li></ol>" % esc(rest).replace("\x00", " "))
            elif tag == "TABHDR":
                tbl = "<table><tr>" + "".join("<th>%s</th>" % esc(c) for c in cells) + "</tr>"
            elif tag in ("TABROW", "ROW"):
                row = "<tr>" + "".join("<td>%s</td>" % esc(c).replace("\x00", " ") for c in cells) + "</tr>"
                if tbl is None:
                    tbl = "<table>" + row
                else:
                    tbl += row
            elif tag == "TABEND":
                if tbl:
                    cur.append(tbl + "</table>")
                tbl = None
            elif tag in ("IMG", "CROP"):
                pp = rest.split()
                fid = pp[0] if pp else ""
                w = pp[1].replace("cm", "") if len(pp) > 1 else None
                cur.append(img_tag(fid, w))
            elif tag == "FULLPAGE":
                pp = rest.split()
                pg3 = re.sub(r"\D", "", pp[0]) or str(prev)
                w = pp[1].replace("cm", "") if len(pp) > 1 else None
                w = "15.2"   # page entière de l'original : largeur bornée pour tenir sur la page
                cur.append(img_tag("full_p%03d" % int(pg3), w))
            elif tag == "CAP":
                cur.append("<p class='cap'>%s</p>" % esc(rest))
            elif tag == "NOTE":
                cur.append("<p class='note'>%s</p>" % esc(rest))
            elif tag == "FORMULA":
                cur.append("<p class='f'>%s</p>" % esc(rest))
            elif tag == "LBL":
                cur.append("<p class='lbl'>%s</p>" % esc(rest))
            else:
                cur.append("<p class='note'>[وسم غير معروف: @%s %s]</p>" % (tag, esc(rest)))
    if cur is not None:
        pages.append((prev, "\n".join(cur)))
    return pages

def main():
    import pymupdf
    files = []
    for d in ARDIRS:
        files += sorted(glob.glob(d + "/*.md"))
    pages = render(files)
    os.makedirs(os.path.dirname(OUTPDF), exist_ok=True)
    writer = pymupdf.DocumentWriter(OUTPDF)
    a4 = pymupdf.paper_rect("a4")

    IDENT = getattr(pymupdf, "Identity", None) or pymupdf.Matrix(1, 1)

    def rectfn(pno, filled):
        return a4, a4 + (34, 30, -34, -30), IDENT
    for pg, body in pages:
        hdr = "<h1 class='pg'>صفحة %d من الأصل</h1>" % pg if pg else ""
        st = pymupdf.Story(html="<html><head><style>%s</style></head><body>%s<div>%s</div></body></html>" % (CSS, hdr, body),
                           archive=pymupdf.Archive("."))
        st.write(writer, rectfn)
    writer.close()
    d = pymupdf.open(OUTPDF)
    print("pages PDF:", d.page_count, "->", OUTPDF, round(os.path.getsize(OUTPDF) / 1e6, 3), "MB")
    for i in (0, 1):
        p = d[i]
        pix = p.get_pixmap(dpi=110)
        pix.save(f"work/prev_{i}.png")
    print("samples:", d[0].get_text()[:60].replace("\n", " | "))

main()
