import re
import os

docsrc = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(docsrc)

fn_map = {
    1: '1 Vide articulum',
    7: '2 Nouveaux Essais',
    8: '3 Animadvertamus',
    11: '4 Kritik der',
    12: '5 Operae pretium',
    17: '7 Hic terminus',
    18: '8 De his cfr.',
    20: '9 In opere',
    22: '10 Haec exempla',
    25: '11 Hoc adagium',
    26: '12 Cfr. de hac',
    27: '13 De distinguendo',
    29: '14 Cfr. articulum',
    30: '16 In editione'
}

chapter2_dir = os.path.join(root, 'chapter-02')

pages_lines = []
for p in range(1, 39):
    book_p = p + 26
    fname = os.path.join(chapter2_dir, f'page-{book_p:03d}.txt')
    with open(fname) as f:
        text = f.read().rstrip()
    if p in fn_map:
        idx = text.find(fn_map[p])
        body = text[:idx].rstrip()
    else:
        body = text
    lines = [l.strip() for l in body.split('\n') if l.strip()]
    pages_lines.append(lines)

hyphen_boundaries = {5, 8, 10, 16, 17, 19, 23, 29, 30, 32, 33, 34, 35, 36}
same_para_boundaries = {4, 11, 13, 15, 20, 21, 22, 24, 25, 26, 27, 28, 37}

all_elements = []
for p_idx, lines in enumerate(pages_lines):
    p_num = p_idx + 1
    for l_idx, line in enumerate(lines):
        if l_idx == 0 and p_idx > 0:
            prev_p = p_idx
            if prev_p in hyphen_boundaries:
                prev_elem = all_elements.pop()
                assert prev_elem.endswith('-'), f"Expected hyphen at end of P{prev_p}: {prev_elem[-30:]}"
                merged = prev_elem[:-1] + line
                all_elements.append(merged)
                continue
            elif prev_p in same_para_boundaries:
                prev_elem = all_elements.pop()
                merged = prev_elem + " " + line
                all_elements.append(merged)
                continue
            elif prev_p == 7:
                all_elements.append(line)
                continue
        all_elements.append(line)

# Construct output markdown blocks
blocks = []
i = 0
while i < len(all_elements):
    el = all_elements[i]
    
    if el == "CAPUT II":
        blocks.append("# CAPUT II")
        i += 1
        continue
    if el == "DE PROBLEMATE NECESSITATIS":
        blocks.append("DE PROBLEMATE NECESSITATIS")
        i += 1
        continue
    if el == "Animadversiones praeviae.":
        blocks.append("*Animadversiones praeviae.*")
        i += 1
        continue
    if el.startswith("§ "):
        blocks.append(f"## {el}")
        i += 1
        continue
    if re.match(r'^[1-9]\.\s+[A-Z«]', el):
        blocks.append(f"### {el}")
        i += 1
        continue
        
    # Pebble rows
    if el.startswith("1  3  5 .....") and i + 1 < len(all_elements) and all_elements[i+1].startswith("2  4  6 ....."):
        blocks.append(f"{all_elements[i]}  \n{all_elements[i+1]}")
        i += 2
        continue
        
    if el.startswith("1  4  7 .....") and i + 2 < len(all_elements) and all_elements[i+1].startswith("2  5  8 .....") and all_elements[i+2].startswith("3  6  9 ....."):
        blocks.append(f"{all_elements[i]}  \n{all_elements[i+1]}  \n{all_elements[i+2]}")
        i += 3
        continue
        
    # Leibniz Demonstration
    if el == "« Démonstration :" and i + 4 < len(all_elements) and "Donc (par l'axiome)" in all_elements[i+4]:
        quote_block = (
            f"{all_elements[i]}  \n"
            f"{all_elements[i+1]}  \n"
            f"{all_elements[i+2]}  \n"
            f"{all_elements[i+3]}  \n"
            f"{all_elements[i+4]}"
        )
        blocks.append(quote_block)
        i += 5
        continue
        
    blocks.append(el)
    i += 1

