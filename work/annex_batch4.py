# -*- coding: utf-8 -*-
"""Annexes du lot 4 (pages PDF 189–243 : fin Annexe A, Annexe B, LES DOUBLURES, catalogue
fournitures, planches, glossaire, listes de figures/tableaux)."""
import os, json

CONFIRM = ("اعتُمدت المصطلحات الآتية نهائيًّا في كامل الدليل (بطلب من صاحب الملف وتثبيتِه بتاريخ 4 نوفمبر 2026) "
           "ولا تُغيَّر في أي موضع من الدفعات الأربع: veston/paletot = ستر الرجل · matelassage = الفِرش · "
           "découpage = التقطيع · thermocollage = اللّصق الحراري · gamme de montage = خطّ التجميع · "
           "gamme opératoire = السلسلة العملياتية · triplure = الحشوة الوسطى · doublure = البطانة · "
           "entoilage/garniture = الحشو · parementure = الحاشية الداخلية · passepoil = الحاشية الضيّقة · "
           "banane = الشريط المنحني · feutre/feutrine = اللِّبّاد · surfil = التغبير · "
           "boutonnière = شقّ الزرّ · pressing = الكبس · laize = عَرض القماش (بالمتر) · tolérance = تحمُّل · "
           "stagiaire = متربص · stage = تربص · maître de stage / tuteur = مرشد التربص · convention de stage = اتفاقية التربص · "
           "encadrement = التأطير · rapport de stage = تقرير التربص · évaluation = تقييم · ressources humaines = الموارد البشرية.")

CONFIRM_NOTE = ("تثبيت المصطلحات: بموافقة صاحب الملف بتاريخ 4 نوفمبر 2026 اعتُمدت مصطلحات veston/paletot (ستر الرجل)، "
                "matelassage (الفِرش)، découpage (التقطيع)، thermocollage (اللّصق الحراري)، gamme de montage (خطّ التجميع)، "
                "gamme opératoire (السلسلة العملياتية)، triplure (الحشوة الوسطى)، doublure (البطانة)، laize (عَرض القماش بالمتر) "
                "نهائيةً في كامل الدليل، وحُسمت الوحدة في «laize 1,50 cm» (ص177) و«laize 0,90 cm» بصوابها بالمتر (m) لا السنتيمتر. "
                "أمّا البنود التي لم تُحسَم لأنها أخطاء في الأصل لا مصطلحات (اختلاف العملة € / D في ص227–228، العدد «00» للقطعة 16 في ص122، "
                "القطعة 45 بلا تسمية في ص129، الغرزة «30» بدل «301» في ص144–146، التحمّلات «+45 م / +85 م / +115 م» في ص194، "
                "تعارض ترقيم بطاقات ص204–205 مع جداول ص110–111) فقد أبقيناها كما وردت في الأصل مع ملاحظة المترجم، "
                "وهي تنتظر قرار المؤسسة؛ وكُلُّها مفصَّلة في ملف «تعليمات_التعديل.txt» المرفق مع التسليم.")

