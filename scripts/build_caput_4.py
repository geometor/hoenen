import os
import re

docsrc = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(docsrc)

chapter4_dir = os.path.join(root, 'archive', 'chapter-04')

fn_map = {
    97: '1 Ea quae Hilbert',
    101: '2 Liceat hic exscribere',
    103: '3 B. RUSSELL',
    105: '6 Inde patet',
    106: 'tio » movent',
    107: '7 Cfr.',
    108: '9 De Caelo',
    110: '10 H. POINCARÉ',
    113: '11 Ita optime',
    122: '12 Bene tamen',
    123: '13 Dicimus',
    124: '14 Informe',
    127: '15 In operis',
    130: '16 W. KILLING',
    131: '17 « Der',
    132: 'Winkel bilden',
    135: '21 F. HAUSDORF',
    137: '22 Ita v. g.',
    139: '25 Etiam notio',
    143: '26 Notari',
    145: '27 Cfr. v. g.',
    146: 'Addimus verba Euclidis',
    148: '29 S. ALBERTUS',
    149: '30 Ita principium',
    150: '31 Repetimus',
}

fn_replacements = {
    97: [('inveniuntur 1.', 'inveniuntur [^1].')],
    101: [('differentiae numericae 2.', 'differentiae numericae [^2].')],
    103: [
        ('B. Russell 3 :', 'B. Russell [^3] :'),
        ('tanquam praestigia » 4.', 'tanquam praestigia » [^4].'),
        ('non spatio » 5.', 'non spatio » [^5].'),
    ],
    105: [('puram 6.', 'puram [^6].')],
    107: [
        ('τοῖς ἐκεῖ 7.', 'τοῖς ἐκεῖ [^7].'),
        ('δὲ γραμμήν 8.', 'δὲ γραμμήν [^8].'),
    ],
    108: [('geometrarum 9.', 'geometrarum [^9].')],
    110: [('geometria » 10.', 'geometria » [^10].')],
    113: [('non vult 11.', 'non vult [^11].')],
    122: [('verificantur 12.', 'verificantur [^12].')],
    123: [('consequenter 13 linea', 'consequenter [^13] linea')],
    124: [('forme) 14, i. e.', 'forme) [^14], i. e.')],
    127: [('plani 15.', 'plani [^15].')],
    130: [('remittimur 16.', 'remittimur [^16].')],
    131: [
        ('aequales sunt » 17.', 'aequales sunt » [^17].'),
        ('inaequales angulos » 18.', 'inaequales angulos » [^18].'),
        ('secentur » 19.', 'secentur » [^19].'),
    ],
    132: [('la pensée 20.', 'la pensée [^20].')],
    135: [('deponere » 21.', 'deponere » [^21].')],
    137: [
        ('axiomata Euclidis 22.', 'axiomata Euclidis [^22].'),
        ('difficultatem 23 ;', 'difficultatem [^23] ;'),
        ('duos rectos 24.', 'duos rectos [^24].'),
    ],
    139: [('momenti est 25.', 'momenti est [^25].')],
    143: [('calamitatem mentalem continet 26.', 'calamitatem mentalem continet [^26].')],
    145: [
        ('difficultates 27 et', 'difficultates [^27] et'),
        ('ita scribit 28 :', 'ita scribit [^28] :'),
    ],
    146: [('tanquam latus). Id veris-', 'tanquam latus).[^note] Id veris-')],
    148: [('Albertus Magnus 29 ;', 'Albertus Magnus [^29] ;')],
    149: [('ignoramus 30.', 'ignoramus [^30].')],
    150: [('sensu terminorum 31.', 'sensu terminorum [^31].')],
}

pages_text = {}
for p in range(95, 157):
    fname = os.path.join(chapter4_dir, f'page-{p:03d}.txt')
    with open(fname, 'r', encoding='utf-8') as f:
        text = f.read().rstrip()
    if p in fn_map:
        idx = text.find(fn_map[p])
        assert idx != -1, f"Footnote pattern '{fn_map[p]}' not found in page {p}"
        text = text[:idx].rstrip()
    if p in fn_replacements:
        for old, new in fn_replacements[p]:
            assert old in text, f"Footnote callout '{old}' not found in page {p}"
            text = text.replace(old, new)
    pages_text[p] = text

# Strip title block from page 95
p95 = pages_text[95]
idx95 = p95.find('In praecedentibus capitibus')
assert idx95 != -1, "Opening text not found in page 95"
pages_text[95] = p95[idx95:]

