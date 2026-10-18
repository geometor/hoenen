#!/usr/bin/env python3
"""
scripts/prepare_folio_review.py

Organizes the 287 page scans and diplomatic transcriptions from `archive/`
into `resources/hoenen_1954/volume_I/<section>/` for the GEOMETOR Folio Reviewer:
- Creates relative symlinks `<NNNN>.png` -> `../../../../archive/<archive_dir>/page-NNN.png`
  (plus `-partial.png` and `-photo.png` variants where present).
- Converts `page-NNN.txt` into clean diplomatic `<NNNN>.rst` files with top
  reStructuredText field-list metadata and validated RST body.
"""

import os
import re
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE_DIR = os.path.join(BASE_DIR, "archive")
OUT_VOL_DIR = os.path.join(BASE_DIR, "resources", "hoenen_1954", "volume_I")

SECTIONS = [
    ("preface", "00_preface", "Praefatio"),
    ("chapter-01", "01_caput_1", "Caput I"),
    ("chapter-02", "02_caput_2", "Caput II"),
    ("chapter-03", "03_caput_3", "Caput III"),
    ("chapter-04", "04_caput_4", "Caput IV"),
    ("chapter-05", "05_caput_5", "Caput V"),
    ("chapter-06", "06_caput_6", "Caput VI"),
    ("chapter-07", "07_caput_7", "Caput VII"),
    ("appendix", "08_appendix", "Appendix"),
    ("index", "09_index", "Index Analyticus"),
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


def clean_inline_rst(text: str) -> str:
    """Convert Markdown footnote refs and sanitize stray inline markup for RST."""
    # Escape Principia Mathematica theorem numbers like (*2.01) or (*1.2)
    text = re.sub(r"\(\*(\d)", r"(\*\1", text)

    # Convert [^12] -> [#f12]_ ensuring a preceding space if attached to word/punct
    def repl_fn(m):
        prefix = m.group(1)
        fn_id = m.group(2)
        if prefix and not prefix.isspace():
            return f"{prefix} [#f{fn_id}]_"
        return f"{prefix}[#f{fn_id}]_"

    text = re.sub(r"(^|.)\[\^(\d+)\]", repl_fn, text)
    return text


def convert_page_txt_to_rst(raw_text: str, page_num: int, book_title: str, section_slug: str) -> str:
    folio_str = f"{page_num:04d}"
    status = "rescan_needed" if page_num in RESCAN_NEEDED_PAGES else "ok"

    meta_lines = [
        f":folio: {folio_str}",
        f":page: {page_num}",
        ":volume: I",
        f":book: {book_title}",
        f":section: {section_slug}",
        f":title: {book_title} — p. {page_num}",
        ":language: la",
        f":status: {status}",
        "",
    ]

    referenced_fns = set(re.findall(r"\[\^(\d+)\]", raw_text))
    lines = raw_text.splitlines()

    # Remove trailing empty lines and isolated printer signature/page number at very bottom (e.g. "835")
    while lines and not lines[-1].strip():
        lines.pop()
    if lines and re.match(r"^\s*\d+\s*$", lines[-1]):
        lines.pop()
    while lines and not lines[-1].strip():
        lines.pop()

    # Process lines into blocks
    out_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()

        # Blank line
        if not stripped:
            out_lines.append("")
            i += 1
            continue

        # Typographic asterism (* or *   *) -> RST transition
        if re.match(r"^[\*\s]+$", stripped):
            while i + 1 < len(lines) and re.match(r"^[\*\s]*$", lines[i + 1].strip()):
                i += 1
            if out_lines and out_lines[-1] != "":
                out_lines.append("")
            out_lines.append("----")
            out_lines.append("")
            i += 1
            continue

        # Running header at top of page like "10     CAPUT I" or "DE NOETICA GEOMETRIAE    11"
        if i == 0 and re.match(r"^(\d+\s{3,}.+|.+\s{3,}\d+)$", stripped):
            out_lines.append(f".. rubric:: {stripped}")
            out_lines.append("")
            i += 1
            continue

        # Markdown headings: # ..., ## ..., ### ...
        m_head = re.match(r"^(#{1,5})\s+(.*)$", stripped)
        if m_head:
            level = len(m_head.group(1))
            title_txt = clean_inline_rst(m_head.group(2).strip())
            ch = HEADING_CHARS.get(level, "^")
            bar = ch * max(len(title_txt), 4)
            if out_lines and out_lines[-1] != "":
                out_lines.append("")
            out_lines.append(title_txt)
            out_lines.append(bar)
            out_lines.append("")
            i += 1
            continue

        # Plain-text major headings on their own line: PRAEFATIO, CAPUT I..VII, APPENDIX, INDEX ANALYTICUS
        if re.match(r"^(PRAEFATIO|CAPUT\s+[IVXLCDM]+|APPENDIX|INDEX ANALYTICUS)$", stripped):
            ch = "="
            bar = ch * max(len(stripped), 4)
            if out_lines and out_lines[-1] != "":
                out_lines.append("")
            out_lines.append(stripped)
            out_lines.append(bar)
            out_lines.append("")
            i += 1
            continue

        # Plain-text section headings starting with § N.
        if re.match(r"^§\s*\d+\.", stripped) and not stripped.endswith(tuple(str(d) for d in range(10))):
            title_parts = [stripped]
            while i + 1 < len(lines) and lines[i + 1].strip() and lines[i + 1].strip().isupper():
                i += 1
                title_parts.append(lines[i].strip())
            full_title = clean_inline_rst(" ".join(title_parts))
            ch = "~"
            bar = ch * max(len(full_title), 4)
            if out_lines and out_lines[-1] != "":
                out_lines.append("")
            out_lines.append(full_title)
            out_lines.append(bar)
            out_lines.append("")
            i += 1
            continue

        # Markdown footnote definition: [^1]: ...
        m_fn = re.match(r"^\[\^(\d+)\]:\s*(.*)$", stripped)
        if m_fn:
            fn_id = m_fn.group(1)
            fn_body = clean_inline_rst(m_fn.group(2).strip())
            if out_lines and out_lines[-1] != "":
                out_lines.append("")
            out_lines.append(f".. [#f{fn_id}] {fn_body}")
            out_lines.append("")
            i += 1
            continue

        # Bare footnote definition at bottom of page when [^N] was used in body: "1 Vide..."
        m_bare_fn = re.match(r"^(\d+)\s+(.*)$", stripped)
        if (
            m_bare_fn
            and m_bare_fn.group(1) in referenced_fns
            and not m_bare_fn.group(2).startswith("et ")
        ):
            fn_id = m_bare_fn.group(1)
            referenced_fns.discard(fn_id)
            fn_body = clean_inline_rst(m_bare_fn.group(2).strip())
            if out_lines and out_lines[-1] != "":
                out_lines.append("")
            out_lines.append(f".. [#f{fn_id}] {fn_body}")
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r"^(\d+)\s+", lines[i].strip()):
                out_lines.append(f"   {clean_inline_rst(lines[i].strip())}")
                i += 1
            out_lines.append("")
            continue

        # Regular line
        cleaned = clean_inline_rst(stripped)
        prev_nonblank = bool(out_lines and out_lines[-1] != "")
        if prev_nonblank:
            if re.match(r"^(\d+[\.\)]|[a-zA-Z][\.\)]|\*|-)\s+", cleaned):
                out_lines.append("")
        out_lines.append(cleaned)
        i += 1

    # Collapse multiple blank lines
    final_body = []
    for l in out_lines:
        if l == "" and (not final_body or final_body[-1] == ""):
            continue
        final_body.append(l)

    return "\n".join(meta_lines + final_body).rstrip() + "\n"