MANUAL = [
(189,"p189_r1","Aucun texte (pictogramme 3D : personnage tenant un chronomètre)",
 "لا نصّ داخل الصورة؛ نصّ التمرين «Reliez chaque phrase avec la réponse qui convient» في طبقة النصّ، والأصل لا يرسم خطوط الوصل"),
(190,"p190_r1 (رأس الجدول)","Nom de la table | Rôle de la table","اسم الطاولة | دور الطاولة (الجداول السّتّة معادة البناء في المتن)"),
(191,"p191_r1","Aucun texte (pictogramme : femme et ampoule)","لا نصّ داخل الصورة (أيقونة زخرفية)"),
(192,"p192_r1 / p192_r2 / p192_r3","Photos de défauts de fil (seda/trame) — sans légende imprimée",
 "صور عيوب الخيوط بلا تسمية مطبوعة؛ التسميات في المتن من طبقة النصّ"),
(193,"p193_r3","Trois échantillons (trou, flèche de sens, accroc) — sans texte","ثلاث عيّنات (ثقب، سهم اتّجاه، تمزّق) بلا نصّ"),
(194,"p194_r1 … p194_r4","Photo de tache circulaire ; rouleau de tissu avec gros plan ; mètre-ruban et feuille ; étoffage sur table",
 "صور فوتوغرافيّة مرافقة للعيوب 5–7 بلا نصّ داخلي؛ التعليقات في المتن"),
(195,"p195_r1 (عنوان البطاقة)","Recherche du métrage du tissus — Laize: 0,90m – Longeur: 2,59m",
 "البحث عن عدد أمتار القماش — العرض 0,90 م — الطول 2,59 م («Longeur» خطأ مطبعي في Longueur، و«tissus» بصيغة الجمع)"),
(196,"p196_r1 (عنوان)","Recherche du métrage de la doublure — Laize: 0,90m – Longeur: 1,29m",
 "البحث عن عدد أمتار البطانة — العرض 0,90 م — الطول 1,29 م"),
(197,"p197_r1 (عنوان)","Recherche du métrage de la triplure taille 44 — Laize: 1,50m – Longeur: 0,82m",
 "البحث عن عدد أمتار الحشوة الوسطى مقاس 44 — العرض 1,50 م — الطول 0,82 م (العرض هنا 1,50 م بينما اعتمدت اللوحتان السابقتان 0,90 م)"),
(198,"p198_r1","Aucun texte (pictogramme : ampoule dans un nuage)","لا نصّ داخل الصورة (أيقونة زخرفية)"),
(200,"p200_r1","Bonne longueur | Trop courte | Trop longue — Longueur de la manche | Largeur de la veste",
 "طول جيّد | قصير جدًّا | طويل جدًّا — طول الكمّ | عرض السترة (ستّ صور توضيحيّة لطول الكمّ وعرض السترة)"),
(200,"p200_r4","Trois vestons illustrés, sans texte","ثلاث سترات مرسومة بلا نصّ (مقارنة اتّساع الردّادة)"),
(201,"p201_r2","Plis inclinés dans le revers :","طَيّات مائلة في الردّادة:"),
(201,"p201_r3","REVERS (dessin de revers hachuré)","الردّادة (رسم تخطيطيّ مُظلَّل بكلمة REVERS)"),
(202,"p202_r1","Aucun texte (pictogramme : main tenant un trophée)","لا نصّ داخل الصورة (أيقونة)"),
(203,"p203_r1 (بطاقة كاملة)","Gamme de montage de la manche tailleur — N° | Opération | Schémas | Equipements — 01 Executer les fausses boutonnières sur les dessus manches (MU) — 02 Former le coin en anglais sur le bas du dessus de manche et piquer (MU) — 03 Plier le rectangle du bas du dessous de manche et piquer l'extrémité de la manche — 04 Repasser les coutures coin manche du dessus manche et bas du dessous manche (Fer à vapeur) — 05 Piquer le dessus et le dessous manche (couture coude) à 1cm et faire un point d'arrêt sur la première boutonière (MU) — 06 Fermer coutures coude doublure à 1cm (MU) — 07 Fermer le bas de manche doublures + Tissu (MU) — 08 Fermer la couture saignée tissu et doublure et laisser une ouverture saignée doublure (MU) — 09 Repasser les coutures saignées, coude et bas de manche (Fer à vapeur)",
 "خطّ تجميع كمّ التايلور — ت | العملية | المخطّط | التجهيز — 01 إنجاز الشقوق الكاذبة على قطعتَي أعلى الكمّ (آلة عامة) — 02 تكوين زاوية «الإنجليزي» في أسفل أعلى الكمّ وخياطتها (آلة عامة) — 03 طيّ المستطيل في أسفل أسفل الكمّ وخياطة طرف الكمّ — 04 كيّ خياطات زاوية الكمّ (مكواة بخار) — 05 خياطة أعلى الكمّ وأسفلّه معًا (خياطة المِرفق) على 1 سم مع غرزة إيقاف عند الشقّ الأوّل — 06 إغلاق خياطتَي مِرفق البطانة على 1 سم — 07 إغلاق أسفل الكمّ (البطانة + القماش) — 08 إغلاق خياطة الحاشية المعلَّقة (saignée) للقماش والبطانة مع ترك فتحة في حاشية البطانة — 09 كيّ خياطات الحاشية المعلَّقة والمِرفق وأسفل الكمّ (مكواة بخار). الجدول المعرَّب الكامل في المتن (ص203)"),
(204,"p204 (بطاقة 18 صفاً)","Tissu : 01 DEVANT … 18 TIRETTE — Doublure : 01 … 11 — Triplure : 01 … 20 (ص205)",
 "أُعيد بناء الجداول الثلاثة كاملةً في المتن (صفحات 204–205) بنفس ترتيب الأصل وأرقامه، مع تسجيل الأخطاء الواردة فيه"),
(206,"p206_r1","Gamme de montage poche appliquée — N | DESIGNATION | D'OPERATION | SCHEMAS OU SECTIONS | REPRESENTATION A PLAT — 01 Préparer le rentré de la poche en le repassant — 02 Exécuter ourlet de la poche — 03 Plaquer la poche sur vêtement",
 "خطّ تجميع الجيب المُلبَّق — ت | التسمية | العملية | المخطّطات أو المقاطع | التمثيل المسطّح — 01 تجهيز طِيّة الجيب الداخلية (rentré) بكيّها — 02 إنجاز حاشية الجيب المدورة (ourlet) — 03 إلباق الجيب على اللباس (plaquer). الجدول المعرَّب في المتن"),
(207,"p207_r1 (جرد تسمية)","Nomenclature de la veste croisée — RP | NP | DESIGNATION | MATIERE | RENSEIGNEMENT — 44 15 BOUTONS PLASTIQUE MARRON — 43 PAIRE EPAULETTE FEUTRINE GRIS — 42 PLASTRON TOILE TAILLEUR BEIGE — 41 CIGARE — 40 DESSOUS DE COL FEUTRINE GRIS — 39→25 TRIPLURE … TOILE COLLANTE NOIR — 24→13 TIRETTE / SAC DE POCHE … / DOUBLURE … TAFFETA MARRON — 12→01 PASSE POILE … / PATTE POCHE FOITRINE / RABAT POCHE COTE / BANANE / DESSUS DE COL / DESSOUS DE MANCHE / DESSUS DE MANCHE / PARMENTURE DU DEVANT / PETIT COTE / DOS / DEVANT — Echelle | C.F.P.A Soumaa-C.F.P.A Tigzirt | CHAIB CH & LOUNIS B | Habillement 2018-2019",
 "جدول جرد تسمية السترة المزدوجة الأزرار (44 صفاً) أُعيد بناؤه كاملاً في المتن مع ترجمة كل تسمية؛ العمودان «المادة» و«البيان» مدموجتان على نطاقات صفوف في الأصل (بلاستيك 44، لِبّاد 43 و40، قماش تايلور 42–41، قماش لاصق 39–25، تفتاه 24–13، ترغال 12–01). أسماء المؤسّسات والمُعدِّين تُترك كما هي"),
(208,"p208_r1","S-A-A | S-B-B | S-C-C avec renvois numérotés 01 à 40",
 "ثلاثة مخطّطات مقطعيّة للعناصر المُخرَجة بعناوين مقاطع (S-A-A، S-B-B، S-C-C) مع أرقام إحالية على القطع من 01 إلى 40 (بلا نصّ آخر)"),
(210,"p210_r1 (عنوان)","Recherche du métrage du tissus (étude de cas) taille 48 — Laize: 1,50m – Longeur: 1,60m",
 "البحث عن عدد أمتار القماش (دراسة حالة) مقاس 48 — العرض 1,50 م — الطول 1,60 م؛ تسميات القطع: Dos, Devant, Dessous manche, Dessus manche, Petit Côté, Garniture, Dessus Col, Rabat, Banane, PAR P.Poitrine, PAR P.Côté, PAR P.P.S, P.P.F, D.F (اتّجاه خيط السَّدَى)"),
(210,"p210_r1 (ملاحظة)","Un des blocs est libellé «Garniture T44» alors que la planche est annoncée taille 48",
 "إحدى القطع في لوحة مقاس 48 مكتوبة «Garniture T44» (مقاس 44)؛ أُبقيت كما في الأصل مع هذا التنبيه"),
(211,"p211_r1 (عنوان)","Recherche du métrage de la doublure (étude de cas) taille 44 — Laize: 1,50m – Longeur: 1,25m",
 "البحث عن عدد أمتار البطانة (دراسة حالة) مقاس 44 — العرض 1,50 م — الطول 1,25 م؛ والباترونات داخل اللوحة كلّها موسومة بـ T48"),
(211,"p211_r2 (عنوان)","Recherche du métrage de la triplure (étude de cas) taille 48 — Laize: 1,50m – Longeur: 0,90m",
 "البحث عن عدد أمتار الحشوة الوسطى (دراسة حالة) مقاس 48 — العرض 1,50 م — الطول 0,90 م"),
(213,"p213_r1","Planche identique à p210 (texte et cotations compris)","اللوحة مطابقة حرفيًّا للوحة ص210 (العنوان والتسميات والأرقام)؛ تكرار في الأصل"),
(214,"p214_r1 / p214_r2","Planches identiques à p211_r1 et p211_r2","اللوحتان مطابقتان حرفيًّا للوحتَي ص211 (البطانة والحشوة الوسطى)؛ تكرار في الأصل"),
(217,"p217_r1 (عنوان)","Recherche du métrage Tissu (Imbrication de deux tailles 44 et 48) — Laize: 1,50m – Longeur: 3,29m",
 "البحث عن عدد أمتار القماش (تداخُل مقاسَين 44 و48) — العرض 1,50 م — الطول 3,29 م؛ القطع البنفسجيّة T44 والأخرى T48، منها Devant Supérieur, Devant Inferieur, Dos, Dessus manche, Petit coté, Col, Poche américaine, Garniture"),
(218,"p218_r1 (عنوان)","Recherche du métrage de la doublure (Imbrication de deux tailles 44 et 48) — Laize: 1,50m – Longeur: 2,60m",
 "البحث عن عدد أمتار البطانة (تداخُل مقاسَين 44 و48) — العرض 1,50 م — الطول 2,60 م"),
(219,"p219_r1 (عنوان)","Recherche du métrage de la triplure (Imbrication de deux tailles 44 et 48) — Laize: 1,50m – Longeur: 1,68m — Poche américaine | P.P.S | P.P.C",
 "البحث عن عدد أمتار الحشوة الوسطى (تداخُل مقاسَين 44 و48) — العرض 1,50 م — الطول 1,68 م، مع تسميات مختصرة: جيب أمريكي (Poche américaine)، P.P.S (حاشية ضيّقة لجيب الصدر)، P.P.C (حاشية ضيّقة للجيب الجانبي)"),
(221,"p221_r1 (Annexe B)","Annexe B — Objectifs intermédiaires | Critères particuliers de performance | Eléments de contenu — LES SPESIFICATION DE LA PREPARATION DE VESTON / DEROULEMENT DES ETAPES DE FABRICATION / APPLICATION DE LA GAMME DE MONTAGE",
 "الملحق (ب): المحاور | الأهداف الوسيطة | معايير الأداء الخاصّة | عناصر المحتوى؛ «SPESIFICATION» خطأ مطبعي في SPÉCIFICATION. الجدول المعرَّب الكامل في المتن (ص221)"),
(222,"p222_r1","Tissé | Maille — Le tissu doublure «chaîne et trame» est plus rigide… plus souple","منسوج | محبوك — العمودان مترجمان في جدول المتن"),
(223,"p223_r1 (جدول)","NOM | CARACTERISTIQUES | ECHANTILLON | ENTRETIEN — Cupro / Acétate / Soie / Crêpe de chine / Crêpe satin / Crêpe Georgette / Élasthanne / Satin",
 "الاسم | الخصائص | العيّنة | العناية — ثمانية أصناف من بطانات المنسوج؛ ترجمة الخصائص في جدول المتن، وعمود «العيّنة» صور بلا نصّ وعمود «العناية» فارغ في الأصل"),
(224,"p224_r1 (جدول)","Taffetas / Sergé / voile de soie — descriptions — «Le taffetas est un tissu précieux et coûteux… Il est utilisé pour la confection des doublures de vestes et manteaux»",
 "تفتاه — أميرّية (sergé) — حرير رقيق؛ التعريفات مترجمة في المتن. عمود «العناية» في الأصل فارغ"),
(225,"p225–p226 (نصّ فقط)","Vêtement d'hiver / d'été / de luxe / sportif / pour l'ameublement — grammages et compositions (150 g/m², 100 g/m², 90 g/m²; 70% acétate 30% cupro; 53% cupro 47% acétate; 96% acétate 4% élasthanne; 75% triacétate 25% polyamide)",
 "ألبسة الشتاء / الصيف / الفخمة / الرياضيّة / أثاث المنزل مع الأوزان والتراكيب؛ مُترجَمة كاملة في المتن (ص225–226) — الأرقام كما هي"),
(227,"p227_r1 (NON TISSÉ)","Références | Laize | Coloris | Tarifs | Descriptifs — 968345 (Blanc) / 968347 (Gris anthracite) — 90 cm — 2,70 € le Mètre — Entoilage thermocollant léger/moyen/ferme — fixage source de chaleur (fer à repasser 130° / 145° avec pression et vapeur) — Composition : Fibres polyester, polyamide",
 "غير منسوج: المرجع | العرض | الألوان | الأسعار | الأوصاف — المراجع 968345/968347/968348/968349/968350/968352، العرض 90 سم، الألوان أبيض ورمادي فحمي، الأسعار 2,70 € و2,60 € و2,50 € للمتر، شروط التثبيت 130°/145° مع ضغط وبخار، التركيب: ألياف بوليستر وبولي أميد (الجدول المعرَّب في المتن)"),
(228,"p228_r1 (TISSÉ)","1496G7 — 0,75 D le Mètre — RTB 35 — 1,99 D le Mètre — 366057 — 4,90 D le Mètre — conditions d'emploi: 130°/150° pendant 12 à 15 secondes",
 "منسوج: المرجع 1496G7 بسعر 0,75 د للمتر، RTB 35 بـ1,99 د، 366057 بـ4,90 د؛ شروط الاستعمال 130°/150° مدّة 12 إلى 15 ثانية. الأسعار هنا بالدِينار (D) بينما هي في ص227 باليورو (€) — خطأ عملة يحتاج تصحيحًا من المؤسسة"),
(229,"p229_r1 / p229_r2","LA GAMME DE COLORES DES TISSU — nuancier en roue d'échantillons sans légende",
 "ترويسة: «مجموعة ألوان الأقمشة» (والصواب COLORIS)؛ واللوحة عجلة ألوان من عيّنات قماش مرتَّبة نجمةً بلا نصّ"),
(230,"p230_r1 / p230_r2","MATIERE SECONDAIRES ET ACCESSOIRES — Plastron | Feutrine | Toile collante (échantillons sur schéma de veston)",
 "ترويسة: «الموادّ الثانويّة والتوابع» (والصواب MATIÈRES SECONDAIRES)؛ واللوحة مخطّط لجزء من السترة عليه عيّنات مسمّاة: الصّدريّة (Plastron)، اللِبّاد (Feutrine)، القماش اللاصق (Toile collante)"),
(231,"p231_r1 / p231_r2","DEMINITION DES TAILLES (DROP) — 50 CM — DROP 6 pour une taille 50 — DROP 8 pour une taille 50",
 "ترويسة: «تحديد المقاسات (القوام)» (والصواب DÉFINITION)؛ ورسمان يقيسان 50 سم مع قوام DROP 6 وقوام DROP 8 لمقاس 50. ملاحظة: DROP 8 قيمة موجبة بينما النصّ يعرّف القوام بالفروق السالبة"),
(232,"p232 (نصّ فقط)","Le vêtement sportif / homme / pantalon — «Le pantalon se détermine par le demi-tour de poitrine»",
 "النصّ في طبقة النصّ ومُترجَم في المتن؛ العبارة عن السروال خاطئة وحدةً (الصواب محيط الخصر/الورك) وسُجِّلت"),
(233,"p233 (نصّ + أيقونات)","la réparation par DROP — CNM 2006 / CNM 2016 — DROP -2, DROP 0, DROP -2 — 0,15%…0,28%",
 "الجداول والنِّسب مُترجمة في المتن؛ «réparation» والصواب «répartition»؛ وDROP −2 ورد مرّتين والصواب في الثانية +2"),
(234,"p234_r1 / p234_r2","CORRESPONDANCE TAILLES FRANCAISES / ITALIENNES — «Les tailles que nous vous demandons d'indiquer sur le bon de commande sont les tailles françaises» — VESTES HOMME 44 46 48 50 52 54 56 / 46 48 50 52 54 56 58 — PANTALON HOMME 40 42 44 46 48 50 52 / 46 48 50 52 54 56 58 — VESTES FEMME 34 36 38 40 42 44 46 / 38 40 42 44 46 48 50 — PANTALONS FEMME idem — XS S M L XL XXL XXXL / XXS XS S M L XL XXL",
 "مقابلة المقاسات الفرنسية/الإيطالية — الجملة الحمراء: «المقاسات التي نطلب منكم بيانها في سند الطلبيّة هي المقاسات الفرنسية»؛ وأربعة جداول (سترات رجاليّة، سراويل رجاليّة، سترات نسائيّة، سراويل نسائيّة) أُعيد بناؤها في المتن (ص234) بنفس الصفوف والأعمدة"),
(235,"p235–p239 (مسرد)","Glossaire de la coupe et couture — Aisance, À même, Ampleur, Cintrer, Coupe à plat, Cran de montage, Cranter, Creuser, Croisure, Déplacement de pince, Droit-fil, Élargissements, Embu, Évaser, Fourche, Fronce, Galber, Godet, Gradation, Lisière, Modélisme, Montant, Monter, Moulage, Parementure, Patron de base, Patron du corsage de base, Patron sans pinces, Patron d'exécution/modèle, Patron sur mesure, Patron standard, Patronage, Pince, Perroquet ou pistolet, Platitude, Pli, Stylisme, Transformations — Termes utilisés : Spécifications, Caractéristique, Standard, Limites (tolérances)",
 "المسرد مُعرب بالكامل مع تعريفاته في متن هذا النطاق (ص235–238)، ثمّ «المستعمل من الألفاظ في المواصفات» (ص239)؛ مصطلحات التعريفات أُضيفت إلى المسرد العام في الملحق (ج)"),
(240,"p240–p243 (قوائم)","LISTE DE FIGURIENE CHAPITRE I | LISTE DE FIGURE CHAPITRE II | LISTE DE TABLEAU CHAPITRE I/II | LISTE DES TABLEAU CHAPITRE I-III | LISTE DES FIGURES CHAPITRE III | LISTE DES FICHER CHAPITRE 01",
 "قوائم الأشكال والجداول معربة بندًا بندًا في المتن (ص240–243) مع أرقام صفحات الأصل؛ العناوين فيها فيها أخطاء مطبعية (FIGURIENE، FICHER) وقد سُجِّلت"),
]

