import os
import re

docsrc = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(docsrc)

chapter3_dir = os.path.join(root, 'chapter-03')

fn_map = {
    66: '1 87 b 35',
    67: '2 Cfr. Cl. BAEUMKER',
    68: '3 J. STUART MILL',
    70: '5 E. STUDY',
    75: '7 Forte aliquis',
    79: '8 COUTURAT',
    80: '9 « Bei der Bildung',
    83: '11 S. Thomas'
}

fn_replacements = {
    66: [('mus » 1.', 'mus » [^1].')],
    67: [('explicat 2.', 'explicat [^2].')],
    68: [('concipi » 3.', 'concipi » [^3].'), ('fictitia » 4.', 'fictitia » [^4].')],
    70: [('libro 5 clare', 'libro [^5] clare'), ('οὐθέν » 6.', 'οὐθέν » [^6].')],
    75: [('limitatum 7.', 'limitatum [^7].')],
    79: [('solidum » 8.', 'solidum » [^8].')],
    80: [('pag. 10) 9.', 'pag. 10) [^9].'), ('conservant » 10.', 'conservant » [^10].')],
    83: [('species intelligibiles 11 quas', 'species intelligibiles [^11] quas')]
}

pages_text = {}
for p in range(65, 95):
    fname = os.path.join(chapter3_dir, f'page-{p:03d}.txt')
    with open(fname, 'r', encoding='utf-8') as f:
        text = f.read().rstrip()
    if p in fn_map:
        idx = text.find(fn_map[p])
        assert idx != -1, f"Footnote pattern not found in page {p}"
        text = text[:idx].rstrip()
    if p in fn_replacements:
        for old, new in fn_replacements[p]:
            assert old in text, f"Footnote callout '{old}' not found in page {p}"
            text = text.replace(old, new)
    pages_text[p] = text

# Strip title block from page 65
p65 = pages_text[65]
idx65 = p65.find("Iam agendum erit")
pages_text[65] = p65[idx65:]

hyphen_page_boundaries = {68, 72, 78, 82, 84, 91, 92}
same_para_page_boundaries = {65, 67, 69, 70, 73, 74, 75, 76, 79, 83, 86, 87, 88, 89, 90, 93}

joined_lines = []
for p in range(65, 95):
    lines = [l.strip() for l in pages_text[p].splitlines() if l.strip()]
    if p > 65:
        prev_p = p - 1
        if prev_p in hyphen_page_boundaries:
            prev_line = joined_lines.pop()
            assert prev_line.endswith('-'), f"Expected hyphen at end of P{prev_p}: {prev_line}"
            joined_line = prev_line[:-1] + lines[0]
            joined_lines.append(joined_line)
            lines = lines[1:]
        elif prev_p in same_para_page_boundaries:
            prev_line = joined_lines.pop()
            joined_line = prev_line + " " + lines[0]
            joined_lines.append(joined_line)
            lines = lines[1:]
    joined_lines.extend(lines)

# Explicit list of headings
headings = {
    "§ 1. DE POSITIONE PROBLEMATIS.": "## § 1. DE POSITIONE PROBLEMATIS.",
    "1. In quonam consistat problema.": "### 1. In quonam consistat problema.",
    "2. Quaedam historica.": "### 2. Quaedam historica.",
    "3. Solutio quaerenda.": "### 3. Solutio quaerenda.",
    "§ 2. DE PRIMIS NOTIONIBUS GEOMETRIAE CLASSICAE.": "## § 2. DE PRIMIS NOTIONIBUS GEOMETRIAE CLASSICAE.",
    "1. De puncto, linea, superficie.": "### 1. De puncto, linea, superficie.",
    "2. Divisio entis extensi.": "### 2. Divisio entis extensi.",
    "3. De dimensionibus.": "### 3. De dimensionibus.",
    "4. De obiectione ex « folio Moebii » desumpta.": "### 4. De obiectione ex « folio Moebii » desumpta.",
    "5. Quae ex his colligantur pro noetica generali.": "### 5. Quae ex his colligantur pro noetica generali.",
    "6. De divisibilitate in infinitum.": "### 6. De divisibilitate in infinitum.",
    "7. De geometria ut scientia constructiva.": "### 7. De geometria ut scientia constructiva.",
}

