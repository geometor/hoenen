import os
import re

docsrc = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(docsrc)

chapter6_dir = os.path.join(root, 'chapter-06')

fn_map = {
    200: '1 « Qu\'on réalise',
    203: '2 De hac questione',
    206: '3 A. EINSTEIN',
    207: 'altro. Dunque senza',
    211: '4 In casibus physicis',
    212: 'bilibus propriis pagg. 508-517',
    216: '6 Adsunt exceptiones',
    221: '7 De his cfr.',
}

fn_replacements = {
    200: [('quo mensuramus » 1. Et ita', 'quo mensuramus » [^1]. Et ita')],
    203: [('menti 2.', 'menti [^2].')],
    206: [('tum est 3.', 'tum est [^3].')],
    211: [('intellectiva associata 4, nobis innotescit', 'intellectiva associata [^4], nobis innotescit')],
    212: [('§ 3. DE EXTENSIONE SUCCESSIVA 5.', '§ 3. DE EXTENSIONE SUCCESSIVA [^5].')],
    216: [('praecognosci debet 6. Operatio', 'praecognosci debet [^6]. Operatio')],
    221: [('actus per potentiam 7.', 'actus per potentiam [^7].')],
}

pages_text = {}
for p in range(195, 223):
    fname = os.path.join(chapter6_dir, f'page-{p:03d}.txt')
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

# Strip title block from page 195
p195 = pages_text[195]
idx195 = p195.find('Ex iis quae supra exponebamus')
assert idx195 != -1, 'Opening text not found in page 195'
pages_text[195] = p195[idx195:]

hyphen_page_boundaries = {200, 205, 208, 209, 210, 212, 213, 219, 220}
same_para_page_boundaries = {195, 197, 201, 203, 204, 207, 211, 214, 216, 217, 218}

joined_lines = []
for p in range(195, 223):
    raw_lines = pages_text[p].splitlines()
    lines = []
    for l in raw_lines:
        if not l.strip():
            continue
        lines.append(l.strip())

    if p > 195:
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

# Merge multi-line headings
i = 0
while i < len(joined_lines):
    if joined_lines[i] == '§ 1. ITERATA COMPARATIO GEOMETRIAE' and i+1 < len(joined_lines) and joined_lines[i+1] == 'EUCLIDICAE ET NON-EUCLIDICAE.':
        joined_lines[i] = '§ 1. ITERATA COMPARATIO GEOMETRIAE EUCLIDICAE ET NON-EUCLIDICAE.'
        del joined_lines[i+1]
    elif joined_lines[i] == '§ 2. DE EXTENSIONE UT EST SUBIECTUM' and i+1 < len(joined_lines) and joined_lines[i+1] == 'FUNDAMENTALE GEOMETRIAE.':
        joined_lines[i] = '§ 2. DE EXTENSIONE UT EST SUBIECTUM FUNDAMENTALE GEOMETRIAE.'
        del joined_lines[i+1]
    elif joined_lines[i] == 'C) De independentia relativa notionis extensionis ab expe-' and i+1 < len(joined_lines) and joined_lines[i+1] == 'rientia.':
        joined_lines[i] = 'C) De independentia relativa notionis extensionis ab experientia.'
        del joined_lines[i+1]
    i += 1

headings = {
    '§ 1. ITERATA COMPARATIO GEOMETRIAE EUCLIDICAE ET NON-EUCLIDICAE.': '## § 1. Iterata comparatio geometriae euclidicae et non-euclidicae.',
    '§ 2. DE EXTENSIONE UT EST SUBIECTUM FUNDAMENTALE GEOMETRIAE.': '## § 2. De extensione ut est subiectum fundamentale geometriae.',
    'A. De extensione corporum.': '### A. De extensione corporum.',
    'B) De spatio.': '### B) De spatio.',
    'C) De independentia relativa notionis extensionis ab experientia.': '### C) De independentia relativa notionis extensionis ab experientia.',
    '§ 3. DE EXTENSIONE SUCCESSIVA [^5].': '## § 3. De extensione successiva [^5].',
    '1. De ipsa notione et eius propriis.': '### 1. De ipsa notione et eius propriis.',
    '2. Conclusiones.': '### 2. Conclusiones.',
}

