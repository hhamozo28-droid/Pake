# -*- coding: utf-8 -*-
"""Annexes du lot 3 (pages PDF 109–188 : Chapitre III — UNIFORMISATION DE LA GAMME DES VESTONS,
tableaux de pièces, gammes opératoire et de montage, collection, repassage, étude de cas,
tolérances, bibliographie, début de l'ANNEXE A)."""
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

CONFIRM_NOTE = ("تثبيت المصطلحات: بموافقة صاحب الملف بتاريخ 4 نوفمبر 2026 اعتُمدت مصطلحات gamme de montage (خطّ التجميع)، "
                "gamme opératoire (السلسلة العملياتية)، triplure (الحشوة الوسطى)، doublure (البطانة)، entoilage (الحشو)، "
                "parementure (الحاشية الداخلية)، passepoil (الحاشية الضيّقة)، surfil (التغبير)، boutonnière (شقّ الزرّ)، "
                "repassage/presse (الكَيّ/الكبس)، tolérance (تحمُّل) نهائيةً في كامل الدليل. "
                "وفي هذا النطاق تحديدًا استعمل الأصل تسميات متبدّلة للشيء نفسه: «triplure» (ص111) مقابل «toile coulante» "
                "(ص127–130) مقابل «entoilage» (ص131–134)؛ وقد وحّدناها في العربية إلى «الحشوة الوسطى» و«الحريرة الجارية» "
                "و«الحشو» بالترتيب، مع إبقاء اللفظ الفرنسيّ تحت كلّ عنوان. "
                "أمّا البنود التي لم تُحسَم لأنها أخطاء في الأصل لا اختيار مصطلح — مثل «00» للقطعة 16 (ص122)، والقطعة 45 "
                "بلا تسمية (ص130)، وتكرار رقم القطعة 60 مرّتين (ص134)، والغرزة «30» بدل «301» (ص144–146)، والعَرض "
                "بالسنتيمتر في ص177 («laize de 1,50 cm») — فقد أبقيناها كما وردت مع ملاحظة المترجم، وهي تنتظر قرار المؤسّسة؛ "
                "وكُلّها مفصَّلة في ملفّ «تعليمات_التعديل.txt» المرفق مع التسليم.")

