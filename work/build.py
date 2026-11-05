# -*- coding: utf-8 -*-
"""Construit le .docx arabe RTL à partir du balisage léger (work/ar*/ *.md).

    TAG=batch4 ARDIR=work/ar4 ANNEX=annex_batch4 OUT=out.docx python work/build.py
"""
import json, os, re, sys, glob
try:
    import pymupdf as fitz
except ImportError:
    import fitz
SRC=os.environ.get("SRC","work/source-VC-2019-veston.pdf")
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

TAG=os.environ.get("TAG","batch1")
FIGDIR=f"work/{TAG}_figs"
ARDIR=os.environ.get("ARDIR","work/ar")
ANNEX=os.environ.get("ANNEX","annex_batch1")
OUT=os.environ.get("OUT","out.docx")
blocks=json.load(open(f"work/{TAG}_blocks.json"))
REG={r["id"]:r for p in blocks["pages"] for r in p["regions"]}

_xj=f"work/{TAG}_extra.json"
if os.path.exists(_xj):
    for _e in json.load(open(_xj)): REG.setdefault(_e["id"], _e)

LINEBY={}
for p in blocks["pages"]:
    for l in p["lines"]:
        if l["reg"]: LINEBY.setdefault(l["reg"],[]).append(l)

AR_FONT="Simplified Arabic"; HEAD_FONT="Traditional Arabic"
doc=Document()

# ---------- page setup (A4, marges, RTL) ----------
sec=doc.sections[0]
sec.orientation=WD_ORIENT.PORTRAIT
sec.page_width=Cm(21.0); sec.page_height=Cm(29.7)
sec.top_margin=Cm(2.0); sec.bottom_margin=Cm(1.6)
sec.left_margin=Cm(1.5); sec.right_margin=Cm(1.5)
sec.header_distance=Cm(1.0); sec.footer_distance=Cm(1.0)

def rtl_paragraph(p):
    pPr=p._p.get_or_add_pPr()
    if pPr.find(qn('w:bidi')) is None:
        b=OxmlElement('w:bidi'); b.set(qn('w:val'),'1'); pPr.insert(0,b)

def rtl_section(s):
    sectPr=s._sectPr
    if sectPr.find(qn('w:bidi')) is None:
        b=OxmlElement('w:bidi'); b.set(qn('w:val'),'1')
        ref=sectPr.find(qn('w:docGrid'))
        if ref is not None: ref.addprevious(b)
        else: sectPr.append(b)
rtl_section(sec)

def style_font(st, name, size, bold=False, color=None, cs=True):
    f=st.font; f.name=name; f.size=Pt(size); f.bold=bold
    if color: f.color.rgb=RGBColor.from_string(color)
    rPr=st.element.get_or_add_rPr(); rFonts=rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts=OxmlElement('w:rFonts'); rPr.append(rFonts)
    rFonts.set(qn('w:ascii'),name); rFonts.set(qn('w:hAnsi'),name); rFonts.set(qn('w:cs'),name)
    if cs:
        sz=OxmlElement('w:szCs'); sz.set(qn('w:val'),str(int(size*2))); rPr.append(sz)
        b=OxmlElement('w:bCs'); b.set(qn('w:val'),'1' if bold else '0'); rPr.append(b)

S=doc.styles
style_font(S['Normal'], AR_FONT, 14)
S['Normal'].paragraph_format.space_after=Pt(4); S['Normal'].paragraph_format.line_spacing=1.15
for nm,sz,col in (('Heading 1',20,'C00000'),('Heading 2',17,'C00000'),('Heading 3',15,'7030A0'),('Heading 4',14,'002060')):
    style_font(S[nm], HEAD_FONT, sz, True, col)
    S[nm].paragraph_format.space_before=Pt(8); S[nm].paragraph_format.space_after=Pt(6)
for nm in ('List Bullet','List Number','List Bullet 2','List Number 2'):
    try: style_font(S[nm], AR_FONT, 14)
    except KeyError: pass

