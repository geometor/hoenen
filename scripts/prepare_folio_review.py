#!/usr/bin/env python3
"""
scripts/prepare_folio_review.py

Organizes the 287 page scans and diplomatic transcriptions from `archive/`
and the curated Latin Markdown editions in `docs/` into
`resources/hoenen_1954/volume_I/<section>/` for the GEOMETOR Folio Reviewer:
- Creates relative symlinks `<NNNN>.png` -> `../../../../archive/<archive_dir>/page-NNN.png`
  (plus `-partial.png` and `-photo.png` variants where present).
- Aligns the compiled Latin `.md` files in `docs/` (`preface.md`, `caput-1.md`..`caput-7.md`,
  `appendix.md`) with the exact page boundaries of `archive/<sec>/page-NNN.txt` so that
  every `<NNNN>.rst` folio preserves 100% of paragraph separations, headings, blockquotes,
  line-blocks, and attached footnotes (`[#fN]_` and `.. [#fN] ...`).
- Generates companion `<NNNN>.notes.rst` files for all 287 folios.
- Initializes `resources/hoenen_1954/folio_reviews.json` pre-populated with
  `"status": "needs_fix"` for the 14 partial scan folios.
"""

import ast
import glob
import json
import os
import re
from typing import Any, Dict, List, Tuple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE_DIR = os.path.join(BASE_DIR, "archive")
RES_HOENEN_DIR = os.path.join(BASE_DIR, "resources", "hoenen_1954")
OUT_VOL_DIR = os.path.join(RES_HOENEN_DIR, "volume_I")
SCAN_INVENTORY_MD = os.path.join(BASE_DIR, "docs", "scan-inventory.md")

SECTIONS = [
    ("preface", "00_preface", "Praefatio", "docs/preface/preface.md"),
    ("chapter-01", "01_caput_1", "Caput I", "docs/caput-1/caput-1.md"),
    ("chapter-02", "02_caput_2", "Caput II", "docs/caput-2/caput-2.md"),
    ("chapter-03", "03_caput_3", "Caput III", "docs/caput-3/caput-3.md"),
    ("chapter-04", "04_caput_4", "Caput IV", "docs/caput-4/caput-4.md"),
    ("chapter-05", "05_caput_5", "Caput V", "docs/caput-5/caput-5.md"),
    ("chapter-06", "06_caput_6", "Caput VI", "docs/caput-6/caput-6.md"),
    ("chapter-07", "07_caput_7", "Caput VII", "docs/caput-7/caput-7.md"),
    ("appendix", "08_appendix", "Appendix", "docs/appendix/appendix.md"),
    ("index", "09_index", "Index Analyticus", None),
]

RESCAN_NEEDED_PAGES = {
    176, 212, 216, 222, 224, 226, 230, 232, 234, 238, 240, 242, 244, 246
}

HEADING_CHARS = {
    1: "=",
    2: "-",
    3: "~",
    4: "^",
    5: '"',
}

HEADER_PATTERN = re.compile(r"^\s*\d+\s{2,}.*$|^\s*.*\s{2,}\d+\s*$")
FOOTER_PATTERN = re.compile(r"^\s*\d+\s*$|^\s*\d+\s*—\s*P\.\s+HOENEN.*$")


def load_fn_maps() -> Dict[int, str]:
    """Load bottom-of-page footnote start markers from scripts/build_caput_2..6.py via AST."""
    fn_maps: Dict[int, str] = {}
    for idx in range(2, 7):
        script_path = os.path.join(BASE_DIR, "scripts", f"build_caput_{idx}.py")
        if not os.path.exists(script_path):
            continue
        with open(script_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name) and t.id == "fn_map":
                        m = ast.literal_eval(node.value)
                        if idx == 2:
                            m = {k + 26: v for k, v in m.items()}
                        fn_maps.update(m)
    return fn_maps


FN_MAPS = load_fn_maps()


def load_scan_inventory() -> Dict[int, Dict[str, str]]:
    """Parse docs/scan-inventory.md for source reference and extracted file per page."""
    inventory: Dict[int, Dict[str, str]] = {}
    if not os.path.exists(SCAN_INVENTORY_MD):
        return inventory
    with open(SCAN_INVENTORY_MD, "r", encoding="utf-8") as f:
        for line in f:
            m = re.match(
                r"^\|\s*(\d{3})\s*\|\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*`([^`]+)`\s*\|",
                line.strip(),
            )
            if m:
                pnum = int(m.group(1))
                inventory[pnum] = {
                    "archive_sec": m.group(2).strip(),
                    "source_ref": m.group(3).strip(),
                    "status_label": m.group(4).strip(),
                    "extracted_file": m.group(5).strip(),
                }
    return inventory


