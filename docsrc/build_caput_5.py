import os
import re

docsrc = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(docsrc)

chapter5_dir = os.path.join(root, 'chapter-05')

fn_map = {
    158: '1 Ita Th. Heath',
    159: '2 Cfr. discussionem',
    161: '3 Ita formam',
    163: '4 De termino',
    164: '5 J. LOCKE',
    165: '6 Ita bene',
    166: '7 G. STAMMLER',
    169: '8 « I believe',
    172: '9 « Sind irgendeine',
    179: '10 Haec iam observata',
    188: '[^11]:',
    192: '[^12]:'
}

fn_replacements = {
    158: [('hanc theoriam applicabat 1.', 'hanc theoriam applicabat [^1].')],
    159: [('vocat 2 ;', 'vocat [^2] ;')],
    161: [('formarum syllogismorum 3.', 'formarum syllogismorum [^3].')],
    163: [('« dispositionibus rei » 4 determinatis', '« dispositionibus rei » [^4] determinatis')],
    164: [('methodos syllogizandi » 5.', 'methodos syllogizandi » [^5].')],
    165: [('(germanice « des Gedachten » ) 6.', '(germanice « des Gedachten » ) [^6].')],
    166: [('Dictum est 7 logicam', 'Dictum est [^7] logicam')],
    169: [('2 + 2 = 4 » 8.', '2 + 2 = 4 » [^8].')],
    172: [('scil. inversa » 9.', 'scil. inversa » [^9].')],
    179: [('eadem in specie individua 10. Est', 'eadem in specie individua [^10]. Est')],
}

pages_text = {}
for p in range(157, 195):
    fname = os.path.join(chapter5_dir, f'page-{p:03d}.txt')
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

# Strip title block from page 157
p157 = pages_text[157]
idx157 = p157.find('In capitibus praecedentibus')
assert idx157 != -1, 'Opening text not found in page 157'
pages_text[157] = p157[idx157:]

hyphen_page_boundaries = {157, 164, 165, 166, 170, 173, 179, 180, 181, 185, 186, 187, 188, 189, 193}
same_para_page_boundaries = {158, 159, 161, 163, 167, 168, 169, 171, 172, 174, 176, 177, 182, 183, 184, 190, 191, 192}

diagram_lines = {
    '    A    B    C    D    E        K',
    '  ──•────•────•────•────•────────•──'
}

joined_lines = []
for p in range(157, 195):
    raw_lines = pages_text[p].splitlines()
    lines = []
    for l in raw_lines:
        if not l.strip():
            continue
        if l in diagram_lines:
            lines.append(l)
        else:
            lines.append(l.strip())

    if p > 157:
        prev_p = p - 1
        if prev_p in hyphen_page_boundaries:
            prev_line = joined_lines.pop()
            assert prev_line.endswith('-'), f'Expected hyphen at end of P{prev_p}: {prev_line}'
            joined_line = prev_line[:-1] + lines[0]
            joined_lines.append(joined_line)
            lines = lines[1:]
        elif prev_p in same_para_page_boundaries:
            prev_line = joined_lines.pop()
            joined_line = prev_line + ' ' + lines[0]
            joined_lines.append(joined_line)
            lines = lines[1:]
    joined_lines.extend(lines)

# Merge two-line section heading on p175
i = 0
while i < len(joined_lines):
    if joined_lines[i] == '§ 4. De appellatione ad phantasma in aliis' and i+1 < len(joined_lines) and joined_lines[i+1] == 'scientiis.':
        joined_lines[i] = '§ 4. De appellatione ad phantasma in aliis scientiis.'
        del joined_lines[i+1]
    i += 1