NOTES = [
"نطاق الدفعة الرابعة: صفحات PDF 189–243. تكملة «ANNEXE A» (تصحيحات تمارين الفصول الثلاثة والتمارين التركيبيّة) في ص189–220، ثمّ «ANNEXE B» (جدول الأهداف والمضامين ومعايير الكفاءة) في ص221، ثمّ فصل «البَطانات LES DOUBLURES» في ص222–226، ثمّ «CATALOGUE FOURNITURES THERMOCOLLANT» في ص227–228، ثمّ لوحات الألوان والموادّ الثانويّة وتحديد المقاسات (DROP) وجدول المقابلات الفرنسية/الإيطالية في ص229–234، ثمّ مسرد القصّ والخياطة وألفاظ المواصفات في ص235–239، وأخيرًا قوائم الأشكال والجداول في ص240–243.",
"الترقيم المطبوع في هذا النطاق رومانيّ بالكامل (III في ص189، IV في ص190، XI، XII… LIV في ص240 وما بعدها) لأنّ الملاحق تُفتتح بترقيم جديد؛ لذلك لا يُقارَن رقم صفحة PDF برقم الأصل بقاعدة ثابتة، وذُكر رقم صفحة الأصل عند كل صورة وجدول.",
"ص189: تمرين المطابقة «Reliez chaque phrase avec la réponse qui convient» بلا أيّ خطّ وصل مرسوم في الأصل، وبنية الصفحة مزّقت العمودين («le haut» و«paire» نزلا إلى السطر التالي). أعيد تركيب العبارات الأربع من تعريفات الفصل الأول، والزواج الواردة ليست مفتاح تصحيح مذكورًا في الأصل بل قراءة مترجِم؛ تحتاج تأكيد المؤسسة. الصورة الوحيدة في الصفحة أيقونة (شخص يحمل ساعة إيقاف).",
"ص190: جدول «طاولات الفرش وأدوارها» بستّة صفوف؛ رأساه «Nom de la table | Rôle de la table»، وقد أعيد بناؤه عربيًّا كاملًا.",
"ص191–194: عيوب القماش 1–7 مرفقة بصور فوتوغرافيّة لا تسميات لها في الأصل؛ أُدرِجت الصور في مواضعها مع تسمية عربيّة من صياغتنا موضّحة أنها ليست من الأصل.",
"ص194: أرقام التحمّل في البند 7 («+ 45 م»، «+ 85 م»، «+ 115 م») غير منطقية وحدةً؛ أُبقيت كما وردت.",
"ص195–198: لوحات حساب عدد الأمتار (توزيع الباترونات على الفرشة) مكتوبة بالكامل داخل الصور. العناوين فيها تحمل خطأين مطبعيَّين: «Longeur» بدل «Longueur»، و«du tissus» بصيغة الجمع. كما أنّ العرض المذكور يختلف بين اللوحات (0,90 م في ص195 و196، و1,50 م في ص197) مع أنّ الحسابات مبنية على عرض 0,90 م؛ أُبقيت العناوين كما هي مع هذا التنبيه.",
"ص197: الحسابات تكتب المقام «20,2» في معادلة الهدر مع أنّ وزن الباترونات 20,3 غ والمقام الصحيح هو وزن الرسم 23,8 غ؛ والنتيجة 14,70% محسوبة على 23,8 غ فهي صحيحة، والخطأ في كتابة المقام فقط. وفي ص197–198 تكرار/سقوط لأرقام الصفحات الرومانيّة (IX ثمّ IX ثمّ X…).",
"ص199: عنوان الفصل بلا إغلاق قوس: «CORRECTION DES EXERCICES CHAPITRE 2 (section 01»؛ وسطر «Complétez le vide par les mots qui convient :» يفتتح بنقطتين مكرّرتين في الأصل.",
"ص200: عبارة «la plus fomente» ليست فرنسيّة صحيحة؛ لعلّ الصواب «la plus fournie» أو «la plus brillante»؛ تُرجمت بحسب السياق مع التنبيه. كما أنّ الصورة الثانية (p200_r2) بلا نصّ، والصورة الرابعة (p200_r4) بلا تسمية.",
"ص201: الترويسة والصورة الأخيرة أيقونتان (علامة صحّ حمراء، شخصان يشيران) بلا محتوى نصّي؛ أمّا الرسم الموسوم «REVERS» فهو داخل الصورة.",
"ص202: عنوان الصفحة «CORRECTION DES EXERCICES CHAPITRE 01: EXCERCICEDE SYNTHESE» مع أنّ المضمون تصحيحات نهاية الفصل الثاني؛ و«EXCERCICEDE» مكتوبة بلا فصل. أُبقي رقم الفصل الصحيح (الثاني) في العنوان العربي وسُجِّل الخطأ.",
"ص203: ليست بطاقة التمرين التركيبي، بل بطاقة «خطّ تجميع كمّ التايلور» (Gamme de montage de la manche tailleur) بتسع عمليات؛ أُعيد بناؤها جدولا عربيًّا كاملا مع العمود «الرسم» مُحالًا إلى القصاصة. وفيها «Exécuter» بلا حرف «é»، و«la première boutonière» (والصواب boutonnière).",
"ص204–205: ثلاث بطاقات جرد (القماش 18 صفاً، البطانة 11 صفاً، الحشوة الوسطى 20 صفاً) معادة البناء عربيةً بنفس صفوف الأصل وأعمدته. أخطاء الأصل المُثبَتة: القطعة 13 والقطعة 15 تحملان العدد «05» بدل «01»؛ ظهر البطانة بقطعة واحدة (01) مقابل قطعتين في ص111؛ «Pate poche poitrine» والصواب Patte؛ «porte feuille» والصواب portefeuille؛ الصّفّان 19 و20 من بطاقة الحشوة مبتورا التسمية («Parementure poche» دون إتمام).",
"ص204–205 مقابل ص110–111: ترتيب القطع يختلف بين بطاقة الملحق وجدول الفصل الثالث، وعدد القطعة 13 مختلف؛ كلاهما نُقل كما ورد، والتوفيق بينهما يحتاج قرار المؤسسة.",
"ص206: بطاقة «خطّ تجميع الجيب المُلبَّق» بثلاثة صفوف مع أعمدة «DESIGNATION | D'OPERATION | SCHEMAS OU SECTIONS | REPRESENTATION A PLAT»؛ أُعيد بناؤها عربيًّا، ورؤوس الأعمدة الأصلية مترجمة في الملحق (أ).",
"ص207: صفحة كاملة صورةٌ واحدة (جرد تسمية السترة المزدوجة الأزرار، 44 صفاً مع رسمين)؛ أُعيد بناء الجدول كاملاً في المتن، وخلايا «المادة/البيان» المدموجة أُعيدت قيمتها في كل صفّ لتسهيل القراءة. العناوين داخل الصورة: «Echelle | Nomenclature de la veste croisée | C.F.P.A Soumaa-C.F.P.A Tigzirt | CHAIB CH & LOUNIS B | Habillement 2018-2019».",
"ص208: ثلاثة مخطّطات مقطعيّة (S-A-A، S-B-B، S-C-C) بأرقام إحالية 01–40 بلا نصّ آخر؛ أُبقيَت كقصاصة لأنّ الأرقام تُقرأ من الرسم وحده.",
"ص209: هدر القماش مكتوب 6,66% والصواب 6,67% (1,4 ÷ 21 × 100)، وهدر الحشوة الوسطى مكتوب 7,94% والصواب 7,65% (0,91 ÷ 11,9 × 100)؛ أمّا هدر البطانة 6,47% فسلامٌ من الحساب (1,26 ÷ 19,46 × 100 = 6,47%). أرقام الأصل مُبقاة كما هي مع ذكر التصحيح هنا.",
"ص210: «المردود = 100 − 7,94 = 92,36» لا يستقيم (الصحيح 92,06؛ أو 92,35 إذا اعتمدنا الهدر 7,65%). أُبقي الرقم مع التنبيه.",
"ص210–211 مقابل ص213–214: اللوحات الأربع مكرّرة حرفيًّا في الصفحتين؛ أُبقيت الصفحات المكرّرة مع تسمية صريحة بالازدواج بدل حذفها، حفاظًا على تطابق عدد الصفحات مع الأصل.",
"ص211: لوحة البطانة مُوسومة «taille 44» مع أنّ كل القطع داخلها مكتوبة T48؛ كما أنّ لوحة الحشوة الوسطى تجمع مقاس 48 وعرضًا من 0,90 م دون بيان ذلك في النصّ. أُبقيت كما وردت.",
"ص215 و220: الصفحتان متطابقتان حرفيًّا (6,25% و8,33% و6,62%) مع كتابة رمز وزن الرسم «Ptr» بدل «Petr»، وقسمة هدر البطانة على 38,5 (وزن الباترونات) بدل 42 (وزن الرسم) مع أنّ النتيجة 8,33% محسوبة على 42. أُبقيت الصفحتان مع هذا التنبيه.",
"ص216: الصفحة تحمل ملاحظة واحدة («L’imbrication des tailles est plus avantageuse pour le rendement de matière») وقد أُدرجت في المتن كما هي.",
"ص217–219: لوحات تداخُل مقاسَين (44 و48) بأطوال مختلفة (3,29 م للقماش، 2,60 م للبطانة، 1,68 م للحشوة) على عرض 1,50 م؛ العنوان في ص217 يخلط بين «tissus» و«Taille» و«Imbrication» بحروف كبيرة وصغيرة بلا قاعدة، و«Longeur» خطأ مطبعي. في ص219 تُستعمل اختصارات غير مشروحة في الأصل: P.P.S وP.P.C وRabat T48.",
"ص221 (ANNEXE B): الجدول ثلاثة أعمدة («Objectifs intermédiaires | Critères particuliers de performance | Eléments de contenu») وعنوانه داخل شريط أزرق؛ العمود الأوّل يحمل عنوان المحور نفسه؛ و«LES SPESIFICATION DE LA PREPARATION DE VESTON» فيه خطأ مطبعي (SPESIFICATION) وغياب الجمع. أُعيد بناء المضامين عربيًّا مع الإحالة إلى القصاصة.",
"ص222–226 (LES DOUBLURES): عناوين الفرع غير موحّدة في الأصل: «I.1.1 :», «I-1-3», «I-1-4 :», «I.1.5:»؛ وحّدناها في العربية إلى مستوى واحد (H2) ليعمل جدول المحتويات، وسُجِّل الاختلاف. كما أنّ عمود «ENTRETIEN» في جداول ص223–224 فارغ في الأصل، وعمود «ECHANTILLON» صور بلا نصّ.",
"ص227 مقابل ص228: الأسعار في ص227 باليورو (2,70 € / 2,60 € / 2,50 € للمتر) وفي ص228 بـ«D» (0,75 D / 1,99 D / 4,90 D)؛ لا يمكن أن يكون الفهرس بعملة واحدة وأخرى بأخرى، وهي نقطة تحتاج تصحيحًا من المؤسسة. كذلك عناوين الجدولين «NON TISSE» و«TISSÉ» بلا تشكيل موحّد.",
"ص229–231: ترويسات داخل الصور بأخطاء إملائية: «LA GAMME DE COLORES DES TISSU» (والصواب COLORIS)، «MATIERE SECONDAIRES ET ACCESSOIRES» (والصواب MATIÈRES SECONDAIRES)، «DEMINITION DES TAILLES (DROP)» (والصواب DÉFINITION). وقد تُرجمت الترويسات مع ذكر الصواب تحت كل صورة.",
"ص231: الرسمان يقدّمان «DROP 6» و«DROP 8» بقيمة موجبة لمقاس 50، بينما النصّ (ص232) يعرّف القوام بالفرق الناقص (−6)؛ التناقض في الأصل وأُبقي مع التنبيه.",
"ص232: «pour les bas: le pantalon = ½ tour de poitrine» خطأ في الأصل (الصواب محيط الخصر أو الورك)؛ تُرجم كما ورد مع ذكر الصواب في ملاحظة المترجم.",
"ص233: «la réparation par DROP» والصواب «la répartition»؛ والمرجع مكتوب «CNM 2006» في العنوان و«CNM 2016» في سطر «INFORMATION»؛ وسطر DROP الأخير مكرر («−2» بعد «0»)؛ ومجموع النِّسب 100,29% بدل 100%. جميعها مُبقاة كما وردت مع التصحيحات في ملاحظات المترجم.",
"ص235–238 (المسرد): العنوان بالحروف الحمراء الكبيرة (18pt) والتعريفات بخطّ عادي؛ ترتيب المداخل أبجديّ مع اختلال في الأصل (مثلا «A- Même» بعد «Aisance»، و«Pince» قبل «Perroquet ou pistolet» في ترتيب الحروف)، وفيه مداخِل بلا تعريف («Patron d'exécution») مع قفزة ترقيم (XLVII→XLIX). أعيدت المداخل بترتيب الأصل مع ترجمتها كاملة.",
"ص239 (Termes utilisés): أربعة تعريفات (Spécifications / Caractéristique / Standard / Limites) مع قوائم نقطية؛ تُرجمت كما هي. مثال «Standard» في الأصل يذكر «les vêtements de travail (médecins, pompiers, les laboratoires chimistes) — les parachutes» دون إتمام الجملة.",
"ص240–243 (قوائم الأشكال والجداول): القوائم في الأصل غير مكتملة الترقيم ولا تشير إلى أرقام صفحات PDF بل إلى الترقيم المطبوع القديم؛ وفيها: «LISTE DE FIGURIENE» (والصواب DES FIGURES)، الشكل الأوّل من الفصل الثاني مرقّم «Figure 013»، والشكل 04 مكرر مع 03 قبله، و«FIG64» بلا نقطة، و«LISTE DES FICHER CHAPITRE 01» (والصواب FICHES)، وقوائم الفصل الثاني تنتقل من XVIII إلى XIX ثم تعيد XIX. أُعيدت البنود كاملة في جداول عربيّة مع صفحة الأصل كما وردت.",
"لم تُرقَّم الأشكال في المتن العربي بأرقام جديدة داخل هذه القوائم (لأنّ الأصل يدرجها في نهاية الدليل)، ولذلك بقيت الأرقام كما في الأصل تمامًا. ومن يريد تحديث القائمة لتتوافق مع أرقام الأشكال المعتمدة في الأجزاء المترجمة (I.nn، II.nn، III.nn) فليُبلّغ لتُعاد صياغتها.",
"الصور المستعادة: في ص197 و198 و201 و215 و233 أعاد المستخرِج إدراج 16 صورة صغيرة كانت تلتصق بشريط الزخرفة الجانبي؛ فُحصت جميعًا على ورقة تلامس فتبيّن أنها أيقونات زخرفية (مربّعات ومصابيح وأشرطة ألوان) بلا أيّ نصّ، ولذلك لم تُدرَج في المتن، وسُجِّل ذلك هنا حتى لا تُتجاوز هذه الصور بصمت.",
"بلا قصاصات: الصفحات 199، 204، 205، 209، 212، 215، 216، 220، 225، 226، 232، 233 و235–243 لا تحتوي صورًا في الأصل ضمن هذه المعالجة (نصٌّ فقط أو جداول نصّية)، فجاءت مترجمةً نصًّا وجداولَ حقيقيّة.",
"تنسيق الدفعة الرابعة: 55 صفحة من الأصل (189–243) أُدرجت كل واحدة منها في صفحة مستقلة، مع 53 قصاصة عالية الدقة بالحجم الأصلي دون تغيير النسبة، و24 جدولًا عربيًّا معاد البناء بنفس صفوف الأصل وأعمدته واتّجاه RTL (منها جداول 44 صفا و20 صفا و18 صفا)، ومسرد بـ40 مدخلًا، وقوائم الأشكال والجداول (155 بندًا) في جداول رباعية/ثنائية.",
]
NOTES.append(CONFIRM_NOTE)