hyphen_page_boundaries = {96, 99, 100, 103, 111, 115, 117, 118, 128, 140, 141, 142, 150, 151, 153, 154, 155}
same_para_page_boundaries = {97, 101, 104, 107, 109, 112, 113, 114, 116, 121, 123, 125, 126, 130, 133, 134, 135, 136, 137, 138, 139, 143, 144, 145, 146, 147, 149}

joined_lines = []
for p in range(95, 157):
    raw_lines = [l.strip() for l in pages_text[p].splitlines() if l.strip()]
    lines = []
    skip = False
    for idx_l, l in enumerate(raw_lines):
        if l == '*' and idx_l + 1 < len(raw_lines) and raw_lines[idx_l+1] == '*    *':
            lines.append('* * *')
            skip = True
        elif skip:
            skip = False
        else:
            lines.append(l)

    if p > 95:
        prev_p = p - 1
        if prev_p in hyphen_page_boundaries:
            prev_line = joined_lines.pop()
            assert prev_line.endswith('-'), f"Expected hyphen at end of P{prev_p}: {prev_line}"
            joined_line = prev_line[:-1] + lines[0]
            joined_lines.append(joined_line)
            lines = lines[1:]
        elif prev_p in same_para_page_boundaries:
            prev_line = joined_lines.pop()
            joined_line = prev_line + ' ' + lines[0]
            joined_lines.append(joined_line)
            lines = lines[1:]
    joined_lines.extend(lines)

# Merge two-line section headings on p140 and p143
i = 0
while i < len(joined_lines):
    if joined_lines[i] == '§ 6. De geometria non-Euclidica relate' and i+1 < len(joined_lines) and joined_lines[i+1] == 'ad cognitionem humanae mentis.':
        joined_lines[i] = '§ 6. De geometria non-Euclidica relate ad cognitionem humanae mentis.'
        del joined_lines[i+1]
    elif joined_lines[i] == '§ 7. De geometria classica' and i+1 < len(joined_lines) and joined_lines[i+1] == 'relate ad philosophiam cognitionis.':
        joined_lines[i] = '§ 7. De geometria classica relate ad philosophiam cognitionis.'
        del joined_lines[i+1]
    i += 1

headings = {
    '§ 1. DE PRINCIPIO INDIVIDUATIONIS IN GEOMETRICIS.': '## § 1. DE PRINCIPIO INDIVIDUATIONIS IN GEOMETRICIS.',
    '§ 2. DE MOTU IN GEOMETRICIS.': '## § 2. DE MOTU IN GEOMETRICIS.',
    '§ 3. DE CONGRUENTIA FIGURARUM.': '## § 3. DE CONGRUENTIA FIGURARUM.',
    '§ 4. DE FIGURIS EXACTIS.': '## § 4. DE FIGURIS EXACTIS.',
    '1. Animadversiones praeviae.': '### 1. Animadversiones praeviae.',
    '2. De notione directionis.': '### 2. De notione directionis.',
    '3. De continuo directionum.': '### 3. De continuo directionum.',
    '4. Curvae et rectae.': '### 4. Curvae et rectae.',
    '5. De superficie.': '### 5. De superficie.',
    '6. De existentia rectae et plani.': '### 6. De existentia rectae et plani.',
    '7. De connexionibus rectae et plani [^15].': '### 7. De connexionibus rectae et plani [^15].',
    '8. Iterum de notione directionis.': '### 8. Iterum de notione directionis.',
    '9. De directione apud Euclidem.': '### 9. De directione apud Euclidem.',
    '§ 5. De geometria Euclidica et non-Euclidica.': '## § 5. De geometria Euclidica et non-Euclidica.',
    '§ 6. De geometria non-Euclidica relate ad cognitionem humanae mentis.': '## § 6. De geometria non-Euclidica relate ad cognitionem humanae mentis.',
    '§ 7. De geometria classica relate ad philosophiam cognitionis.': '## § 7. De geometria classica relate ad philosophiam cognitionis.'
}

