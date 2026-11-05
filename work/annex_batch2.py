# -*- coding: utf-8 -*-
"""Annexes du lot 2 (pages PDF 62–108 : Chapitre II — DÉROULEMENT DES ÉTAPES DE FABRICATION,
thermocollage, assemblage provisoire, essayages, défauts et corrections du prototype)."""
import os, json

CONFIRM = ("اعتُمدت المصطلحات الآتية نهائيًّا في كامل الدليل (بطلب من صاحب الملف وتثبيتِه بتاريخ 4 نوفمبر 2026) "
           "ولا تُغيَّر في أيّ موضع من الدفعات الأربع: veston/paletot = ستر الرجل · matelassage = الفِرش · "
           "découpage = التقطيع · thermocollage = اللّصق الحراري · gamme de montage = خطّ التجميع · "
           "gamme opératoire = السلسلة العملياتية · triplure = الحشوة الوسطى · doublure = البطانة · "
           "entoilage/garniture = الحشو · parementure = الحاشية الداخلية · passepoil = الحاشية الضيّقة · "
           "banane = الشريط المنحني · feutre/feutrine = اللِّبّاد · surfil = التغبير · "
           "boutonnière = شقّ الزرّ · pressing = الكبس · laize = عَرض القماش (بالمتر) · tolérance = تحمُّل · "
           "stagiaire = متربص · stage = تربص · maître de stage / tuteur = مرشد التربص · convention de stage = اتفاقية التربص · "
           "encadrement = التأطير · rapport de stage = تقرير التربص · évaluation = تقييم · ressources humaines = الموارد البشرية.")

CONFIRM_NOTE = ("تثبيت المصطلحات: بموافقة صاحب الملف بتاريخ 4 نوفمبر 2026 اعتُمدت مصطلحات veston (ستر الرجل)، "
                "thermocollage (اللّصق الحراري)، gamme de montage (خطّ التجميع)، gamme opératoire (السلسلة العملياتية)، "
                "triplure (الحشوة الوسطى)، doublure (البطانة)، parementure (الحاشية الداخلية)، passepoil (الحاشية الضيّقة)، "
                "surfil (التغبير)، boutonnière (شقّ الزرّ)، pressing (الكبس) نهائيةً في كامل الدليل، وطُبِّق ذلك في هذا النطاق "
                "(ص62–108) رغم أنّ الأصل يستعمل مرادفات متبدّلة في الصفحة نفسها (مثل «entoilage» و«garniture» و«triplure» "
                "للحشو، و«cigarette» و«cigare» لشريط أعلى الكمّ، و«passe poile» و«passepoil»). "
                "أمّا ما هو خطأ في الأصل لا اختيار مصطلح — مثل «indication» بدل «enduction» في ص70، و«Kupffer» مقابل «Kuffner» "
                "في ص70–72، و«manqué» بدل «marqué» في ص77، و«MeSH/qualité» بدل «mailles/densité» في ص72، وقفزة ترقيم الجداول "
                "من II.01 إلى II.05 — فقد أُبقي كما ورد مع ملاحظة المترجم تحت الموضع، وهي تنتظر قرار المؤسّسة؛ وكُلّها مفصَّلة "
                "في ملفّ «تعليمات_التعديل.txt» المرفق مع التسليم.")