GLOSS_EXTRA = [
("aisance","هامش الراحة"),
("à même (coupé à même)","مقطوع في القِطعة نفسها"),
("ampleur","السَّسَعة"),
("cintrer","تخصير اللباس"),
("coupe à plat","القصّ المسطّح"),
("cran de montage","علامة الوصل (عقدة التجميع)"),
("cranter","تكريش الحافة (شقوق صغيرة)"),
("creuser","تعميق الكَسرة أو الفتحة"),
("croisure","زائدة التداخل (شريط الأزرار)"),
("déplacement de pince","نقل الكَسرة"),
("droit-fil","خيط السَّدَى (اتّجاه السَّدَى)"),
("largeur utile / laize","العرض النافع (عرض القماش)"),
("élargissements","التوسيعات"),
("embu","امتلاء رأس الكمّ"),
("évaser","التوسُّع (توسعة الأسفل)"),
("fourche / enfourchure","الفُرجة (بين الساقين)"),
("fronce","الكرشة / التشريط"),
("galon","الحاشية الزخرفية (الشرائط)"),
("galber","تقويس الخطّ / التدوير"),
("godet","الجيب المُذنَّب (التوسيع الدائري)"),
("gradation","التدرّج بين المقاسات"),
("lisière","حاشية القماش (غير المتنسّلة)"),
("modélisme","تصميم الأزياء/النمذجة"),
("montant","الارتفاع (من الخصر إلى الفُرجة)"),
("monter (une manche)","تركيب (الكمّ)"),
("moulage","التنمير على تمثال الخياطة"),
("parementure","الحاشية الداخلية"),
("patron de base","الباترون الأساسيّ"),
("patron sans pinces","باترون الجذع بلا كَسرات"),
("patron d'exécution / patron modèle","باترون التنفيذ / الباترون النموذج"),
("patron sur mesure","الباترون على القياس"),
("patron standard","الباترون القياسي"),
("patronage","علم الباترون"),
("pince","الكَسرة"),
("perroquet / pistolet","الببّغاء/المسدّس (أداة رسم المنحنيات)"),
("platitude","الاستواء"),
("pli","الطِيّة"),
("stylisme","تصميم الأزياء (الرسم)"),
("transformations","التحويرات"),
("valeur de couture","قيمة الخياطة (هامش الخياطة)"),
("doublure","البطانة"),
("tissu de doublure","قماش البطانة"),
("entoilage / triplure","الحشو / الحشوة الوسطى"),
("thermocollant / thermocollage","اللاصق حراريًّا / اللّصق الحراري"),
("toile tailleur","قماش تايلور (الحشو البنيوي)"),
("feutre / feutrine","اللِبّاد"),
("plastron","الصّدريّة"),
("épaulette","وسادة الكتف"),
("saignée","الحاشية المعلَّقة (خياطة saignée)"),
("coin anglais","زاوية «الإنجليزي» في أسفل الكمّ"),
("fausse boutonnière","الشقّ الكاذب"),
("ourlet","الحاشية المدورة (الأورلة)"),
("plaquer (une poche)","إلباق الجيب"),
("rentré","طِيّة الحافة الداخلية"),
("garniture","الحشوة (التبطين الخفيف)"),
("cupro","الكوبرو (حرير بامبرغ)"),
("acétate","الأسيتات"),
("crêpe de chine","الكريب الصيني"),
("crêpe Georgette","كريب جورجيت"),
("élasthanne (stretch)","المِرْن (المطّاط)"),
("satin duchesse","ساتان دوشِس"),
("triacétate","ثلاثي الأسيتات"),
("antistatique","مضادّ الكهرباء الساكنة"),
("East-care","معالجة East-care (عدم التجعّد)"),
("grammage","الوزن النسيجي (غ/م²)"),
("imbrication des tailles","تداخُل المقاسات في الفرش"),
("recherche du métrage","البحث عن عدد الأمتار"),
("rendement / perte","المردود / الهدر"),
("spécification","مواصفة"),
("caractéristique","خاصّة"),
("standard","معيار مرجعي"),
("limites / tolérances","الحدود / التحمّلات"),
("grille d'évaluation formative","شبكة التقييم التكويني"),
("bon de commande","سند الطلبيّة"),
("nuancier (gamme de coloris)","لوحة الألوان"),
("drop (morfologie du torse)","القوام (DROP)"),
("taille commerciale","المقاس التجاريّ"),
("mesures anthropométriques","القياسات الجسديّة (أنثروبومتريّة)"),
("campagne nationale de mensuration","الحملة الوطنيّة للقياس"),
("hauteur du dos","طول الظهر"),
("emmanchure","فتحة الكمّ"),
("encolure","فتحة العنق"),
("petit côté","الحاشية الجانبية الصغيرة"),
("banane","الشريط المنحني (الموزيّ)"),
("patte de poche","لِسان الجيب"),
("rabat","لِسنة الجيب"),
("passepoil / passé-poil","الحاشية الضيّقة"),
("tirette","اللِّسان (الساحب)"),
("sac de poche","كيس الجيب"),
("fond de poche","قعر الجيب"),
("nomenclature","جرد التسمية"),
("échantillon","عيّنة"),
("tarif / prix au mètre","السعر / سعر المتر"),
("laize 90 cm / 1,50 m","عرض 90 سم / 1,50 م"),
("références (catalogue)","المراجع الرقميّة في الفهرس"),
]