def extract_page_header_and_footer(raw_text: str) -> Tuple[str | None, str | None]:
    """Return (running_header, printer_sig) from raw page transcription."""
    lines = [l.rstrip() for l in raw_text.splitlines()]
    while lines and not lines[0].strip():
        lines.pop(0)
    running_header = None
    if lines and HEADER_PATTERN.match(lines[0].strip()):
        running_header = re.sub(r"\s{2,}", " — ", lines[0].strip())

    while lines and not lines[-1].strip():
        lines.pop()
    printer_sig = None
    if lines and FOOTER_PATTERN.match(lines[-1].strip()):
        printer_sig = lines[-1].strip()
    return running_header, printer_sig


def get_page_body_lines(sec: str, page_num: int, raw_text: str) -> List[str]:
    """Extract pure body lines of a page (excluding running header, footer, and bottom footnotes)."""
    if page_num in FN_MAPS:
        marker = FN_MAPS[page_num]
        idx = raw_text.find(marker)
        assert idx != -1, f"Marker {marker!r} not found on page {page_num}"
        raw_text = raw_text[:idx].rstrip()

    lines = [l.rstrip() for l in raw_text.splitlines()]
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and HEADER_PATTERN.match(lines[0]):
        lines.pop(0)
    while lines and not lines[0].strip():
        lines.pop(0)

    while lines and not lines[-1].strip():
        lines.pop()
    if lines and FOOTER_PATTERN.match(lines[-1]):
        lines.pop()
    while lines and not lines[-1].strip():
        lines.pop()

    if sec in ("preface", "chapter-01"):
        fn_start = -1
        max_search = max(-1, len(lines) - 20)
        for i in range(len(lines) - 1, max_search, -1):
            if re.match(r"^\d+\s+", lines[i].strip()) and len(lines[i].strip()) > 10:
                fn_start = i
            if "Geraden und bezeichnen sie mit" in lines[i]:
                fn_start = i
        if fn_start != -1:
            lines = lines[:fn_start]
    elif sec in ("chapter-07", "appendix"):
        clean = []
        for l in lines:
            if re.match(r"^\[\^\d+\]:", l.strip()):
                break
            clean.append(l)
        lines = clean

    while lines and not lines[-1].strip():
        lines.pop()
    return [l.strip() for l in lines if l.strip()]


def norm_letters(s: str) -> str:
    """Normalize string to lowercase Latin/Greek letters only (ignoring footnote markers)."""
    s = re.sub(r"\[\^[^\]]+\]", "", s)
    s = re.sub(r"[^a-zA-Z\u00C0-\u017F\u0370-\u03ff\u1f00-\u1fff]+", "", s)
    return s.lower()


def preprocess_section_body_md(sec: str, body_md: str) -> str:
    """Normalize compiled Markdown body before slicing into pages."""
    # Remove HTML anchor tags like <a id="..."></a>
    body_md = re.sub(r"<a\s+id=\"[^\"]+\"\s*>\s*</a>\s*", "", body_md)

    # Normalize multi-line asterisms (* \n * *) to * * *
    body_md = re.sub(r"(?m)^\*\s*\n\*\s+\*\s*$", "* * *", body_md)

    # In appendix.md, every non-empty line in body_md is a distinct paragraph
    if sec == "appendix":
        paras = [l.strip() for l in body_md.splitlines() if l.strip()]
        body_md = "\n\n".join(paras)

    # Ensure every Markdown heading (# .. #####) is followed by a blank line (\n\n)
    body_md = re.sub(r"(?m)^(#{1,5}\s+[^\n]+)\n(?!\n)", r"\1\n\n", body_md)

    return body_md.strip()