# (page_source, zone, texte_original, traduction / situation dans le corps)
MANUAL = [
(63,"p63_r1 / p63_r2","Plan de thermocollage du devant (dessin avec renvois, sans légende imprimée)",
 "مخطّط اللّصق الحراريّ للمقدّمة بأرقام إحالية داخل الرسم؛ الشرح في المتن (II.1) والتسمية تحت الصورة"),
(64,"p64_r1 … p64_r3","Trois photos : fer à repasser, presse à chaud, table à repasser",
 "ثلاث صور: مكواة، مكبس حراريّ، طاولة كَيّ؛ بلا نصّ داخل الصور"),
(65,"p65_r1 / p65_r2","Échantillons de triplure et de toile collante (grossissement d'armure)",
 "عيّنتا الحشوة الوسطى والقماش اللاصق مع تكبير بنية النسج؛ لا نصّ داخل الصور، والخصائص في جدول المتن"),
(66,"p66_r1","Tableau II.01 (image de tableau) — Température | Temps | Pression | Vapeur",
 "الجدول II.01 (شروط اللّصق الحراريّ) صورةُ جدول في الأصل؛ أعيد بناؤه في المتن بالقيم نفسها، وعمود «Vapeur» فارغ في الأصل"),
(68,"p68_r1 / p68_r2","Photos de défauts de thermocollage (bulles, décollement, brillance) — sans légende",
 "صور عيوب اللّصق الحراريّ (فقاعات، انفصال، لمعان) بلا تسمية مطبوعة؛ التسميات من صياغة المترجم موضَّحة أنها ليست من الأصل"),
(69,"p69_r1","Carte d'entretien KUPFFER (extrait de notice technique)",
 "بطاقة العناية لشركة KUPFFER (مقتطف من نشرة تقنيّة)؛ النصّ داخل الصورة، وقد نُقل حرفيًّا في هذا الملحق وترجم تحتها. "
 "اسم الشركة يُكتب تارةً «Kupffer» وتارةً «Kuffner» في الدليل (انظر ص70–72)"),
(70,"p70_r1 (لوحة شروط)","INDICATION de l'enduction — Température 130°/150° — Temps 12 à 15 s — Pression 3 à 5 bars",
 "لوحة شروط اللّصق؛ العنوان في الأصل «INDICATION» والصواب «INDICATION DE L'ENDUCTION» أو «CONSEILS D'ENDUCTION»؛ "
 "نُقلت القيم كما هي في جدول المتن (ص70) مع ملاحظة الخطأ"),
(71,"p71_r1","Brochure Kuffner France — tableau des températures par article ( toile, triplure, doublure )",
 "جدول درجات الحرارة بحسب الصنف من نشرة Kuffner France؛ النصّ داخل الصورة (صغر الحروف) فاستُخرج ما أمكن قراءته "
 "وذُكر الباقي «غير مقروء في الأصل» بدل تخمينه"),
(72,"p72_r1","Mailles et densité d'étoffage (schéma d'échantillon avec mesures)",
 "رسم عيّنة يبيّن عدد العروق والكثافة؛ العنوان في الأصل «MeSH … qualité» (أحرف إنجليزيّة متسلّلة) والصواب «mailles» و«densité»؛ "
 "جاء التصحيح تحت الصورة في المتن"),
(73,"p73_r1 … p73_r4","Quatre catégories de support de triplure (face, dos, emmanchure, bas) — photos légendées dans l'image",
 "أربع فئات من سَنَد الحشوة الوسطى؛ التسميات داخل الصور وقد نُقلت في المتن (فئات السُّند) مع ترجمة كلّ تسمية"),
(74,"p74_r1 / p74_r2","Deux exercices écrits (pages d'élèves) — sans texte d'image",
 "صفحتا تمرين بلا نصّ داخل الصورة؛ نصّ التمرين في طبقة النصّ وقد ترجم في المتن (II.1.2.4) مع «Répondrez» الخاطئ المذكور"),
(76,"p76_r1 (جدول مصوَّر)","Tableau II.05 — Ordre | Désignation des pièces | Mode d'assemblage | Observation",
 "الجدول II.05 (خطّ التجميع المؤقّت) صورةُ جدول؛ أعيد بناؤه عربيًّا في المتن بالصفوف والأرقام نفسها. "
 "والأصل يقفز عن الجداول II.02 وII.03 وII.04 (لا وجود لها في هذا النطاق)"),
(77,"p77_r1 / p77_r2","Trois méthodes d'assemblage (à plat, en chaîne, par élément) — schémas annotés",
 "ثلاث طرق للتجميع، مع تعليقات داخل الرسوم («manqué» بدل «marqué» في إحدى اللوحات)؛ نُقلت التعليقات في المتن مع التنبيه"),
(78,"p78_r1 … p78_r4","Photos de montage provisoire (piquage, surfil, bâti) — sans légende imprimée",
 "صور التركيب المؤقّت (خياطة، تغبير، تذييب) بلا تسمية مطبوعة؛ الترتيب في المتن بحسب ترتيب الصور في الصفحة"),
(80,"p80_r1 / p80_r3","Placement du patron sur le tissu — Figure II.23 ; tracé avec droit-fil et crans — Figure II.24",
 "توزيع الباترون على القماش، ثمّ رسم الباترون مع خيط السَّدَى والشقوق؛ الرسوم تحمل أرقام إحالية داخلها فقط"),
(81,"p81_r1 / p81_r3 / p81_r4","Points bouclettes, thermocollage des pièces, assemblage — Figures II.25 à II.27",
 "الغرزة الحلقيّة، واللّصق الحراريّ للقطع، وتجميع السترة؛ صور متتالية بلا نصّ داخلي غير الأرقام"),
(82,"p82_r1 / p82_r3 / p82_r5","Point chevron du revers, premier aspect, emplacement du col — Figures II.28 à II.30",
 "غرزة السَّهم في ردّادة الياقة، والمظهر الأوّل، وموضع الياقة؛ التعليقات في طبقة النصّ ومترجَمة تحت الأشكال"),
(83,"p83_r1 / p83_r2 / p83_r4","Rembourrage d'épaulette, cigarette cousue, montage de la manche — Figures II.31 à II.33",
 "حشو ساد الكتف، وخياطة «السيجارة» في رأس الكمّ، وتركيب الكمّ على تمثال الخياطة؛ لا نصّ داخل الصور"),
(84,"p84_r1 / p84_r3 / p84_r5","Feutrine du col (points zig-zag), montage du col, aspect final — Figures II.34 à II.36",
 "لِبّاد الياقة بغرزة متعرّجة، وتركيب الياقة، والمظهر النهائيّ؛ العنوان الفرنسيّ «Concorde né feutrine du col» مبتور كما في الأصل"),
(85,"p85_r1 (جدول مصوَّر)","Tableau II.6 : divers défauts du veston (photos légendées dans l'image)",
 "الجدول II.6 (عيوب مختلفة في السترة) لوحة مصوَّرة بأربع صور وتعليقات داخلها؛ التعليقات نُقلت في هذا الملحق "
 "(انظر أسفله) لأنّ الأصل لا يضعها في طبقة النصّ"),
(85,"p85_r1 (نصّ داخل الصورة)","Épaulette trop serrée | Épaulette très grande | Devant large | Profondeur d'emmanchure",
 "ساد مشدود جدًّا | ساد كبير جدًّا | مقدّمة واسعة | عمق فتحة الكمّ — وهي عناوين ص86 في المتن، فذُكرت هنا للربط"),
(86,"p86_r1 / p86_r3 / p86_r5","Défauts d'épaulette, de devant, de manche — Figures II.38 à II.40",
 "علل ساد الكتف والمقدّمة والكمّ؛ لا نصّ داخل الصور؛ والشكل II.37 مفقود في الأصل (قفزة ترقيم)"),
(87,"p87_r1 / p87_r3","Longueur de manche par rapport à la taille, défauts de fermeture boutonnage — Figures II.41, II.42",
 "طول الكمّ بالنسبة إلى القَدّ، وعيوب إغلاق الأزرار؛ صور بلا نصّ"),
(88,"p88_r1","Largeur de revers et largeur de cravate (photo de face avec cravate) — Figure II.43",
 "عرض الردّادة وعرض ربطة العنق (صورة أماميّة)؛ لا نصّ داخل الصورة"),
(89,"p89_r1 … p89_r3","N°01 / N°02 / N°03 et V01 … V05 : vestons comparés (légendes dans l'image)",
 "صور المقارنة مع تسمياتها داخل الصورة (N:01، N:02، N:03 وV01 إلى V05)؛ الأسئلة في طبقة النصّ ومترجَمة في المتن"),
(90,"p90_r1","Dos de la veste avec fente — Figure II.44 (cotes inscrites dans le dessin)",
 "ظهر السترة مع الشقّ؛ الأرقام (25 سم، 4 سم) مكتوبة داخل الرسم وقد نُقلت في المتن"),
(91,"p91_r1 / p91_r3","Devant : boutonnières, poche poitrine, rabat ; petit côté avec valeurs de couture",
 "مقدّمة السترة بشقوق الأزرار وجيب الصدر والغطاء، والحاشية الجانبية الصغيرة بقيم الخياطة؛ التعليقات داخل الرسوم"),
(92,"p92_r1 / p92_r3","Manche tailleur (ouverture de 10 cm × 3 cm) et parementure du devant — Figures II.47, II.48",
 "الكمّ بفتحة 10 سم × 3 سم، والحاشية الداخلية للمقدّمة؛ الأرقام داخل الرسم، والنصّ في طبقة النصّ"),
(93,"p93_r1 (لوح كبير)","II.3.1.6.1 : La doublFureIG48de: dlaoumbluanchere dos, devant, petit coté",
 "سطر العنوان في ص93 مطبوع فوق بعضه في الأصل (عنوان فرعيّ وتسمية شكل تداخلا حرفًا بحرف)؛ القراءة الأرجح: "
 "«II.3.1.6.1 : La doublure du dos, devant, petit côté» و«Figure II.48: doublure des dos, devant, petit côté»؛ "
 "ذُكر النصّ كما ورد في المتن مع هذا الشرح"),
(95,"p95_r1 / p96_r1 / p97_r1","Éléments thermocollants (dos, devant, petit côté), thermocollé de la manche, renforts d'emmanchure et d'épaule",
 "ثلاث صفحات مصوَّرة بالكامل بلا شرح نصّيّ في الأصل؛ التعليمات داخل الصور (أرقام إحالية وأسماء قطع)؛ "
 "نُقلت الصور كاملة وتُرجمت تسمياتها في هذا الملحق"),
(95,"p95_r1 (نصّ داخل الصور)","Devant | Dos | Petit côté | Entoilage poitrine | Toile de corps | Toile de revers | Thermocollant",
 "المقدّمة | الظهر | الحاشية الجانبية الصغيرة | حشو الصدر | حريرة الجسم | حريرة الردّادة | اللاصق الحراريّ"),
(97,"p97_r1 (نصّ داخل الصور)","Emmanchure | Épaule | Renfort | Band d'épaule",
 "فتحة الكمّ | الكتف | التدعيم | شريط الكتف"),
(106,"p106_r1 (صورة التمرين)","Manche et col de prototype à corriger — aucune légende imprimée",
 "صورة واحدة كبيرة لتمرين ص106 (الكمّ والياقة قبل التصحيح)؛ لا نصّ داخل الصورة، والسؤالان في طبقة النصّ"),
(107,"p107_r1 (إطار)","Résumé dans un encadré grisé (texte en plusieurs blocs)",
 "ملخّص الفصل داخل إطار مُظلَّل؛ الأسطر مقطّعة في كتل، وقد أُعيد تركيبها في المتن كما تُقرأ"),
]

