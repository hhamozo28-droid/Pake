# إعادة إنتاج ترجمة الدليل (AR)

الملفات:
- `source-VC-2019-veston.pdf` — ملف المصدر (243 صفحة) — مرجع وحيد، لا يُعدَّل.
- `extract.py` — الاستخراج: `python work/extract.py P0 P1 batchN`
  ينتج `work/batchN_blocks.json` (نص + مناطق)، `work/batchN_extra.json` (صور صغيرة/منسيّة)،
  `work/batchN_figs/*.jpg` (قصاصات بالحجم الأصلي — مُتجاهَلة في git، تُعاد توليدَها)،
  `work/skel/batchN_skeleton.txt` (سكلتون للقراءة).
- `ar/ ar2/ ar3/ ar4/` — نصّ الترجمة العربيّة بوسوم بسيطة (انظر الترويسة في `build.py`).
- `build.py` — بناء ملف دفعة واحدة، و`build_all.py` — الملف الكامل.
- `companion2.py` — ملف الملاحق المستقلّ لكل دفعة.
- `annex_batchN.py` / `annex_all.py` — نصوص الصور + ملاحظات المترجم + المسرد.
- `pdf_preview.py` — معاينة PDF.

الأمر الكامل لكل دفعة (من جذر المستودع):

```
python work/extract.py    1 61   batch1
python work/extract.py   62 108  batch2
python work/extract.py  109 188  batch3
python work/extract.py  189 243  batch4
TAG=batch4 ARDIR=work/ar4 ANNEX=annex_batch4 OUT=out4.docx python work/build.py
CTITLE="ملحق نصوص الصور والملاحظات — الدفعة 4" COMP=out4-annex.docx ANNEX=annex_batch4 python work/companion2.py
```

المدفوعات: 1 = ص1–61 · 2 = ص62–108 · 3 = ص109–188 · 4 = ص189–243.
المسرد مُثبَّت (4 نوفمبر 2026) ولا يتغيّر المصطلح في أي موضع.