# ---------- helpers ----------
def P(text="", style=None, align=None, size=None, bold=None, color=None, italic=None, space_before=None, ind=None, keep=True):
    p=doc.add_paragraph(style=style)
    rtl_paragraph(p)
    if align is not None: p.alignment=align
    if text:
        r=p.add_run(text)
        r.font.name=AR_FONT
        rPr=r._element.get_or_add_rPr(); rf=OxmlElement('w:rFonts')
        rf.set(qn('w:ascii'),AR_FONT); rf.set(qn('w:hAnsi'),AR_FONT); rf.set(qn('w:cs'),AR_FONT); rPr.append(rf)
        if size: r.font.size=Pt(size)
        if bold is not None: r.bold=bold; r.font.bold=bold
        if italic is not None: r.italic=italic
        if color: r.font.color.rgb=RGBColor.from_string(color)
        sz=OxmlElement('w:szCs'); sz.set(qn('w:val'),str(int((size or 14)*2))); rPr.append(sz)
    if ind is not None:
        p.paragraph_format.left_indent=Cm(ind)
    if space_before is not None: p.paragraph_format.space_before=Pt(space_before)
    p.paragraph_format.keep_together=keep
    return p

def add_field(par, instr):
    r=par.add_run()
    fc=OxmlElement('w:fldChar'); fc.set(qn('w:fldCharType'),'begin'); r._r.append(fc)
    r2=par.add_run(); it=OxmlElement('w:instrText'); it.set(qn('xml:space'),'preserve'); it.text=instr; r2._r.append(it)
    r3=par.add_run(); fc2=OxmlElement('w:fldChar'); fc2.set(qn('w:fldCharType'),'separate'); r3._r.append(fc2)
    r4=par.add_run("…")
    r5=par.add_run(); fc3=OxmlElement('w:fldChar'); fc3.set(qn('w:fldCharType'),'end'); r5._r.append(fc3)

def shade(el, fill, borders=None):
    pr = el._p.get_or_add_pPr() if hasattr(el,'_p') else el._tc.get_or_add_tcPr()
    sh=OxmlElement('w:shd'); sh.set(qn('w:val'),'clear'); sh.set(qn('w:color'),'auto'); sh.set(qn('w:fill'),fill); pr.append(sh)
    if borders:
        pbdr=OxmlElement('w:pBdr')
        for side in ('top','left','bottom','right'):
            e=OxmlElement(f'w:{side}'); e.set(qn('w:val'),'single'); e.set(qn('w:sz'),'8'); e.set(qn('w:space'),'2'); e.set(qn('w:color'),borders); pbdr.append(e)
        pr.append(pbdr)

def add_picture(fid, width_cm):
    path=f"{FIGDIR}/{fid}.jpg"
    if not os.path.exists(path): path=f"{FIGDIR}/{fid}.png"
    if not os.path.exists(path):
        P(f"[صورة مفقودة: {fid}]", color="FF0000"); return
    r=REG.get(fid)
    orig_cm = (r["w_pt"] if r else 0)*0.0352778
    w = min(orig_cm if orig_cm else float(width_cm), 18.0)
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; rtl_paragraph(p)
    p.paragraph_format.space_before=Pt(4); p.paragraph_format.space_after=Pt(0)
    p.add_run().add_picture(path, width=Cm(w if w>1 else float(width_cm)))

def add_table(rows, header=None, widths=None, fontsz=12):
    ncol=max(len(r) for r in rows)
    t=doc.add_table(rows=0, cols=ncol)
    t.style='Table Grid'
    t.alignment=WD_TABLE_ALIGNMENT.CENTER
    tblPr=t._tbl.tblPr
    bv=OxmlElement('w:bidiVisual'); bv.set(qn('w:val'),'1'); tblPr.append(bv)
    allrows=([header] if header else [])+rows
    for i,row in enumerate(allrows):
        cells=t.add_row().cells
        for j in range(ncol):
            txt = row[j] if j < len(row) else ""
            cell=cells[j]
            cell.text=""
            par=cell.paragraphs[0]; rtl_paragraph(par)
            par.alignment=WD_ALIGN_PARAGRAPH.RIGHT
            par.paragraph_format.space_after=Pt(2)
            run=par.add_run(txt); run.font.name=AR_FONT; run.font.size=Pt(fontsz)
            rPr=run._element.get_or_add_rPr()
            rf=OxmlElement('w:rFonts'); rf.set(qn('w:ascii'),AR_FONT); rf.set(qn('w:hAnsi'),AR_FONT); rf.set(qn('w:cs'),AR_FONT); rPr.append(rf)
            if i==0 and header:
                run.bold=True; run.font.color.rgb=RGBColor.from_string("C00000")
                tcPr=cell._tc.get_or_add_tcPr(); sh=OxmlElement('w:shd')
                sh.set(qn('w:val'),'clear'); sh.set(qn('w:fill'),'FDE9D9'); tcPr.append(sh)
    return t

