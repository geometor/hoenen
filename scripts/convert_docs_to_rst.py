#!/usr/bin/env python3
"""
scripts/convert_docs_to_rst.py

Deterministic converter that transforms the curated Markdown files in `docs/`
into pure Sphinx / `photon-platform/publish` reStructuredText in `docsrc/`
with canonical cross-reference labels (`.. _label:`) and `:ref:` links.
"""

import os
import re
import sys
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
DOCS_DIR = os.path.join(BASE_DIR, "docs")
DOCSRC_DIR = os.path.join(BASE_DIR, "docsrc")

CHAPTER_META = [
    {
        "id": "preface",
        "num": None,
        "la_short": "Praefatio",
        "en_short": "Preface",
        "la_title": "Praefatio",
        "en_title": "Preface",
        "has_summary": False,
    },
    {
        "id": "caput-1",
        "num": 1,
        "la_short": "Caput I",
        "en_short": "Chapter I",
        "la_title": "Caput I. - De origine cognitionis geometricae et de eius problematica",
        "en_title": "Chapter I. - On the Origin of Geometric Cognition and Its Problematic",
        "has_summary": True,
    },
    {
        "id": "caput-2",
        "num": 2,
        "la_short": "Caput II",
        "en_short": "Chapter II",
        "la_title": "Caput II. - De problemate necessitatis",
        "en_title": "Chapter II. - On the Problem of Necessity",
        "has_summary": True,
    },
    {
        "id": "caput-3",
        "num": 3,
        "la_short": "Caput III",
        "en_short": "Chapter III",
        "la_title": "Caput III. - De problemate exactitudinis. Pars I. - De existentia indivisibilium",
        "en_title": "Chapter III. - On the Problem of Exactitude. Part I: On the Existence of Indivisibles",
        "has_summary": True,
    },
    {
        "id": "caput-4",
        "num": 4,
        "la_short": "Caput IV",
        "en_short": "Chapter IV",
        "la_title": "Caput IV. - De problemate exactitudinis. Pars II. - De figuris et relationibus exactis",
        "en_title": "Chapter IV. - On the Problem of Exactitude. Part II: On Exact Figures and Relations",
        "has_summary": True,
    },
    {
        "id": "caput-5",
        "num": 5,
        "la_short": "Caput V",
        "en_short": "Chapter V",
        "la_title": "Caput V. - De Axiomatica",
        "en_title": "Chapter V. - On Axiomatics",
        "has_summary": True,
    },
    {
        "id": "caput-6",
        "num": 6,
        "la_short": "Caput VI",
        "en_short": "Chapter VI",
        "la_title": "Caput VI. - De subiecto fundamentali geometriae",
        "en_title": "Chapter VI. - On the Fundamental Subject of Geometry",
        "has_summary": True,
    },
    {
        "id": "caput-7",
        "num": 7,
        "la_short": "Caput VII",
        "en_short": "Chapter VII",
        "la_title": "Caput VII. - De extensione ut est materia intelligibilis",
        "en_title": "Chapter VII. - On Extension as Intelligible Matter",
        "has_summary": True,
    },
    {
        "id": "appendix",
        "num": 8,
        "la_short": "Appendix",
        "en_short": "Appendix",
        "la_title": "APPENDIX: De connexionibus necessariis inter actus existentiales",
        "en_title": "APPENDIX: On Necessary Connections Between Existential Acts",
        "has_summary": True,
    },
]

SUBTITLE_TEXTS = {
    "ON THE PROBLEM OF EXACTITUDE",
    "DE PROBLEMATE EXACTITUDINIS",
    "ON THE PROBLEM OF NECESSITY",
    "DE PROBLEMATE NECESSITATIS",
    "ON THE ORIGIN OF GEOMETRIC KNOWLEDGE",
    "DE ORIGINE COGNITIONIS GEOMETRICAE",
    "AND ITS PROBLEMATICS",
    "ET DE EIUS PROBLEMATICA",
    "ON AXIOMATICS",
    "DE AXIOMATICA",
    "ON THE FUNDAMENTAL SUBJECT OF GEOMETRY",
    "DE SUBIECTO FUNDAMENTALI GEOMETRIAE",
    "ON EXTENSION",
    "DE EXTENSIONE",
    "AS INTELLIGIBLE MATTER",
    "UT EST MATERIA INTELLIGIBILIS",
    "ON THE NECESSARY CONNECTIONS",
    "DE CONNEXIONIBUS NECESSARIIS",
    "BETWEEN EXISTENTIAL ACTS",
    "INTER ACTUS EXISTENTIALES",
    "PART I",
    "PARS I",
    "ON THE EXISTENCE OF INDIVISIBLES",
    "DE EXISTENTIA INDIVISIBILIUM",
    "PART II",
    "PARS II",
    "ON EXACT FIGURES AND RELATIONS",
    "DE FIGURIS ET RELATIONIBUS EXACTIS",
}

RST_BAR_CHARS = {
    1: "=",
    2: "-",
    3: "~",
    4: "^",
    5: '"',
}


def is_chapter_banner_heading(txt: str) -> bool:
    t = txt.strip()
    if t.startswith("CHAPTER") or t.startswith("CAPUT") or t in ("APPENDIX", "PRAEFATIO", "PREFACE"):
        return True
    if t in SUBTITLE_TEXTS:
        return True
    return False


def kramdown_slug(text: str) -> str:
    t = re.sub(r"\[\^[^\]]+\]", "", text)
    t = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", t)
    t = re.sub(r"[*_`]", "", t).strip()
    t_lower = t.lower().replace("'", "").replace("’", "")
    res = ""
    for char in t_lower:
        if char.isalnum() or char == "-":
            res += char
        else:
            res += "-"
    res = re.sub(r"-+", "-", res).strip("-")
    return res