# Paragraph start predicates:
# We know where paragraphs start in the text. Let's build a set of paragraph-starting prefixes:
para_starts = [
    # Page 65
    "Iam agendum erit de altero problemate,",
    "Recolamus ex praecedentibus, problema exactitudinis",
    # Page 66
    "Si igitur geometria in origine sua dependet a datis sensitivis,",
    "Animadverte bene : in problemate necessitatis,",
    "Ad hoc problema philosophi non solent valde attendere",
    "A) Philosophi. Aristoteles problema optime novit,",
    "« etiamsi possibile esset sentire triangulum habere angulos duobus rectis aequales,",
    "Principale, ad quod nunc attendendum, non est consequens",
    # Page 67
    "Inde haec propositio de summa angulorum trianguli",
    "In antiquitate Proclus saepius urget inexactitudinem",
    "Apud philosophos moderniores problema exactitudinis",
    "Pro Stuart Mill, qui theorias Berkeley et Hume persequitur,",
    "« Non existunt puncta sine magnitudine ;",
    "Immo nec possibiles sunt illae figurae :",
    # Page 68
    "« Puncta, lineae, circuli, et quadrata,",
    "Et eius conclusio est :",
    "« Exactitudo peculiaris, quae supponitur esse characteristica",
    "Pro Stuart Mill problema exactitudinis non existit,",
    "B) Mathematici. In critica mathematica moderna,",
    # Page 69
    "Non solent considerare problema necessitatis.",
    "In unico tamen casu, scilicet ubi agitur de critica postulati V.",
    "Mathematici igitur non solent considerare problema",
    "Exacte, sed breviter, id iam in capite primo descriptum",
    # Page 70
    "Nemo forte uberius et magis in specie problema exposuit",
    "« Evolutio theoriae modernae functionum demonstravit,",
    "His verbis problema exactitudinis clare ponitur ;",
    # Page 71
    "Ita de facto problema exactitudinis geometricae iterum",
    "Unica igitur quaestio haec esse potest : num existant",
    "Clarum est problema involvere quaestiones de existentia",
    # Page 72
    "Primae notiones geometricae exactae, quas examinare",
    "Ipse (op. cit. pagg. 9-11) ita rem prosequitur,",
    "Quoad notionem puncti Wellstein ita procedit.",
    # Page 73
    "Si autem, ita Wellstein pergit post quasdam dilucidationes,",
    "Et ex sua analysi concludit : ad primam definitionem",
    "Revera, si ita tantum notiones exactae geometricae",
    # Page 74
    "Ut hunc intellectum inveniamus, non incipimus a puncto,",
    "Primum « proprium » quod in ente extenso, intuitu intellectus",
    "Possumus addere quaedam, quae rem magis describunt :",
    "Limes relate ad partes, quas dividit, duplicem habet",
    "A) Superficies. Hic igitur limes est superficies et describi",
    # Page 75
    "Existit ergo limes indivisibilis (indivisibilis sub respectu",
    "Hic autem limes est superficies, est id in quod (« contra",
    "B) Linea et punctum. Relate ad hanc divisibilitatem",
    # Page 76
    "Et limes inter duas partes lineae est punctum,",
    "Linea sub alio respectu (in quantum est « iuxta » partes)",
    "De existentia igitur mathematica horum limitum constat :",
    "Si quis ut ideam lineae vel puncti concipiat, vult sequi",
    "C) De indivisibilibus in rerum natura. Existuntne indivisibilia",
    # Page 77
    "Loquebamur de « respectu sub quo superficies est indivisibilis ».",
    "Quid sit dimensio, definitione technica, quae constat",
    # Page 78
    "Ecce criterium claritatis huius notionis : Interrogamus,",
    "Dicebamus supra : existunt mathematice in ente extenso",
    "D) De dimensionibus limitum. Si nunc consideramus",
    "Potestne existere ens quatuor dimensionum, cuius limes",
    "Methodus nostra investigandi notiones superficiei, dein",
    # Page 79
    "Haec superficies habet quandam proprietatem miram ; dicitur esse unilateralis.",
    "Ecce quomodo ex hac proprietate superficierum, quae",
    "« Quidam auctores superficiem definiunt tanquam id quod solidum limitat.",
    "Simili modo Wellstein :",
    "« In formando conceptu superficiei tantum ex superficie externa",
    # Page 80
    "Contendunt igitur talem superficiem unilateralem non",
    "Errant tamen : ut notio superficiei (limitis per quem",
    "« Existunt utique superficies unilaterales, quae nullam partem",
    "Alia consideratio folii Moebii (etiam integri i. e. talis,",
    "Hic transcribimus descriptionem methodi constructionis",
    "« Sumamus folium (v. g. papyraceum) quod habet figuram rectanguli",
    # Page 81
    "Et tunc ita ratiocinamur : Folium Moebii constat ex",
    "Attendamus nunc ad id quod ex nostra operatione resultat.",
    "Quia de tali corpore mentionem facimus, aliud animadvertamus.",
    # Page 82
    "A) Theoria Aristotelis. In supra dictis legere possumus :",
    "Teste igitur conscientia influxus phantasmatis requiritur",
    "Ex datis igitur sensitivis hauritur iudicium intellectivum",
    # Page 83
    "« Similitudo illa quam Philosophus ponit, non attenditur quantum",
    "Iuxta hanc theoriam universaliter id quod in iudicio",
    "Alia quoque animadversio, quae supra exposita in",
    # Page 84
    "B) Theoria Platonis. Si analysis nostra confirmat theoriam",
    "C) Theoria Kantii. Etiam theoria formae subiectivae",
    "D) Theoria empirismi. Ex iis quae videbamus nunc",
    # Page 85
    "Falsum quoque est id quod ab eodem auctore audiebamus :",
    "Nota. — Analysin nostram incepimus in eo puncto,",
    "Supra per transennam attendimus ad sententiam, quae",
    # Page 86
    "A) De divisibilitate in extensa. Notio indivisibilium",
    "Ex hac enim iam scimus : extensum dividi potest in",
    "Inde habemus : ex illo uno phantasmate, a quo incipiebamus,",
    "Hoc principium divisibilitatis in infinitum ope elementorum",
    # Page 87
    "Ecce : partes in quas extensum dividitur, si ad invicem",
    "B) De linea ut « collectione » punctorum. Ex dictis quaedam",
    "Iam in antiqua geometria sermo est de linea, ut est « locus punctorum »,",
    # Page 88
    "Aliter res sese habet in theoria moderna collectionum,",
    "Plurimi, ut dictum est, nativam theoriam collectionum",
    # Page 89
    "Quidquid id est, extensum non potest considerari ut",
    "C) De aequationibus geometriae analyticae. Talis formula",
    # Page 90
    "Applicatio. Haec applicari possunt ad solvendum argumentum,",
    "Operae pretium est ut hoc argumentum expositum audiamus",
    "« L'intuition ne peut nous donner la rigueur ni même la certitude,",
    "Citons quelques exemples. Nous savons qu'il existe des fonctions",
    # Page 91
    "Et alors il est clair que nous pourrons toujours nous représenter",
    "Nous serons ainsi amenés, à moins d'être avertis par une analyse",
    "Argumentum quod examinamus, in ultima alinea exprimitur.",
    "Sumamus exemplum simplicissimum, classicum, talis",
    "Functio autem ita definita est ubique continua : et",
    # Page 92
    "Interrogamus autem : num revera geometrice « existit »",
    "Utrum haec functio analytice sensum habet, hic non",
    "Postea, primo a Weiersztrasz, constructae sunt functiones,",
    # Page 93
    "De his curvis vide ingeniose exposita apud F. Klein",
    "In superioribus exempla simplicissima « constructionis »",
    "Haec notio « constructionis » a Kantio tanquam per",
    "Hic modus interpretandi constructionem obiectorum in",
    # Page 94
    "Et in hoc inveniendo, simul intelligimus dependentiam"
]