para_starts = [
    # P195
    'Ex iis quae supra exponebamus diversae sequuntur',
    'Dictum est (cfr. Gregorianum, 1951, pagg. 432 et 451) :',
    'Constat : si (praeter alia axiomata consueta) postulatum V',
    # P196
    'Constat igitur : si in extenso postulatum V valet, id',
    'Nunc autem haec structura extensionis, sive sit eucli-',
    'Et id fieri potest, immo debet. Nam haec structura',
    # P197
    'Notio directionis lineae relate ad « spatium » ambiens ad',
    'Notio haec directionis pertinet revera ad primitivas et',
    'Haec dein applicari potest (IV § 4 n. 4) ad comparandas',
    # P198
    'Nunc tantum ad hoc attendimus : De se extensio in',
    'Et addendum est, quia hoc interdum negatur : curva-',
    'Et ita videmus : subiectum fundamentale geometriarum',
    # P199
    'Nota. Hic adhuc inquirendum esset in illos casus in',
    'Ad hanc conclusionem perveneramus : « extensio » et',
    'Hanc positionem magis dilucidare debemus propter',
    'Opinio illa fortiter propugnatur a Poincaré ubi, sensu',
    # P200
    "Ait (La science et l'hypothèse ch. V n. 2 pag. 92) : « realize-",
    'Ex omnibus, quae supra dicta sunt, clarum est, non',
    'Haec dein a Poincaré magis evolvuntur, et in fine per-',
    'Quae citavimus sufficiunt, post omnia, quae supra vide-',
    # P201
    'Plus etiam dein inveniebamus, ea scil. quae respiciunt',
    # P202
    'Semel acquisitis primis hisce principiis exactitudinis',
    'Si hi casus debite considerantur, invenimus responsum',
    # P203
    'Non omnis usus termini « spatii » nec omnis usus no-',
    'Quomodo haec notio « spatii in quo corpora collocantur »',
    'Ex eis, quae in his libris exponuntur, patet : 1) in rea-',
    'Extensio ut est origo, subiectum fundamentale, geometriae',
    # P204
    'Sed dantur aliae proprietates extensionis corporum,',
    'Prima inter has proprietates iam supra (V § 4 n. 2 pag.',
    'In hac consideratione unum praesertim est clarum :',
    # P205
    'Contactus inter corpora, quem hucusque consideraba-',
    'Tale systema extensum integrale, quod vocari potest',
    'Sed vox « spatii » per excellentiam in alio sensu adhi-',
    # P206
    'Intuitiones, quas in hac paragrapho breviter (et alibi',
    'Sed eas iterum invenit Einstein in suis meditationibus',
    # P207
    'Et ita perfecte redimus ad doctrinam S. Thomae ;',
    'Hinc manifestum esse videtur, quod usus vocis « spatii »',
    'Origo geometriae est igitur empirica ; dependet ab ex-',
    'Id sese in reflexione etiam praescientifica manifestat.',
    # P208
    'Etiam alio modo haec differentia sese manifestat in',
    'Et etiam attendendum est : Haec differentia noetica',
    # P209
    'In intellectu igitur adest quaedam autonomia relate',
    'Ex eis quae inveniebamus, decisive iudicare possumus',
    'Saepe in investigando problemate, quomodo et in quo',
    # P210
    'Haec, quamquam sunt utilissima et pro scientia psy-',
    'Incipit, ut dictum est, investigatio in activitatem in-',
    # P211
    'Haec etiam clariora fiunt ex comparatione cum « casi-',
    'Salvari non potest in quantum mensurae figurarum et',
    # P212
    'Subiectum geometriae fundamentale est extensio cor-',
    # P213
    'In motu locali duplex invenitur extensio (praeter ex-',
    'In utroque casu duratio est quantitas stricte dicta,',
    'Possibilitas motuum inter se congruentium, quae supra',
    # P214
    'Haec convenientia inter extensionem linearum geome-',
    'Sed dantur quoque discrepantiae inter utramque ex-',
    '1. Fundamentalis differentia haec esse videtur : Dura-',
    '2. Extensio corporis, nobis ex datis sensuum nota, est',
    # P215
    'Haec omnia desunt in illa dimensione unidimensionali,',
    '3. Est et alia differentia inter utramque extensionem',
    # P216
    'Omnis quantitas — etiam quantitas virtutis — men-',
    'Et exprimitur ope numerorum i. e. numero (integro vel',
    '4. In considerando modo, quo haec operatio mensurandi',
    # P217
    'Simili modo duae durationes determinatae possunt esse',
    '5. Sed adsunt discrimina. Haec simultaneitas duratio-',
    '6. A parte rei, antecedenter ad observationem nostram,',
    # P218
    'Haec connexa sunt cum alio proprio in quo duratio',
    'Notio simultaneitatis est notio primitiva. Inde definitio-',
    # P219
    'Concludendo quaedam proponimus, quae momentum',
    'A) Exactitudo in relationibus chronometricis. In mensu-',
    'Haec in primis valorem habent in diiudicanda positione',
    'Indicamus unum experimentum huius generis, quod',
    # P220
    'B) Specimen particulare analogiae. Notiones extensionis',
    'Hic alius casus adest. Utriusque extensionis, tum sta-',
    'Ceterum similis casus analogiae iam in ipsa extensione',
    # P221
    'C) De chronotopo. Maior est discrepantia inter notiones',
    'Haec quae dicuntur de ipsa extensione, valent de eius',
    # P222
    'Inde diiudicare possumus conatus (ex primo tempore',
]

