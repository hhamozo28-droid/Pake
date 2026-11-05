# -*- coding: utf-8 -*-
"""Annexes fusionnées des quatre lots : une seule liste (a) pour les textes des images,
une seule liste (b) de notes du traducteur, et un glossaire consolidé (c)."""
import importlib, os

LOTS = [("annex_batch1", "الدفعة الأولى (ص1–61)"),
        ("annex_batch2", "الدفعة الثانية (ص62–108)"),
        ("annex_batch3", "الدفعة الثالثة (ص109–188)"),
        ("annex_batch4", "الدفعة الرابعة (ص189–243)")]


def build(doc, blocks, LINEBY, FIGDIR, REG, P, add_table, add_picture, shade, rtl_paragraph,
          WD_ALIGN, Pt_, Cm_, RGB_, WD_BRK):
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
    from docx.shared import Pt, Cm, RGBColor
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

    def head(text, style='Heading 1'):
        h = doc.add_paragraph(style=style); rtl_paragraph(h); h.add_run(text)
        doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    mods = [importlib.import_module(m) for m, _ in LOTS]
    ranges = {"annex_batch1": (1, 61), "annex_batch2": (62, 108),
              "annex_batch3": (109, 188), "annex_batch4": (189, 243)}

    # ---------- الملحق (أ) : نصوص الصور ----------
    rows = []
    handled = set()
    for mod, (tag_label) in zip(mods, [lab for _, lab in LOTS]):
        name = [m for m, l in LOTS if mod.__name__.endswith(m.split("_")[-1])]
        for pg, sup, fr, ar in getattr(mod, "MANUAL", []):
            rows.append([str(pg), tag_label, sup, fr, ar])
        lo, hi = ranges[["annex_batch1", "annex_batch2", "annex_batch3", "annex_batch4"][mods.index(mod)]]
        ids = set()
        for pg, sup, fr, ar in getattr(mod, "MANUAL", []):
            for tok in str(sup).replace("(", " ").replace(")", " ").replace("/", " ").replace(",", " ").split():
                if "_r" in tok or "_d" in tok:
                    ids.add(tok)
        handled |= ids
        for p in blocks["pages"]:
            if not (lo <= p["page"] <= hi):
                continue
            for r in p["regions"]:
                if r["id"] in ids or r["id"] in handled:
                    continue
                if not r.get("has_image", True):
                    continue
                if r["w_pt"] * r["h_pt"] > 0.70 * 595 * 841:
                    continue
                lines = [l["text"].strip() for l in p["lines"] if l["reg"] == r["id"] and l["text"].strip()]
                if not lines:
                    continue
                fr = " — ".join(lines)
                if len(fr) < 8:
                    continue
                rows.append([str(p["page"]), tag_label, f"{r['id']} ({r['kind']})", fr,
                             "تُرجمت في صلب الدليل (التسمية تحت الصورة / الجدول العربيّ المقابل)"])
                handled.add(r["id"])
    for t, (lo, hi) in zip(("batch1", "batch2", "batch3", "batch4"),
                           ((1, 61), (62, 108), (109, 188), (189, 243))):
        ex = f"work/{t}_extra.json"
        if not os.path.exists(ex):
            continue
        import json
        for e in json.load(open(ex)):
            if e["id"] in handled:
                continue
            rows.append([str(e["page"]), "قصاصات مُستعادة", f"{e['id']} (صورة مستعادة)",
                         "لا نصّ: أيقونة/عنصر زخرفة صغير ملحق بإطار الصفحة",
                         "فُحصت على ورقة تلامس فتبيّن أنّها بلا محتوى؛ لم تُدرَج في المتن"])
            handled.add(e["id"])
    rows.sort(key=lambda r: (int(r[0]), str(r[2])))
    head("الملحق (أ) — النصوص الواردة داخل الصور ولوحات الأصل (كلّ الدليل: ص1–243)")
    P("تجمع هذه القائمة — على مدى صفحات الأصل كلّها — كلّ نصّ داخل صورة أو لوحة مصوَّرة: بطاقات الأقمشة ويافطاتها، "
      "ولوحات الشركة المصنِّعة للاصق الحراريّ، وشروط اللّصق، وبطاقات جداول القطع برسوم «Schématisation»، وبطاقاتا "
      "السلسلة العملياتيّة وخطّ التجميع برموز الآلات والغرز، ولوحا المجموعة الموسميّة، وصور خطوات الكَيّ، وصفحات جرد "
      "القطع ومقاطع الإخراج ولوحات التفاصيل، وشبكة التقويم، وفهرس اللوازم، ولوحات الألوان، وشريطا عنوّني «ANNEXE A» و"
      "«ANNEXE B». والعمود الثاني يبيّن الدفعة التي نُقل منها النصّ. وما كان من تسمية شكل مدرجة في طبقة النصّ فقد تُرجم "
      "تحت الصورة نفسها في المتن؛ والرسوم التي لا تحتمل الفصل عن أصلها (جداول مرسومة باليد، نشرة شركة، لوحات) نُقلت "
      "صورةً كاملة مع ذكر ذلك بدل تخمين قيمها.", size=12)
    add_table(rows, header="صفحة الأصل||الدفعة||الصورة / اللوحة||النصّ كما ورد في الأصل||الترجمة العربية والموضع", fontsz=9)

    # ---------- الملحق (ب) : ملاحظات المترجم ----------
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    head("الملحق (ب) — ملاحظات المترجم والتصحيحات والبنود التي تحتاج تأكيدًا (كلّ الدليل)")
    n = 0
    for mod, label in zip(mods, [lab for _, lab in LOTS]):
        P(label, size=14, bold=True, color="C00000")
        for note in getattr(mod, "NOTES", []):
            n += 1
            P(f"{n}- {note}", size=13)

    # ---------- الملحق (ج) : المسرد الموحَّد ----------
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    head("الملحق (ج) — مسرد المصطلحات الموحَّد (كلّ الدليل)")
    P("مسرد واحد مجمع من مَسارد الدفعات الأربع؛ حُذِّف المكرَّر بحيث يبقى لكلّ لفظ فرنسيّ مقابلٌ عربيّ واحد، طبقًا "
      "لتثبيت المصطلحات بتاريخ 4 نوفمبر 2026. وهذا العمود مرجعُ المصحِّح: أيّ تغيير فيها يسري على الدفعات كلّها.", size=12)
    P(mods[0].CONFIRM, size=11, color="C00000")
    seen = {}
    for mod in mods:
        for fr, ar in getattr(mod, "GLOSS_EXTRA", []):
            k = fr.strip().lower()
            if k not in seen:
                seen[k] = (fr, ar)
    for fr, ar in [("veston / paletot", "ستر الرجل"), ("matelassage", "الفِرش"), ("découpage", "التقطيع"),
                   ("thermocollage", "اللّصق الحراري"), ("gamme de montage", "خطّ التجميع"),
                   ("gamme opératoire", "السلسلة العملياتية"), ("triplure", "الحشوة الوسطى"),
                   ("doublure", "البطانة"), ("entoilage / garniture", "الحشو"),
                   ("parementure", "الحاشية الداخلية"), ("passepoil", "الحاشية الضيّقة"),
                   ("banane", "الشريط المنحني"), ("feutre / feutrine", "اللِّبّاد"), ("surfil", "التغبير"),
                   ("boutonnière", "شقّ الزرّ"), ("pressing", "الكبس"), ("laize", "عَرض القماش (بالمتر)"),
                   ("tolérance", "تحمُّل"), ("stagiaire", "متربص"), ("stage", "تربص"),
                   ("maître de stage / tuteur", "مرشد التربص"), ("convention de stage", "اتفاقية التربص"),
                   ("encadrement", "التأطير"), ("rapport de stage", "تقرير التربص"),
                   ("évaluation", "تقييم"), ("ressources humaines", "الموارد البشريّة")]:
        if fr.strip().lower() not in seen:
            seen[fr.strip().lower()] = (fr, ar)
    add_table([list(v) for v in seen.values()], header="الفرنسية||العربية", fontsz=11)

    # ---------- الملحق (د) : ترقيم الأصل كما هو ----------
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    head("الملحق (د) — ترقيم صفحات الأصل ودلالتُه في هذا الملفّ")
    for line in [
        "صفحات PDF 1–12 (الغلاف، صفحة المُعِدّ، الفهرس، التقديم، بطاقة المهنة، بطاقة المقياس، جدول الأهداف): بلا رقم "
        "مطبوع في الأصل؛ وهذا المقطع من الملفّ لا يحمل ترقيمًا في التذييل.",
        "صفحات PDF 13–186: الترقيم المطبوع = رقم PDF − 1 (فص13 من الملفّ مرقَّم 12 … وص186 مرقَّمة 185)؛ وقد فُتح مقطع "
        "ترقيم عاديّ يبدأ من 12 ليُطابق الأصل صفحةً بصفحة.",
        "صفحات PDF 187–243: ترقيم رومانيّ من I (ص187 = I، ص196 = X، ص207 = XIX، ص218 = XXIX، ص243 = LIV)؛ وقد فُتح "
        "مقطع رومانيّ يبدأ من I. والملاحق المترجَمة (هذا الملحق) تابعةٌ للمقطع الرومانيّ نفسه كما في الأصل.",
        "الأصل يُسقط أربعة أرقام ترقيم: ص155 و156 تحملان الرقم المطبوع نفسه في موضعَي التكرار، وص100 تحمل رقمَين "
        "(«86» و«99»)، وص197–198 تكرّر الرقم IX ثمّ X، وص210 و213 (وكذلك 211 و214، و215 و220) صفحاتٌ متطابقة المحتوى؛ "
        "أُبقيَت كلّها كما هي لئلّا يختلّ التقابل مع الأصل.",
        "النتيجة: إذا طُبِع هذا الملفّ فستكون أرقام التذييل مطابقةً لأرقام الأصل في المقطعَين الثاني والثالث، ومطابقةً "
        "لعدد صفحات الأصل في المقطع الأوّل (بلا أرقام).",
    ]:
        P("• " + line, size=13)