# We also handle block quotes or formulas like `y = x sin 1/x`
# Let's inspect paragraphs assembled by joining lines
paragraphs = []
current_p_lines = []

def starts_new_para(line):
    if line in headings:
        return True
    for prefix in para_starts:
        if line.startswith(prefix[:25]):
            return True
    return False

i = 0
while i < len(joined_lines):
    line = joined_lines[i]
    if line in headings:
        if current_p_lines:
            paragraphs.append(current_p_lines)
            current_p_lines = []
        paragraphs.append([line])
        i += 1
        continue
    
    if starts_new_para(line) and current_p_lines:
        paragraphs.append(current_p_lines)
        current_p_lines = []
    
    current_p_lines.append(line)
    i += 1

if current_p_lines:
    paragraphs.append(current_p_lines)

# Now join lines in each paragraph:
# Handle hyphens at line ends: if line.endswith('-'), merge without hyphen; else join with space.
formatted_blocks = []
for p_lines in paragraphs:
    if len(p_lines) == 1 and p_lines[0] in headings:
        formatted_blocks.append(headings[p_lines[0]])
        continue
    
    full_text = ""
    for idx, l in enumerate(p_lines):
        if idx == 0:
            full_text = l
        else:
            if full_text.endswith('-'):
                full_text = full_text[:-1] + l
            else:
                full_text = full_text + " " + l
    # Clean multiple spaces
    full_text = re.sub(r' +', ' ', full_text).strip()
    formatted_blocks.append(full_text)