def build(doc, blocks, LINEBY, FIGDIR, REG, P, add_table, add_picture, shade, rtl_paragraph,
          WD_ALIGN, Pt_, Cm_, RGB_, WD_BRK):
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
    def head(text, style='Heading 1'):
        h=doc.add_paragraph(style=style); rtl_paragraph(h); h.add_run(text)
        doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    rows=[]
    pages=[p for p in blocks["pages"] if 189<=p["page"]<=243]
    for pg, sup, fr, ar in MANUAL:
        rows.append([str(pg), sup, fr, ar])
    extra_ids=set()
    for pg, sup, fr, ar in MANUAL:
        for tok in str(sup).replace("("," ").replace(")"," ").replace("/"," ").replace(","," ").split():
            if "_r" in tok or "_d" in tok: extra_ids.add(tok)
    for p in pages:
        for r in p["regions"]:
            if r["id"] in extra_ids: continue
            lines=[l["text"].strip() for l in p["lines"] if l["reg"]==r["id"] and l["text"].strip()]
            if not lines: continue
            fr=" — ".join(lines)
            if len(fr)<8: continue
            rows.append([str(p["page"]), f"{r['id']} ({r['kind']})", fr,
                         "تُرجمت في صلب الدليل (التسمية تحت الصورة / الجدول العربي المقابل)"])
    ex=f"work/{os.environ.get('TAG','batch4')}_extra.json"
    if os.path.exists(ex):
        for e in json.load(open(ex)):
            if e["id"] in extra_ids: continue
            rows.append([str(e["page"]), f"{e['id']} (صورة مستعادة)",
                         "لا نصّ: أيقونة/عنصر زخرفة صغير ملحق بإطار الصفحة",
                         "فُحصت على ورقة تلامس فتبيّن أنها بلا محتوى؛ لم تُدرج في المتن"])
    rows.sort(key=lambda r:(int(r[0]), r[1]))
    head("الملحق (أ) — النصوص الواردة داخل الصور وترجمتها (الدفعة الرابعة: ص189–243)")
    P("تضمّ هذه القائمة كل نصّ داخل صورة أو لوحة مصوّرة في صفحات الأصل 189–243: عناوين البطاقات، رؤوس الجداول، بطاقات جرد التسمية، لوحات توزيع الباترونات، فهرس اللوازم، الجداول الموسومة، وأيقونات لا نصّ فيها (ذُكرت كذلك حتى لا تُتجاوز بصمت). وما كان من تسمية شكل مُدرَجة في طبقة النصّ فقد تُرجم تحت الصورة نفسها في المتن.", size=12)
    add_table(rows, header="صفحة الأصل||الصورة / اللوحة||النص كما ورد في الأصل||الترجمة العربية والموضع", fontsz=9)

    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    head("الملحق (ب) — ملاحظات المترجم والتصحيحات والبنود التي تحتاج تأكيداً (الدفعة الرابعة)")
    for i,n in enumerate(NOTES,1):
        P(f"{i}- {n}", size=13)

    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    head("الملحق (ج) — تكملة مسرد المصطلحات (الدفعة الرابعة)")
    P("يُضاف هذا المسرد إلى مَسارد الدفعات الثلاث السابقة؛ وهو مستمدّ من «مسرد القصّ والخياطة» في صفحات الأصل 235–238 ومن فصل البَطانات وفهرس اللوازم. وقد ثُبِّتت المصطلحات بتاريخ 4 نوفمبر 2026 فأصبحت نهائية.", size=12)
    P(CONFIRM, size=11, color="C00000")
    add_table([[fr,ar] for fr,ar in GLOSS_EXTRA], header="الفرنسية||العربية", fontsz=11)