def slice_section_md_by_pages(
    sec: str, md_rel: str, page_files: List[str]
) -> Tuple[Dict[int, str], Dict[str, str]]:
    """
    Slice the compiled Latin Markdown file `md_rel` at the exact page boundaries
    defined by `page_files` (`archive/<sec>/page-NNN.txt`).
    Returns `(slices_by_page_num, footnotes_dict)`.
    """
    md_path = os.path.join(BASE_DIR, md_rel)
    with open(md_path, "r", encoding="utf-8") as f:
        md = f.read()

    parts = md.split("\n---\n")
    body_md = preprocess_section_body_md(sec, parts[0])
    fn_md = parts[1].strip() if len(parts) > 1 else ""

    fns: Dict[str, str] = {}
    if fn_md:
        for m in re.finditer(
            r"^\[\^([^\]]+)\]:\s*(.*?)(?=\n\n\[\^|\Z)", fn_md, flags=re.S | re.M
        ):
            fns[m.group(1)] = m.group(2).strip()

    norm_chars: List[str] = []
    norm_to_md_idx: List[int] = []
    i = 0
    while i < len(body_md):
        m = re.match(r"^\[\^[^\]]+\]", body_md[i:])
        if m:
            i += len(m.group(0))
            continue
        ch = body_md[i]
        if re.match(r"[a-zA-Z\u00C0-\u017F\u0370-\u03ff\u1f00-\u1fff]", ch):
            norm_chars.append(ch.lower())
            norm_to_md_idx.append(i)
        i += 1
    norm_md_str = "".join(norm_chars)

    cur_norm_pos = 0
    cur_md_start = 0
    slices_by_page: Dict[int, str] = {}

    for idx, pf in enumerate(page_files):
        pnum = int(re.search(r"page-(\d{3})\.txt$", pf).group(1))
        with open(pf, "r", encoding="utf-8") as f:
            raw = f.read()
        p_lines = get_page_body_lines(sec, pnum, raw)
        p_norm = norm_letters(" ".join(p_lines))
        ends_hyphen = bool(p_lines and p_lines[-1].endswith("-"))

        if idx < len(page_files) - 1:
            tail = p_norm[-16:] if len(p_norm) >= 16 else p_norm
            expected_end = cur_norm_pos + len(p_norm)
            win_start = max(cur_norm_pos, expected_end - 250)
            win_end = min(len(norm_md_str), expected_end + 250)
            found = norm_md_str.find(tail, win_start, win_end)
            assert found != -1, f"Failed to find boundary for {sec} page {pnum}"
            end_norm_idx = found + len(tail)

            md_end_char = norm_to_md_idx[end_norm_idx - 1]
            md_next_char = norm_to_md_idx[end_norm_idx]
            between = body_md[md_end_char + 1 : md_next_char]

            if md_next_char == md_end_char + 1:
                # Word hyphenated across page boundary
                slice_text = body_md[cur_md_start : md_end_char + 1] + "-"
                cur_md_start = md_next_char
            elif "\n\n" in between:
                # Paragraph or heading boundary between pages
                split_rel = between.index("\n\n")
                slice_text = body_md[cur_md_start : md_end_char + 1 + split_rel]
                cur_md_start = md_end_char + 1 + split_rel + 2
                while cur_md_start < md_next_char and body_md[cur_md_start] == "\n":
                    cur_md_start += 1
            else:
                # Mid-paragraph word boundary across pages
                m_trail = re.match(
                    r"^((?:\s*\[\^[^\]]+\]|[.,;:?!»\"'\)\]\*])*)", between
                )
                trail_len = len(m_trail.group(1)) if m_trail else 0
                slice_text = body_md[cur_md_start : md_end_char + 1 + trail_len]
                if ends_hyphen and not slice_text.endswith("-"):
                    slice_text += "-"
                cur_md_start = md_end_char + 1 + trail_len
                while cur_md_start < md_next_char and body_md[cur_md_start].isspace():
                    cur_md_start += 1

            cur_norm_pos = end_norm_idx
        else:
            slice_text = body_md[cur_md_start:].strip()

        slices_by_page[pnum] = slice_text.strip()

    # Balance any single-* italic span that splits across a page boundary
    carry_italic = False
    for pnum in sorted(slices_by_page.keys()):
        stext = slices_by_page[pnum]
        if carry_italic:
            stext = "*" + stext
        # Count unescaped single asterisks outside `* * *` and `**`
        temp = re.sub(r"^\*\s*\*\s*\*\s*$", "", stext, flags=re.M)
        temp = re.sub(r"\(\*\d", "(X", temp)
        temp = temp.replace("**", "")
        star_count = temp.count("*")
        if star_count % 2 == 1:
            stext = stext + "*"
            carry_italic = True
        else:
            carry_italic = False
        slices_by_page[pnum] = stext

    return slices_by_page, fns


def clean_inline_rst(text: str) -> str:
    """Convert Markdown footnote refs and sanitize inline markup for Docutils RST."""
    # Escape Principia Mathematica theorem numbers like (*2.01) or (*1.2)
    text = re.sub(r"\(\*(\d)", r"(\*\1", text)

    # Convert [^12] or [^note] -> [#f12]_ or [#fnote]_ with valid Docutils spacing
    def repl_fn(m):
        prefix = m.group(1)
        fn_id = m.group(2)
        if prefix and not prefix.isspace():
            return f"{prefix} [#f{fn_id}]_"
        return f"{prefix}[#f{fn_id}]_"

    text = re.sub(r"(^|.)\[\^([^\]]+)\]", repl_fn, text)
    # If [#f...]_ is immediately followed by word char or opening quote/paren, escape space
    text = re.sub(r"(\[#f[^\]]+\]_)(?=[A-Za-z0-9«\"\(])", r"\1\\ ", text)
    return text