MANUAL = [
(110,"p110 (جدول مصوَّر جزئيًّا)","Tableau 01 : Les pièces à couper de veston (Tissu) — N° Pièce | Désignation | Multiplicateur | Ordre de pièce dans le placement (cliché) | Tissu",
 "الجدول 01 (18 قطعة)؛ رؤوس أعمدته في طبقة النصّ وقد ترجمت في المتن. خانة «Tissu» مدموجة في الأصل بكلمة «Tergal du laine» "
 "عبر كامل العمود، ففُكِّكت في كلّ صفّ لتسهيل القراءة، وذُكر ذلك تحت الجدول"),
(111,"p111 (جدول مصوَّر)","Tableau n02 : Les pièces à Doubler du veston (doublure) — 11 lignes, «Taffetas»",
 "الجدول 02 (قطع البطانة)؛ تسميته في الأصل «Tableau n02» بحرف n؛ والخانة الأخيرة مدموجة بكلمة «Taffetas» وحدها فأُعيدت "
 "في كلّ صفّ. والقطعة 05 مكتوبة «Dessus manche» كالقطعة 04 (والصواب Dessous manche)؛ خطأ في الأصل أُبقي مع التنبيه"),
(112,"p112 (جدول مصوَّر)","Tableau 03 : Les pièces de veston à thermocoller — colonne «Thermocoller»",
 "الجدول 03 (22 سطرًا)؛ رأس العمود الأخير «Thermocoller» (فعل لا اسم) فترجم إلى «يُلصَق حراريًّا»؛ وترقيم التوزيع "
 "«01/16» مكررّ للمقدّمة، و«02/16» ثلاث مرّات للظهر، و«03/16» مرّتين للكمّ، و«15/16» مرّتين — لأنّ الخانة تُعرِّف بطاقة "
 "التوزيع لا ترتيب القطعة؛ والرقم 6 كُتب «6/16» بلا صفر"),
(113,"p113 (شريط رأس البطاقة)","PRODUIT : POCHE PASSE POILEE — MACHINE | TYPE DE POINT | NBR PTS CM — 301 | 504 | 304 | 107 | Néant",
 "شريط رأس بطاقة «الجيب ذي الحاشية الضيّقة»: المنتوج، الآلة، نوع الغرزة، عدد الغرز في السنتيمتر، ثمّ خمسة رموز "
 "(301، 504، 304، 107، لا شيء) وردت قبل رأسٍ ثانٍ (ETP N° | OPERATIONS | SECTIONS SORTIES | TMPS | EQPS)؛ هذا الخلط "
 "من تنضيد الأصل، والرموز نُسبت إلى صفوفها في الجدول المعرَّب بمجاورتها الطبعتيّة لها"),
(113,"p113_r1 / p113_r2","Deux schémas de la première opération (76×50 pt et 195×70 pt), sans texte",
 "رسمان صغيران للخطوة الأولى بلا نصّ داخلهما؛ أُلحِقا في المتن بحجمهما"),
(114,"p114_r1 … p114_r5","Piquer et ENTOILER : DOUBLUR E DU DEVANT -L 'endroit de poche intérieur — CONFORM ER OU PLIER",
 "نصّ الخطوات 02–04 مكسَّر داخل خلايا ضيّقة في الأصل (DOUBLUR/E، CONFORM/ER OU، -L 'endroit)؛ أُعيد تركيب العبارات في "
 "الجدول العربيّ مع ذكر القطع الأصليّ تحت الجدول"),
(115,"p115_r1 … p115_r4","Étapes 05 à 07 ; phase écrite verticalement « M O N T A G E »",
 "الخطوات 05–07؛ ومرحلة «التجميع» مكتوبة عموديًّا حرفًا حرفًا في هامش الأصل؛ الرمز 301 ملاصق لكلّ خطوة فنُسب إليها"),
(116,"p116_r1 … p116_r4","Étapes 08 à 11 avec codes 301, 304, 301, 516",
 "الخطوات 08–11 مع رموز الغرز 301 و304 و301 و516؛ لا نصّ داخل الصور"),
(117,"p117_r1 / p117_r2","Étapes 12 et 13 (FIXER / Repasser) — «Tableau 04 : Gamme opératoire de la poche passe poilée»",
 "الخطوتان 12 و13؛ وتسمية الجدول 04 وردت في الأصل بعد محتواه (في نهاية الجدول لا في أوّله)؛ أُبقي موضعها مع التنبيه"),
(118,"p118_r1 + شريط رأس","PRODUIT VESTON — MACHINE | TYPE DE POINT | NBR PTS CM — 301 | 504 | 304 | 107 | Néant",
 "شريط رأس بطاقة «ستر الرجل» (بداية الجداول 05–09) بنفس خانات ص113؛ أُدرج في المتن مع ملاحظة أنّ «MATIERE :» بلا قيمة"),
(119,"p119_r1 / p119_r2","Tableau des pièces Tissu — schémas dessinés (Devant : -Supérieur, -Inferieur ; Dos)",
 "رسوم القطع 01 و02 (خلايا «Schématisation») لا نصّ فيها؛ رؤوس الجدول (N° | Désignation | Schématisation | NP | N PT) "
 "بلا شرح في الدليل، وقد فُسِّرت في ملاحظة المترجم: NP = عدد القطع، N PT = رمز نوع الغرزة/البطاقة"),
(120,"p120_r1 … p120_r3","Schémas des pièces 03 à 05 (P- cote, Dessus de manche, Dessous de manche) avec code 301",
 "رسوم القطع 03–05؛ الاختصار «P- cote» (والصواب petit côté) في الأصل، ورمز 301 مكتوب في خلية N PT"),
(122,"p122_r1 / p122_r2","Schémas des pièces 10 à 17 — NP de la pièce 16 : «00»",
 "رسوم القطع 10–17؛ عدد القطعة 16 ورد «00» في الأصل (والمرجّح 01)؛ أُبقي مع التنبيه، وهو من بنود قرار المؤسّسة"),
(123,"p123_r1 / p123_r2","Pièce 18 — «Tableau 05 : Tableau des pièces tissu (tergal)»",
 "القطعة 18 وتسمية الجدول 05 (وردت في نهاية الجدول)؛ لا نصّ داخل الصورتين"),
(126,"p126_r1 / p126_r2","Pièces 25 à 29 (doublure) — «Tiret» et code 301",
 "رسوم قطع البطانة 25–29؛ القطعة 29 سمّاها هذا الجدول «Tiret» والجدول 02 «Tirette»؛ الفرق وارد في الأصل وأُبقي"),
(130,"p130_r1 … p130_r3","Pièces 42 à 45 (toile coulante) — la ligne 45 est sans désignation",
 "رسوم القطع 42–45؛ سطر القطعة 45 بلا تسمية في الأصل (خانة Désignation فارغة) فأُبقي فارغًا في الجدول العربيّ مع التنبيه"),
(131,"p131_r1 … p131_r3","Tableau de pièce l'entoilage — phase écrite verticalement «ENTOILER / PRESSE»",
 "رأس الجدول في الأصل مبتور («Désignati / on» على سطرين)، والمرحلة مكتوبة عموديًّا فالتبست بالأرقام؛ وخانتا NP وN PT "
 "فارغتان عدا كلمة «Presse»"),
(134,"p134_r1 … p134_r4","Pièces 56 à 65 — «La watt», «Le cigare», «Porte de feuille», numéro 60 répété",
 "رسوم قطع الحشو 56–65؛ «La watt» و«Le cigare» لفظتان إنجليزيّتان (wadding/cigar) تسلّلتا إلى نصّ فرنسيّ، والصواب ouate "
 "وpassepoil cigarette؛ ورقم القطعة 60 مكررّ مرّتين (سطرًا 328 و394 في طبقة النصّ)"),
(135,"p135_r1 … p135_r3","Gamme de montage — N° | Désignation | Schématisation | NP | N PT ; étapes 01 à 03",
 "رأس جدول خطّ التجميع (ص135–153) هو نفسه رأس بطاقات القطع؛ والصور الثلاثة رسوم خطوات 01–03 بلا نصّ"),
(143,"p143 (نصّ داخل العمود)","Perfor / euse — M-S — 404 (étape 28 : tracer la boutonnière, exécuter les fausses boutonnières)",
 "اسم الآلة في الأصل مقطوع على سطرين («Perfor/euse»)؛ ورمز الغرزة 404؛ وقد أُبقيَا مع ملاحظة تحت الجدول"),
(144,"p144–p146 (عمود الغرز)","Code «30» aux étapes 30, 33 (p145) et 36 (p146) au lieu de «301»",
 "رمز الغرزة كُتب «30» في ثلاثة مواضع من الأصل بدل «301»؛ أُبقي كما ورد لأنّ تصحيحه يحتاج قرار المؤسّسة"),
(146,"p146_r1 / p146_r2","Étape 36 : Mante la manche et fixer le cigare en respectant la distribution de l'embu",
 "الفعل «Mante» ليس فرنسيًّا (والصواب Monter)، وهو يتكرّر في ص151 الخطوة 49؛ و«le cigare» سمّى به الدليل ما سمّاه في "
 "ص83 «la cigarette»؛ و«l'embu» والصواب l'emboîture"),
(152,"p152_r1 … p152_r3","Étapes 52 à 54 — «les posses boutants», machines «M.N», «Presse»",
 "الخطوات 52–54؛ عبارة «les posses boutants» لا تُقرأ (والأرجح les poches boutantes أو les pattemouilles)؛ وأسماء "
 "الماكينات (M-U، M-S، C-tail، M.N، Perforeuse، Presse) بلا شرح في أيّ مكان من الدليل"),
(153,"p153_r1","Étape 55 : Mise en emballage — «Sache» plastique — 301",
 "خطوة التغليف في كيس بلاستيكيّ؛ «Sache» (والصواب sachet)؛ ولا محلّ لخطوة تغليف في خطّ تجميع الخياطة، لأنّها من مرحلة "
 "التعبئة والإرسال (ص190 من الأصل)"),
(157,"p157_r1 (لوحة كاملة)","LA COLLECTION PRINTEMP – ETE — planche de vestons numérotés",
 "لوحة مجموعة الربيع/الصيف صفحةٌ مصوَّرة بالكامل بلا نصّ في طبقة النصّ؛ العنوان «PRINTEMP» (والصواب PRINTEMPS)؛ وأرقام "
 "النماذج داخل اللوحة لا تُفصل عنها، فنُقلت الصورة كاملة"),
(158,"p158_r1 (لوحة كاملة)","LA COLLECTION AUTOMNE – HIVER — planche de vestons numérotés",
 "لوحة مجموعة الخريف/الشتاء؛ المعالجة نفسها كما في ص157"),
(159,"p159_r1","Figure 01 : le repassage — source Pinterest",
 "صورة واحدة للشكل III.01 (الكَيّ)؛ تسميته في الأصل بلا «III»؛ وفي الصفحة نفسها عنوان فرعيّ مرقّم «III.2.1» مكررّ مع "
 "ص155 (والصواب III.2.2)"),
(161,"p161_r1 / p161_r2","Figure 02 : table de repassage | Figure III.03 : l'étiqueté de la veste",
 "صورتان؛ التسمية الأولى بلا «III» والثانية بـ«III» في الصفحة نفسها؛ و«l'étiqueté» (والصواب l'étiquette)"),
(164,"p164_r1 / p164_r2","Figure 06 : protection de la veste | Figure 07 : la veste à plat",
 "صورتان بلا «III» في تسميتهما؛ والنصّ يستعمل «le revêtement» للدلالة على البطانة (doublure)"),
(165,"p165_r1 / p165_r2","Figure 08 : repassez les sections arriérées | Figure 09 : l'avant de la veste",
 "صورتان؛ «sections arriérées» ليست تسمية تقنيّة (والصواب la partie arrière)؛ تُرجم المعنى وسُجِّلت عبارة الأصل"),
(166,"p166_r1 / p166_r2","Figure 10 : repassage l'avant de la veste | Figure 11 : apprêtez le manche",
 "صورتان؛ «le manche» (المقبض) بدل «la manche» (الكمّ) خطأ في الأصل؛ و«Apprêtez» تعني التجهيز/التنجيل"),
(167,"p167_r1","Figure 12 : repassage de la manche | Figure 13 : Accrochez la veste",
 "صورتا كَيّ الكمّ وتعليق السترة؛ التسميتان بفعل الأمر بدل اسم، كما في الأصل"),
(171,"p171_r1 (صفحة كاملة)","III.3.1.2 : Nomenclature du prototype de la veste — planche dessinée",
 "ص171 صورة واحدة: جدول جرد قطع النموذج الأوّل مرسوم مع رسم السترة وأرقام القطع؛ لا نصّ قابل للنسخ، فنُقلت الصفحة "
 "كاملة، وتُرجمت تسميات القطع في هذا الملحق (وهي أنفسها جداول ص119–134)"),
(172,"p172_r1 (صفحة كاملة)","III.3.1.3 : Sections sorties — planche avec renvois numérotés",
 "ص172 صورة واحدة لمقاطع الإخراج (أرقام إحالية على الرسم)؛ بلا نصّ؛ نُقلت كاملة"),
(174,"p174_r1 / p175_r1 / p176_r1","Dessin détail de chaque élément (trois planches annotées)",
 "ثلاث صفحات رسوميّة (تفاصيل المقدّمة والكمّ والجيوب) بتعليقات داخل الرسوم، وبلا نصّ في طبقة النصّ؛ أُدرجت الرسوم كاملة، "
 "وهذه العبارات الواردة داخلها: Devant, Revers, Cran, Col, Poche passepoilée, Rabat, Fente, Dos, Emmanchure, "
 "Tête de manche, Boutonnières — بالترتيب: المقدّمة، الردّادة، الشقّ، الياقة، الجيب ذو الحاشية الضيّقة، الغطاء، الشقّ "
 "الجانبيّ، الظهر، فتحة الكمّ، رأس الكمّ، شقوق الأزرار"),
(184,"p184_r1 (شبكة مصوَّرة)","Grille d'évaluation formative — Oui / Non | Evaluation par le formateur | Auto évaluation par le stagiaire",
 "شبكة التقويم التكوينيّ صورةٌ واحدة بأربعة أعمدة وصفوف مُرقَّمة (1-1، 2-1 … 6-1)؛ أُدرجت كاملة، وأُعيدت خانتا «نعم/لا» "
 "في المتن لأنّ الأصل يشرحهما بمثالَين (5-1 مُكتسَب، 6-1 غير مُكتسَب)"),
(187,"p187_r2 (شريط عنوان)","ANNEEX A",
 "شريط عنوان الملحق في الأصل مكتوب «ANNEEX A» (والصواب ANNEXE A)؛ نُقل كما ورد، ووُضعت الترجمة الصحيحة في المتن مع التنبيه"),
]