headings = {
    '§ 1. De methodo axiomatica.': '## § 1. De methodo axiomatica.',
    '1. De axiomatica stricte dicta.': '### 1. De axiomatica stricte dicta.',
    '2. De methodo Aristotelis.': '### 2. De methodo Aristotelis.',
    '3. Semi-axiomatica.': '### 3. Semi-axiomatica.',
    '§ 2. De fundamento possibilitatis axiomaticae.': '## § 2. De fundamento possibilitatis axiomaticae.',
    '1. De syllogismo verbis expresso.': '### 1. De syllogismo verbis expresso.',
    '2. De syllogismo mentali et verbali noetice spectato.': '### 2. De syllogismo mentali et verbali noetice spectato.',
    '§ 3. De executione programmatis axiomatici': '## § 3. De executione programmatis axiomatici.',
    '1. Animadversiones praeviae': '### 1. Animadversiones praeviae.',
    '2. Difficultates intrinsecae.': '### 2. Difficultates intrinsecae.',
    '§ 4. De appellatione ad phantasma in aliis scientiis.': '## § 4. De appellatione ad phantasma in aliis scientiis.',
    '1. Animadversiones generales.': '### 1. Animadversiones generales.',
    '2. In statuendis primis principiis.': '### 2. In statuendis primis principiis.',
    '3. In deductione scientifica.': '### 3. In deductione scientifica.',
    '§ 5. DE APPLICATIONE GEOMETRIAE [^11].': '## § 5. DE APPLICATIONE GEOMETRIAE [^11].',
}