NOTES = [
"نطاق الدفعة الثانية: صفحات PDF 62–108، أي الفصل الثاني «مجرى خطوات التصنيع» (DÉROULEMENT DES ETAPES DE FABRICATION) كلُّه: اللّصق الحراريّ ومواده وشروطه (ص62–73)، وخطّ التجميع المؤقّت (ص74–84)، والتحقّق من المظهر والعيوب والتصحيحات (ص85–105)، والتمارين والملخّص (ص106–108).",
"الأرقام في هذا النطاق: رقم PDF = رقم صفحة الأصل + 1 (ص62 = 61 … ص108 = 107)؛ وقد ذُكر رقما الصفحة معًا عند كلّ صورة وجدول.",
"ترقيم الجداول مضطرب في الأصل: يبدأ بـ«Tableau II.01» (ص66) ثمّ يقفز إلى «Tableau II.05» (ص76)، وتليه «Tableau II.6» (ص85) بحذف الصفر. أبقيَت الأرقام كما وردت، ولم نَعِد ترقيمها، لأنّ قائمة الجداول في نهاية الدليل (ص241–243) تشير إليها بهذه الأرقام.",
"ترقيم الفروع مضطرب كذلك: «II.2.2» ورد مرّتين (ص77 «Epaisseur et Rigidité des épaulettes»، وص85 «Vérification de l'aspect du veston»)، و«II.2.3» مرّتين (ص78 «le devant de la veste tailleur»، وص86 «Divers défauts du veston»). أعطينا الفرعَين الأخيرين الرقمَين II.2.5 وII.2.6 ليظهر تتابع صحيح في جدول المحتويات، وسُجِّل ذلك تحت كلّ عنوان حتى يبقى المطابقة مع الأصل ممكنة.",
"الشكل II.37 مفقود: ينتقل الأصل من II.36 (ص84) إلى II.38 (ص86)؛ وفي قائمة الأشكال (ص240–241) يُذكر «37 : Divers défauts du veston ص83» و«38 : défauts d'épaulette ص85» — أي أنّ القائمة لا تطابق المتن لا في الرقم ولا في الصفحة. ذُكر ذلك في المتن وفي قائمة الأشكال عند إعادة بنائها في الدفعة الرابعة.",
"الأسماء التجاريّة: «Kupffer» (ص70 و215 من الأصل) و«Kuffner» (ص71–72) و«KUPFFER FRANCE» (ص185 في قائمة المراجع)؛ لا يمكن أن تكون ثلاث أسماء لوثيقة واحدة، وقد تُرِكت كما وردت مع التنبيه، والمرجّح «Kuffner» (اسم الشركة الألمانيّة) — والحسم للمؤسّسة.",
"ص70: «indication» في سياق شروط اللّصق، والمراد «enduction» (الطلاء/التطعيم)؛ ص72: «MeSH» و«qualité» محلّ «mailles» و«densité» (أحرف إنجليزيّة تسلّلت إلى النصّ)؛ ص77: «manqué» محلّ «marqué»؛ ص74: «Répondrez» محلّ «Répondez»؛ ص60–61 (الدفعة الأولى): «laize 0,90 cm» و«Faite». جُميعها أخطاء طباعة في الأصل، أبقيناها كما هي مع ملاحظة تحت الموضع.",
"ص83: «Ou mannequin vivante» (والصواب «sur un mannequin vivant»)، و«la couture de tété de la manche» (والصواب «tête de la manche»)؛ ص84: «Concorde né feutrine du col» عبارة لا تُقرأ (لعلّ الصواب «Accorder le feutrine du col aux points zig-zag»)؛ ص83–84 أيضًا: «les défauts a corrigée» (والصواب à corriger).",
"ص85–105 (العيوب) مبنية في الأصل على عنوان فرعيّ ثمّ «La cause» ثمّ قائمة أسباب ثمّ صورة؛ حافظنا على هذه البنية حرفيًّا بما فيها تكرار عبارة «La cause» بلا ترقيم، لأنّها طريقة عرض المعطى في الدليل.",
"ص89: تمرين المقارنة بخمس سترات وثلاث سترات؛ الأسئلة في الأصل موزَّعة على عمودين فقرأناها بالترتيب الرأسيّ لكلّ عمود؛ والأرقام N:01 وV01… هي تسميات الصور نفسها لا إحالات إلى جدول.",
"ص90–93 (التصحيحات على الباترون): الأبعاد مكتوبة داخل الرسوم؛ وقد نُقلت كما هي. وفي ص91 تناقض في الأصل: عرض جيب الصدر 10 سم وارتفاعه 2,5 سم (II.3.1.2)، ثمّ عرض 12 سم وعمق 12 إلى 13 سم (II.3.1.3)؛ أبقيَ القياسان معًا مع تنبيه، والحسم للمؤسّسة.",
"ص92: «parementure» (مرّتين، والصواب parementure)، و«rélargies» (والصواب élargissements)؛ ص93: سطر عنوان مطبوع فوق سطر تسمية شكل فتولّد نصّ غير مقروء؛ وقد أُرفقت القراءة الأرجح في ملاحظة المترجم بدل تغيير النصّ.",
"ص94–97: أربع صفحات بلا شرح نصّيّ في الأصل (عنوان واحد + صورة أو صورتان؛ والتعليمات كلّها داخل الصور)؛ نُقلت الصور كاملة، ونُقلت التسميات الفرنسيّة داخلها إلى هذا الملحق ترجمةً وشرحًا.",
"ص98–105: الطَيّات الأفقيّة والعموديّة والمائلة وأسبابها؛ ص100 فيها رقمان مطبوعان في التذييل («86» و«99») — الرقم 86 خطأ من الأصل، والرقم الصحيح 99. ص101: تسمية الشكل II.61 تقول «couture cotée devant» بينما المتن يتحدّث عن خياطة جانب الظهر؛ تعارض أُبقي مع التنبيه. ص103: عنوان مكررّ («Longueur de dos insuffisante dans la ligne en dessus de sous bras») ثانيهما يُفهم منه «زائد» لا «ناقص»؛ ص104: «ver» و«voit» (والصواب vers وvoir)؛ ص105: «777manche» (أرقام سبقت الكلمة، والصواب de la manche) و«A-L 'aplomb» بمسافة فاصلة.",
"ص106: الصفحة سؤالان وصورة واحدة كبيرة بلا تسمية؛ وص107 الملخّص داخل إطار مُظلَّل (أسطر مقطّعة في كتل، أعيد تركيبها)؛ ص108 التمرين التركيبيّ (تخصّص، وحدة، مدّة 7 ساعات، هدف، موادّ، أدوات، توابع، وضع التشغيل، طريقة السَّير) وفيه «accessoires: mettre ruban» (والصواب mètre ruban) وسطر يتيم هو نقطتان رأسيتان فقط في آخر الصفحة، وقد أُبقي.",
"تنسيق الدفعة الثانية: 47 صفحة من الأصل أُدرجت كلّ واحدة في صفحة مستقلّة، مع 78 قصاصة عالية الدقّة بالحجم الأصلي دون تغيير نسبة الأبعاد، وجدولين عربيّين معاد بناؤهما (II.01 وII.05)، وكلّ خطأ في الأصل موثَّق بملاحظة «ملاحظة المترجم» تحت موضعه.",
]
NOTES.append(CONFIRM_NOTE)