NOTES = [
"نطاق الدفعة الثالثة: صفحات PDF 109–188، أي الفصل الثالث «توحيد خطّ سترات الرجل» كلُّه: إعداد خطّ التصنيع وجداول القطع "
"(ص109–112)، والسلسلة العملياتيّة للجيب ذي الحاشية الضيّقة (ص113–117)، وبطاقات القطع الأربع (ص118–134)، وجدول خطّ "
"التجميع بـ55 خطوة (ص135–153)، والتمرين (ص154)، والمجموعة الموسميّة (ص155–158)، وتقنيات الكَيّ (ص159–167) وتمارينها "
"(ص168)، ودراسة حالة السترة الكلاسيكيّة (ص169–176)، وتمرين عدد الأمتار التركيبيّ (ص177)، والمواصفات والتحمُّلات "
"(ص178–180)، والملخّصَين (ص181–182)، وتمرين تركيب الوحدة (ص183)، وشبكة التقويم (ص184)، والمراجع (ص185–186)، ثمّ "
"أوّل صفحتَين من «ANNEXE A» بتصحيحات تمارين الفصل الأوّل (ص187–188).",
"الأرقام: ص109–186 مرقَّمة بإزاحة ثابتة (رقم PDF − 1)؛ ومن ص187 يبدأ ترقيم رومانيّ جديد (I في ص187، II في ص188) "
"لافتتاح الملاحق. لذلك ذُكر رقما الصفحة معًا عند كلّ صورة وجدول، ولا يجوز في الملفّ الموحد أن يُطبَّق مقطع ترقيم واحد "
"على هذا النطاق كلّه.",
"جداول القطع 01 و02 و03 (ص110–112) والجداول 05 إلى 08 (ص119–134) تغطّي المعطى نفسه (قطع القماش والبطانة والحريرة "
"الجارية والحشو) بصيغتَين مختلفتَين: الجدول 01 بعمود «Ordre de pièce dans le placement (cliché)»، والجدول 05 بعمودَي "
"«NP» و«N PT» بلا شرح للأحرف. أُعيد بناء الثمانية كما وردت، والفروق مُسجَّلة تحت كلّ جدول، والتوفيق بينها يحتاج قرار "
"المؤسّسة.",
"أخطاء ثوابت في جداول القطع: القطعة 05 «Dessus manche» مكرّرة بدل «Dessous manche» (ص110 و111 و120 و125)؛ و«1/18» "
"مرّتان للمقدّمة (ص110)؛ و«00» عددًا للقطعة 16 (ص122)؛ والقطعة 45 بلا تسمية (ص130)؛ ورقم القطعة 60 مكرّر مرّتين (ص134)؛ "
"و«Tiret» مقابل «Tirette»؛ و«La watt» و«Le cigare» بدل ouate وpassepoil cigarette. جميعها أُبقيَت كما وردت.",
"بطاقات العمليات (ص113–117 و119–153) في الأصل جداولُ مرسومة: النصّ داخل خلايا ضيّقة فيتكسّر («DOUBLUR E»، "
"«CONFORM/ER»، «Désignati / on»، «Perfor / euse»)، وعناوين المراحل مكتوبة عموديًّا في العمود الأوّل («PREPARATION»، "
"«MONTAGE»، «ENTOILER»، «PRESSE») فتلتصق بالحروف والأرقام. أعيد تركيب العبارات في الجداول العربيّة، وذُكر اللفظ "
"الأصليّ كما طُبِع تحت كلّ جدول. ولم يشرح الدليل رموز الآلات (M-U، C-tail، M-S، M.N، Perforeuse، Presse) في أيّ موضع — "
"وهي تحتاج بيانًا من المؤسّسة.",
"السلسلة العملياتيّة للجيب ذي الحاشية الضيّقة (الجدول 04، ص113–117) مقسَّمة على خمس صفحات، وص113 تحمل رأسَين للجدول "
"في آن؛ فبُنِي جدولٌ واحد من 13 خطوة، ونُسِب كلّ رمز غرزة إلى صفّه بمجاورته الطبعتيّة، وأُعلِن ذلك صراحةً تحت الجدول. "
"والخانتان TMPS (الزمن) وSECTIONS SORTIES فارغتان في الأصل، والفعل «MARQUERER» (والصواب MARQUER).",
"جدول خطّ التجميع (الجدول 09، ص135–153): 55 خطوة متّصلة؛ رؤوسه في ص135 وتسميته في ص153. العمودان «NP» و«N PT» "
"يحملان هنا الآلةَ ورمزَ الغرزة لا عددَ القطع (عكس بطاقات القطع) — تناقض في استعمال الأحرف داخل الدليل، فُسِّر بحسب "
"السياق وسُجِّل.",
"ص144–146: رمز الغرزة «30» بدل «301» في الخطوات 30 و33 و36؛ وص143 و147 و152: رمز «404» في سياق شقوق الأزرار التي "
"رمزها في ص116 هو «304». أبقيَت الرموز كما وردت، لأنّ تصحيحها يغيّر دلالة الآلة.",
"ص146 و151: الفعل «Mante» (ليس فرنسيًّا؛ الصواب Monter)؛ ص144 و151: «coin angler» منقولة عن الإنجليزية (والصواب coin "
"en onglet)؛ ص152: «les posses boutants» غير مقروءة؛ ص153: «Sache» (والصواب sachet)؛ ص146 و151 و152: «embu» و"
"«thermocollante» (والصواب thermocollant، لأنّ passement مذكَّر). تُرجم المعنى بحسب الأرجح مع عبارة الأصل تحت الجدول.",
"ص155 و156: ص156 تكرارٌ حرفيّ لآخر ص155 (عنوان «III.2. 1.2 : Le cadre de collection» والنصّ نفسه)؛ أُبقي التكرار "
"حفاظًا على تطابق عدد الصفحات مع الأصل، وسُجِّل. وفي ص155 نفسها «parmenture ou saisonnière» عبارة لا تُقرأ (لعلّها خطأ "
"مسح ضوئيّ)، و«Colorie» بدل coloris، و«qui les réunis» بدل réunit، و«chemiser» بدل chemises.",
"ص157 و158: لوحتا المجموعتين صورٌ بالكامل بلا نصّ (وأرقام النماذج داخل الرسم)، فلا ترجمة ممكنة لمحتواها؛ ذُكر ذلك "
"صراحة في المتن ونُقلت اللوحتان كاملتَين.",
"ص159–167 (تقنيات الكَيّ): هذا الجزء نصّ إرشاديّ موجَّه إلى المستهلك بصيغة المخاطب («vous pouvez la repasser à la "
"maison»)، لا نصٌّ مهنيّ، وهو منقول بلا إحالة إلى مصدر؛ تُرجم كما هو. أرقام الفروع مضطربة: «III.2.1» مكررّ مع ص155، ثمّ "
"«III.2.1.1» يتلوه مباشرةً «III.2.2.2» (بلا III.2.2.1). وتسميات الأشكال غير موحَّدة («Figure 01»، «Figure III.03»، "
"«Figure 06»…). والأخطاء اللغويّة كثيرة: étés/êtes، bruler، distillé، importance quantité، il faillait، le manche، "
"arriérées، retractées، saignement repassé، à l'accrochez، maitre a repassé، unirent — وكلّها موثَّقة تحت موضعها.",
"ص169 (البطاقة التقنيّة): «LA VESTE CASSIQUE» و«ficher technique» و«TOLERONCES» (والصواب CLASSIQUE، fiche، TOLérANCES)؛ "
"وقائمة التحمُّلات فيها خانتان بلا قيمة («Solidité fentes ouverture bas de manches»)، و«− 1mm» مكرّرة؛ وخانة «Matériel :» "
"فارغة. ص170 (الوصف): «DESSIN» مرّتين بلا نصّ (الخلّيتان مصوَّرتان)، و«Boutonnage avec 03 bouton» (والصواب boutons)، "
"و«avec quatre fausses» مبتورة (يُفهم fausses boutonnières)، و«Entièrement double» (والصواب doublé).",
"ص171–176: ستّ صفحات بلا نصّ قابل للنسخ (جرد القطع، مقاطع الإخراج، وثلاث لوحات تفاصيل)؛ نُقلت "
"صورُها كاملة بالحجم الأصلي، وتُرجمت تسمياتها في الملحق (أ) بدل إعادة بناء جداول بالتخمين.",
"ص177 (تمرين 10 ساعات): «laize de 1,50 cm» — الوحدة في الأصل سنتيمتر والصواب متر (الخطأ نفسه في ص17 و61 من الدفعة "
"الأولى)؛ و«Faite la recherche» (والصواب Faites)؛ و«mettre ruban» (والصواب mètre ruban)؛ و«tête bêche» (الوضع المعاكس "
"للباترونات) تُرجمت بحسب معناها التقنيّ مع إبقاء المصطلح.",
"ص181 و182: «III.5 : RESUME» يتلوه «III.7 : Résume général» — الرقم III.6 مُسقَط في الأصل؛ و«Résume» بدل «Résumé» "
"مرّتين، وتحتَه «Résumé générale» (تذكير/مؤنّث مختلط)؛ و«Le présent manuel intitule» (والصواب s'intitule)؛ و«Ce "
"document repose» (والصواب Cette). ص183: «EXCERCICE SYNTHESE DU MODULE» بلا «DE» وبخطأ إملائيّ، و«de la veste proposé "
"homme» (والصواب proposée pour homme).",
"ص185–186 (المراجع): عناوين الكتب تُرجمت مع إبقاء الأصل؛ لكنّ لائحة المواقع اعتلّ توثيقها: «Www Organisation "
"scientifique du travail .cours-ofppt.com .fichier Maroc.PDF» و«Www source Pinterest. Com toutes les photos du manuel» "
"و«www.Les équipements de protection individuelle. PDF» — أي أنّ عناوين الصفحات دُمجت بمكان الروابط فلا يمكن استخراج "
"رابط صحيح منها؛ ولم نُصلِحها لأنّ ذلك يستلزم تتبّع المصدر الأصليّ. واسم المؤلِّفة مكتوب «CHRISTELLE BENTOUT» هنا و"
"«Christelle benetout» في ص111 (والصواب Benetaout).",
"ص187–188: افتتاح «ANNEXE A» (العنوان في الأصل «ANNEEX A») بتصحيحات تمارين الفصل الأوّل؛ الترقيم الرومانيّ يبدأ هنا "
"(I ثمّ II)، وهو ما يفسّر مقاطع الترقيم الثلاثة في الملفّ الموحد. إجابات ص187 مختصرة إلى حدّ الإبهام («De mettre une "
"semelle téflon au fer»، «Tergale et Dacron» — والاسم التجاريّ Tergal)؛ و«Les trois types d'armures» تُرجمت إلى بنى "
"النسيج (سادة، تويل، ساتان) لا إلى «أنسجة السَّدَى». ص188 تتضمن صيغتَي الهدر والمردود: (Petr − Pp)/Petr × 100 و"
"Pp/Petr × 100، وقد بُنِيَت في المتن بوسم الصيغة لا كنصٍّ عاديّ.",
"تنسيق الدفعة الثالثة: 80 صفحة من الأصل أُدرجت كلّ واحدة في صفحة مستقلّة، مع 147 قصاصة عالية الدقّة بالحجم الأصلي دون "
"تغيير نسبة الأبعاد، و40 جدولًا عربيًّا معاد البناء (منها جدول بخطّ تجميع من 55 خطوة، وثلاثة جداول قطع، وجدول 22 سطرًا "
"لّلصق الحراريّ)، ومسرد بـ120 مدخلًا، وكلّ خطأ في الأصل موثَّق بملاحظة تحت موضعه.",
]
NOTES.append(CONFIRM_NOTE)