para_starts = [
    # P157
    'In capitibus praecedentibus saepe sermo erat de « axio-',
    'In hac constructione scientiae non est, nec potest esse,',
    'Voces, quae adhibentur, sunt eaedem ac illae, quae in',
    'Quia haec methodus, perfecte elaborata a mathematicis,',
    # P158
    'Aristoteles, uti dictum est, theoriam exponit scientiae',
    'Aristoteles distinguit inter « intellectum » stricte dic-',
    'Ipsius igitur geometriae sola functio est pura deductio',
    'Sed est diversum ab axiomatica sensu moderno. Aris-',
    # P159
    'Ex hac prima diversitate ab axiomatica moderna aliae,',
    'Etiam systema quoddam, quodammodo intermedium,',
    # P160
    'Haec exigentia primorum principiorum pro geometria',
    'In capitibus praecedentibus nos diversa axiomata per',
    'Methodus, quam cl. Freudenthal proponit, iure nomi-',
    'In diiudicanda axiomatica statim difficultas quaedam',
    # P161
    'Haec « abstractio symbolica » consistit in hac simplici',
    'In medio aevo haec symbola (litterae), quae in exponen-',
    'Conditiones. In hac « abstractione », in qua loco verbo-',
    '1) Termini debent habere sensum ; etiamsi hic nobis',
    # P162
    '2) Insuper nobis nota esse debet structura proposi-',
    'Sed non opus est ut haec theoretice iam examinata',
    'Haec quae dicta sunt, spectant propositiones praedica-',
    'Et hoc est fundamentum possibilitatis axiomaticae.',
    # P163
    'A) Activitas syllogizans est intuitiva. Syllogizando ratio-',
    'Ipse syllogismus nihil dicit de ipsa mente et eius opera-',
    'Haec intuitio necessitatis est eiusdem generis ac illa,',
    'Analogo modo mens est activa in syllogizando. In syl-',
    'B) Activitas syllogizans est naturalis. Supra iam diceba-',
    # P164
    'Id clarum est ex ipsa historia logicae. Aristoteles, cons-',
    'Tale ratiocinium rectum est activitas, quae provenit',
    'Illae « leges logicae » nec dicendae sunt leges psychologicae, nam respiciunt obiecta. Saepe nominantur « leges',
    # P165
    'In construenda scientia, haec forma, quae ita abstrahi',
    'Et ita leges logicae utentis non sunt « normae » proprie',
    'Logica docens, vel theoretica, quae inde ab hac logica',
    # P166
    'Dicebamus « etiam ipse modus Barbara ». Nam hic',
    'Ita in construenda scientia, in deducendo, duplicem',
    'In hac « logica docente », theoretica, poterimus, etiam',
    # P167
    'Hae leges logicae universaliter agunt de ipsis rebus, de',
    'Ita etiam axiomatica stricte dicta procedere poterit ;',
    'Ex praecedentibus concludere licet : methodus axioma-',
    'Hoc systema axiomatum necessario satisfacere debet',
    # P168
    'Sunt qui dicant hanc exigentiam non requiri, ut systemati quae-',
    'De hac positione extrema unum tantum verbum dicimus. Vox',
    'Si pars scientiae modo axiomatico construitur, vel po-',
    # P169
    'A) Difficultas practica. Difficultas practica in eo consistit',
    'Legatur apud Hilbert demonstratio simplicissimi theo-',
    'Interrogemus axiomaticum : Num admittis tale theo-',
    'Diximus demonstrationem theorematis 5 apud Hilbert etiam figura geometrica illustrari. Haec sane non additur,',
    # P170
    'Haec methodus introducitur, aiunt, ut rigor analyseos',
    'B) Difficultas theoretica. Difficultatem iuris adesse, sta-',
    'Et in tali casu « appellationis » ad phantasma dispositio rei quae aspicitur, est potius geometrica quam « logica » ;',
    # P171
    'Ut responsum habeatur, inquisitio noetica non ad',
    'Poincaré, qui sane methodos modernae axiomaticae',
    'Si quis hoc asserit (et permulti mathematici hoc facere',
    'Ecce enuntiatio huius theorematis 6 : « In quovis numero dato',
    # P172
    'Ordo huius seriei symbolorum aspiciendus est, ut in-',
    # P173
    'Et ubicunque hoc theorema applicatur, et id fit saepis-',
    'Etiam finis enuntiationis theorematis 6 ad eandem du-',
    # P174
    'Et intelligimus positionem Poincaré, de qua supra dic-',
    'Haec quae detegimus in examine noetico propositio-',
    # P175
    'Axiomatica igitur pura etiam theoretice non potest',
    'Difficultatem quae ex applicatione profluit, in § 5 con-',
    'Geometria igitur, propter difficultates tum practicas',
    # P176
    'Et videbamus Euclidem laudandum esse eo quod etiam',
    'Ut autem haec necessitas recursus ad phantasma, et',
    'Supra, in primis quattuor capitibus iam abunde vide-',
    '1) Localisatio est praevia motui secundum locum ;',
    '2) Hae relationes locales sunt relationes in ordine',
    # P177
    '3) Ut supra iam dictum est, ut contactus successi-',
    'Obiectiva possibilitas motus corporis rigidi profluit ex',
    'Sed nunc non de primis principiis, axiomatibus, sermo',
    'A) De arithmetica. Dicimus : in deductione arithmetica',
    # P178
    'Interrogamus : quid fit noetice in mente nostra, dum',
    'Animadvertimus primo : processus mentis hic consistit',
    'Dicimus potius hoc ratiocinium pertinere ad « typum » Barbara ;',
    'Naturaliter igitur intuemur in tali syllogismo mentali,',
    'Inde habemus quod primo observamus : in omni tali',
    # P179
    'Et talis operatio videtur adesse in singulis fere gressi-',
    'Alterum, quod animadvertendum est in hac operatio-',
    'Sub respectu abstractionis casus omnino idem ac casus',
    # P180
    'In hoc casu simplicissimo sufficit inspectio rapida phan-',
    'Altera igitur animadversio erit haec : in singulis fere',
    'Hic bene adnimadvertendum est relate ad propositionem, quae',
    'Resumamus : In singulis fere gressibus deductionis',
    'Utrumque elementum, quod in singulis illis gressibus',
    # P181
    'B) Logistica. Hoc forte mirum erit, sed revera in me-',
    'Deductio logistica, etiam ea quae ipsam hanc artem',
    'Distinguuntur regulae primitivae et derivatae. Nomi-',
    'Videamus specimen substitutionis, et quidem eam quae',
    # P182
    'Et haec semper iterum recurrunt, in singulis fere gres-',
    'Et animadvertamus adhuc : haec phantasmata vel data',
    'Notamus insuper : in logistica, secundum Whitehead',
    # P183
    'Recapitulatio. In superioribus videbamus : geometria',
    'Ipse syllogismus, qui est medium deductionis in axio-',
    'Ut universalitas necessitatis talis intuitionis magis illu-',
    'In his calculis arithmeticis sensus intuitivus terminorum',
    'Interrogare possumus de aliis scientiis ; ibi in genere',
    # P184
    'C) Deductio in aliis scientiis. In scientiis, quae non',
    'Sed ita id facimus ut, aliter ac in axiomatica, semper',
    'Signum huius invenimus in methodo classica disputandi',
    'Extremum specimen in hoc contextu est illud quod',
    # P185
    'In hoc puncto aliquid obviam habemus, quod prima',
    'Non ideo omne quod in axiomatica comprehenditur,',
    'Homo in scientiis realitatem attingere intendit, sed',
    # P186
    'Sed in hoc labore mentali magnopere adiuvatur per',
    'Hic autem quaestio oritur : undenam provenit haec',
    'Ecce quaedam puncta forte attentione digna. Si nova',
    'Id iam agnoscere possumus, ubi agitur de intuitionibus',
    # P187
    'Hic casus est utique adhuc valde simplex et facilis. In',
    'In casibus ubi agitur de dispositione rerum « quorum',
    'Sed in fine ad intellectionem sensus specifici conclusionum tendimus, et aciem mentis ad dispositiones rerum non',
    # P188
    'Mens igitur humana, in modo suo naturali deducendi,',
    'Nota. In neo-positivismo moderno, saltem secundum',
    'A) De applicatione geometriae classicae. Geometria clas-',
    # P189
    'In hac applicatione necessitas relationum in extensis',
    'Ita scientia mathematica extensorum physicorum, « phy-',
    'B) De applicabilitate geometriae axiomatice constructae.',
    'Ipsa notio extensionis in his verbis non videtur exprimi ;',
    # P190
    'Sed dein examinari debet, utrum axiomata, quae nunc',
    'In verificatione axiomatum (et idem valet si theorema',
    'Ex dictis resultat : ut geometria axiomatice constructa',
    'Maior est etiam difficultas, si problema exactitudinis',
    # P191
    'Non ita in applicatione geometriae axiomatice con-',
    'Sumamus propositionem axiomaticam (apud Hilbert',
    'Directe igitur geometria axiomatica (post introductum',
    # P192
    'Sed ut haec solutio difficultatis vere valida sit, requiri-',
    'Sunt mathematici qui contendunt, illud onus appli-',
    'In tali separatione superba, quasi-aristocratica, geo-',
    # P193
    'Physici ergo a tali mathematico nullum auxilium expec-',
    # P194
    'Clarum est talem physicum in hoc tendere, ut scientiam',
    'Geometria axiomatice constructa diversis defectibus',
    'Utilitatem tamen habere potest methodus axiomatica',
    'Omnia autem haec invitare videntur philosophum scho-',
]

