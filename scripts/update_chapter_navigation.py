#!/usr/bin/env python3
"""
scripts/update_chapter_navigation.py

Updates and verifies the in-page menu bars across all chapter and document
Markdown files in docs/ to:
1. Ensure the top menu bar contains only core edition/language links
   (e.g., Latin | English | Summary | Notes), without track navigation arrows
   ([← Prev], [Next →]), which are provided by the site header.
2. Remove any bottom menu blocks and trailing separators.
3. Clean out redundant [Conspectus Totius Operis] or [Table of Contents] links.
"""

import os
import re

# Canonical reading sequences for each track
TRACKS = {
    'latin': [
        ('Praefatio', 'docs/preface/preface.md'),
        ('Caput I', 'docs/caput-1/caput-1.md'),
        ('Caput II', 'docs/caput-2/caput-2.md'),
        ('Caput III', 'docs/caput-3/caput-3.md'),
        ('Caput IV', 'docs/caput-4/caput-4.md'),
        ('Caput V', 'docs/caput-5/caput-5.md'),
        ('Caput VI', 'docs/caput-6/caput-6.md'),
        ('Caput VII', 'docs/caput-7/caput-7.md'),
        ('Appendix', 'docs/appendix/appendix.md'),
        ('Index Analyticus', 'docs/end-index/end_index.md')
    ],
    'english': [
        ('Preface', 'docs/preface/preface-en.md'),
        ('Chapter I', 'docs/caput-1/caput-1-en.md'),
        ('Chapter II', 'docs/caput-2/caput-2-en.md'),
        ('Chapter III', 'docs/caput-3/caput-3-en.md'),
        ('Chapter IV', 'docs/caput-4/caput-4-en.md'),
        ('Chapter V', 'docs/caput-5/caput-5-en.md'),
        ('Chapter VI', 'docs/caput-6/caput-6-en.md'),
        ('Chapter VII', 'docs/caput-7/caput-7-en.md'),
        ('Appendix', 'docs/appendix/appendix-en.md'),
        ('Analytical Index', 'docs/end-index/end_index-en.md')
    ],
    'summary': [
        ('Caput I Summary', 'docs/caput-1/caput-1-summary.md'),
        ('Caput II Summary', 'docs/caput-2/caput-2-summary.md'),
        ('Caput III Summary', 'docs/caput-3/caput-3-summary.md'),
        ('Caput IV Summary', 'docs/caput-4/caput-4-summary.md'),
        ('Caput V Summary', 'docs/caput-5/caput-5-summary.md'),
        ('Caput VI Summary', 'docs/caput-6/caput-6-summary.md'),
        ('Caput VII Summary', 'docs/caput-7/caput-7-summary.md'),
        ('Appendix Summary', 'docs/appendix/appendix-summary.md')
    ],
    'notes': [
        ('Praefatio Notes', 'docs/preface/translation-benchmark-preface.md'),
        ('Caput I Notes', 'docs/caput-1/translation-benchmark-caput-1.md'),
        ('Caput II Notes', 'docs/caput-2/translation-notes-caput-2.md'),
        ('Caput III Notes', 'docs/caput-3/translation-notes-caput-3.md'),
        ('Caput IV Notes', 'docs/caput-4/translation-notes-caput-4.md'),
        ('Caput V Notes', 'docs/caput-5/translation-notes-caput-5.md'),
        ('Caput VI Notes', 'docs/caput-6/translation-notes-caput-6.md'),
        ('Caput VII Notes', 'docs/caput-7/translation-notes-caput-7.md'),
        ('Appendix Notes', 'docs/appendix/translation-notes-appendix.md')
    ],
    'model-3.1': [
        ('Praefatio (3.1)', 'docs/preface/preface-en-3.1.md'),
        ('Caput I (3.1)', 'docs/caput-1/caput-1-en-3.1.md')
    ]
}

def extract_core_links(line):
    """Extracts the central edition/language links from a menu bar blockquote."""
    text = line[2:].strip()
    parts = [p.strip() for p in text.split('|')]
    core_parts = []
    for p in parts:
        # Filter out existing prev/next track navigation
        if re.search(r'\[\s*←.*?\]\(', p) or re.search(r'\[.*?→\s*\]\(', p):
            continue
        # Filter out Conspectus / Table of Contents links
        if 'Conspectus Totius Operis' in p or 'Table of Contents' in p:
            continue
        core_parts.append(p)
    return ' | '.join(core_parts)

def update_all():
    file_meta = {}
    for tname, items in TRACKS.items():
        for i, (label, path) in enumerate(items):
            prev_item = items[i-1] if i > 0 else None
            next_item = items[i+1] if i < len(items) - 1 else None
            file_meta[path] = {
                'track': tname,
                'label': label,
                'prev': prev_item,
                'next': next_item
            }

    updated_files = 0
    for filepath, meta in file_meta.items():
        if not os.path.exists(filepath):
            print(f"Warning: file not found: {filepath}")
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if not lines:
            continue

        file_dir = os.path.dirname(filepath)
        prev_link = ""
        if meta['prev']:
            rel_prev = os.path.relpath(meta['prev'][1], file_dir)
            prev_link = f"[← {meta['prev'][0]}]({rel_prev})"

        next_link = ""
        if meta['next']:
            rel_next = os.path.relpath(meta['next'][1], file_dir)
            next_link = f"[{meta['next'][0]} →]({rel_next})"

        # Look for the top menu bar (typically line 0)
        top_bar_idx = None
        for i, l in enumerate(lines[:5]):
            if l.startswith('> ') and ('Latin' in l or 'English' in l) and ('|' in l):
                top_bar_idx = i
                break

        if top_bar_idx is not None:
            core = extract_core_links(lines[top_bar_idx])
            parts = []
            if prev_link:
                parts.append(prev_link)
            parts.append(core)
            if next_link:
                parts.append(next_link)
            lines[top_bar_idx] = '> ' + ' | '.join(parts) + '\n'

        # Check for bottom menu bar (a '> ' line after top_bar_idx)
        # and strip it along with any preceding '---'
        while lines and not lines[-1].strip():
            lines.pop()

        # If the last non-empty line is a menu bar, remove it
        if lines and lines[-1].startswith('> ') and ('Latin' in lines[-1] or 'English' in lines[-1]):
            lines.pop()
            while lines and not lines[-1].strip():
                lines.pop()
            # If the preceding line is '---', remove it as well
            if lines and lines[-1].strip() == '---':
                lines.pop()
            while lines and not lines[-1].strip():
                lines.pop()

        lines.append('\n')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        updated_files += 1
        print(f"Updated navigation in {filepath}")

    print(f"\nSuccessfully updated navigation in {updated_files} files.")

if __name__ == '__main__':
    update_all()