GLOSS_EXTRA = [
("uniformisation de la gamme","توحيد خطّ سترات الرجل"),
("gamme de fabrication","خطّ التصنيع"),
("agent d'étude","موظّف الدراسة"),
("temps total de fabrication","الوقت الإجماليّ للتصنيع"),
("schéma de couture","مخطّط الخياطة"),
("multiplicateur","المُضاعِف (عدد القطع في القصّة)"),
("ordre de pièce dans le placement","ترتيب القطعة في توزيع القصّ"),
("cliché (de placement)","بطاقة التوزيع"),
("NP / N PT","عدد القطع / رمز نوع الغرزة (أحرف بلا شرح في الأصل)"),
("pièces à couper","القطع الواجب قصّها"),
("pièces à doubler","القطع الواجب تبطينها"),
("pièces à thermocoller","القطع الواجب لصقها حراريًّا"),
("toile coulante","الحريرة الجارية (قماش اللّصق)"),
("entoilage","الحشو"),
("tergal","ترغال"),
("taffetas","تفتا"),
("drap","ثوب صوفيّ (drap)"),
("feutre / feutrine","لِبّاد"),
("banane","شريط منحني (موزيّ)"),
("tirette / tiret","سَحّابة / لِسان"),
("poche américaine","الجيب الأمريكيّ"),
("poche portefeuille","جيب المحفظة"),
("poche cigarette","جيب السيجارة"),
("poche stylo","جيب القلم"),
("poche plaquée","الجيب المُلبَّق"),
("fond de poche","قعر الجيب"),
("sac de poche","قِرب الجيب"),
("patte de poche","لسان الجيب"),
("parementure de poche","الحاشية الداخلية للجيب"),
("passepoil / passe-poil","الحاشية الضيّقة"),
("marquer l'emplacement","تعليم الموضع"),
("entoiler","حشو القطعة (تَلبيدها)"),
("conformer / plier","التطابق / الطيّ"),
("surfiler","التغبير"),
("positionner","التوزيع/التموضع"),
("écarter la couture","إبعاد الخياطة"),
("fixer les triangles","تثبيت المثلّثات"),
("plaquer","الإلباق"),
("fermer le sac","إغلاق القِرب"),
("glacer","التلجيم (تسطيح الحافة)"),
("section sortie","القسم المُخرَج"),
("phase de travail","مرحلة العمل"),
("préparation / montage / finition","التحضير / التجميع / التشطيب"),
("gamme provisoire / définitive","الخطّ المؤقّت / النهائيّ"),
("piquer la pince","خياطة القَصة"),
("assembler le petit côté","تجميع الحاشية الجانبية الصغيرة"),
("retourner et repasser","القلب والكَيّ"),
("couture saignée","الخياطة المَكتومة"),
("couture coude","خياطة المِرفق"),
("coin en onglet","الزاوية المائلة (المسمّاة في الأصل anglais/angler)"),
]