para_starts = [
    'In praecedentibus capitibus agebamus de duobus pro-',
    'Recolamus breviter, quare exsurgat problema exacti-',
    '« Ea quae geometria contendit de suis obiectis : punctis,',
    'Si igitur geometria in origine sua dependet a datis',
    'Quoad existentiam obiectorum quae notionibus exactis',
    'Diligenter examinandi sunt processus qui in mente',
    '« Omnis nostra cognitio originaliter consistit in notitia primo-',
    'Agitur de omni nostra cognitione in eius origine, « ori-',
    'In hac altera parte disquisitionis nostrae de problemate',
    'Non agimus hic de principio individuationis metaphy-',
    'Hic igitur tantum sermo est de geometricis i. e. de fi-',
    'Possuntne dari plures figurae quae tum in quantitate',
    'Quodnam est fundamentum huius affirmationis ? Non',
    'Extensum ut tale est igitur vere « materia intelligibilis » pro geometricis ; ex ea materia actuari possunt figurae,',
    'Per transennam notamus : ex hac consideratione sequi-',
    'Prima facie difficultas quaedam moveri posset v. g. ex conside-',
    'Insuper extensum ita limitatum per hanc superficiem, est vel potest',
    'Figurae congruentes solo situ differunt. Animadverti-',
    'In tota hac expositione praesertim attendendum est',
    'Prius autem aliud considerandum est. Geometrae saepe',
    'Euclides motum figurarum adhibet in primo theore-',
    'Euclides igitur in argumento applicat translationem,',
    'Argumentum Euclidis « nullum habet valorem logicum et omnem',
    '« Primo, notio motus implicat, nostros triangulos non esse spa-',
    'Dicit igitur Russell, motum pertinere ad corpora, non',
    'Haec valde urgenda sunt, quia possibilitas motus est',
    'Distinguamus antecedenter ipsum motum ab eo quod',
    'In motu attendi possunt eius velocitas et eius causa.',
    'Dein : quia motus est mutatio, requirit causam effi-',
    'Duo autem sunt aspectus in ipso motu, secundum quos',
    'Alter respectus secundum quem ad eam pertinet est',
    'Primo : directio est quid qualitativi ; non est quidem',
    'Aristoteles in tractatu de tempore (Phys. IV 11, 219 a 10-18) iam',
    'ἐπεὶ δὲ τὸ κινούμενον κινεῖται ἔκ τινος εἴς τι καὶ πᾶν μέγεθος συνεχές,',
    'Prius igitur continuitas invenitur in extenso et inde haec sequi-',
    'τὸ δὴ πρότερον καὶ ὕστερον ἐν τόπῳ πρῶτόν ἐστιν. ἐνταῦθα μὲν δὲ τῇ',
    'Inde dicendum esse videtur : considerare motum non',
    'Inde non mirum est, apud geometras motum adhiberi',
    'Utilem posse esse methodum hanc ad definiendas li-',
    'Consideratio igitur motus sine ullo dubio pertinet ad',
    'Euclides igitur, adhibendo motum ut medium demon-',
    'Idem B. Russell de quo supra, diversa illa elementa',
    'Ait : corpora quae ita moventur ut ad invicem appli-',
    'Haec obiectio plane valeret, si possibilitas figurae con-',
    'Demonstratio enim Euclidica sine notione translationis',
    'Singula elementa quibus usi sumus, inveniuntur in',
    'Post ea quae videbamus relate ad demonstrationem hanc Eucli-',
    'Concludere possumus : sicut in abstrahendis notioni-',
    'Et ea quae antea (III § 2 n. 7) videbamus, pro hoc casu',
    'Principium individuationis, prout hucusque applica-',
    'Iam in secundo capite, in « geometria inexacta », pote-',
    'Hae notiones et haec axiomata conservantur quoque',
    'Hilbert quidem in eligendis (« creandis ») notionibus et',
    'Altera animadversio haec est : quia has proprias pas-',
    'Tertia animadversio est : Tanquam omnino eaedem (vel',
    'Dicebamus : locutiones punctum situm est in linea et',
    'Si una tantum linea consideratur, ut supra iam dictum',
    'Haec maioris sunt momenti, si non unicam dimensio-',
    'Duae lineae a et b transeant per idem punctum P ;',
    'Diversitas directionum linearum relate ad invicem in',
    'Aliud proprium est valde curiosum. Divergentia in',
    'Haec profluunt ex eis, quae in § 3 dicta sunt, scilicet :',
    'Et nota insuper : figurae congruentes « solo situ » in',
    'Si figurae congruentes compositae sunt ex multis lineis,',
    'Divergentia quae, iuxta supra dicta, mensuram admit-',
    'Etiam statim sine ulteriori examine intelligitur, circa',
    'Nam etiam alio modo continuitas in hoc problemate',
    'Haec directio in calculo infinitesimali consideratur, et',
    'Notio accurata directionis in infinitesimalibus atten-',
    'In geometria inexacta iam sermo esse potest de « lineis »',
    'Ut hoc efficiamus, recolamus directiones linearum quoad',
    'Quae de diversis lineis dicebamus, applicari possunt',
    'Haec quoque videtur esse notio quam Euclides in sua definitione',
    '« ἑπόμενόν ἐστι τῷ ῥύσιν εἶναι τοῦ σημείου τὴν γραμμὴν καὶ τὴν εὐ-',
    'Dantur igitur lineae sensibiliter rectae et curvae et',
    'Superficies sensibiliter plana, quae in experientia nostra',
    'Utrum in geometria exacta, recta, planum et eorum',
    'Praecipua quae inquirenda sunt, ut ex supra dictis',
    'Supra dictum est, definitionem lineae rectae quae ab Euclide',
    'Iam inquirendum est, utrum figurae exactae, in primis',
    'Supra iam videbamus hanc inexactitudinem iam esse',
    'Ea quae inveniebamus relate ad notionem exactam',
    'A) De linea recta. Incipiamus a linea recta. Vidimus',
    'Sed insuper vidimus, diversitatem directionum ap-',
    'Utrumque autem etiam mathematice existere, exten-',
    'Dicimus, in extenso « spatio » rem ita se habere ; nam iterum,',
    'Una veritas intuitiva quae connexionem puncti et rec-',
    'In superficie sensibiliter et clare incurvata haec obser-',
    'Sed haec diversitas et identitas respectuum versus',
    'Sit superficies sensibiliter incurvata, cuius facies con-',
    'Superficies igitur plana, quae eodem modo respicit',
    'Quae ultimo loco dicta sunt, respiciunt connexiones',
    'Primum quod statim sequitur est : recta quae duo',
    'In ipso autem plano per duo puncta unica tantum recta',
    'Sequuntur quaedam quae adhibent motum figurarum',
    'Planum quod rectam continet, circa eam volvi potest.',
    'Inde statim sequitur existere circulos qui in plano describi possunt ex quovis puncto tanquam centro et cum',
    'Inde iam determinari potest notio anguli. Iam in geo-',
    'Notemus praesertim id quod est essentiale in tota hac',
    'Inde resultat consequentia maximi momenti. In plano',
    'Et haec consequentia constituit geometriam Euclidi-',
    'Haec conclusio maximi momenti sequitur ex ipsa no-',
    'Unus modus proponendi difficultatem iam supra ob-',
    'Haec vera essent, si de facto directionem ita definire-',
    'Uberiora et meliora sunt quae inveniuntur apud Kil-',
    'Hanc methodum tribuit Leibnizio ; sed eam peiorem',
    'Ut hoc efficiat, incipit dicendo ideam directionis, ab',
    'Id quod cl. auctor intendit, clarius intelligitur (simul',
    '« Tantum dici potest : illae rectae habent similem vel',
    'Et ideo praesertim hunc auctorem et eius difficultatem',
    'Et de toto hoc processu dici potest : haec ex experien-',
    'Recte igitur dicitur, consequentiam quam supra ex',
    'Relate ad supra dicta duae animadversiones sequantur.',
    'Altera animadversio haec est. In theoria unicae paral-',
    'Ex analysi nostra sequitur geometria Euclidica, et',
    'Haec anno 1904 conscripta sunt ; sed etiam postea',
    'Geometria non-Euclidica habet quidem sensum verum',
    'Observamus primo. Error qui saepe tribuitur eis qui',
    'Ex quo etiam statim patet, nos non committere alium',
    'Quaenam erat in decursu historiae difficultas quae',
    'Mirum est, tam paucos mathematicos, qui de postulato',
    'E contra celeberrimus F. Klein, ut facere solet, omnino',
    'Ex eius expositione manifestum est : agitur de nostro',
    'Si hoc medium non adesset vel non inveniretur, dicen-',
    'Dicebamus diversa extensa esse possibilia ; ex hucusque',
    'Haec dicenda sunt si non adest aliud medium decidendi',
    'Loco harum notionum usi sumus notione directionis ;',
    'Quid igitur dicendum de eis extensis, a Klein descrip-',
    'Unum breviter addimus : modo descripto geometria',
    'Hoc igitur sensu geometria Euclidica est necessaria et',
    'Ita geometria Euclidica potest esse unica et tamen',
    'Ex praedictis facile est solvere difficultatem quae mo-',
    'Contra theoriam Kantii potius alio modo ex geometria arguere',
    'Si autem difficultas modernorum contra ipsam indolem',
    'Ex supra dictis obiectio facile solvitur. Primo interro-',
    'Sed 2°, iuxta supra exposita etiam plus dicendum est :',
    'Sit igitur conclusio ex hac paragrapho : totum aenigma',
    'Vindicata geometria classica ab erroribus qui immerito',
    'Invenimus axioma quoddam in geometria classica, quod',
    'Proprie loquendo plus quam unam veritatem huius',
    'Manifestum igitur est, in geometria classica quasdam',
    'Ad classem « dignitatum » pertinebunt ea quae divisi-',
    'Euclides carpitur ex eo quod sine argumento assumit,',
    'Adest et alius. Num peccat Euclides, non explicite et',
    'Dein adest et aliud iudicium virtuale. Quia datur punc-',
    'Qualis est affirmatio intuitiva intersectionis duorum illorum circulorum, talia sunt principia quae nec demonstrari',
    'Sed bene attendenti utrique necessitati, sese manifestat',
    'Sed nunc attendenti hoc est manifestum : necessitas',
    'Inde sequitur : in construendo syllogismo, cuius forma',
    'Non ita res sese habet in intellectu principiorum. Evi-',
    'Hinc fit ut opus scientiae stricte dictae — scientiae con-',
    'Conclusiones esse necessarias, semper igitur intelligi-',
    'Ea quae dicebamus spectant necessitatem propositio-',
    'Inde etiam melius intelligitur, quare axiomatica mo-',
    'Theoria classica, sicut ab Aristotele in sua theoria co-',
    'Unde etiam in conceptione geometriae Aristotelica',
    'Scientia quae principia iustificat, apud Platonem erat',
    'Difficultas quaedam praevia hic oriri poterit ex eis quae',
    'Dicamus primo : ibi interdum absque dubio tales syl-',
    'Dein autem dicendum est : etiamsi hic inde aliquis',
    'Inter eos sunt quidam qui non sunt syllogismi formales,',
    'Iudicium virtuale adest, ubi mens nexum necessarium',
    'Relate ad hos processus mentis humanae adhuc obser-',
    'Si igitur ipse hic modus naturalis procedendi mentis',
    'In praecedentibus plura puncta tangimus quae amplio-',
]