footnotes = [
    "[^1]: Vide articulum nostrum De origine primorum principiorum scientiae apud Gregorianum XIV (1933) pagg. 153-184.",
    ("[^2]: Nouveaux Essais sur l'entendement L. IV Ch. VII § 10\n"
     "    « Définitions 1) deux est un et un\n"
     "    2) trois est deux et un\n"
     "    3) quatre est trois et un\n"
     "    Axiome; mettant des choses égales à la place, l'égalité demeure »."),
    "[^3]: Animadvertamus « axioma » non semel sed in singulis gressibus applicari. Simili modo procedit Couturat in Rev. Mét. et Mor. 1904 pag. 339.",
    "[^4]: Kritik der reinen Vernunft ed. 2 pagg. 14-15 « Zuvörderst musz bemerkt werden dasz eigentliche mathematische Sätze jederzeit Urtheile a priori und nicht empirisch sind, weil sie Notwendigkeit bei sich führen, welche aus Erfahrung nicht abgenommen werden kann ». Idem ad litteram passus in Proleg. § 2 c n. 2.",
    "[^5]: Operae pretium esset investigare historiam huius infelicis principii.",
    "[^6]: De hac doctrina vide opus supra citatum La théorie du jugement d'après St. Thomas d'Aquin passim.",
    "[^7]: Hic terminus a Cartesio adhibetur ad describendam hanc proprietatem corporis ut talis Principia Philos. II n. 64.",
    "[^8]: De his cfr. nostram communicationem in congresso philosophica Amstelodamensi anni 1948, Pour une philosophie de la connaissance de l'étendu physique in Gregorianum 1949 pagg. 193-203.",
    "[^9]: In opere Vorlesungen über neuere Geometrie. In editione altera (1926) axioma, ad quod alludimus, invenitur pag. 20 (IV Kernsatz).",
    "[^10]: Haec exempla simul cum comparatione cum iudiciis physicis iam habentur apud Hessenberg Kritik und System in Mathematik und Philosophie in Abhandlungen der Friesschen Schule II pagg. 102-106. Folium Moebii est exemplum valde simplex in hoc genere. Idem auctor (pag. 105) narrat universitatem technicam Berolinensem (Charlottenburg) possidere imagines (modelli), superficierum multo magis complicatarum, quae a mathematico Stahl ex materia elastica confectae sunt, et dein sectione divisae. In his superficiebus « connexus » est tam complicatus, ut nullus homo ex sola inspectione phantasmatis praedicere possit quid resultaturum sit ex scissione. Videtur idem Stahl descripsisse suas indagationes sub titulo de iudiciis experimentalibus mathematicis (mathematische Erfahrungssätze).",
    "[^11]: Hoc adagium mitigandum est per additum : « nisi ipse intellectus ». Id tribuitur Leibnizio, et iure quidem. Sed invenitur iam apud S. Thomam. Cfr. Théorie du Jugement ed. 2 pagg. 214-215.",
    "[^12]: Cfr. de hac re articulum nostrum in libro commemorativo Universitatis catholicae Mediolanensis Cartesio (1937) cui titulus Le « Cogito ergo sum » comme intuition et comme mouvement de la pensée pagg. 457-471.",
    "[^13]: De distinguendo « determinativo » a « motivo » vide Théorie du Jug. ed. 2 pagg. 25 sqq.",
    "[^14]: Cfr. articulum supra iam citatum Le « Cogito ergo sum » comme intuition et comme mouvement de la pensée.",
    "[^15]: Haec theoria per longum et latum exponitur in singulis fere capitibus operis nostri supra iam citati La théorie du jugement d'après St. Thomas d'Aquin.",
    "[^16]: In editione altera (1926) eius operis, supra (pag. 46) iam citati, inveniuntur pagg. 5-8, 19 sq.",
    "[^17]: De his cfr. Théor. du jug. ch. III et IV."
]

full_md = "\n\n".join(blocks) + "\n\n---\n\n" + "\n\n".join(footnotes) + "\n"

out_path = os.path.join(root, "docs", "caput-2.md")
with open(out_path, "w") as f:
    f.write(full_md)

print(f"Wrote {out_path} successfully ({len(full_md)} bytes).")