# Header block
doc_header = [
    "# CAPUT III",
    "DE PROBLEMATE EXACTITUDINIS",
    "## PARS I. DE EXISTENTIA INDIVISIBILIUM"
]

footnotes = [
    "[^1]: 87 b 35 : καὶ εἰ ἦν αἰσθάνεσθαι τὸ τρίγωνον ὅτι δυσὶν ὀρθαῖς ἴσας ἔχει τὰς γωνίας, ἐζητοῦμεν ἂν ἀπόδειξιν καὶ οὐχ ὥσπερ φασί τινες ἠπιστάμεθα. Cfr. Met. III 2, 997 b 35 (S. Th. lect. 7 n. 416). Ibi Protagorae obiectio profertur, quae ex eo movetur, quod in lineis sensilibus recta non tangit circulum in uno puncto.",
    "[^2]: Cfr. Cl. BAEUMKER, Das Problem der Materie in der Griechischen Philosophie pagg. 422 sqq.",
    ("[^3]: J. STUART MILL, System of Logic I ed. 5 (1862) pag. 255 :\n"
     "    « There exist no points without magnitude ; no lines without breath, nor perfectly straight ; no circles with all their radii exactly equal, nor squares with all their angles perfectly right ... according to any test we have of possibility, they are not even possible. Their existence, so far as we can form any judgment, would seem to be inconsistent with the physical constitution of our planet at least, if not of the universe ... the points, lines, circles, and squares, which any one has in his mind, are (I apprehend) simply copies of the points, lines, circles, and squares, which he has known in his experience. Our idea of a point, I apprehend to be simply our idea of the minimum visibile, the smallest portion of surface which we can see. A line, as defined by geometers, is wholly inconceivable »."),
    "[^4]: Ibid. pag. 257 : « The peculiar accuracy, supposed to be characteristic of the first principles of geometry, thus appears to be fictitious ».",
    "[^5]: E. STUDY, Die realistische Weltansicht und die Lehre vom Raume pagg. 74 sqq.",
    "[^6]: Op. cit. pag. 9 « Die Entwicklung der modernen Funktionentheorie hat gezeigt, dass die Kritik der Grundlagen nicht am fünften Postulat, sondern gleich an der ersten Definition hätte ansetzen sollen : σημεῖόν ἐστιν οὗ μέρος οὐθέν ».",
    "[^7]: Forte aliquis ex hac inspectione in superficiem corporis limitati iam vellet habere ideam superficiei et quidem ita, ut in ipsa sensatione iam esset indivisibilis ut limes corporis ; nobis hoc non sufficit ; putamus enim nos in sensatione superficiei iam videre aliquam profunditatem corporis ; ita ut iam ex hac sensatione habeamus notionem tertiae dimensionis. Ceterum si hoc non esset verum, methodus nostra intuitionis intellectus esset adhibenda ubi agitur de linea et puncto, ut statim indicabimus ; nam linea certe non sine latitudine est in sensatione nostra.",
    "[^8]: COUTURAT, Revue de Métaph. et de Morale 1904 pag. 810 : « Certains auteurs définissent la surface comme ce qui limite un solide. Or il existe certaines surfaces qui n'ont qu'une face, ou dont les deux faces se relient d'une manière continue, de sorte qu'elles ne partagent pas l'espace en deux régions séparées, et ne peuvent par suite servir à délimiter un solide ».",
    "[^9]: « Bei der Bildung des Flächenbegriffs nur von der Oberfläche oder dem zwei Körpern Gemeinsamen auszugehen, ist nicht ausreichend, weil es Flächen gibt, die nicht als Ganzes Oberfläche eines Körpers, nicht Trenungsfläche zweier Körper sein können ».",
    "[^10]: A. VOSS, Ueber die mathematische Erkenntnis in Die Kultur der Gegenwart III pag. E 96 : « Allerdings gibt es einseitige Flächen, die keinen Raumteil begrenzen, aber diese Eigenschaft kommt ihnen nur ihres besonderen Zusammenhangs zufolge zu, während ihre elementaren Teile den angegebenen Charakter bewahren ».",
    "[^11]: S. Thomas, uti notum est, non intendit dicere, intellectum primo cognoscere suas species, sed species quae sunt in rebus. Cfr. Th. d. J. pag. 32."
]

full_md_blocks = doc_header + formatted_blocks
full_md = "\n\n".join(full_md_blocks) + "\n\n---\n\n" + "\n\n".join(footnotes) + "\n"

out_path = os.path.join(root, "docs", "caput-3.md")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(full_md)

print(f"Wrote {out_path} successfully ({len(full_md)} bytes, {len(full_md_blocks)} blocks).")
