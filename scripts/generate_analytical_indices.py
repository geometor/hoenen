#!/usr/bin/env python3
"""
scripts/generate_analytical_indices.py

Generates the bilingual Analytical Index (Index Analyticus):
1. docs/end-index/end_index.md (Latin)
2. docs/end-index/end_index-en.md (English)

Features:
- Removes raw dot leaders and book page numbers.
- Structures every entry as a nested Markdown list item for clean line breaks.
- Directly hyperlinks each entry to its exact heading anchor in the chapter HTML file.
- Preserves bilingual titles (English entry + Latin subtitle in parens) in the English edition.
- Maintains 100% 1-to-1 structural symmetry across chapters.
"""

import os
import re
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
END_INDEX_DIR = os.path.join(DOCS_DIR, 'end-index')

CHAPTER_SECTIONS = [
    {
        'id': 'caput-1',
        'en_title': 'Chapter I. - On the Origin of Geometric Cognition and Its Problematic',
        'la_title': 'Caput I. - De origine cognitionis geometricae et de eius problematica',
        'en_file': 'caput-1/caput-1-en.html',
        'la_file': 'caput-1/caput-1.html'
    },
    {
        'id': 'caput-2',
        'en_title': 'Chapter II. - On the Problem of Necessity',
        'la_title': 'Caput II. - De problemate necessitatis',
        'en_file': 'caput-2/caput-2-en.html',
        'la_file': 'caput-2/caput-2.html'
    },
    {
        'id': 'caput-3',
        'en_title': 'Chapter III. - On the Problem of Exactitude. Part I: On the Existence of Indivisibles',
        'la_title': 'Caput III. - De problemate exactitudinis. Pars I. - De existentia indivisibilium',
        'en_file': 'caput-3/caput-3-en.html',
        'la_file': 'caput-3/caput-3.html'
    },
    {
        'id': 'caput-4',
        'en_title': 'Chapter IV. - On the Problem of Exactitude. Part II: On Exact Figures and Relations',
        'la_title': 'Caput IV. - De problemate exactitudinis. Pars II. - De figuris et relationibus exactis',
        'en_file': 'caput-4/caput-4-en.html',
        'la_file': 'caput-4/caput-4.html'
    },
    {
        'id': 'caput-5',
        'en_title': 'Chapter V. - On Axiomatics',
        'la_title': 'Caput V. - De Axiomatica',
        'en_file': 'caput-5/caput-5-en.html',
        'la_file': 'caput-5/caput-5.html'
    },
    {
        'id': 'caput-6',
        'en_title': 'Chapter VI. - On the Fundamental Subject of Geometry',
        'la_title': 'Caput VI. - De subjecto fundamentali geometriae',
        'en_file': 'caput-6/caput-6-en.html',
        'la_file': 'caput-6/caput-6.html'
    },
    {
        'id': 'caput-7',
        'en_title': 'Chapter VII. - On Extension as Intelligible Matter',
        'la_title': 'Caput VII. - De extensione ut est materia intelligibilis',
        'en_file': 'caput-7/caput-7-en.html',
        'la_file': 'caput-7/caput-7.html'
    },
    {
        'id': 'appendix',
        'en_title': 'APPENDIX: On Necessary Connections Between Existential Acts',
        'la_title': 'APPENDIX: De connexionibus necessariis inter actus existentiales',
        'en_file': 'appendix/appendix-en.html',
        'la_file': 'appendix/appendix.html'
    }
]

def norm(s):
    s = s.replace('’', "'").replace('“', '"').replace('”', '"').replace('«', '"').replace('»', '"')
    s = re.sub(r'\[\^[^\]]+\]', '', s)
    s = re.sub(r'[*_`]', '', s)
    return s.strip().lower()

def kramdown_slug(text):
    t = re.sub(r'\[\^[^\]]+\]', '', text)
    t = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', t)
    t = re.sub(r'[*_`]', '', t).strip()
    t_lower = t.lower().replace("'", "").replace("’", "")
    
    res = ''
    for char in t_lower:
        if char.isalnum() or char == '-':
            res += char
        elif char in [' ', '.', ':', ';', ',', '?', '!', '"', '«', '»', '(', ')', '[', ']', '$', '=', '+']:
            res += '-'
        else:
            res += '-'
    res = re.sub(r'-+', '-', res)
    res = res.strip('-')
    return res