def main():
    total_folios = 0
    total_symlinks = 0
    rescan_count = 0

    for archive_sub, sec_slug, book_title in SECTIONS:
        src_dir = os.path.join(ARCHIVE_DIR, archive_sub)
        dst_dir = os.path.join(OUT_VOL_DIR, sec_slug)
        os.makedirs(dst_dir, exist_ok=True)

        # Find all page-NNN*.png files
        png_files = sorted(glob.glob(os.path.join(src_dir, "page-*.png")))
        for png_path in png_files:
            fname = os.path.basename(png_path)
            m = re.match(r"^page-(\d{3})(.*\.png)$", fname)
            if not m:
                continue
            page_num = int(m.group(1))
            suffix = m.group(2)  # ".png" or "-partial.png" or "-photo.png"
            dst_name = f"{page_num:04d}{suffix}"
            dst_link = os.path.join(dst_dir, dst_name)
            rel_target = os.path.relpath(png_path, dst_dir)
            if os.path.lexists(dst_link):
                os.remove(dst_link)
            os.symlink(rel_target, dst_link)
            total_symlinks += 1

        # Find all page-NNN.txt files
        txt_files = sorted(glob.glob(os.path.join(src_dir, "page-[0-9][0-9][0-9].txt")))
        for txt_path in txt_files:
            fname = os.path.basename(txt_path)
            m = re.match(r"^page-(\d{3})\.txt$", fname)
            if not m:
                continue
            page_num = int(m.group(1))
            with open(txt_path, "r", encoding="utf-8") as f:
                raw_text = f.read()

            rst_content = convert_page_txt_to_rst(raw_text, page_num, book_title, sec_slug)
            dst_rst = os.path.join(dst_dir, f"{page_num:04d}.rst")
            with open(dst_rst, "w", encoding="utf-8") as f:
                f.write(rst_content)
            total_folios += 1
            if page_num in RESCAN_NEEDED_PAGES:
                rescan_count += 1

    print(f"Prepared {total_folios} folio .rst files and {total_symlinks} image symlinks in {OUT_VOL_DIR}")
    print(f"Marked {rescan_count} folios as :status: rescan_needed")


if __name__ == "__main__":
    main()