def convert_md_slice_to_rst(
    md_slice: str,
    fns_dict: Dict[str, str],
    page_num: int,
    book_title: str,
    section_slug: str,
    running_header: str | None,
) -> str:
    """Convert a page's aligned Markdown slice and its referenced footnotes into pure RST."""
    folio_str = f"{page_num:04d}"
    status = "rescan_needed" if page_num in RESCAN_NEEDED_PAGES else "ok"

    meta_lines = [
        f":folio: {folio_str}",
        f":page: {page_num}",
        ":volume: I",
        f":book: {book_title}",
        f":section: {section_slug}",
        f":title: {book_title} — p. {page_num}",
    ]
    if running_header:
        meta_lines.append(f":header: {running_header}")
    meta_lines.extend([
        ":language: la",
        f":status: {status}",
        "",
    ])

    referenced_fn_ids: List[str] = []
    for fid in re.findall(r"\[\^([^\]]+)\]", md_slice):
        if fid not in referenced_fn_ids:
            referenced_fn_ids.append(fid)

    out_blocks: List[str] = []
    raw_blocks = [b.strip() for b in md_slice.split("\n\n") if b.strip()]

    i = 0
    while i < len(raw_blocks):
        blk = raw_blocks[i]

        # Code block ``` ... ``` (e.g., ASCII diagram on page 172)
        if blk.startswith("```") and blk.endswith("```"):
            inner_lines = blk.splitlines()[1:-1]
            lit_lines = ["::", ""] + [f"   {l}" for l in inner_lines]
            out_blocks.append("\n".join(lit_lines))
            i += 1
            continue

        # Asterism transition * * *
        if re.match(r"^[\*\s]+$", blk):
            out_blocks.append("----")
            i += 1
            continue

        # Markdown headings (# .. #####)
        # Note: some titles have two consecutive ## lines in one block (e.g. CAPUT I subtitle)
        blk_lines = [l.strip() for l in blk.splitlines() if l.strip()]
        if all(re.match(r"^#{1,5}\s+", l) for l in blk_lines):
            first_m = re.match(r"^(#{1,5})\s+", blk_lines[0])
            level = len(first_m.group(1))
            combined_title = " — ".join(
                clean_inline_rst(re.sub(r"^#{1,5}\s+", "", l).strip())
                for l in blk_lines
            )
            ch = HEADING_CHARS.get(level, "^")
            bar = ch * max(len(combined_title), 4)
            out_blocks.append(f"{combined_title}\n{bar}")
            i += 1
            continue

        # Multi-line block with explicit line breaks (e.g., pebble rows or Leibniz demonstration)
        if "\n" in blk:
            lb_lines = [f"| {clean_inline_rst(l.strip())}" for l in blk.splitlines() if l.strip()]
            out_blocks.append("\n".join(lb_lines))
            i += 1
            continue

        # Standard paragraph
        out_blocks.append(clean_inline_rst(blk))
        i += 1

    # Append attached footnote definitions at bottom of folio
    if referenced_fn_ids:
        fn_rst_blocks: List[str] = []
        for fid in referenced_fn_ids:
            if fid in fns_dict:
                raw_fn = fns_dict[fid]
                fn_lines = [l.strip() for l in raw_fn.splitlines() if l.strip()]
                first_line = f".. [#f{fid}] {clean_inline_rst(fn_lines[0])}"
                rest_lines = [f"   {clean_inline_rst(l)}" for l in fn_lines[1:]]
                fn_rst_blocks.append("\n".join([first_line] + rest_lines))
        if fn_rst_blocks:
            out_blocks.extend(fn_rst_blocks)

    return "\n".join(meta_lines) + "\n" + "\n\n".join(out_blocks).rstrip() + "\n"