def parse_english_index_entries():
    raw_path = os.path.join(END_INDEX_DIR, 'end_index-en.md')
    with open(raw_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    roman_map = {
        'I': 'caput-1', 'II': 'caput-2', 'III': 'caput-3', 'IV': 'caput-4',
        'V': 'caput-5', 'VI': 'caput-6', 'VII': 'caput-7'
    }

    cur_ch = None
    entries = []

    for line in lines:
        if line.startswith('###'):
            if 'Preface' in line:
                cur_ch = 'preface'
            elif 'APPENDIX' in line:
                cur_ch = 'appendix'
            else:
                m = re.search(r'Chapter\s+([IVXLCDM]+)', line)
                if m:
                    cur_ch = roman_map[m.group(1)]
            continue
        if not line.strip().startswith('*') or not cur_ch or cur_ch == 'preface':
            continue
        
        indent = len(line) - len(line.lstrip())
        content = line.strip().lstrip('*').strip()
        
        # Strip any existing links for idempotency
        while re.search(r'\[([^\[\]]+)\]\([^\)]+\)', content):
            content = re.sub(r'\[([^\[\]]+)\]\([^\)]+\)', r'\1', content)
            
        content_clean = re.sub(r'[\s\.]+\d+\s*$', '', content).strip()
        
        m = re.match(r'^(.*?)\s*\*\((.*?)\)\*$', content_clean)
        if m:
            en_title = m.group(1).strip()
            la_title = m.group(2).strip()
        else:
            en_title = content_clean
            la_title = content_clean
        
        # Normalize special entries
        if en_title.startswith('*Preliminary Remarks'):
            en_title = 'Preliminary Remarks'
            la_title = 'Animadversiones praeviae'
        elif en_title == '*Conspectus*':
            en_title = 'Conspectus'
            la_title = 'Conspectus'
        elif en_title == '*Recapitulation*':
            en_title = 'Recapitulation'
            la_title = 'Recapitulatio'
        elif en_title == '*Note on Neo-Positivism*':
            en_title = 'Note on Neo-Positivism'
            la_title = 'Nota de neo-positivismo'
        elif en_title == '*Additions*':
            en_title = 'Additions'
            la_title = 'Additiones'
        
        entries.append({
            'ch': cur_ch,
            'indent': indent,
            'en': en_title,
            'la': la_title
        })

    return entries

def get_markdown_headings(fpath):
    heads = []
    with open(fpath, encoding='utf-8') as f:
        for line in f:
            m = re.match(r'^(#{1,6})\s+(.*)$', line.strip())
            if m:
                level = len(m.group(1))
                txt = m.group(2).strip()
                if txt.startswith('CHAPTER') or txt.startswith('CAPUT') or txt == 'Footnotes' or txt == 'APPENDIX':
                    continue
                if txt in [
                    'ON THE PROBLEM OF EXACTITUDE', 'DE PROBLEMATE EXACTITUDINIS',
                    'ON THE PROBLEM OF NECESSITY', 'DE PROBLEMATE NECESSITATIS',
                    'ON THE ORIGIN OF GEOMETRIC KNOWLEDGE', 'DE ORIGINE COGNITIONIS GEOMETRICAE',
                    'AND ITS PROBLEMATICS', 'ET DE EIUS PROBLEMATICA',
                    'ON AXIOMATICS', 'DE AXIOMATICA',
                    'ON THE FUNDAMENTAL SUBJECT OF GEOMETRY', 'DE SUBIECTO FUNDAMENTALI GEOMETRIAE',
                    'ON EXTENSION', 'DE EXTENSIONE',
                    'AS INTELLIGIBLE MATTER', 'UT EST MATERIA INTELLIGIBILIS',
                    'ON THE NECESSARY CONNECTIONS', 'DE CONNEXIONIBUS NECESSARIIS',
                    'BETWEEN EXISTENTIAL ACTS', 'INTER ACTUS EXISTENTIALES',
                    'PART I', 'PARS I',
                    'ON THE EXISTENCE OF INDIVISIBLES', 'DE EXISTENTIA INDIVISIBILIUM',
                    'PART II', 'PARS II',
                    'ON EXACT FIGURES AND RELATIONS', 'DE FIGURIS ET RELATIONIBUS EXACTIS'
                ]:
                    continue
                heads.append((level, txt))
    return heads

def build_indices():
    entries = parse_english_index_entries()

    # Load live_ids if available
    live_ids_path = '/home/phi/.gemini/antigravity/brain/85f0c79d-92f0-4820-a283-c3a9fec40013/scratch/heading_ids.json'
    live_ids = {'en': {}, 'la': {}}
    if os.path.exists(live_ids_path):
        with open(live_ids_path, 'r', encoding='utf-8') as f:
            live_ids = json.load(f)

    # 1. Generate English Index
    en_lines = [
        "# ANALYTICAL INDEX (TABLE OF CONTENTS)",
        "",
        "*(Index Analyticus, pp. 289–293)*",
        "",
        "---",
        "",
        "### [Preface](../preface/preface-en.html) *(Praefatio)*",
        ""
    ]

    # 2. Generate Latin Index
    la_lines = [
        "# INDEX ANALYTICUS",
        "",
        "*(pp. 289–293)*",
        "",
        "---",
        "",
        "### [Praefatio](../preface/preface.html)",
        ""
    ]

    for sec in CHAPTER_SECTIONS:
        ch = sec['id']
        en_lines.append("---")
        en_lines.append("")
        en_lines.append(f"### [{sec['en_title']}](../{sec['en_file']}) *({sec['la_title']})*")

        la_lines.append("---")
        la_lines.append("")
        la_lines.append(f"### [{sec['la_title']}](../{sec['la_file']})")

        ch_ents = [e for e in entries if e['ch'] == ch]
        en_heads = get_markdown_headings(os.path.join(DOCS_DIR, ch, f"{ch}-en.md"))
        la_heads = get_markdown_headings(os.path.join(DOCS_DIR, ch, f"{ch}.md"))

        if len(ch_ents) != len(en_heads) or len(ch_ents) != len(la_heads):
            raise ValueError(f"Heading count mismatch in {ch}: entries={len(ch_ents)}, en={len(en_heads)}, la={len(la_heads)}")

        live_en_dict = {norm(h[2]): h[1] for h in live_ids['en'].get(ch, [])}
        live_la_dict = {norm(h[2]): h[1] for h in live_ids['la'].get(ch, [])}

        for i, e in enumerate(ch_ents):
            indent_str = " " * e['indent']
            en_txt = en_heads[i][1]
            la_txt = la_heads[i][1]

            hid_en = live_en_dict.get(norm(en_txt)) or kramdown_slug(en_txt)
            hid_la = live_la_dict.get(norm(la_txt)) or kramdown_slug(la_txt)

            en_link = f"../{sec['en_file']}#{hid_en}"
            en_title = e['en']
            la_title = e['la']

            # Extract numbering prefix from en_title if not already present on la_title
            m_pfx = re.match(r'^(\*?\*?§\s*\d+\.\*?\*?|\d+\.\s*-?|[A-D]\.\s*-?)\s*', en_title)
            pfx = m_pfx.group(0) if m_pfx else ''
            if pfx and not la_title.startswith(pfx.strip()):
                la_display = f"{pfx}{la_title}"
            else:
                la_display = la_title

            en_line = f"{indent_str}* [{en_title}]({en_link}) *({la_title})*"
            la_line = f"{indent_str}* [{la_display}](../{sec['la_file']}#{hid_la})"

            en_lines.append(en_line)
            la_lines.append(la_line)

        en_lines.append("")
        la_lines.append("")

    # Write files
    en_path = os.path.join(END_INDEX_DIR, 'end_index-en.md')
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(en_lines).rstrip() + "\n")
    print(f"Generated {en_path} ({len(en_lines)} lines)")

    la_path = os.path.join(END_INDEX_DIR, 'end_index.md')
    with open(la_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(la_lines).rstrip() + "\n")
    print(f"Generated {la_path} ({len(la_lines)} lines)")

if __name__ == '__main__':
    build_indices()
