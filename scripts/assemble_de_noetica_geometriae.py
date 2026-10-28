#!/usr/bin/env python3
"""
scripts/assemble_de_noetica_geometriae.py

Depaginates the 287 reviewed and enriched Latin folios from
`resources/de_noetica_geometriae/00_preface..08_appendix` into the
Codex chapter files under `docsrc/de_noetica_geometriae/`:
- Merges cross-page split words (hyphenation), mid-sentence page breaks,
  and same-paragraph terminal-punctuation page breaks.
- Preserves all restored authorial italics (`*...*`), 3-space indented
  blockquotes (`   « ... »`), and `:cite:`, `:term:`, and `:person:` tags.
- Preserves all 135 canonical section labels (`.. _caput-N-la-sM:...`) and
  standardized heading underlines (`=`, `-`, `~`, `^`, `"`).
- Collects and outputs all chapter footnotes (`.. [#f1] ...`) at the end
  of each chapter.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path("/home/phi/PROJECTS/geometor/hoenen")
RES_DIR = ROOT / "resources" / "de_noetica_geometriae"
BOOK_DOC_DIR = ROOT / "docsrc" / "de_noetica_geometriae"

CHAPTERS: List[Tuple[str, str]] = [
    ("00_preface", "preface/preface.rst"),
    ("01_caput_1", "caput-1/caput-1.rst"),
    ("02_caput_2", "caput-2/caput-2.rst"),
    ("03_caput_3", "caput-3/caput-3.rst"),
    ("04_caput_4", "caput-4/caput-4.rst"),
    ("05_caput_5", "caput-5/caput-5.rst"),
    ("06_caput_6", "caput-6/caput-6.rst"),
    ("07_caput_7", "caput-7/caput-7.rst"),
    ("08_appendix", "appendix/appendix.rst"),
]


def norm_alnum(s: str) -> str:
    """Normalize string to lowercase letters/digits, stripping RST roles and footnote refs."""
    s = re.sub(r":(?:cite|term|person):`([^`<]+?)(?:\s*<[^>]+>)?`", r"\1", s)
    s = re.sub(r"\[#[^\]]+\]_", "", s)
    s = re.sub(r"\[\^[^\]]+\]", "", s)
    return re.sub(r"[^a-zA-Z0-9\u00C0-\u017F\u0370-\u03ff\u1f00-\u1fff]", "", s).lower()


def is_heading_block(block: str) -> bool:
    """Return True if `block` is a 2-line RST section heading."""
    lines = block.strip().splitlines()
    if len(lines) == 2 and re.match(r"^[=\-~^\"+]{3,}$", lines[1].strip()):
        return True
    return False


def is_blockquote(block: str) -> bool:
    """Return True if `block` is an indented blockquote (starts with 3+ spaces)."""
    lines = [l for l in block.splitlines() if l.strip()]
    return bool(lines) and all(l.startswith("   ") for l in lines)


def split_folio_content(txt: str) -> Tuple[List[str], List[str]]:
    """Return (body_blocks, footnote_blocks) from a folio `.rst` file."""
    lines = txt.splitlines()
    i = 0
    # Skip top field-list metadata
    while i < len(lines) and lines[i].strip():
        i += 1
    while i < len(lines) and not lines[i].strip():
        i += 1

    body_lines: List[str] = []
    fn_lines: List[str] = []
    in_fn = False
    for line in lines[i:]:
        if re.match(r"^\.\.\s+\[#", line):
            in_fn = True
        if in_fn:
            fn_lines.append(line)
        else:
            body_lines.append(line)

    body_str = "\n".join(body_lines).strip()
    raw_blocks = [b.rstrip() for b in re.split(r"\n\s*\n", body_str) if b.strip()]

    fn_str = "\n".join(fn_lines).strip()
    fn_blocks: List[str] = []
    if fn_str:
        m_iter = list(re.finditer(r"(?m)^\.\.\s+\[#[^\]]+\]\s+", fn_str))
        for idx, m in enumerate(m_iter):
            start = m.start()
            end = m_iter[idx + 1].start() if idx + 1 < len(m_iter) else len(fn_str)
            fn_block = fn_str[start:end].strip()
            # Join wrapped lines inside a footnote into clean single-line or indented block
            fn_blocks.append(fn_block)

    return raw_blocks, fn_blocks


def extract_chapter_preamble_and_labels(
    chap_txt: str,
) -> Tuple[str, List[Tuple[str, str, str, str]], List[str]]:
    """Extract (preamble, section_labels, normalized_paragraphs) from existing chapter RST."""
    # Strip any legacy `.. container:: track-nav` or existing `.. contents::` block before re-extracting
    chap_txt = re.sub(
        r"\n*\.\.\s+container::\s+track-nav\n+(?:[ \t]+[^\n]+\n?)+",
        "\n",
        chap_txt,
    )
    chap_txt = re.sub(
        r"\n*\.\.\s+contents::[^\n]*\n+(?:[ \t]+:[^\n]+\n?)+",
        "\n",
        chap_txt,
    )
    # Preamble ends right after the level-1 `===` chapter heading and optional `.. rubric::` subtitle
    m_head = re.search(
        r"(?m)^([^\n]+\n={3,}(?:\n+\.\.\s+rubric::\s+[^\n]+)*)",
        chap_txt,
    )
    assert m_head is not None, "Chapter level-1 heading not found in chapter RST"
    preamble = chap_txt[: m_head.end()].strip()
    if "_preface-" not in preamble:
        preamble += (
            "\n\n.. contents:: Conspectus Capitis\n"
            "   :local:\n"
            "   :depth: 3\n"
            "   :backlinks: none"
        )

    # Extract all labeled headings after preamble
    rest = chap_txt[m_head.end() :]
    labels: List[Tuple[str, str, str, str]] = []
    for m in re.finditer(r"(?m)^\.\.\s+_([^:]+):\n\n([^\n]+)\n([=\-~^\"+]+)$", rest):
        lbl = m.group(1).strip()
        title = m.group(2).strip()
        uline_char = m.group(3).strip()[0]
        labels.append((lbl, title, norm_alnum(title), uline_char))

    chap_paras = [norm_alnum(p) for p in rest.split("\n\n") if norm_alnum(p)]
    return preamble, labels, chap_paras


def join_across_page_boundary(p1: str, p2: str) -> str:
    """Join block `p1` (end of page N) and `p2` (start of page N+1) into a single block."""
    bq1 = is_blockquote(p1)
    bq2 = is_blockquote(p2)
    p2_stripped = p2.lstrip() if bq1 and bq2 else p2.strip()

    # Case 1: Hyphenated word split at end of p1
    # Check if p1 ends with `-*` and p2 starts with `*` (italicized word split across pages)
    if re.search(r"-\*\s*$", p1) and p2_stripped.startswith("*"):
        p1_clean = re.sub(r"-\*\s*$", "", p1)
        p2_clean = p2_stripped[1:]
        return p1_clean + p2_clean

    # Check if p1 ends with `-` (possibly inside `:term:` or normal word)
    if re.search(r"-\s*$", p1):
        p1_clean = re.sub(r"-\s*$", "", p1)
        return p1_clean + p2_stripped

    # Case 2: Normal space join
    return p1.rstrip() + " " + p2_stripped


def should_merge_page_boundary(p1: str, p2: str, chap_paras: List[str], label_norms: set[str]) -> bool:
    """Return True if `p1` (last block of page N) and `p2` (first block of page N+1) belong to the same paragraph."""
    if is_heading_block(p1) or is_heading_block(p2):
        return False
    if p1.strip() == "* * *" or p2.strip() == "* * *":
        return False
    if p1.lstrip().startswith("| ") or p2.lstrip().startswith("| "):
        return False
    if norm_alnum(p1) in label_norms or norm_alnum(p2) in label_norms:
        return False
    # Check for the 6 inline lead-in headings so we never merge across them
    for lead in (
        "A). *Methodus Leibnizii.*",
        "B). *Methodus Mercier.*",
        "C). Notamus breviter.",
        "*Conspectus.*",
        "*Nota.* In neo-positivismo",
        "Ad has breves animadversiones restringere",
    ):
        if p2.strip().startswith(lead):
            return False

    # If one is a blockquote and the other is not, do not merge
    if is_blockquote(p1) != is_blockquote(p2):
        return False

    # Rule 1: Ends with a hyphen
    if re.search(r"-\*?\s*$", p1):
        return True

    # Rule 2: Does not end with terminal sentence punctuation
    # Strip trailing footnote refs, closing quotes/parens/italics
    tail_check = re.sub(r"(\s*\[#[^\]]+\]_|\*|\)|\]|»|\")+\s*$", "", p1.strip())
    if not re.search(r"[.?!:]$", tail_check):
        return True

    # Rule 3: Ends with terminal punctuation, check if joined in existing chapter paragraphs
    n1 = norm_alnum(p1)
    n2 = norm_alnum(p2)
    if len(n1) >= 15 and len(n2) >= 15:
        tail = n1[-25:]
        head = n2[:25]
        for cp in chap_paras:
            pos1 = cp.find(tail)
            if pos1 != -1:
                pos2 = cp.find(head, pos1)
                if pos2 != -1 and (pos2 - (pos1 + len(tail))) <= 5:
                    return True

    return False


def expand_inline_lead_in_headings(blocks: List[str]) -> List[str]:
    """Split the 6 inline lead-in headings into standalone heading blocks to match the Analytical Index."""
    expanded: List[str] = []
    for b in blocks:
        s = b.strip()
        if s.startswith("A). *Methodus Leibnizii.* "):
            expanded.append("A) *Methodus Leibnizii.*\n^^^^^^^^^^^^^^^^^^^^^^^^")
            expanded.append(s[len("A). *Methodus Leibnizii.* ") :].strip())
        elif s.startswith("B). *Methodus Mercier.* "):
            expanded.append("B) *Methodus Mercier.*\n^^^^^^^^^^^^^^^^^^^^^^")
            expanded.append(s[len("B). *Methodus Mercier.* ") :].strip())
        elif s.startswith("C). Notamus breviter. Nec deductio *logistica*"):
            expanded.append("C) *Deductio logistica.*\n^^^^^^^^^^^^^^^^^^^^^^^^")
            expanded.append("Notamus breviter: " + s[len("C). Notamus breviter. ") :].strip())
        elif s.startswith("*Conspectus.* In hisce igitur"):
            expanded.append("*Conspectus.*\n^^^^^^^^^^^^^")
            expanded.append(s[len("*Conspectus.* ") :].strip())
        elif s.startswith("*Nota.* In neo-positivismo moderno"):
            expanded.append("*Nota de neo-positivismo.*\n^^^^^^^^^^^^^^^^^^^^^^^^^^")
            expanded.append(s[len("*Nota.* ") :].strip())
        elif s.startswith("Ad has breves animadversiones restringere debebamus"):
            expanded.append("Additiones\n~~~~~~~~~~")
            expanded.append(b)
        else:
            expanded.append(b)
    return expanded


def assemble_chapter(sec_name: str, rel_rst: str) -> Tuple[int, int, int]:
    """Assemble a single chapter from its folios and write to `BOOK_DOC_DIR / rel_rst`."""
    chap_path = BOOK_DOC_DIR / rel_rst
    chap_txt = chap_path.read_text(encoding="utf-8")
    preamble, labels, chap_paras = extract_chapter_preamble_and_labels(chap_txt)
    label_norms = {nt for _, _, nt, _ in labels}

    folios = sorted((RES_DIR / sec_name).glob("[0-9][0-9][0-9][0-9].rst"))
    accumulated_blocks: List[str] = []
    all_footnotes: List[str] = []

    for f_idx, f_path in enumerate(folios):
        f_blocks, f_fns = split_folio_content(f_path.read_text(encoding="utf-8"))
        all_footnotes.extend(f_fns)

        # On the first folio of a chapter, skip the chapter title and subtitle headings
        if f_idx == 0:
            while f_blocks and is_heading_block(f_blocks[0]):
                h_norm = norm_alnum(f_blocks[0].splitlines()[0])
                if h_norm in label_norms:
                    break
                f_blocks.pop(0)

        for b_idx, block in enumerate(f_blocks):
            if b_idx == 0 and accumulated_blocks:
                if should_merge_page_boundary(
                    accumulated_blocks[-1], block, chap_paras, label_norms
                ):
                    accumulated_blocks[-1] = join_across_page_boundary(
                        accumulated_blocks[-1], block
                    )
                    continue
            accumulated_blocks.append(block)

    # Expand the 6 inline lead-in headings so all 135 section labels match
    accumulated_blocks = expand_inline_lead_in_headings(accumulated_blocks)

    # Attach canonical section labels (`.. _label:`) and standardize underline characters
    label_idx = 0
    final_blocks: List[str] = [preamble]

    for block in accumulated_blocks:
        lines = block.strip().splitlines()
        title_line = lines[0].strip() if is_heading_block(block) else block.strip()
        b_norm = norm_alnum(title_line)

        if label_idx < len(labels) and b_norm == labels[label_idx][2]:
            lbl, _orig_title, _nt, uline_char = labels[label_idx]
            label_idx += 1
            uline = uline_char * max(3, len(title_line))
            final_blocks.append(f".. _{lbl}:\n\n{title_line}\n{uline}")
        elif is_heading_block(block):
            # Keep heading block with its underline matching title length
            u_char = lines[1].strip()[0]
            uline = u_char * max(3, len(title_line))
            final_blocks.append(f"{title_line}\n{uline}")
        else:
            final_blocks.append(block)

    assert label_idx == len(labels), (
        f"Chapter {sec_name}: matched {label_idx}/{len(labels)} labels! "
        f"Next unmatched: {labels[label_idx] if label_idx < len(labels) else None}"
    )

    if all_footnotes:
        final_blocks.append("----")
        final_blocks.extend(all_footnotes)

    out_text = "\n\n".join(final_blocks) + "\n"
    chap_path.write_text(out_text, encoding="utf-8")
    return len(folios), len(labels), len(all_footnotes)


def main() -> None:
    total_folios = 0
    total_labels = 0
    total_fns = 0
    for sec_name, rel_rst in CHAPTERS:
        n_f, n_l, n_fn = assemble_chapter(sec_name, rel_rst)
        total_folios += n_f
        total_labels += n_l
        total_fns += n_fn
        print(
            f"Assembled {rel_rst:<30} from {n_f:2d} folios | {n_l:2d} section labels | {n_fn:2d} footnotes"
        )
    print(
        f"Total assembled: {total_folios} folios, {total_labels} section labels, {total_fns} footnotes."
    )


if __name__ == "__main__":
    main()