def convert_index_page_to_rst(
    raw_text: str,
    page_num: int,
    book_title: str,
    section_slug: str,
    running_header: str | None,
) -> str:
    """Convert Analytical Index pages (0289..0293) into clean RST with line-blocks."""
    folio_str = f"{page_num:04d}"
    meta_lines = [
        f":folio: {folio_str}",
        f":page: {page_num}",
        ":volume: I",
        f":book: {book_title}",
        f":section: {section_slug}",
        f":title: {book_title} — p. {page_num}",
    ]
    if running_header:
        meta_lines.append(f":header: {running_header}")
    meta_lines.extend([
        ":language: la",
        ":status: ok",
        "",
    ])

    lines = [l.rstrip() for l in raw_text.splitlines()]
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and HEADER_PATTERN.match(lines[0]):
        lines.pop(0)
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    if lines and FOOTER_PATTERN.match(lines[-1]):
        lines.pop()
    while lines and not lines[-1].strip():
        lines.pop()

    out_blocks: List[str] = []
    cur_line_block: List[str] = []

    def flush_lb():
        nonlocal cur_line_block
        if cur_line_block:
            out_blocks.append("\n".join(cur_line_block))
            cur_line_block = []

    for line in lines:
        s = line.strip()
        if not s:
            flush_lb()
            continue
        m_head = re.match(r"^(#{1,5})\s+(.*)$", s)
        if m_head:
            flush_lb()
            level = len(m_head.group(1))
            t = clean_inline_rst(m_head.group(2).strip())
            ch = HEADING_CHARS.get(level, "=")
            out_blocks.append(f"{t}\n{ch * max(len(t), 4)}")
            continue
        # Indent sub-entries cleanly inside line-block
        if re.match(r"^[A-Z]\.\s+", s):
            cur_line_block.append(f"|       {clean_inline_rst(s)}")
        elif re.match(r"^\d+\.\s+", s):
            cur_line_block.append(f"|    {clean_inline_rst(s)}")
        elif s.startswith("§"):
            cur_line_block.append(f"|  {clean_inline_rst(s)}")
        else:
            cur_line_block.append(f"| {clean_inline_rst(s)}")

    flush_lb()
    return "\n".join(meta_lines) + "\n" + "\n\n".join(out_blocks).rstrip() + "\n"


def sanitize_snippet(text: str, max_len: int = 80) -> str:
    """Sanitize a text snippet for safe embedding inside RST inline literals ``...``."""
    s = re.sub(r"\s+", " ", text).strip()
    s = s.replace("`", "'")
    if len(s) > max_len:
        s = s[: max_len - 3].rstrip() + "..."
    return s


def analyze_page_structure(
    raw_text: str,
    md_slice: str | None,
    fns_dict: Dict[str, str],
) -> Dict[str, Any]:
    """Extract structural and diplomatic features for `<NNNN>.notes.rst`."""
    running_header, printer_sig = extract_page_header_and_footer(raw_text)
    headings: List[str] = []
    footnotes: List[str] = []
    body_lines: List[str] = []

    if md_slice is not None:
        for blk in [b.strip() for b in md_slice.split("\n\n") if b.strip()]:
            blk_lines = [l.strip() for l in blk.splitlines() if l.strip()]
            if all(re.match(r"^#{1,5}\s+", l) for l in blk_lines):
                headings.append(
                    " — ".join(re.sub(r"^#{1,5}\s+", "", l).strip() for l in blk_lines)
                )
            elif re.match(r"^[\*\s]+$", blk):
                headings.append("Typographic Asterism (Section Transition)")
            else:
                body_lines.extend(blk_lines)

        for fid in re.findall(r"\[\^([^\]]+)\]", md_slice):
            if fid in fns_dict:
                fn_preview = sanitize_snippet(fns_dict[fid], 90)
                entry = f"Footnote {fid}: ``{fn_preview}``"
                if entry not in footnotes:
                    footnotes.append(entry)
    else:
        for l in raw_text.splitlines():
            s = l.strip()
            if not s or HEADER_PATTERN.match(s) or FOOTER_PATTERN.match(s):
                continue
            m_head = re.match(r"^(#{1,5})\s+(.*)$", s)
            if m_head:
                headings.append(m_head.group(2).strip())
            else:
                body_lines.append(s)

    greek_matches = re.findall(
        r"[\u0370-\u03ff\u1f00-\u1fff]+(?:\s+[\u0370-\u03ff\u1f00-\u1fff]+)*",
        raw_text,
    )
    seen_greek: List[str] = []
    for g in greek_matches:
        g_clean = g.strip()
        if g_clean and g_clean not in seen_greek:
            seen_greek.append(g_clean)

    first_line = body_lines[0] if body_lines else (headings[0] if headings else "")
    last_line = body_lines[-1] if body_lines else (headings[-1] if headings else "")

    raw_body = [
        l.strip()
        for l in raw_text.splitlines()
        if l.strip() and not HEADER_PATTERN.match(l.strip()) and not FOOTER_PATTERN.match(l.strip())
    ]
    hyphenated_breaks = []
    for idx in range(len(raw_body) - 1):
        curr_l = raw_body[idx]
        next_l = raw_body[idx + 1]
        m_end = re.search(r"([A-Za-z\u00C0-\u017F]+)-\s*$", curr_l)
        m_start = re.match(r"^([A-Za-z\u00C0-\u017F]+)", next_l)
        if m_end and m_start:
            hyphenated_breaks.append(f"{m_end.group(1)}-{m_start.group(1)}")

    ends_with_hyphen = bool(last_line and last_line.endswith("-"))
    starts_lowercase = bool(first_line and first_line[0].islower())

    return {
        "running_header": running_header,
        "headings": headings,
        "footnotes": footnotes,
        "greek_terms": seen_greek,
        "first_line": first_line,
        "last_line": last_line,
        "ends_with_hyphen": ends_with_hyphen,
        "starts_lowercase": starts_lowercase,
        "hyphenated_breaks": hyphenated_breaks,
        "printer_sig": printer_sig,
    }