# ---------- header / footer ----------
hdr=sec.header.paragraphs[0]; hdr.alignment=WD_ALIGN_PARAGRAPH.CENTER; rtl_paragraph(hdr)
def set_header(text):
    hdr.text=""
    r=hdr.add_run(text or ""); r.font.name=AR_FONT; r.font.size=Pt(11); r.bold=True
    r.font.color.rgb=RGBColor.from_string("7030A0")
set_header("")
ftr=sec.footer.paragraphs[0]; ftr.alignment=WD_ALIGN_PARAGRAPH.CENTER; rtl_paragraph(ftr)
r=ftr.add_run("صفحة "); r.font.name=AR_FONT; r.font.size=Pt(11)
add_field(ftr,"PAGE")
r=ftr.add_run(" من "); r.font.name=AR_FONT; r.font.size=Pt(11)
add_field(ftr,"NUMPAGES")

# ---------- markup parser ----------
HEADTXT={}
NUM_RE=re.compile(r"^@N(\d+)\s*(.*)$")
def parse(files):
    cur_page=None; intab=False; tabrows=[]; tabhdr=None; ncounter={}
    def flush():
        nonlocal tabrows, tabhdr, intab
        if tabrows or tabhdr:
            add_table(tabrows, header=tabhdr, fontsz=12)
        tabrows=[]; tabhdr=None; intab=False
    for fn in files:
        for raw in open(fn,encoding="utf-8").read().split("\n"):
            s=raw.strip()
            if not s: continue
            if s.startswith("@TABEND"): flush(); continue
            if intab and (s.startswith("@TABROW") or s.startswith("@ROW")):
                t = "@TABROW" if s.startswith("@TABROW") else "@ROW"
                tabrows.append([c.strip() for c in s[len(t):].split("||")]); continue
            if s.startswith("#PAGE"):
                pg=int(s.split()[1])
                if cur_page is not None:
                    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
                cur_page=pg; continue
            if s.startswith("@SEC"): set_header(HEADTXT.get("x","")); continue
            if s.startswith("@TABHDR"):
                flush(); tabhdr=[c.strip() for c in s[len("@TABHDR"):].split("||")]; intab=True; continue
            m=re.match(r"^@HEAD\s+(.*)$", s)
            if m: HEADTXT["x"]=m.group(1); set_header(m.group(1)); continue
            if s=="@TOC":
                P("جدول المحتويات (يُحدَّث آلياً في Word: زر F9)", align=WD_ALIGN_PARAGRAPH.CENTER, size=12, italic=True, color="808080")
                p=doc.add_paragraph(); rtl_paragraph(p); add_field(p, r'TOC \o "1-3" \h \z \u')
                continue
            if s.startswith("@FULLPAGE"):
                flush()
                parts=s.split()
                pg=int(parts[1]); box=None
                if len(parts)>=7: box=fitz.Rect(*[float(v) for v in parts[2:6]]); w=float(parts[6])
                else: w=float(parts[2]) if len(parts)>2 else 17.0
                fn=f"{FIGDIR}/full_p{pg:03d}.jpg"
                if not os.path.exists(fn):
                    os.makedirs(FIGDIR,exist_ok=True)
                    dd=fitz.open(SRC); pa=dd[pg-1]
                    clip=(box & pa.rect) if box else pa.rect
                    pix=pa.get_pixmap(matrix=fitz.Matrix(200/72,200/72), clip=clip, alpha=False)
                    png=fn[:-4]+".png"; pix.save(png)
                    from PIL import Image
                    Image.open(png).convert("RGB").save(fn, quality=88, optimize=True); os.remove(png)
                    dd.close()
                pp=doc.add_paragraph(); pp.alignment=WD_ALIGN_PARAGRAPH.CENTER; rtl_paragraph(pp)
                pp.add_run().add_picture(fn, width=Cm(min(w,18.0)))
                continue
            if s.startswith("@IMG") or s.startswith("@CROP"):
                flush()
                parts=s.split()
                add_picture(parts[1], float(parts[2]) if len(parts)>2 else 14.0); continue
            if s.startswith("@DOTS"):
                flush(); P("……………………………………………………………………………………………………………………",
                          align=WD_ALIGN_PARAGRAPH.CENTER, color="A6A6A6"); continue
            if s.startswith("@FORMULA"):
                flush(); P(s[9:], align=WD_ALIGN_PARAGRAPH.CENTER, size=14, bold=True, color="C00000"); continue
            if s.startswith("@CAP"):
                p=P(s[4:], align=WD_ALIGN_PARAGRAPH.CENTER, size=12, bold=True, color="000000")
                shade(p, "FDE9D9", "ED9B33"); continue
            if s.startswith("@NOTE"):
                flush()
                p=P("ملاحظة المترجم: "+s[5:].strip(), align=WD_ALIGN_PARAGRAPH.RIGHT, size=11, italic=True, color="7030A0")
                shade(p, "F2F2F2", "BFBFBF"); continue
            if s.startswith("@LBL"):
                flush(); body=s[4:].strip()
                if "||" in body:
                    k,v=body.split("||",1)
                    p=doc.add_paragraph(); rtl_paragraph(p); p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
                    r1=p.add_run(k.strip()+": "); r1.bold=True; r1.font.name=AR_FONT; r1.font.size=Pt(13)
                    if v.strip():
                        r2=p.add_run(v.strip()); r2.font.name=AR_FONT; r2.font.size=Pt(13)
                else:
                    P(body, size=13, bold=True, color="CC0099")
                continue
            if s.startswith("@TITLE"):
                flush(); P(s[7:], align=WD_ALIGN_PARAGRAPH.CENTER, size=18, bold=True); continue
            if s.startswith("@TITLES"):
                flush(); P(s[8:], align=WD_ALIGN_PARAGRAPH.CENTER, size=15, bold=True); continue
            if s.startswith("@DATE"):
                flush(); P(s[6:], align=WD_ALIGN_PARAGRAPH.CENTER, size=15, bold=True); continue
            for tag,st in (("@H1",'Heading 1'),("@H2",'Heading 2'),("@H3",'Heading 3'),("@H4",'Heading 4')):
                if s.startswith(tag):
                    flush()
                    h=doc.add_paragraph(style=st); rtl_paragraph(h); h.add_run(s[len(tag):].strip())
                    break
            else:
                if s.startswith("@U2"): P(s[3:], style='List Bullet 2', size=13)
                elif s.startswith("@U"): P(s[2:], style='List Bullet', size=14)
                elif NUM_RE.match(s):
                    m=NUM_RE.match(s); lvl=int(m.group(1)); txt=m.group(2)
                    ncounter[lvl]=ncounter.get(lvl,0)+1
                    P(f"{ncounter[lvl]}- {txt}", style='List Number' if lvl==1 else 'List Number 2', size=14)
                elif s.startswith("@P4"): P(s[3:], size=13, bold=True, color="002060", ind=0.8)
                elif s.startswith("@P3"): P(s[3:], size=14, bold=True, color="7030A0")
                elif s.startswith("@P2"): P(s[3:], size=14, bold=True)
                elif s.startswith("@B"): P(s[2:], size=14, bold=True, color="C00000")
                elif s.startswith("@P"): P(s[2:], size=14)
                elif s.startswith("@"):
                    P(f"[وسم غير معروف: {s[:40]}]", color="FF0000", size=11)
                elif s.startswith("@CENTERHEAD"): pass
    flush()

parse(sorted(glob.glob(ARDIR+"/*.md")))

# ---------- annexes ----------
sys.path.insert(0,"work")
AN=__import__(ANNEX)
AN.build(doc, blocks, LINEBY, FIGDIR, REG, P, add_table, add_picture, shade, rtl_paragraph,
         WD_ALIGN_PARAGRAPH, Pt, Cm, RGBColor, WD_BREAK)

os.makedirs("traduction",exist_ok=True)
out="traduction/"+OUT
doc.save(out)
print("saved", out, round(os.path.getsize(out)/1e6,3), "MB")