GLOSS_EXTRA += [
("fausses boutonnières","الشقوق الوهميّة"),
("point d'arrêt","غرزة الإيقاف"),
("distribution de l'emboîture","توزيع امتلاء رأس الكمّ"),
("pose de l'épaulette","تثبيت ساد الكتف"),
("griffe de marque / de taille","علامة الماركة / المقاس"),
("coutures ouvertes","الخياطات المفتوحة (المكويّة جانبًا)"),
("mise en emballage","التغليف"),
("collection capsule","المجموعة «الكبسولة»"),
("plan de la collection","مخطّط المجموعة"),
("cadre de collection","إطار المجموعة"),
("campagne (printemps-été / automne-hiver)","حملة (ربيع/صيف — خريف/شتاء)"),
("direction commerciale","المصلحة التجاريّة"),
("étude qualitative et quantitative","الدراسة النوعيّة والكمّيّة"),
("étude de concurrence","دراسة المنافسة"),
("grossiste / détaillant","تاجر جملة / تجزئة"),
("prix de vente / prix de revient","ثمن البيع / سعر الكلفة"),
("échantillons matière-fournitures","نماذج الموادّ واللوازم"),
("table à repasser","طاولة الكَيّ"),
("presse en cours / presse finale","الكبس الجاري / الكبس النهائيّ"),
("vapeur / eau distillée","البخار / الماء المقطَّر"),
("déluster / défroisser","إزالة البريق / فرد التجعّدات"),
("préformage","التشكيل المسبق"),
("surépaisseurs","الزوائد السميكة (تراكب الخياطات)"),
("le grainage","الحَبّ (مظهر النسيج)"),
("patte-mouille","الرقعة الرطبة"),
("étude de cas","دراسة حالة"),
("fiche technique de fabrication","البطاقة التقنيّة للتصنيع"),
("réglage de la longueur du point","ضبط طول الغرزة"),
("points par 10 mm","عدد الغرز في 10 مم"),
("fils poly-coton n°120 / 150","خيوط بولي‑قطن رقم 120 / 150"),
("aiguille n°90","إبرة رقم 90"),
("raccord (assemblage)","المطابقة عند التجميع"),
("symétrie","التناظر"),
("surpiqûre","الخياطة الظاهرة الإضافيّة"),
("conformité du produit","مطابقة المنتوج"),
("tolérance de précision","تحمُّل الدقّة"),
("tolérance de positionnement des crantages","تحمُّل توزيع الشقوق"),
("tolérance de traçage","تحمُّل الرَّسم"),
("écart admissible","الانحراف المقبول"),
("plus ou moins 1 mm / 3 mm","زائد/ناقص 1 مم / 3 مم"),
("grade de qualité (faute pour «niveau de qualité»)","درجة الجودة (خطأ في الأصل)"),
("dessin technique","المخطّط التقنيّ"),
("nomenclature du prototype","جرد تسمية النموذج الأوّل"),
("fiche qualité","بطاقة الجودة"),
("grille d'évaluation formative","شبكة التقويم التكوينيّ"),
("auto-évaluation","التقويم الذاتيّ"),
("bibliographie","قائمة المراجع"),
("recherche du métrage","البحث عن عدد الأمتار"),
("imbrication (tête bêche)","التداخُل (الوضع المعاكس)"),
("matelas / table de matelassage","المَطحَر / طاولة الفرش"),
("longueur utile de la table","الطول النافع للطاولة"),
("perte / rendement","الهدر / المردود"),
("méthode de pesage","طريقة الوزن"),
("méthode de boulette","طريقة الكُرَيّة"),
("méthode géométrique","الطريقة الهندسيّة"),
("poids du tracé (Petr)","وزن الرسم (Petr)"),
("poids des patrons (Pp)","وزن الباترونات (Pp)"),
("armure toile / sergée / satin","بنية السَّادة / التويل / الساتان"),
("essais (combustion, solubilité, réactif)","الاختبارات (الاحتراق، الذوبان، الكاشف)"),
("code international d'entretien","المدوَّنة الدوليّة للعناية"),
("sens chaîne / droit-fil","اتّجاه السَّدَى / استقامة خيط السَّدَى"),
("hauteur constante / en escalier","ارتفاع ثابت / متدرِّج على هيئة دَرَج"),
("épaulette","ساد الكتف"),
("cigare / cigarette (de tête de manche)","شريط أعلى الكمّ (المسمّى في الأصل سيجارًا/سيجارة)"),
("banane (de dos)","شريط الظهر المنحني"),
("feutre de col","لِبّاد الياقة"),
("triangle de poche","مثلّث الجيب"),
("languette","اللِّسان الصغير"),
("passement thermocollant","الشريط اللاصق حراريًّا"),
("ourlet / bas de veste","الحاشية المدورة / أسفل السترة"),
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
        if not (109 <= p["page"] <= 188):
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
    ex = f"work/{os.environ.get('TAG', 'batch3')}_extra.json"
    if os.path.exists(ex):
        for e in json.load(open(ex)):
            if e["id"] in extra_ids:
                continue
            rows.append([str(e["page"]), f"{e['id']} (صورة مستعادة)",
                         "لا نصّ: أيقونة/عنصر زخرفة صغير ملحق بإطار الصفحة",
                         "فُحصت على ورقة تلامس فتبيّن أنّها بلا محتوى؛ لم تُدرَج في المتن"])
    rows.sort(key=lambda r: (int(r[0]), str(r[1])))
    head("الملحق (أ) — النصوص الواردة داخل الصور ولوحات الأصل (الدفعة الثالثة: ص109–188)")
    P("تضمّ هذه القائمة كلّ نصّ داخل صورة أو لوحة مصوَّرة في صفحات الأصل 109–188: أشرطة رؤوس البطاقات، وجداول القطع "
      "برسوم «Schématisation»، وبطاقتا السلسلة العملياتيّة وخطّ التجميع برموز الآلات والغرز، ولوحتا المجموعة الموسميّة، "
      "وصور خطوات الكَيّ، وصفحة جرد القطع ومقاطع الإخراج ولوحات التفاصيل (ص171–176)، وشبكة التقويم، وشريط عنوان "
      "«ANNEXE A». وما كان من تسمية شكل مدرجة في طبقة النصّ فقد تُرجم تحت الصورة نفسها في المتن. والرسوم التي لا تحتمل "
      "الفصل عن أصلها (جداول مرسومة باليد) نُقلت صورةً كاملة، وذكرنا ذلك بدل تخمين قيمها.", size=12)
    add_table(rows, header="صفحة الأصل||الصورة / اللوحة||النصّ كما ورد في الأصل||الترجمة العربية والموضع", fontsz=9)

    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    head("الملحق (ب) — ملاحظات المترجم والتصحيحات والبنود التي تحتاج تأكيدًا (الدفعة الثالثة)")
    for i, n in enumerate(NOTES, 1):
        P(f"{i}- {n}", size=13)

    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    head("الملحق (ج) — مسرد مصطلحات الدفعة الثالثة (خطّ التجميع، البطاقات، المجموعة، الكَيّ، التحمُّلات)")
    P("يُضاف هذا المسرد إلى مَسارد الدفعات الأخرى؛ وهو مستمدّ من الفصل الثالث (توحيد خطّ سترات الرجل) في صفحات الأصل "
      "109–188: جداول القطع، والسلسلتان العملياتيّة والتجميعيّة، والمجموعة الموسميّة، وتقنيات الكَيّ، ودراسة الحالة، "
      "والتحمُّلات، وتمارين عدد الأمتار. وقد ثُبِّتت المصطلحات بتاريخ 4 نوفمبر 2026 فأصبحت نهائيّة.", size=12)
    P(CONFIRM, size=11, color="C00000")
    add_table([[fr, ar] for fr, ar in GLOSS_EXTRA], header="الفرنسية||العربية", fontsz=11)