para_starts_set = set(para_starts)

paragraphs = []
cur_p = []
for idx, line in enumerate(joined_lines):
    if line in headings:
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
    "# CAPUT VI",
    "DE SUBIECTO FUNDAMENTALI GEOMETRIAE"
]

footnotes = [
    '[^1]: « Qu\'on réalise un cercle matériel, qu\'on en mesure le rayon et la circonférence, et qu\'on cherche à voir si le rapport de ces deux longueurs est égale à π, qu\'aura-t-on fait ? On aura fait une expérience, non sur les propriétés de l\'espace, mais sur celles de la matière avec laquelle on a réalisé ce rond et de celle dont est fait le mètre qui a servi aux mesures ».',
    '[^2]: De hac questione philosophica cfr. Cosmologiam nostram liber I cap. II in ed. 4 pagg. 64-134 ; Filosofia della natura inorganica, cap. III pagg. 93-142.',
    '[^3]: A. EINSTEIN in periodico Forum I 1930 pag. 173 ; cfr. Cosmologiam ed. 4 pag. 468, ubi textus originalis legi potest, et Filos. d. nat. inorg. pag. 110. Ex hoc transcribimus versionem italicam verborum Einstein : « Esso (lo spazio) presuppone la concezione del mondo corporeo oggettivo. Io posso riconoscere i corpi attraverso le loro caratteristiche sensibili, senza ancora concepirli come spaziali. Se si forma in questo modo il concetto dei corpi, l\'esperienza sensibile ci costringe a stabilire relazioni locali tra i corpi, cioè relazioni di mutuo contatto. Cio che noi indichiamo come relazioni spaziali tra i corpi non è niente altro. Dunque senza il concetto dei corpi nessun concetto di relazioni spaziali tra i corpi, e senza il concetto delle relazioni spaziali nessun concetto di spazio ». Sublineatio est nostra.',
    '[^4]: In casibus physicis quibusdam etiam talis intuitio invenitur, scilicet ubi de intensitate qualitatum agitur. De hac exceptione hic agere non possumus ; vide plura in Cosmologia ed. 4 notam de sensibilibus propriis pagg. 508-517, et in Gregorianum, 1948, pagg. 295-303.',
    '[^5]: De hac materia cfr. Gregorianum, 1953, pag. 3-31 De duratione successiva et de quaestionibus connexis.',
    '[^6]: Adsunt exceptiones ; in theoria « dimensionum physicarum » genus commune interdum derivari potest ex mensuris.',
    '[^7]: De his cfr. investigationem nostram De connexionibus necessariis inter actus existentiales in Gregorianum 1953 pagg. 603-31, praesertim pagg. 635, 637, infra in appendice.'
]

full_md_blocks = doc_header + formatted_blocks
full_md = "\n\n".join(full_md_blocks) + "\n\n---\n\n" + "\n\n".join(footnotes) + "\n"

out_path = os.path.join(root, "docs", "caput-6.md")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(full_md)

print(f"Wrote {out_path} successfully ({len(full_md)} bytes, {len(full_md_blocks)} blocks).")