para_starts_set = set(para_starts)

paragraphs = []
cur_p = []
for idx, line in enumerate(joined_lines):
    if line in headings or line == '* * *':
        if cur_p:
            paragraphs.append(cur_p)
            cur_p = []
        paragraphs.append([line])
        continue
    if (line in para_starts_set) and cur_p:
        paragraphs.append(cur_p)
        cur_p = []
    cur_p.append(line)

if cur_p:
    paragraphs.append(cur_p)

formatted_blocks = []
for p_lines in paragraphs:
    if len(p_lines) == 1 and p_lines[0] in headings:
        formatted_blocks.append(headings[p_lines[0]])
        continue
    if len(p_lines) == 1 and p_lines[0] == '* * *':
        formatted_blocks.append('* * *')
        continue
    
    full_text = ""
    for idx, l in enumerate(p_lines):
        if idx == 0:
            full_text = l
        else:
            if full_text.endswith('-'):
                if full_text.endswith('non-'):
                    full_text = full_text + l
                else:
                    full_text = full_text[:-1] + l
            else:
                full_text = full_text + " " + l
    full_text = re.sub(r' +', ' ', full_text).strip()
    formatted_blocks.append(full_text)

doc_header = [
    "# CAPUT IV",
    "DE PROBLEMATE EXACTITUDINIS",
    "## PARS II. DE FIGURIS ET RELATIONIBUS EXACTIS",
    "### Animadversiones praeviae."
]