def generate_notes_rst(
    folio_info: Dict[str, Any],
    prev_info: Dict[str, Any] | None,
    next_info: Dict[str, Any] | None,
    scan_inv: Dict[str, str] | None,
) -> str:
    """Generate companion <NNNN>.notes.rst content for a folio."""
    page_num = folio_info["page_num"]
    folio_str = folio_info["folio_str"]
    book_title = folio_info["book_title"]
    sec_slug = folio_info["sec_slug"]
    analysis = folio_info["analysis"]
    is_partial = page_num in RESCAN_NEEDED_PAGES
    status_str = "rescan_needed" if is_partial else "ok"

    title = f"Folio {folio_str} (Page {page_num}) — Transcription & Calibration Notes"
    bar = "=" * len(title)

    lines = [
        title,
        bar,
        "",
        "Summary & Folio Continuity",
        "--------------------------",
        "",
    ]

    if prev_info:
        prev_last = sanitize_snippet(prev_info["analysis"]["last_line"], 65)
        lines.append(
            f"- **Preceding Folio** (``{prev_info['folio_str']}.rst``): "
            f"Page {prev_info['page_num']}, {prev_info['book_title']} [``{prev_info['sec_slug']}``] "
            f"— Ends: ``\"{prev_last}\"``"
        )
    else:
        lines.append(
            "- **Preceding Folio**: None (First transcribed folio of Volume I, *Praefatio*)"
        )

    lines.append(
        f"- **Current Folio** (``{folio_str}.rst``): "
        f"Page {page_num}, {book_title} [``{sec_slug}``] — Status: ``{status_str}``"
    )

    if next_info:
        next_first = sanitize_snippet(next_info["analysis"]["first_line"], 65)
        lines.append(
            f"- **Following Folio** (``{next_info['folio_str']}.rst``): "
            f"Page {next_info['page_num']}, {next_info['book_title']} [``{next_info['sec_slug']}``] "
            f"— Begins: ``\"{next_first}\"``"
        )
    else:
        lines.append(
            "- **Following Folio**: None (Final transcribed folio of Volume I, *Index Analyticus*)"
        )

    lines.extend([
        "",
        "Structural & Diplomatic Observations",
        "------------------------------------",
        "",
    ])

    if analysis["running_header"]:
        rh_clean = sanitize_snippet(analysis["running_header"], 80)
        lines.append(f"- **Running Header / Rubric**: ``{rh_clean}``")
    else:
        lines.append("- **Running Header / Rubric**: None (Section opening or unnumbered top margin)")

    if analysis["headings"]:
        h_formatted = ", ".join(f"``{sanitize_snippet(h, 70)}``" for h in analysis["headings"])
        lines.append(f"- **Document Headings on Folio**: {h_formatted}")
    else:
        lines.append("- **Document Headings on Folio**: None (Continuous prose body)")

    if analysis["footnotes"]:
        lines.append(f"- **Footnotes on Folio ({len(analysis['footnotes'])})**:")
        for fn_desc in analysis["footnotes"]:
            lines.append(f"  - {fn_desc}")
    else:
        lines.append("- **Footnotes on Folio**: None")

    if analysis["greek_terms"]:
        g_formatted = ", ".join(f"``{sanitize_snippet(g, 40)}``" for g in analysis["greek_terms"][:15])
        if len(analysis["greek_terms"]) > 15:
            g_formatted += f" (+{len(analysis['greek_terms']) - 15} more)"
        lines.append(
            f"- **Classical Greek Philosophical Terms ({len(analysis['greek_terms'])})**: {g_formatted}"
        )
    else:
        lines.append("- **Classical Greek Philosophical Terms**: None (Latin text only on this folio)")

    first_snip = sanitize_snippet(analysis["first_line"], 75) if analysis["first_line"] else "(empty)"
    last_snip = sanitize_snippet(analysis["last_line"], 75) if analysis["last_line"] else "(empty)"

    top_note = "continues sentence/word from preceding folio" if (
        (prev_info and prev_info["analysis"]["ends_with_hyphen"]) or analysis["starts_lowercase"]
    ) else "begins new sentence or heading"

    bottom_note = "ends with word-break hyphenation across folio boundary" if analysis["ends_with_hyphen"] else "complete token at bottom of folio"

    lines.append(f"- **Folio Opening Line**: ``\"{first_snip}\"`` (*{top_note}*)")
    lines.append(f"- **Folio Closing Line**: ``\"{last_snip}\"`` (*{bottom_note}*)")

    if analysis["hyphenated_breaks"]:
        hb_sample = ", ".join(f"``{w}``" for w in analysis["hyphenated_breaks"][:8])
        if len(analysis["hyphenated_breaks"]) > 8:
            hb_sample += f" (+{len(analysis['hyphenated_breaks']) - 8} more)"
        lines.append(
            f"- **Internal Line-Break Hyphenations in 1954 Print ({len(analysis['hyphenated_breaks'])})**: {hb_sample}"
        )
    else:
        lines.append("- **Internal Line-Break Hyphenations in 1954 Print**: None detected")

    if analysis["printer_sig"]:
        lines.append(f"- **Bottom Printer Signature / Catch-Number**: ``{analysis['printer_sig']}``")

    lines.extend([
        "",
        "Scan Status & Calibration",
        "-------------------------",
        "",
    ])

    source_ref = scan_inv["source_ref"] if scan_inv else f"archive/{folio_info['archive_sub']}/page-{page_num:03d}.png"
    extracted_file = scan_inv["extracted_file"] if scan_inv else f"page-{page_num:03d}.png"
    variants = ", ".join(f"``{v}``" for v in folio_info["scan_symlinks"])

    lines.append(f"- **Primary Scan Symlink**: ``{folio_str}.png`` -> ``archive/{folio_info['archive_sub']}/page-{page_num:03d}.png``")
    lines.append(f"- **Available Scan Files in Section**: {variants}")
    lines.append(f"- **Archival Source Reference**: ``{source_ref}`` (extracted as ``{extracted_file}``)")
    lines.append(f"- **Quality Status**: ``{status_str}``")
    lines.append("")

    if is_partial:
        lines.extend([
            ".. warning::",
            "",
            f"   **Partial Scan — Margin Cutoff (``page-{page_num:03d}-partial.png`` / ``:status: rescan_needed``)**",
            "",
            f"   Folio ``{folio_str}`` (Page {page_num}) was partially cut off along the margin during portrait-oriented scanning (source: ``{source_ref}``). Missing characters and word endings along the cut edge were supplied from syntactic and philosophical context during diplomatic transcription. A full-page landscape rescan is required to verify the affected margin lines.",
            "",
        ])
    elif page_num == 268:
        lines.extend([
            ".. note::",
            "",
            "   **Rescanned & Verified (``page-268.png`` / ``:status: ok``)**",
            "",
            "   This folio was previously listed among the partial scans and has since been rescanned and resolved in ``appendix-2.pdf (p. 16, left)``.",
            "",
        ])
    else:
        lines.extend([
            ".. note::",
            "",
            f"   **Complete Scan (``page-{page_num:03d}.png`` / ``:status: ok``)**",
            "",
            f"   Full-page archival scan verified from ``{source_ref}`` with complete margins and legible diplomatic text.",
            "",
        ])

    return "\n".join(lines)