GLOSS_EXTRA = [
("déroulement des étapes de fabrication","مجرى خطوات التصنيع"),
("assemblage provisoire","التجميع المؤقّت"),
("montage définitif","التجميع النهائيّ"),
("pièce de tracé","قطعة الرَّسم"),
("placement du patron","توزيع الباترون"),
("traçage","الرَّسم على القماش"),
("valeur de couture","قيمة الخياطة"),
("remplis (bas, côté)","الحواشي المدورة (الأسفل، الجانبان)"),
("repère de montage / cran","علامة التجميع / الشقّ"),
("ligne de taille","خطّ الخصر"),
("ligne d'épaule","خطّ الكتف"),
("milieu du dos","منتصف الظهر"),
("milieu du devant","منتصف المقدّمة"),
("emmanchure","فتحة الكمّ"),
("tête de manche","رأس الكمّ"),
("dessous de manche","أسفل الكمّ"),
("dessus de manche","أعلى الكمّ"),
("couture de coude","خياطة المِرفق"),
("couture latérale","خياطة الجانب"),
("couture d'épaule","خياطة الكتف"),
("fente du dos","شقّ الظهر"),
("revers","الردّادة"),
("cran du revers","شقّ الردّادة"),
("col tailleur","ياقة التايلور"),
("pied de col","قاعدة الياقة"),
("revers du col","طيّ الياقة"),
("feutrine de col","لِبّاد الياقة"),
("point chevron","غرزة السَّهم"),
("points bouclettes","الغرزة الحلقيّة"),
("point zig-zag","الغرزة المتعرّجة"),
("surfil","التغبير"),
("bâtir / point de bâti","التذييب / غرزة التذييب"),
("piquer","الخياطة بالماكينة"),
("épaulette","ساد الكتف"),
("rembourrage","الحشو (التبطين)"),
("band d'épaule","شريط الكتف"),
("cigarette (de tête de manche)","شريط «السيجارة» أعلى الكمّ"),
("mannequin (d'essayage)","تمثال الخياطة (للبروفة)"),
("mannequin vivant","عارض حيّ"),
("essayage (premier, deuxième, troisième)","البروفة (الأولى، الثانية، الثالثة)"),
("vérification de l'aspect","التحقّق من المظهر"),
("aplomb","الاستقامة (الثقل)"),
("volume","الحجم"),
("proportions","النِّسب"),
("défaut","علّة / عيب"),
("pli horizontal / vertical / incliné","طيّة أفقيّة / عموديّة / مائلة"),
("largueur (faute pour «largeur»)","العَرض (خطأ إملائيّ في الأصل)"),
("profondeur d'emmanchure","عمق فتحة الكمّ"),
("fermeture boutonnage","إغلاق الأزرار"),
("boutonnière","شقّ الزرّ"),
("bouton","زرّ"),
("largeur de cravate","عَرض ربطة العنق"),
("thermocollant / enduction","اللاصق حراريًّا / الطلاء"),
("toile de corps","حريرة الجسم"),
("toile crin / toile tailleur","الحريرة الشعرية / حريرة التايلور"),
("thermocollage (pressing à plat)","اللّصق الحراريّ (الكبس المسطّح)"),
("presse à chaud","المكبس الحراريّ"),
("fer à vapeur","مكواة البخار"),
("température de fixage","حرارة التثبيت"),
("temps de pressage","مدّة الكبس"),
("pression (bars)","الضغط (بار)"),
("vapeur / séchage","البخار / التجفيف"),
("bulles, décollement, brillance","فقاعات، انفصال، لمعان"),
("gamme de montage provisoire","خطّ تجميع مؤقّت"),
("gamme opératoire","السلسلة العملياتية"),
("correction du prototype","تصحيح النموذج الأوّل"),
("concorde / accorder","الموافقة/التسوية بين القطع"),
("petit côté","الحاشية الجانبية الصغيرة"),
("parementure du devant","الحاشية الداخلية للمقدّمة"),
("doublure de manche / de dos","بطانة الكمّ / الظهر"),
("poche intérieure / poche ticket","الجيب الداخليّ / جيب التذكرة"),
("trianglettes","المثلّثات (ألسنة الجيوب)"),
("languette","اللِّسان الصغير"),
("sac de poche","قِرب الجيب"),
("fond de poche","قعر الجيب"),
("rabat","غطاء الجيب"),
("passepoil","الحاشية الضيّقة"),
("tolérance de couture","تحمُّل الخياطة"),
]