footnotes = [
    '[^1]: Ea quae Hilbert in opere Grundlagen der Geometrie tanquam « explicationes » (« Erklärungen ») seriebus axiomatum praemittere et miscere solet, si accurate considerantur, continent quoque iudicia virtualia de passionibus propriis obiectorum, quae dein in axiomatibus magis determinantur.',
    '[^2]: Liceat hic exscribere textum S. Thomae. Ait (In Boet. de Trin. q. 5 a. 3 ad 3) « Materia non est principium diversitatis secundum numerum, nisi secundum quod in multas partes divisa, in singulis partibus formam recipiens eiusdem rationis, plura individua eiusdem speciei constituit. Materia autem dividi non potest nisi ex praesupposita quantitate, qua remota, substantia omnis indivisibilis remanet, et sic prima ratio diversificandi ea quae sunt unius speciei, est penes quantitatem. Quod quidem quantitati competit, in quantum in sua ratione situm, quasi differentiam constitutivam habet, quod nihil est aliud quam ordo partium. Unde etiam abstracta quantitate a materia sensibili per intellectum, adhuc contingit imaginare diversa secundum numerum unius speciei, sicut plures triangulos aequilateres, et plures lineas rectas aequales ». Sola ultima pars horum verborum respicit principium individuationis in geometricis. De hoc vide quoque Met. VII lect. 10 (Cath. n. 1496) ubi quoque distinguitur materia sensibilis, qualitatibus affecta, et materia intelligibilis, continuum scilicet, quod, ut ibi dicitur, pro geometricis est principium individuationis.',
    '[^3]: B. RUSSELL, Principles of Mathematics 1903, ed. 2 1937, n. 390 sq., pagg. 405-407.',
    '[^4]: « It has no logical validity, and strikes every intelligent child as a juggle » (loc. cit.).',
    '[^5]: « In the first place, to speak of motion implies that our triangles are not spatial but material. For a point of space is a position, and can no more change its position than the leopard can change its spots ... motion, in the ordinary sense, is only possible to matter, not to space » (loc. cit.).',
    '[^6]: Inde patet eos qui (forte iuxta ea quae Wellstein dicebat) incipere volunt a figuris, ex filo tenui sed rigido compositis, quas in « spatio » movent, non evitare applicationem principii individuationis, sed id implicite supponere. Nam ut hae figurae moveri possint, praesupponitur extensum (spatium) in quo moventur, talem habere structuram, ut illae figurae diversis partibus « spatii » applicari possint, et quidem modo continue variabili. In illo « spatio » tales limites partium (lineae) ut possibiles, mathematice existentes, praesupponuntur. Possibilitas motus corporis rigidi praesupponit spatium et eius proprietates, non vice versa. Et ex principio individuationis plura derivari possunt quam ex solo principio liberi motus corporum rigidorum. Cfr. Gregorianum 1951 pagg. 449 sq.',
    "[^7]: Cfr. ibid. b 15 sqq. et cap. 12, 220 b 24 sqq. Textus desumptus est ex editione W. D. Ross Aristotle's Physics.",
    '[^8]: Trendelenburg in sua editione adnotat (in loc. cit.) « Quinam sunt qui dicant ? Utrum universi geometrae ? An Pythagorei ? De quo nihil apud commentatores ». S. Thomas i. h. l. (lect. 11, ed. Pirotta n. 170) dicit eos esse Platonicos ; idem affirmat A. E. Taylor in opere Plato the man and his work (ed. 2) 1927) pag. 506. Geminus apud Proclum in textu quem statim videbimus, vocat lineam ῥύσιν τοῦ σημείου. Cfr. quoque Proclum pag. 97, 6 et Simplicium Phys. (ed. Diels) pag. 722, 8.',
    '[^9]: De Caelo I lect. 2 n. 9 « Utitur modo loquendi quo utuntur geometrae, imaginantes quod punctus motus facit lineam, linea vero mota facit superficiem , superficies autem corpus » ; cfr. ibid. II lect. 2 n. 11, Phys. IV lect. 18 n. 4.',
    "[^10]: H. POINCARÉ, La science et l'hypothèse pag. 80 ; cfr. ibid. pag. 60. Ipse auctor integram sententiam sublineat.",
    "[^11]: Ita optime cl. Hadamard (in Encyclopédie Française I 1937, I-52-10) : « Bien entendu, l'auteur des Grundlagen der Geometrie [Hilbert] s'est, dans ce travail logique, laissé constamment guider par l'intuition géométrique ». Cfr. quoque quae dein sequuntur.",
    '[^12]: Bene tamen notandum est : propositiones « geometriae inexactae » vel « approximativae » quae ita inveniuntur, magnopere differunt a propositionibus ordinariis physicis ; nam in hac experientia de rebus geometricis pervenimus quidem ad propositiones quae forte non omnino exactae sunt, quae approximative tantum verificantur — in hoc non differunt a iudiciis de rebus physicis — sed intelligimus semper, propositiones approximativas geometricas esse necessarias. Elementum exactitudinis adhuc deest, sed elementum necessitatis intellectae semper adest.',
    '[^13]: Dicimus « consequenter » ; nam, ut ex dictis manifestum est, « directio » non definitur ope notionis lineae rectae, sed, vice versa, « directio constans » est differentia specifica quae rectam a curva distinguit ; notio autem « directionis », modo supra indicato immediate hauritur ex experientia et est notio primitiva; est « modus transeundi per punctum » cuiusvis lineae. Notio directionis constantis habetur ex eadem experientia, quae directiones sensibiliter constantes revelat. In ulteriori investigatione iam non agitur de notione sed de quaestione utrum existat, de quaestione « an est ». Et agitur unice de problemate exactitudinis. Perperam igitur dicit Helmholtz (Schriften zur Erkenntnistheorie ed. P. Hertz et M. Schlick 1921 pag. 141) : « Wie soll man aber Richtung definieren ; doch wieder nur durch die gerade Linie. Hier bewegen wir uns in einem Circulus vitiosus » (« Quomodo definienda est directio ; tantum utique ope lineae rectae. Hic movemur in circulo vitioso »). Ex supra dictis clare sequitur : directio est idea primitiva quae non definitur technice, sed statim ex experientia hauritur. Ad hanc difficultatem postea redibimus ; ab aliis maiori cum profunditate proponitur.',
    '[^14]: Informe vel « amorphum » ; ita POINCARÉ, Dernières Pensées pag. 62, La valeur de la science pag. 59.',
    '[^15]: In operis Quaestioni riguardanti le matematiche elementari, quod edidit F. Enriques, volumine I (ed. 3) legitur sectio quam scripsit U. Amaldi « sui concetti di retta e di piano ». Hic bene exponuntur difficultates quae surgunt in accurate stabiliendis his connexionibus ; non sunt paucae nec leves. Auctor, uti mos est apud mathematicos, notione directionis uti non vult ; inde difficultates augentur. Facile utique esset, « postulare » axiomata connexionis. Sed in hoc casu problema nostrum noeticum, quod sane dignissimum est quod examinetur, ex integro negligitur. Iam axioma simplex quod affirmat, rectam per duo puncto determinari, non potest directe ex experientia hauriri, propter problema exactitudinis, et exigit analysin noeticam.',
    '[^16]: W. KILLING, Einführung in die Grundlagen der Geometrie, Münster I (1893) II (1898) ; quae de directione rectae dicit inveniuntur in T. I § 3 pagg. 5 sqq.',
    '[^17]: « Der Winkel misst den Richtungsunterschied zweier Geraden ; folglich sind die beiden Winkel gleich, welche zwei Parallelen mit derselben geraden Linie bilden » (pag. 5).',
    '[^18]: « Zwei Geraden haben gleiche oder ungleiche Richtung, wenn sie mit einer beide schneidenden Geraden gleiche oder ungleiche Winkel bilden » (loc. cit. pag. 6).',
    "[^19]: « Man darf nur sagen : sie haben gleiche oder ungleiche Richtung in Bezung auf eine bestimmte dritte Gerade ; dann ist es aber ungewisz, ob zwei Geraden, welche mit einer bestimmten Geraden gleiche Winkel bilden, auch von jeder Geraden unter gleichen Winkeln geschnitten werden » (loc. cit.). Hanc ideam mutuat ex Gauss ad quem remittit. Gauss' Werke IV S. 365. Similem ideam invenimus apud cl. Hölder, Die mathematische Methode pag. 120, vide Cosmologiam nostram pag. 455.",
    '[^20]: Difficultas quam ex cl. Killing exponebamus, etiam invenitur apud cl. U. Amaldi quem supra laudavimus (op. cit. § 3 pag. 46) ; post supra dicta non opus est ut ad eam redeamus.',
    '[^21]: F. HAUSDORF, Das Raumproblem in Annalen der Naturphilosophie III (1904) pag. 3 : « Die Mathematik darf jede aprioristische Konstruktion, die den euklidischen Raum mit seinen speziellen Eigentümlichkeiten, als Denknotwendigkeit, willkürfrei und voraussetzungslos zu deduzieren behauptet, ungeprüft ad Acta legen ».',
    '[^22]: Ita v. g. H. WEYL, Philosophie der Mathematik und Naturwissenschaft (1927) pag. 18 ; J. HADAMARD, Encycl. Franç I (1937) I-52-7 ; H. REICHENBACH, Philos. der Raum-Zeit-Lehre (1928) pag. 10. Hic postulatum simul vocat « extraordinarie cogens » (auszerordentlich zwingend) (!) et tamen parum convincens (« etwas Unbefriedigendes »), quia de infinito aliquid asserit et ideo omnem experientiam possibilem transcendit.',
    '[^23]: F. KLEIN, Elementarmathematik vom höheren Standpunkte aus (II ed. 3 1925) pagg. 189 sq.',
    '[^24]: Cfr. eundem F. Klein (op. cit. pagg. 192-194) qui ibi iterum bene probat, hic agi de problemate exactitudinis sensu descripto et inde hanc possibilitatem deducit.',
    '[^25]: Etiam notio rectae non-Euclidicae ideo non est omnino eadem ac notio rectae Euclidicae exactae.',
    '[^26]: Notari potest, ita etiam constitui posse alias geometrias Euclidicas quae scilicet deducuntur ex systemate propositionum quae omnes, etiam ea quae exprimit postulatum V, in verbis cum axiomatibus Euclidicis congruunt, sed alios sensus habent. Inde agunt de aliis obiectis ; sed haec obiecta sub aliis nominibus in antiqua geometria Euclidica occurrunt. Vide tale systema, a Wellstein elaboratum, in opere, antea iam citato, Weber-Wellstein in Enzyklopaedie der Elementarmathematik II Elemente der Geometrie (ed. 3 1915) pagg. 33-62.',
    '[^27]: Cfr. v. g. TH. WAITZ in suo Commentario in Anal. Priora I 23 ; in eius editione I pagg. 427-429.',
    "[^28]: In eodem opere Principles of Mathematics pagg. 404 sq. : « There is no evidence whatever that the circles which we are told to construct intersect, and if they do not, the whole proposition fails. Euclid's problems are often regarded as existence-theorems, and from this point of view, it is plain, the assumption that the circles in question intersect is precisely the same as the assumption that there is an equilateral triangle on a given base ».",
    '[^29]: S. ALBERTUS MAGNUS, Anal. Prior. I tract. I cap. 9 (in ed. Jammy, 1651, I pag. 298 a) : « terminis utimur transcendentibus, nihil et omnia significantibus. Nihil dico : quia nullam determinatam materiam. Omnia vero dico significantibus : quia omnibus materiis sunt applicabiles, sicut sunt a, b, c ». Etiam pseudo-Thomas in opere Summa totius logicae utitur locutione « termini transcendentes » quibus opponuntur « termini significativi » ; op. cit. tract. VII cap. 2 et 6 (in editione Mandonnet pagg. 102-104, pag. 111).',
    '[^30]: Ita principium generale syllogismi iam ab Aristotele exprimitur (Anal. Prior. I 4, 25 b 37-39) : εἰ τὸ Α κατὰ παντὸς τοῦ Β καὶ τὸ Β κατὰ παντὸς τοῦ Γ, ἀνάγκη τὸ Α κατὰ παντὸς τοῦ Γ κατηγορεῖσθαι.',
    '[^31]: Repetimus : supponi tamen debet terminos sensum habere (id quod quidam axiomatici oblivisci videntur) ; nam ut forma syllogistica valida sit, requiritur, ut termini qui pluries occurrunt, eundem sensum retineant ; sensum igitur habere debent.',
    '[^note]: Addimus verba Euclidis secundum versionem quam legimus apud Heiberg (pagg. 11 sq.) : « In data recta terminata triangulu aequilaterum construere. Sit data recta terminata AB oportet igitur in recta AB terminata triangulum aequilaterum construere. Centro A et radio AB circulus describatur BCD, et rursus centro B radio autem BA circulus describatur ACE, et a puncto C, in quo circuli inter se secant, ad puncta A, B ducantur rectae CA, CB. Iam quoniam punctum A centrum est circuli CDB, erit AC = AB, rursus quoniam B punctum centrum est circuli CAE, est BC = BA. sed demonstratum est etiam CA = AB. quare utraque CA, CB rectae AB aequalis est. quae autem eidem aequalia sunt, etiam inter se aequalia sunt [κ. ἔνν. 1] (i. e. secundum primam e « communibus animi conceptionibus »). itaque etiam CA = CB. itaque CA, AB, BC aequales sunt, quare triangulus ABC aequilaterus est ; et in data recta terminata AB constructus est. quod oportebat fieri ».'
]

full_md_blocks = doc_header + formatted_blocks
full_md = "\n\n".join(full_md_blocks) + "\n\n---\n\n" + "\n\n".join(footnotes) + "\n"

out_path = os.path.join(root, "docs", "caput-4", "caput-4.md")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(full_md)

print(f"Wrote {out_path} successfully ({len(full_md)} bytes, {len(full_md_blocks)} blocks).")