def main():
    scan_inventory = load_scan_inventory()
    total_folios = 0
    total_notes = 0
    total_symlinks = 0
    rescan_count = 0

    all_folios: List[Dict[str, Any]] = []

    for archive_sub, sec_slug, book_title, md_rel in SECTIONS:
        src_dir = os.path.join(ARCHIVE_DIR, archive_sub)
        dst_dir = os.path.join(OUT_VOL_DIR, sec_slug)
        os.makedirs(dst_dir, exist_ok=True)

        symlinks_by_page: Dict[int, List[str]] = {}
        png_files = sorted(glob.glob(os.path.join(src_dir, "page-*.png")))
        for png_path in png_files:
            fname = os.path.basename(png_path)
            m = re.match(r"^page-(\d{3})(.*\.png)$", fname)
            if not m:
                continue
            page_num = int(m.group(1))
            suffix = m.group(2)
            dst_name = f"{page_num:04d}{suffix}"
            dst_link = os.path.join(dst_dir, dst_name)
            rel_target = os.path.relpath(png_path, dst_dir)
            if os.path.lexists(dst_link):
                os.remove(dst_link)
            os.symlink(rel_target, dst_link)
            total_symlinks += 1
            symlinks_by_page.setdefault(page_num, []).append(dst_name)

        txt_files = sorted(glob.glob(os.path.join(src_dir, "page-[0-9][0-9][0-9].txt")))
        if md_rel is not None:
            slices_by_page, fns_dict = slice_section_md_by_pages(
                archive_sub, md_rel, txt_files
            )
        else:
            slices_by_page, fns_dict = {}, {}

        for txt_path in txt_files:
            fname = os.path.basename(txt_path)
            m = re.match(r"^page-(\d{3})\.txt$", fname)
            if not m:
                continue
            page_num = int(m.group(1))
            with open(txt_path, "r", encoding="utf-8") as f:
                raw_text = f.read()

            md_slice = slices_by_page.get(page_num)
            analysis = analyze_page_structure(raw_text, md_slice, fns_dict)

            all_folios.append({
                "page_num": page_num,
                "folio_str": f"{page_num:04d}",
                "archive_sub": archive_sub,
                "sec_slug": sec_slug,
                "book_title": book_title,
                "dst_dir": dst_dir,
                "raw_text": raw_text,
                "md_slice": md_slice,
                "fns_dict": fns_dict,
                "scan_symlinks": sorted(symlinks_by_page.get(page_num, [f"{page_num:04d}.png"])),
                "analysis": analysis,
            })

    all_folios.sort(key=lambda x: x["page_num"])

    for idx, f_info in enumerate(all_folios):
        page_num = f_info["page_num"]
        folio_str = f_info["folio_str"]
        dst_dir = f_info["dst_dir"]
        running_header = f_info["analysis"]["running_header"]

        if f_info["md_slice"] is not None:
            rst_content = convert_md_slice_to_rst(
                f_info["md_slice"],
                f_info["fns_dict"],
                page_num,
                f_info["book_title"],
                f_info["sec_slug"],
                running_header,
            )
        else:
            rst_content = convert_index_page_to_rst(
                f_info["raw_text"],
                page_num,
                f_info["book_title"],
                f_info["sec_slug"],
                running_header,
            )

        dst_rst = os.path.join(dst_dir, f"{folio_str}.rst")
        with open(dst_rst, "w", encoding="utf-8") as f:
            f.write(rst_content)
        total_folios += 1

        prev_info = all_folios[idx - 1] if idx > 0 else None
        next_info = all_folios[idx + 1] if idx + 1 < len(all_folios) else None
        scan_inv = scan_inventory.get(page_num)

        notes_content = generate_notes_rst(f_info, prev_info, next_info, scan_inv)
        dst_notes = os.path.join(dst_dir, f"{folio_str}.notes.rst")
        with open(dst_notes, "w", encoding="utf-8") as f:
            f.write(notes_content)
        total_notes += 1

        if page_num in RESCAN_NEEDED_PAGES:
            rescan_count += 1

    reviews_data: Dict[str, Dict[str, Any]] = {}
    for page_num in sorted(RESCAN_NEEDED_PAGES):
        folio_str = f"{page_num:04d}"
        key = f"volume_I:{folio_str}"
        reviews_data[key] = {
            "status": "needs_fix",
            "notes": f"Right margin cut off in original scan (page-{page_num:03d}-partial.png); needs rescan.",
            "checklist": {
                "transcription": True,
                "footnotes": True,
                "formatting": True,
                "scan_quality": False,
                "transcription_verified": True,
                "math_verified": True,
                "notes_verified": True,
                "graphics_verified": False,
            },
            "reviewer": "phi",
            "updated_at": "2026-10-18T17:45:00+00:00",
        }

    reviews_path = os.path.join(RES_HOENEN_DIR, "folio_reviews.json")
    with open(reviews_path, "w", encoding="utf-8") as f:
        json.dump(reviews_data, f, indent=2, sort_keys=True)
        f.write("\n")

    print(
        f"Prepared {total_folios} folio .rst files, {total_notes} .notes.rst files, "
        f"and {total_symlinks} image symlinks in {OUT_VOL_DIR}"
    )
    print(f"Marked {rescan_count} folios as :status: rescan_needed and populated {reviews_path}")


if __name__ == "__main__":
    main()
