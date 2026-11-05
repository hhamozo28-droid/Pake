# ترجمة دليل «Fabrication prototype veston» — حالة العمل

## الحالة (2026-11-05)
| الدفعة | صفحات الأصل | نصّ عربي | docx مُسلَّم | ملاحق الدفعة |
|---|---|---|---|---|
| 1 | 1–61 | ✅ `work/ar/*.md` | ✅ `traduction/out-batch1.docx` | ⏳ `annex_batch1.py` |
| 2 | 62–108 | ✅ `work/ar2/*.md` | ✅ `traduction/out-batch2.docx` | ⏳ `annex_batch2.py` |
| 3 | 109–188 | ✅ `work/ar3/*.md` | ✅ `traduction/out-batch3.docx` | ⏳ `annex_batch3.py` |
| 4 | 189–243 | ✅ `work/ar4/*.md` | ✅ `traduction/out-batch4.docx` (مع الملاحق) | ✅ `annex_batch4.py` |

روابط التحميل (فرع الجلسة `arena/de0f036b-pake`):
`https://github.com/hhamozo28-droid/Pake/raw/arena/de0f036b-pake/traduction/out-batch1.docx` (وكذلك 2، 3، 4).

## البيئة
```sh
sh work/setup.sh        # .venv + pymupdf + python-docx + pillow
```
كلّ ما هو خارج المستودع يُفقد عند إعادة تهيئة البيئة؛ القصاصات (`work/*_figs/`) مُستثناة من git وتُولَّد عند الاستخراج.

## الأوامر
```sh
# (اختياري) إعادة الاستخراج من PDF
.venv/bin/python work/extract.py 1 61 batch1      # 62 108 batch2 | 109 188 batch3 | 189 243 batch4

# بناء دفعة
TAG=batch1 ARDIR=work/ar  ANNEX=none OUT=out-batch1.docx .venv/bin/python work/build.py
TAG=batch2 ARDIR=work/ar2 ANNEX=none OUT=out-batch2.docx .venv/bin/python work/build.py
TAG=batch3 ARDIR=work/ar3 ANNEX=none OUT=out-batch3.docx .venv/bin/python work/build.py
TAG=batch4 ARDIR=work/ar4 ANNEX=annex_batch4 OUT=out-batch4.docx .venv/bin/python work/build.py
```
`ANNEX=none` للتجربة السريعة (بلا ملاحق)؛ و`OUT` اسم ملف مجرّد يوضع في `traduction/`.

## فحص سريع بعد كلّ بناء
```sh
.venv/bin/python - <<'PY'
from docx import Document; import os
f='traduction/out-batch3.docx'; d=Document(f); x=d.element.body.xml
t="\n".join(p.text for p in d.paragraphs)
print(round(os.path.getsize(f)/1e6,3),'MB | فقرة',len(d.paragraphs),'| جدول',len(d.tables),
      '| صورة',len(d.inline_shapes),'| فاصل',x.count('w:type="page"'),
      '| بالٍ',t.count('وسم غير معروف')+t.count('صورة مفقودة'))
PY
```
الفواصل = عدد الصفحات − 1. الوسم المجهول يظهر فقرةً حمراء في الملفّ.

## الملفات
- `work/extract.py` — استخراج `blocks.json` (صفحات/مناطق/أسطر + `has_image`)، و`*_figs/*.jpg`، و`skel/*_skeleton.txt` (قراءة بشرية).
- `work/build.py` — بنّاء docx من وسوم `@` في `work/ar*/`.
- `work/annex_batch4.py` — واجهة الملحقات (CONFIRM، CONFIRM_NOTE، MANUAL، NOTES، GLOSS_EXTRA)؛ مرجع لأي ملحق دفعة.
- `work/source-VC-2019-veston.pdf` — المصدر (243 ص).

## المتبقّي
1. `annex_batch{1,2,3}.py` (ملاحظات المترجم + نصوص الصور + مسرد لكل دفعة) ثمّ إعادة بناء الدفعات بها.
2. الملفّ الموحَّد 1–243 بثلاثة مقاطع ترقيم (بلا ترقيم 1–12، ثمّ `decimal start=12`، ثمّ `upperRoman start=1`) + معاينة PDF + `تعليمات_التعديل.txt`.