def get_content_headings(fpath: str):
    heads = []
    with open(fpath, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^(#{1,6})\s+(.*)$", line.strip())
            if m:
                level = len(m.group(1))
                txt = m.group(2).strip()
                if is_chapter_banner_heading(txt) or txt == "Footnotes":
                    continue
                heads.append((level, txt))
    return heads


def compute_section_labels_and_levels(ch: str, lang: str, heads):
    """
    Returns a list of (canonical_label, rst_level, raw_heading_text) for each content heading
    in `heads`.
    """
    cur_s = None
    cur_num = None
    result = []
    for _md_level, txt in heads:
        t = txt.strip()
        m_sec = re.match(r"^§\s*(\d+)\.", t)
        m_num = re.match(r"^(\d+)\.", t)
        m_let = re.match(r"^([A-D])[\.\)]\s+", t)
        if m_sec:
            cur_s = f"s{m_sec.group(1)}"
            cur_num = None
            lbl = f"{ch}-{lang}-{cur_s}"
            rst_lvl = 2
        elif cur_s is None:
            lbl = f"{ch}-{lang}-prelim"
            rst_lvl = 2
        elif m_num:
            cur_num = m_num.group(1)
            lbl = f"{ch}-{lang}-{cur_s}-{cur_num}"
            rst_lvl = 3
        elif m_let:
            let = m_let.group(1).lower()
            if cur_num:
                lbl = f"{ch}-{lang}-{cur_s}-{cur_num}-{let}"
                rst_lvl = 4
            else:
                lbl = f"{ch}-{lang}-{cur_s}-{let}"
                rst_lvl = 3
        else:
            tl = t.lower()
            if "conspectus" in tl:
                slug = "conspectus"
            elif "recapitulatio" in tl:
                slug = "recap"
            elif "positivism" in tl:
                slug = "nota"
            elif "addition" in tl:
                slug = "additions"
            else:
                slug = re.sub(r"[^a-z0-9]+", "-", tl).strip("-")
            if cur_num:
                lbl = f"{ch}-{lang}-{cur_s}-{cur_num}-{slug}"
                rst_lvl = 4
            else:
                lbl = f"{ch}-{lang}-{cur_s}-{slug}"
                rst_lvl = 3
        result.append((lbl, rst_lvl, txt))
    return result


def build_url_to_ref_map():
    """Build a comprehensive lookup mapping Markdown internal links to canonical RST labels."""
    url_map = {
        "index.html": "hoenen-index",
        "../index.html": "hoenen-index",
        "bibliography.html": "bibliography",
        "../bibliography.html": "bibliography",
        "agent-chronicle.html": "agent-chronicle",
        "../agent-chronicle.html": "agent-chronicle",
        "scan-inventory.html": "scan-inventory",
        "../scan-inventory.html": "scan-inventory",
        "about/peter-hoenen.html": "about-peter-hoenen",
        "../about/peter-hoenen.html": "about-peter-hoenen",
        "about/analecta-gregorian.html": "about-analecta-gregoriana",
        "../about/analecta-gregorian.html": "about-analecta-gregoriana",
        "about/pontifical-gregorian-university.html": "about-gregorian-university",
        "../about/pontifical-gregorian-university.html": "about-gregorian-university",
        "about/pdf-parsing-guide.html": "about-pdf-parsing-guide",
        "../about/pdf-parsing-guide.html": "about-pdf-parsing-guide",
        "preface/preface.html": "preface-la",
        "../preface/preface.html": "preface-la",
        "preface/preface-en.html": "preface-en",
        "../preface/preface-en.html": "preface-en",
        "preface-en-3.1.md": "preface-en-3-1",
        "caput-1-en-3.1.md": "caput-1-en-3-1",
        "preface/translation-notes-preface.html": "preface-notes",
        "../preface/translation-notes-preface.html": "preface-notes",
        "end-index/end_index.html": "end-index-la",
        "../end-index/end_index.html": "end-index-la",
        "end-index/end_index-en.html": "end-index-en",
        "../end-index/end_index-en.html": "end-index-en",
        "#alphabetical-index-of-authors": "bib-alphabetical-index-of-authors",
        "#chronological-bibliography-ordered-by-death-date": "bib-chronological-bibliography-ordered-by-death-date",
    }

    # Author anchors in bibliography.md
    bib_path = os.path.join(DOCS_DIR, "bibliography.md")
    with open(bib_path, encoding="utf-8") as f:
        for m in re.finditer(r'<a id="([^"]+)"></a>', f.read()):
            slug = m.group(1)
            url_map[f"#{slug}"] = f"bib-{slug}"

    # Chapter & section anchors
    for meta in CHAPTER_META:
        ch = meta["id"]
        url_map[f"{ch}/{ch}.html"] = f"{ch}-la"
        url_map[f"../{ch}/{ch}.html"] = f"{ch}-la"
        url_map[f"{ch}.html"] = f"{ch}-la"
        url_map[f"{ch}/{ch}-en.html"] = f"{ch}-en"
        url_map[f"../{ch}/{ch}-en.html"] = f"{ch}-en"
        url_map[f"{ch}-en.html"] = f"{ch}-en"
        if meta["has_summary"]:
            url_map[f"{ch}/{ch}-summary.html"] = f"{ch}-summary"
            url_map[f"../{ch}/{ch}-summary.html"] = f"{ch}-summary"
        notes_name = f"translation-notes-{ch}.html"
        url_map[f"{ch}/{notes_name}"] = f"{ch}-notes"
        url_map[f"../{ch}/{notes_name}"] = f"{ch}-notes"

        # Footnotes
        for lang, suffix in [("la", ""), ("en", "-en")]:
            md_file = os.path.join(DOCS_DIR, ch, f"{ch}{suffix}.md")
            if os.path.exists(md_file):
                with open(md_file, encoding="utf-8") as f:
                    content = f.read()
                for fn_num in re.findall(r"^\[\^(\d+)\]:", content, re.M):
                    lbl = f"{ch}-{lang}-fn{fn_num}"
                    url_map[f"{ch}/{ch}{suffix}.html#fn:{fn_num}"] = lbl
                    url_map[f"../{ch}/{ch}{suffix}.html#fn:{fn_num}"] = lbl
                    url_map[f"{ch}{suffix}.html#fn:{fn_num}"] = lbl

        if ch == "preface":
            continue

        for lang, suffix in [("la", ""), ("en", "-en")]:
            md_file = os.path.join(DOCS_DIR, ch, f"{ch}{suffix}.md")
            heads = get_content_headings(md_file)
            sec_info = compute_section_labels_and_levels(ch, lang, heads)
            for lbl, _lvl, htxt in sec_info:
                slug1 = kramdown_slug(htxt)
                slug2 = slug1.lstrip("-")
                for s in {slug1, slug2}:
                    url_map[f"{ch}/{ch}{suffix}.html#{s}"] = lbl
                    url_map[f"../{ch}/{ch}{suffix}.html#{s}"] = lbl
                    url_map[f"{ch}{suffix}.html#{s}"] = lbl

    # Also map links from end_index.md and end_index-en.md directly by index position
    from scripts.generate_analytical_indices import CHAPTER_SECTIONS, parse_english_index_entries
    entries = parse_english_index_entries()
    for sec in CHAPTER_SECTIONS:
        ch = sec["id"]
        ch_ents = [e for e in entries if e["ch"] == ch]
        en_info = compute_section_labels_and_levels(
            ch, "en", get_content_headings(os.path.join(DOCS_DIR, ch, f"{ch}-en.md"))
        )
        la_info = compute_section_labels_and_levels(
            ch, "la", get_content_headings(os.path.join(DOCS_DIR, ch, f"{ch}.md"))
        )
        sec_en_idx = [
            m.group(2)
            for m in re.finditer(
                rf"\[([^\[\]]+)\]\((\.\./{ch}/{ch}-en\.html#[^\)]+)\)",
                open(os.path.join(DOCS_DIR, "end-index", "end_index-en.md")).read(),
            )
        ]
        sec_la_idx = [
            m.group(2)
            for m in re.finditer(
                rf"\[([^\[\]]+)\]\((\.\./{ch}/{ch}\.html#[^\)]+)\)",
                open(os.path.join(DOCS_DIR, "end-index", "end_index.md")).read(),
            )
        ]
        for u, (lbl, _, _) in zip(sec_en_idx, en_info):
            url_map[u] = lbl
            url_map[u.replace("../", "")] = lbl
        for u, (lbl, _, _) in zip(sec_la_idx, la_info):
            url_map[u] = lbl
            url_map[u.replace("../", "")] = lbl

    # Special aliases used in bibliography.md and *-summary.md
    special_aliases = {
        "appendix/appendix-en.html#2-velocity-intensity-and-nicole-oresmes-configurations": "appendix-en-s7-additions",
        "appendix/appendix-en.html#3-permanent-qualities-and-modes-of-inherence": "appendix-en-s7-additions",
        "appendix/appendix-en.html#4-contact-aggregates-imitating-essential-continua": "appendix-en-s7-additions",
        "appendix/appendix-en.html#is-esse-conceptualizable": "appendix-en-s7",
        "appendix/appendix-en.html#the-abstract-concept-of-being-ratio-essendi": "appendix-en-s7",
        "appendix/appendix-en.html#the-diversity-of-modes-of-being-act-determined-by-potency": "appendix-en-s7",
        "caput-2/caput-2-en.html#6-on-the-section-of-a-cylinder-and-the-mobius-strip": "caput-2-en-s2-6",
        "caput-2.html#de-problemate-necessitatis": "caput-2-la-prelim",
        "caput-3.html#de-problemate-exactitudinis": "caput-3-la",
        "caput-4.html#de-problemate-exactitudinis": "caput-4-la-prelim",
    }
    url_map.update(special_aliases)
    return url_map


def make_track_nav_rst(ch_id: str, active_track: str) -> list[str]:
    """Generate a cross-track navigation bar container in RST."""
    idx = next((i for i, m in enumerate(CHAPTER_META) if m["id"] == ch_id), None)
    if idx is None:
        return []
    meta = CHAPTER_META[idx]

    tracks = [
        ("la", "Latin", f"{ch_id}-la"),
        ("en", "English", f"{ch_id}-en"),
    ]
    if meta["has_summary"]:
        tracks.append(("summary", "Summary", f"{ch_id}-summary"))
    tracks.append(("notes", "Notes", f"{ch_id}-notes"))

    track_parts = []
    for t_key, t_label, t_ref in tracks:
        if t_key == active_track:
            track_parts.append(f"**{t_label}**")
        else:
            track_parts.append(f":ref:`{t_label} <{t_ref}>`")

    nav_parts = []
    nav_parts.append(":ref:`Conspectus <hoenen-index>`")
    if idx > 0:
        prev_meta = CHAPTER_META[idx - 1]
        prev_id = prev_meta["id"]
        prev_track = active_track if (active_track != "summary" or prev_meta["has_summary"]) else "en"
        prev_lbl = prev_meta["la_short"] if active_track == "la" else prev_meta["en_short"]
        nav_parts.append(f":ref:`← {prev_lbl} <{prev_id}-{prev_track}>`")
    if idx + 1 < len(CHAPTER_META):
        next_meta = CHAPTER_META[idx + 1]
        next_id = next_meta["id"]
        next_track = active_track if (active_track != "summary" or next_meta["has_summary"]) else "en"
        next_lbl = next_meta["la_short"] if active_track == "la" else next_meta["en_short"]
        nav_parts.append(f":ref:`{next_lbl} → <{next_id}-{next_track}>`")

    idx_ref = "end-index-la" if active_track == "la" else "end-index-en"
    nav_parts.append(f":ref:`Index Analyticus <{idx_ref}>`")
    nav_parts.append(":ref:`Bibliography <bibliography>`")

    return [
        ".. container:: track-nav",
        "",
        "   " + " · ".join(track_parts) + " | " + " · ".join(nav_parts),
        "",
    ]


def convert_inline(
    text: str,
    url_map: dict,
    strip_links_for_heading: bool = False,
    defined_fns: set[str] | None = None,
) -> str:
    """Convert Markdown inline syntax (code, links, footnotes, bold-italic) to clean RST."""
    # 1. Protect inline code spans `...` (and **`...`**) with placeholders
    code_placeholders = []

    def save_code(m):
        inner = m.group(1)
        idx = len(code_placeholders)
        code_placeholders.append(f"``{inner}``")
        return f"@@CODE{idx}@@"

    text = re.sub(r"\*{1,2}`([^`\n]+)`\*{1,2}", save_code, text)
    text = re.sub(r"`([^`\n]+)`", save_code, text)

    # 2. Escape Principia Mathematica theorem numbers like (*2.01), *2.01, or *1.2
    text = re.sub(r"(^|[\s\(])\*(\d+\.\d+)", r"\1\\*\2", text)

    # 3. Convert ***bold italic*** -> **bold**
    text = re.sub(r"\*\*\*([^\*\n]+)\*\*\*", r"**\1**", text)

    # 4. Convert Markdown links [label](url)
    def repl_link(m):
        lbl = m.group(1).strip()
        url = m.group(2).strip()
        lbl_clean = re.sub(r"\*{1,2}", "", lbl)
        lbl_clean = re.sub(r"@@CODE(\d+)@@", lambda cm: code_placeholders[int(cm.group(1))].strip("`"), lbl_clean)
        lbl_clean = lbl_clean.replace("$", "")

        if strip_links_for_heading:
            return lbl_clean

        if url in url_map:
            target = url_map[url]
            return f":ref:`{lbl_clean} <{target}>`"
        if url.startswith("http://") or url.startswith("https://"):
            return f"`{lbl_clean} <{url}>`_"
        if url.endswith(".py"):
            return f"``{lbl_clean}``"
        raise ValueError(f"Unmapped internal link URL: {url!r} (label={lbl!r})")

    text = re.sub(r"\*{0,2}\[([^\[\]]+)\]\(([^\)]+)\)\*{0,2}", repl_link, text)

    # 5. Convert footnote references [^12] -> [#f12]_ (with space before [#f12]_)
    def repl_fn(m):
        prefix = m.group(1)
        fn_id = m.group(2)
        if defined_fns is not None and fn_id not in defined_fns:
            return f"{prefix}``[^{fn_id}]``"
        if prefix and not prefix.isspace():
            return f"{prefix} [#f{fn_id}]_"
        return f"{prefix}[#f{fn_id}]_"

    text = re.sub(r"(^|.)\[\^(\d+)\]", repl_fn, text)

    # 6. Restore inline code placeholders
    for idx, code_rst in enumerate(code_placeholders):
        token = f"@@CODE{idx}@@"
        text = text.replace(token, code_rst)

    return text


def render_markdown_table_to_rst(table_lines: list[str], url_map: dict, indent_str: str = "") -> list[str]:
    """Convert a Markdown pipe table into a clean RST `.. list-table::` block."""
    rows = []
    for l in table_lines:
        s = l.strip()
        if s.startswith("|"):
            s = s[1:]
        if s.endswith("|"):
            s = s[:-1]
        cells = [c.strip() for c in s.split("|")]
        if all(re.match(r"^:?-{2,}:?$", c) for c in cells):
            continue
        rows.append(cells)

    if not rows:
        return []

    out = [
        f"{indent_str}.. list-table::",
        f"{indent_str}   :header-rows: 1",
        "",
    ]
    num_cols = len(rows[0])
    for row in rows:
        while len(row) < num_cols:
            row.append("")
        for c_idx, cell in enumerate(row[:num_cols]):
            prefix = f"{indent_str}   * - " if c_idx == 0 else f"{indent_str}     - "
            parts = [p.strip() for p in re.split(r"<br\s*/?>", cell) if p.strip()]
            if not parts:
                out.append(prefix)
            else:
                for p_idx, part in enumerate(parts):
                    conv = convert_inline(part, url_map)
                    if p_idx == 0:
                        out.append(f"{prefix}{conv}")
                    else:
                        out.append("")
                        out.append(f"{indent_str}       {conv}")
    out.append("")
    return out


def convert_markdown_doc_to_rst(
    md_path: str,
    doc_label: str,
    url_map: dict,
    ch_id: str | None = None,
    lang: str | None = None,
    active_track: str | None = None,
) -> str:
    with open(md_path, "r", encoding="utf-8") as f:
        raw = f.read()

    defined_fns = set(re.findall(r"^\[\^(\d+)\]:", raw, re.M))
    lines = raw.splitlines()
    idx = 0
    meta_fields = []

    # 1. Parse optional YAML frontmatter
    if lines and lines[0].strip() == "---":
        idx = 1
        while idx < len(lines) and lines[idx].strip() != "---":
            fm_line = lines[idx].strip()
            m_kv = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", fm_line)
            if m_kv:
                k, v = m_kv.group(1), m_kv.group(2).strip().strip('"')
                v_clean = convert_inline(v, url_map, strip_links_for_heading=True, defined_fns=defined_fns)
                meta_fields.append(f":{k}: {v_clean}")
            idx += 1
        idx += 1  # skip closing ---

    if ch_id and active_track in ("la", "en"):
        meta_fields.append(":layout: book")

    sec_queue = []
    if ch_id and ch_id != "preface" and lang in ("la", "en") and active_track in ("la", "en"):
        heads = get_content_headings(md_path)
        sec_queue = list(compute_section_labels_and_levels(ch_id, lang, heads))

    out = []
    if meta_fields:
        out.extend(meta_fields)
        out.append("")

    out.append(f".. _{doc_label}:")
    out.append("")

    while idx < len(lines) and not lines[idx].strip():
        idx += 1

    # Handle top breadcrumb blockquote in bibliography.md / about/*.md
    if idx < len(lines) and lines[idx].strip().startswith("> ["):
        bc_line = lines[idx].strip()[1:].strip()
        out.append(".. container:: track-nav")
        out.append("")
        out.append("   " + convert_inline(bc_line, url_map, defined_fns=defined_fns))
        out.append("")
        idx += 1
        while idx < len(lines) and (not lines[idx].strip() or lines[idx].strip() == "---"):
            idx += 1

    # Combine multi-line document banner headings at the top into a single Level 1 (=) title + optional rubric
    title_parts = []
    subtitle_parts = []
    if idx < len(lines) and lines[idx].strip().startswith("#"):
        first_h = re.match(r"^(#{1,6})\s+(.*)$", lines[idx].strip())
        if first_h:
            title_parts.append(
                convert_inline(first_h.group(2).strip(), url_map, strip_links_for_heading=True, defined_fns=defined_fns)
            )
            idx += 1
            while idx < len(lines):
                s = lines[idx].strip()
                if not s:
                    idx += 1
                    continue
                m_sub = re.match(r"^(#{1,6})\s+(.*)$", s)
                if m_sub:
                    sub_txt = m_sub.group(2).strip()
                    if m_sub.group(1) == "#" or is_chapter_banner_heading(sub_txt) or sub_txt.startswith("*Bibliographia"):
                        clean_sub = convert_inline(
                            sub_txt, url_map, strip_links_for_heading=True, defined_fns=defined_fns
                        )
                        if m_sub.group(1) == "#":
                            title_parts.append(clean_sub)
                        else:
                            subtitle_parts.append(clean_sub)
                        idx += 1
                        continue
                break

    if title_parts:
        full_title = " — ".join(title_parts)
        bar = "=" * max(len(full_title), 4)
        out.append(full_title)
        out.append(bar)
        out.append("")
        if subtitle_parts:
            sub_str = " — ".join(subtitle_parts)
            out.append(f".. rubric:: {sub_str}")
            out.append("")
        if ch_id and active_track:
            out.extend(make_track_nav_rst(ch_id, active_track))

    in_list = False
    last_list_indent = 0

    while idx < len(lines):
        raw_line = lines[idx]
        stripped = raw_line.strip()

        if not stripped:
            if out and out[-1] != "":
                out.append("")
            idx += 1
            continue

        m_anchor = re.match(r'^<a id="([^"]+)"></a>$', stripped)
        if m_anchor:
            slug = m_anchor.group(1)
            if doc_label == "bibliography":
                if out and out[-1] != "":
                    out.append("")
                out.append(f".. _bib-{slug}:")
                out.append("")
            idx += 1
            continue

        if re.match(r"^-{3,}$", stripped):
            in_list = False
            if out and out[-1] != "":
                out.append("")
            out.append("----")
            out.append("")
            idx += 1
            continue

        m_fence = re.match(r"^(\s*)```([^\n]*)$", raw_line)
        if m_fence:
            in_list = False
            fence_lang = m_fence.group(2).strip() or "text"
            if fence_lang == "mermaid":
                fence_lang = "text"
            idx += 1
            code_lines = []
            while idx < len(lines) and not lines[idx].strip().startswith("```"):
                code_lines.append(lines[idx].rstrip())
                idx += 1
            idx += 1
            if out and out[-1] != "":
                out.append("")
            out.append(f".. code-block:: {fence_lang}")
            out.append("")
            for cl in code_lines:
                out.append(f"   {cl}" if cl.strip() else "")
            out.append("")
            continue

        if stripped.startswith(">"):
            in_list = False
            bq_lines = []
            while idx < len(lines) and lines[idx].strip().startswith(">"):
                content_after_gt = re.sub(r"^>\s?", "", lines[idx].strip())
                bq_lines.append(content_after_gt)
                idx += 1
            if out and out[-1] != "":
                out.append("")
            if bq_lines and re.match(r"^\[!NOTE\]", bq_lines[0]):
                out.append(".. note::")
                out.append("")
                for bl in bq_lines[1:]:
                    out.append(f"   {convert_inline(bl, url_map, defined_fns=defined_fns)}" if bl else "")
                out.append("")
            else:
                in_bq_code = False
                for bl in bq_lines:
                    if bl.strip().startswith("```"):
                        if not in_bq_code:
                            in_bq_code = True
                            out.append("")
                            out.append("   .. code-block:: text")
                            out.append("")
                        else:
                            in_bq_code = False
                            out.append("")
                        continue
                    if in_bq_code:
                        out.append(f"      {bl}" if bl.strip() else "")
                    else:
                        out.append(f"   {convert_inline(bl, url_map, defined_fns=defined_fns)}" if bl else "")
                out.append("")
            continue

        # Markdown pipe table
        if stripped.startswith("|") and stripped.endswith("|"):
            in_list = False
            tbl_lines = []
            while idx < len(lines) and lines[idx].strip().startswith("|") and lines[idx].strip().endswith("|"):
                tbl_lines.append(lines[idx])
                idx += 1
            if out and out[-1] != "":
                out.append("")
            out.extend(render_markdown_table_to_rst(tbl_lines, url_map))
            continue

        # Display math $$...$$
        m_math = re.match(r"^(\s*)\$\$(.+)\$\$\s*$", raw_line)
        if m_math:
            indent_len = len(m_math.group(1))
            math_indent = " " * indent_len
            math_expr = m_math.group(2).strip()
            if out and out[-1] != "":
                out.append("")
            out.append(f"{math_indent}.. math::")
            out.append("")
            out.append(f"{math_indent}   {math_expr}")
            out.append("")
            idx += 1
            continue

        # Markdown headings (#, ##, ###, ####)
        m_head = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m_head:
            in_list = False
            md_lvl = len(m_head.group(1))
            raw_htxt = m_head.group(2).strip()

            if out and out[-1] != "":
                out.append("")

            # Check if this heading matches the next queued canonical section heading
            if sec_queue and raw_htxt == sec_queue[0][2]:
                sec_lbl, rst_lvl, _ = sec_queue.pop(0)
                out.append(f".. _{sec_lbl}:")
                out.append("")
                clean_h = convert_inline(raw_htxt, url_map, strip_links_for_heading=True, defined_fns=defined_fns)
                ch_bar = RST_BAR_CHARS.get(rst_lvl, "^")
                out.append(clean_h)
                out.append(ch_bar * max(len(clean_h), 4))
                out.append("")
                idx += 1
                continue

            # Special labels in bibliography.rst
            if doc_label == "bibliography":
                if "Alphabetical Index" in raw_htxt:
                    out.append(".. _bib-alphabetical-index-of-authors:")
                    out.append("")
                elif "Chronological Bibliography" in raw_htxt:
                    out.append(".. _bib-chronological-bibliography-ordered-by-death-date:")
                    out.append("")

            # Check if heading in *-summary.md has a link [§ M. ...](caput-N.html#...)
            m_sum_link = re.match(r"^\[([^\[\]]+)\]\(([^\)]+)\)$", raw_htxt)
            extra_ref_line = None
            if m_sum_link and m_sum_link.group(2) in url_map:
                la_ref = url_map[m_sum_link.group(2)]
                en_ref = la_ref.replace("-la-", "-en-") if "-la-" in la_ref else la_ref
                if la_ref != en_ref:
                    extra_ref_line = f"*Text:* :ref:`Latin <{la_ref}>` · :ref:`English <{en_ref}>`"
                else:
                    extra_ref_line = f"*Text:* :ref:`Section <{la_ref}>`"

            clean_h = convert_inline(raw_htxt, url_map, strip_links_for_heading=True, defined_fns=defined_fns)
            rst_lvl = 2 if raw_htxt == "Footnotes" else min(max(md_lvl, 2), 5)
            ch_bar = RST_BAR_CHARS.get(rst_lvl, "^")
            out.append(clean_h)
            out.append(ch_bar * max(len(clean_h), 4))
            out.append("")
            if extra_ref_line:
                out.append(extra_ref_line)
                out.append("")
            idx += 1
            continue

        # Footnote definition [^1]: ...
        m_fn_def = re.match(r"^\[\^(\d+)\]:\s*(.*)$", stripped)
        if m_fn_def:
            in_list = False
            fn_num = m_fn_def.group(1)
            fn_body = convert_inline(m_fn_def.group(2).strip(), url_map, defined_fns=defined_fns)
            if out and out[-1] != "":
                out.append("")
            if ch_id and lang in ("la", "en") and active_track in ("la", "en"):
                out.append(f".. _{ch_id}-{lang}-fn{fn_num}:")
                out.append("")
            out.append(f".. [#f{fn_num}] {fn_body}")
            idx += 1
            # Check for indented continuation paragraphs of the footnote
            while idx < len(lines):
                nxt = lines[idx]
                if not nxt.strip():
                    look = idx + 1
                    while look < len(lines) and not lines[look].strip():
                        look += 1
                    if look < len(lines) and lines[look].startswith("    ") and not lines[look].strip().startswith("[^"):
                        out.append("")
                        idx = look
                        out.append(f"   {convert_inline(lines[idx].strip(), url_map, defined_fns=defined_fns)}")
                        idx += 1
                        continue
                    break
                if nxt.startswith("  ") and not nxt.strip().startswith("[^"):
                    out.append(f"   {convert_inline(nxt.strip(), url_map, defined_fns=defined_fns)}")
                    idx += 1
                else:
                    break
            out.append("")
            continue

        # Bullet or numbered list items
        m_list = re.match(r"^(\s*)(\*|-|\d+\.)\s+(.*)$", raw_line)
        if m_list:
            cur_indent = len(m_list.group(1))
            marker = m_list.group(2)
            item_txt = convert_inline(m_list.group(3).strip(), url_map, defined_fns=defined_fns)
            if not in_list or cur_indent != last_list_indent:
                if out and out[-1] != "":
                    out.append("")
            in_list = True
            last_list_indent = cur_indent
            out.append(f"{' ' * cur_indent}{marker} {item_txt}")
            idx += 1
            continue

        # Indented continuation line inside a list (e.g. "  *Notes*: ..." in bibliography.md)
        if in_list and raw_line.startswith("  "):
            lead_spaces = len(raw_line) - len(raw_line.lstrip())
            if out and out[-1] != "":
                out.append("")
            out.append(f"{' ' * lead_spaces}{convert_inline(stripped, url_map, defined_fns=defined_fns)}")
            idx += 1
            continue

        # Regular paragraph line
        if in_list:
            if out and out[-1] != "":
                out.append("")
            in_list = False
        conv_line = convert_inline(stripped, url_map, defined_fns=defined_fns)
        if out and out[-1] != "" and re.match(r"^(\d+[\.\)]|[a-zA-Z][\.\)])\s+", conv_line):
            out.append("")
        out.append(conv_line)
        idx += 1

    # Collapse consecutive blank lines
    cleaned_out = []
    for l in out:
        if l == "" and (not cleaned_out or cleaned_out[-1] == ""):
            continue
        cleaned_out.append(l)

    return "\n".join(cleaned_out).rstrip() + "\n"


def generate_analytical_indices_rst():
    """Generate docsrc/end-index/end_index.rst and docsrc/end-index/end_index-en.rst with :ref: links."""
    from scripts.generate_analytical_indices import CHAPTER_SECTIONS, parse_english_index_entries

    entries = parse_english_index_entries()

    en_lines = [
        ":title: Analytical Index (Table of Contents)",
        ":layout: book",
        "",
        ".. _end-index-en:",
        "",
        "ANALYTICAL INDEX (TABLE OF CONTENTS)",
        "====================================",
        "",
        ".. rubric:: *(Index Analyticus, pp. 289–293)*",
        "",
        ".. container:: track-nav",
        "",
        "   :ref:`Latin <end-index-la>` · **English** | :ref:`Conspectus <hoenen-index>` · :ref:`← Appendix <appendix-en>` · :ref:`Bibliography <bibliography>`",
        "",
        "Preface *(Praefatio)*",
        "---------------------",
        "",
        "* :ref:`Preface (English) <preface-en>` · :ref:`Praefatio (Latin) <preface-la>` · :ref:`Translation Notes <preface-notes>`",
        "",
    ]

    la_lines = [
        ":title: Index Analyticus",
        ":layout: book",
        "",
        ".. _end-index-la:",
        "",
        "INDEX ANALYTICUS",
        "================",
        "",
        ".. rubric:: *(pp. 289–293)*",
        "",
        ".. container:: track-nav",
        "",
        "   **Latin** · :ref:`English <end-index-en>` | :ref:`Conspectus <hoenen-index>` · :ref:`← Appendix <appendix-la>` · :ref:`Bibliography <bibliography>`",
        "",
        "Praefatio",
        "---------",
        "",
        "* :ref:`Praefatio (Latin) <preface-la>` · :ref:`Preface (English) <preface-en>` · :ref:`Notes <preface-notes>`",
        "",
    ]

    for sec in CHAPTER_SECTIONS:
        ch = sec["id"]
        en_h = f"{sec['en_title']}"
        la_h = f"{sec['la_title']}"

        en_lines.extend([
            en_h,
            "-" * max(len(en_h), 4),
            "",
            f"*({la_h})*",
            "",
            f"* :ref:`Full Text (English) <{ch}-en>` · :ref:`Latin <{ch}-la>` · :ref:`Summary <{ch}-summary>` · :ref:`Notes <{ch}-notes>`",
        ])

        la_lines.extend([
            la_h,
            "-" * max(len(la_h), 4),
            "",
            f"* :ref:`Textus Integralis (Latin) <{ch}-la>` · :ref:`English <{ch}-en>` · :ref:`Summary <{ch}-summary>` · :ref:`Notes <{ch}-notes>`",
        ])

        ch_ents = [e for e in entries if e["ch"] == ch]
        en_info = compute_section_labels_and_levels(
            ch, "en", get_content_headings(os.path.join(DOCS_DIR, ch, f"{ch}-en.md"))
        )
        la_info = compute_section_labels_and_levels(
            ch, "la", get_content_headings(os.path.join(DOCS_DIR, ch, f"{ch}.md"))
        )

        last_indent = 0
        for e, (en_lbl, _, _), (la_lbl, _, _) in zip(ch_ents, en_info, la_info):
            cur_indent = e["indent"]
            indent_str = " " * cur_indent
            if cur_indent != last_indent:
                en_lines.append("")
                la_lines.append("")
            last_indent = cur_indent

            en_title = re.sub(r"\*{1,2}", "", e["en"]).replace("$", "").strip()
            la_title = re.sub(r"\*{1,2}", "", e["la"]).replace("$", "").strip()

            m_pfx = re.match(r"^(§\s*\d+\.|\d+\.\s*-?|[A-D]\.\s*-?)\s*", en_title)
            pfx = m_pfx.group(0) if m_pfx else ""
            if pfx and not la_title.startswith(pfx.strip()):
                la_display = f"{pfx}{la_title}"
            else:
                la_display = la_title

            en_lines.append(f"{indent_str}* :ref:`{en_title} <{en_lbl}>` *({la_title})*")
            la_lines.append(f"{indent_str}* :ref:`{la_display} <{la_lbl}>`")

        en_lines.append("")
        la_lines.append("")

    end_dir = os.path.join(DOCSRC_DIR, "end-index")
    os.makedirs(end_dir, exist_ok=True)
    with open(os.path.join(end_dir, "end_index-en.rst"), "w", encoding="utf-8") as f:
        f.write("\n".join(en_lines).rstrip() + "\n")
    with open(os.path.join(end_dir, "end_index.rst"), "w", encoding="utf-8") as f:
        f.write("\n".join(la_lines).rstrip() + "\n")


def generate_master_index_rst():
    """Generate docsrc/index.rst with title page, Conspectus Totius Operis, and Sphinx toctrees."""
    lines = [
        ":title: De Noetica Geometriae. Origine Theoriae Cognitionis",
        ":author: Petrus Hubertus Jacobus Hoenen, S. J.",
        ":series: Analecta Gregoriana, VOL. LXIII, Series Facultatis Philosophicae, Sectio A (n. 5)",
        ":publisher: Apud Aedes Universitatis Gregorianae",
        ":location: Romae",
        ":year: 1954",
        "",
        ".. _hoenen-index:",
        "",
        "DE NOETICA GEOMETRIAE",
        "=====================",
        "",
        ".. rubric:: *(The Noetics of Geometry)* — ORIGINE THEORIAE COGNITIONIS *(The Origin of the Theory of Knowledge)*",
        "",
        ".. container:: title-page",
        "",
        "   | :ref:`Analecta Gregoriana <about-analecta-gregoriana>`",
        "   | Cura :ref:`Pontificiae Universitatis Gregorianae <about-gregorian-university>` edita",
        "   | VOL. LXIII · SERIES FACULTATIS PHILOSOPHICAE · Sectio A (n. 5)",
        "   |",
        "   | auctore :ref:`P. HOENEN S. I. <about-peter-hoenen>`",
        "   | PROFESSORE PHILOSOPHIAE IN :ref:`PONTIFICIA UNIVERSITATE GREGORIANA <about-gregorian-university>`",
        "   | ROMAE — APUD AEDES :ref:`UNIVERSITATIS GREGORIANAE <about-gregorian-university>` — 1954",
        "",
        "----",
        "",
        "Conspectus Totius Operis",
        "------------------------",
        "",
        "*(Table of Contents)*",
        "",
        "Praefatio *(Preface)*",
        "~~~~~~~~~~~~~~~~~~~~~",
        "",
        ":ref:`Latin <preface-la>` · :ref:`English <preface-en>` · :ref:`Notes <preface-notes>`",
        "",
        "Caput I: De Origine Cognitionis Geometricae et de Eius Problematica",
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
        "",
        "*(On the Origin of Geometric Knowledge and Its Problematics)*",
        "",
        ":ref:`Latin <caput-1-la>` · :ref:`English <caput-1-en>` · :ref:`Summary <caput-1-summary>` · :ref:`Notes <caput-1-notes>`",
        "",
        "Caput II: De Problemate Necessitatis",
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
        "",
        "*(On the Problem of Necessity)*",
        "",
        ":ref:`Latin <caput-2-la>` · :ref:`English <caput-2-en>` · :ref:`Summary <caput-2-summary>` · :ref:`Notes <caput-2-notes>`",
        "",
        "Caput III: De Problemate Exactitudinis. Pars I: De Existentia Indivisibilium",
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
        "",
        "*(On the Problem of Exactitude. Part I: On the Existence of Indivisibles)*",
        "",
        ":ref:`Latin <caput-3-la>` · :ref:`English <caput-3-en>` · :ref:`Summary <caput-3-summary>` · :ref:`Notes <caput-3-notes>`",
        "",
        "Caput IV: De Problemate Exactitudinis. Pars II: De Figuris et Relationibus Exactis",
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
        "",
        "*(On the Problem of Exactitude. Part II: On Exact Figures and Relations)*",
        "",
        ":ref:`Latin <caput-4-la>` · :ref:`English <caput-4-en>` · :ref:`Summary <caput-4-summary>` · :ref:`Notes <caput-4-notes>`",
        "",
        "Caput V: De Axiomatica",
        "~~~~~~~~~~~~~~~~~~~~~~",
        "",
        "*(On Axiomatics)*",
        "",
        ":ref:`Latin <caput-5-la>` · :ref:`English <caput-5-en>` · :ref:`Summary <caput-5-summary>` · :ref:`Notes <caput-5-notes>`",
        "",
        "Caput VI: De Subiecto Fundamentali Geometriae",
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
        "",
        "*(On the Fundamental Subject of Geometry)*",
        "",
        ":ref:`Latin <caput-6-la>` · :ref:`English <caput-6-en>` · :ref:`Summary <caput-6-summary>` · :ref:`Notes <caput-6-notes>`",
        "",
        "Caput VII: De Extensione ut est Materia Intelligibilis",
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
        "",
        "*(On Extension as Intelligible Matter)*",
        "",
        ":ref:`Latin <caput-7-la>` · :ref:`English <caput-7-en>` · :ref:`Summary <caput-7-summary>` · :ref:`Notes <caput-7-notes>`",
        "",
        "Appendix: De connexionibus necessariis inter actus existentiales",
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
        "",
        "*(On the Necessary Connections Between Existential Acts)*",
        "",
        ":ref:`Latin <appendix-la>` · :ref:`English <appendix-en>` · :ref:`Summary <appendix-summary>` · :ref:`Notes <appendix-notes>`",
        "",
        "Index Analyticus *(Analytical Index)*",
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
        "",
        ":ref:`Latin <end-index-la>` · :ref:`English <end-index-en>`",
        "",
        "Bibliographia et Fontes *(Bibliography & References)*",
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
        "",
        ":ref:`Systematic Bibliography & Annotated Footnote Concordance <bibliography>`",
        "",
        "----",
        "",
        "Project Documentation",
        "---------------------",
        "",
        "* :ref:`Bibliography & Cited References (Bibliographia et Fontes) <bibliography>`",
        "* :ref:`The Transcription Chronicle: An AI Agent's First-Person Memoir <agent-chronicle>`",
        "* :ref:`Scan Inventory & Problem Page Log <scan-inventory>`",
        "* :ref:`Historical Context: Fr. Peter Hoenen, S.J. <about-peter-hoenen>`",
        "* :ref:`Historical Context: Analecta Gregoriana <about-analecta-gregoriana>`",
        "* :ref:`Historical Context: Pontifical Gregorian University <about-gregorian-university>`",
        "* :ref:`PDF Parsing & Extraction Guide <about-pdf-parsing-guide>`",
        "",
        ".. toctree::",
        "   :maxdepth: 2",
        "   :hidden:",
        "   :caption: English Edition",
        "",
        "   preface/preface-en",
        "   caput-1/caput-1-en",
        "   caput-2/caput-2-en",
        "   caput-3/caput-3-en",
        "   caput-4/caput-4-en",
        "   caput-5/caput-5-en",
        "   caput-6/caput-6-en",
        "   caput-7/caput-7-en",
        "   appendix/appendix-en",
        "   end-index/end_index-en",
        "",
        ".. toctree::",
        "   :maxdepth: 2",
        "   :hidden:",
        "   :caption: Editio Latina (1954)",
        "",
        "   preface/preface",
        "   caput-1/caput-1",
        "   caput-2/caput-2",
        "   caput-3/caput-3",
        "   caput-4/caput-4",
        "   caput-5/caput-5",
        "   caput-6/caput-6",
        "   caput-7/caput-7",
        "   appendix/appendix",
        "   end-index/end_index",
        "",
        ".. toctree::",
        "   :maxdepth: 1",
        "   :hidden:",
        "   :caption: Summaries & Translation Notes",
        "",
        "   preface/translation-notes-preface",
        "   caput-1/caput-1-summary",
        "   caput-1/translation-notes-caput-1",
        "   caput-2/caput-2-summary",
        "   caput-2/translation-notes-caput-2",
        "   caput-3/caput-3-summary",
        "   caput-3/translation-notes-caput-3",
        "   caput-4/caput-4-summary",
        "   caput-4/translation-notes-caput-4",
        "   caput-5/caput-5-summary",
        "   caput-5/translation-notes-caput-5",
        "   caput-6/caput-6-summary",
        "   caput-6/translation-notes-caput-6",
        "   caput-7/caput-7-summary",
        "   caput-7/translation-notes-caput-7",
        "   appendix/appendix-summary",
        "   appendix/translation-notes-appendix",
        "",
        ".. toctree::",
        "   :maxdepth: 1",
        "   :hidden:",
        "   :caption: Scholarly Apparatus & Context",
        "",
        "   bibliography",
        "   agent-chronicle",
        "   scan-inventory",
        "   about/peter-hoenen",
        "   about/analecta-gregorian",
        "   about/pontifical-gregorian-university",
        "   about/pdf-parsing-guide",
        "",
    ]
    with open(os.path.join(DOCSRC_DIR, "index.rst"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def generate_conf_py():
    conf_code = '''from photon_platform.publish.global_conf import *

org = "geometor"
org_name = "GEOMETOR"

repo = "hoenen"
repo_name = "De Noetica Geometriae"

setup_globals(org, org_name, repo, repo_name)

project = "De Noetica Geometriae"
author = "Petrus Hoenen, S.J."
copyright = "1954, Pontificia Universitas Gregoriana • Digital Edition GEOMETOR"
'''
    with open(os.path.join(DOCSRC_DIR, "conf.py"), "w", encoding="utf-8") as f:
        f.write(conf_code)


def main():
    os.makedirs(DOCSRC_DIR, exist_ok=True)
    generate_conf_py()

    url_map = build_url_to_ref_map()
    generate_master_index_rst()
    generate_analytical_indices_rst()

    # Convert chapters, preface, appendix
    for meta in CHAPTER_META:
        ch = meta["id"]
        dst_dir = os.path.join(DOCSRC_DIR, ch)
        os.makedirs(dst_dir, exist_ok=True)

        # Latin
        la_rst = convert_markdown_doc_to_rst(
            os.path.join(DOCS_DIR, ch, f"{ch}.md"),
            doc_label=f"{ch}-la",
            url_map=url_map,
            ch_id=ch,
            lang="la",
            active_track="la",
        )
        with open(os.path.join(dst_dir, f"{ch}.rst"), "w", encoding="utf-8") as f:
            f.write(la_rst)

        # English
        en_rst = convert_markdown_doc_to_rst(
            os.path.join(DOCS_DIR, ch, f"{ch}-en.md"),
            doc_label=f"{ch}-en",
            url_map=url_map,
            ch_id=ch,
            lang="en",
            active_track="en",
        )
        with open(os.path.join(dst_dir, f"{ch}-en.rst"), "w", encoding="utf-8") as f:
            f.write(en_rst)

        # Summary
        if meta["has_summary"]:
            sum_rst = convert_markdown_doc_to_rst(
                os.path.join(DOCS_DIR, ch, f"{ch}-summary.md"),
                doc_label=f"{ch}-summary",
                url_map=url_map,
                ch_id=ch,
                lang="en",
                active_track="summary",
            )
            with open(os.path.join(dst_dir, f"{ch}-summary.rst"), "w", encoding="utf-8") as f:
                f.write(sum_rst)

        # Translation Notes
        notes_rst = convert_markdown_doc_to_rst(
            os.path.join(DOCS_DIR, ch, f"translation-notes-{ch}.md"),
            doc_label=f"{ch}-notes",
            url_map=url_map,
            ch_id=ch,
            lang="en",
            active_track="notes",
        )
        with open(os.path.join(dst_dir, f"translation-notes-{ch}.rst"), "w", encoding="utf-8") as f:
            f.write(notes_rst)

        # Optional 3.1 benchmark files
        bench_md = os.path.join(DOCS_DIR, ch, f"{ch}-en-3.1.md")
        if os.path.exists(bench_md):
            bench_rst = convert_markdown_doc_to_rst(
                bench_md,
                doc_label=f"{ch}-en-3-1",
                url_map=url_map,
                ch_id=ch,
                lang="en",
                active_track=None,
            )
            with open(os.path.join(dst_dir, f"{ch}-en-3.1.rst"), "w", encoding="utf-8") as f:
                f.write(bench_rst)

    # Convert standalone apparatus and about pages
    standalone_docs = [
        ("bibliography.md", "bibliography.rst", "bibliography"),
        ("agent-chronicle.md", "agent-chronicle.rst", "agent-chronicle"),
        ("scan-inventory.md", "scan-inventory.rst", "scan-inventory"),
        ("about/peter-hoenen.md", "about/peter-hoenen.rst", "about-peter-hoenen"),
        ("about/analecta-gregorian.md", "about/analecta-gregorian.rst", "about-analecta-gregoriana"),
        ("about/pontifical-gregorian-university.md", "about/pontifical-gregorian-university.rst", "about-gregorian-university"),
        ("about/pdf-parsing-guide.md", "about/pdf-parsing-guide.rst", "about-pdf-parsing-guide"),
    ]
    for src_rel, dst_rel, lbl in standalone_docs:
        src_p = os.path.join(DOCS_DIR, src_rel)
        dst_p = os.path.join(DOCSRC_DIR, dst_rel)
        os.makedirs(os.path.dirname(dst_p), exist_ok=True)
        rst_txt = convert_markdown_doc_to_rst(src_p, doc_label=lbl, url_map=url_map)
        with open(dst_p, "w", encoding="utf-8") as f:
            f.write(rst_txt)

    rst_files = sorted(glob.glob(os.path.join(DOCSRC_DIR, "**", "*.rst"), recursive=True))
    print(f"Generated {len(rst_files)} .rst files and conf.py in {DOCSRC_DIR}")


if __name__ == "__main__":
    main()