para_starts_set = set(para_starts)

paragraphs = []
cur_p = []
skip_next = False
for idx, line in enumerate(joined_lines):
    if skip_next:
        skip_next = False
        continue
    if line in headings or line == '* * *':
        if cur_p:
            paragraphs.append(cur_p)
            cur_p = []
        paragraphs.append([line])
        continue
    if line == '    A    B    C    D    E        K' and idx + 1 < len(joined_lines) and joined_lines[idx+1] == '  ──•────•────•────•────•────────•──':
        if cur_p:
            paragraphs.append(cur_p)
            cur_p = []
        paragraphs.append(['```\n    A    B    C    D    E        K\n  ──•────•────•────•────•────────•──\n```'])
        skip_next = True
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
    if len(p_lines) == 1 and p_lines[0].startswith('```'):
        formatted_blocks.append(p_lines[0])
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
    "# CAPUT V",
    "DE AXIOMATICA",
    "## § 1. De methodo axiomatica.",
    "### 1. De axiomatica stricte dicta."
]

footnotes = [
    '[^1]: Ita Th. Heath in suo opere famoso A History of Greek Mathematics, Oxford 1921, I pagg. 335 sqq. Idem historicus ibi affirmat (de qua re interdum dubia moventur, vel quod etiam negatur) « Aristotle was no doubt a competent mathematician, though he does not seem to have specialized in mathematics ».',
    '[^2]: Cfr. discussionem inter Cl. Freudenthal et auctorem in Gregor. 1951. H. FR., De fontibus geometriae in intuitione et abstractione quaerendis pagg. 425-433, et auctoris De noetica geometriae, responsum ad animadversiones Cl. Fr. pagg. 434-452.',
    '[^3]: Ita formam syllogismi « Barbara » exprimit et eius valorem affirmat dicendo : « si A praedicatur de omni B, et B de omni C, necesse est A de omni C praedicari » quod ita in « schema » syllogismi reducitur : « omne B est A, atqui omne C est B, ergo omne C est A ». Anal. Priora I, 4 25 b 37-39. De ulteriori evolutione symbolismi Aristotelis cfr. opus nostrum Recherches de logique formelle. La structure du système des syllogismes et des sorites . La logique des notions « au moins » et « tout au plus ». Romae 1947.',
    '[^4]: De termino « dispositio rei » apud S. Thomam (qui est aequivalens termino germanico moderno « Sachverhalt » ) vide Théorie du Jugement Ch. II § 5.',
    '[^5]: J. LOCKE, An essay concerning human understanding Bk. IV ch. 17 § 4 (in ed. Fraser II pagg. 390 sqq.) : « God has not been so sparing to men to make them barely two-legged creatures, and left it to Aristotle to make them rational ... He has given them a mind that can reason, without being instructed in methods of syllogizing ». Leibniz in suo responso ad Locke (Nouveaux Essais ap. Gerhardt V pagg. 458 sqq.) meritum Aristotelis extollit, sed ut clarum est hanc thesin admittit. Similiter HEGEL , Wissenschaft der Logik II I k. 3 Anmerkung. Werke (ed. 1834) pagg. 142 sq.',
    '[^6]: Ita bene A. RIEHL. Logik und Erkenntnistheorie in Kultur der Gegenwart Abt. VI ed. 3 (1921) pag. 71.',
    '[^7]: G. STAMMLER in Begriff, Urteil, Schlusz, Halle-Saale 1928, pagg. 229, 245.',
    '[^8]: « I believe the prime Number Theorem because of de la Vallée-Poussin\'s proof of it, but I do not believe that 2 + 2 = 4 because of the proof in Principia Mathematica ». G. H. HARDY, Mathematical proof in periodico Mind 38 (1929) pag. 17.',
    '[^9]: « Sind irgendeine endliche Anzahl von Punkten einer Geraden gegeben, so lassen sich dieselben stets in der Weise mit A, B, C, D, E, ..... K bezeichnen, dasz der mit B bezeichnete Punkt zwischen A einerseits und C, D, E, ..... K andererseits, ferner C zwischen A, B einerseits und D, E, .... K andererseits, sodann D zwischen A, B, C einerseits, und E, ..... K andererseits liegt. Ausser dieser Bezeichnungsweise gibt es nur noch die umgekehrte Bezeichnungsweise K ..... E, D, C, B, A, die von der nämlichen Beschaffenheit ist ». HILBERT, Grundlagen der Geometrie ed. 7 (1930) pag. 8.',
    '[^10]: Haec iam observata sunt a mathematico Hardy in articulo quem supra iam citavimus (Mind 38 pag. 12) : « If Hilbert has made the Hilbert mathematics with a particular sheet of paper, and I copy them on another sheet, have I made a new mathematics ? Surely it is the same mathematics, and that even if he writes in pencil and I in ink, and his marks are black while mine are red ». (« Si Hilbert construxit mathematicam hilbertianam in particulari folio papyraceo, et ego transcribo illam in alio folio, num construxi novam mathematicam ? Absque dubio est eadem mathematica, etiam si ipse utitur stilo plumbeo et ego atramento, et eius signa sunt nigra et mea rubra ». Hardy his verbis vult indicare necessitatem harum operationum et observationum, et causam huius necessitatis, quae est abstractio formalis intuitiva.',
    '[^11]: Cfr. communicationem nostram iam supra citatam Pour une philosophie de la connaissance de l\'étendue physique in Gregorianum, 1949, pagg. 193-203.',
    '[^12]: Quomodo propria physica obiectorum interdum impedire possint realisationem exactitudinis in corporibus pro uno casu explicavimus in Cosmologia in nota « de ente extenso physico » in ed. 4 pagg. 438-445.'
]

full_md_blocks = doc_header + formatted_blocks
full_md = "\n\n".join(full_md_blocks) + "\n\n---\n\n" + "\n\n".join(footnotes) + "\n"

out_path = os.path.join(root, "docs", "caput-5.md")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(full_md)

print(f"Wrote {out_path} successfully ({len(full_md)} bytes, {len(full_md_blocks)} blocks).")