def build(doc, blocks, LINEBY, FIGDIR, REG, P, add_table, add_picture, shade, rtl_paragraph,
          WD_ALIGN, Pt_, Cm_, RGB_, WD_BRK):
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
    def head(text, style='Heading 1'):
        h = doc.add_paragraph(style=style); rtl_paragraph(h); h.add_run(text)
        doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    rows = []
    for pg, sup, fr, ar in MANUAL:
        rows.append([str(pg), sup, fr, ar])
    extra_ids = set()
    for pg, sup, fr, ar in MANUAL:
        for tok in str(sup).replace("(", " ").replace(")", " ").replace("/", " ").replace(",", " ").split():
            if "_r" in tok or "_d" in tok:
                extra_ids.add(tok)
    for p in blocks["pages"]:
        if not (62 <= p["page"] <= 108):
            continue
        for r in p["regions"]:
            if r["id"] in extra_ids:
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
            rows.append([str(p["page"]), f"{r['id']} ({r['kind']})", fr,
                         "تُرجمت في صلب الدليل (التسمية تحت الصورة / الجدول العربيّ المقابل)"])
    ex = f"work/{os.environ.get('TAG', 'batch2')}_extra.json"
    if os.path.exists(ex):
        for e in json.load(open(ex)):
            if e["id"] in extra_ids:
                continue
            rows.append([str(e["page"]), f"{e['id']} (صورة مستعادة)",
                         "لا نصّ: أيقونة/عنصر زخرفة صغير ملحق بإطار الصفحة",
                         "فُحصت على ورقة تلامس فتبيّن أنّها بلا محتوى؛ لم تُدرَج في المتن"])
    rows.sort(key=lambda r: (int(r[0]), str(r[1])))
    head("الملحق (أ) — النصوص الواردة داخل الصور ولوحات الأصل (الدفعة الثانية: ص62–108)")
    P("تضمّ هذه القائمة كلّ نصّ داخل صورة أو لوحة مصوَّرة في صفحات الأصل 62–108: بطاقات شروط اللّصق الحراريّ، "
      "لوحات الشركة المصنِّعة، جداول العيوب المصوَّرة، رسوم الباترون المعلَّمة بالأبعاد، والصفحات المصوَّرة بالكامل "
      "(ص94–97) التي لا شرح لها في الأصل. وما كان من تسمية شكل مدرجة في طبقة النصّ فقد تُرجم تحت الصورة نفسها في المتن. "
      "وما تعذّرت قراءته من صور النشرات ذُكر صراحةً «غير مقروء في الأصل» ولم يُخمَن.", size=12)
    add_table(rows, header="صفحة الأصل||الصورة / اللوحة||النصّ كما ورد في الأصل||الترجمة العربية والموضع", fontsz=9)

    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    head("الملحق (ب) — ملاحظات المترجم والتصحيحات والبنود التي تحتاج تأكيدًا (الدفعة الثانية)")
    for i, n in enumerate(NOTES, 1):
        P(f"{i}- {n}", size=13)

    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    head("الملحق (ج) — مسرد مصطلحات الدفعة الثانية (التصنيع: اللّصق، التركيب، البروفات، العيوب)")
    P("يُضاف هذا المسرد إلى مَسارد الدفعات الأخرى؛ وهو مستمدّ من الفصل الثاني (مجرى خطوات التصنيع) في صفحات الأصل "
      "62–108. وقد ثُبِّتت المصطلحات بتاريخ 4 نوفمبر 2026 فأصبحت نهائيّة.", size=12)
    P(CONFIRM, size=11, color="C00000")
    add_table([[fr, ar] for fr, ar in GLOSS_EXTRA], header="الفرنسية||العربية", fontsz=11)
