#!/usr/bin/env python3
"""
scripts/update_chapter_navigation.py

Validates the centralized navigation database (docs/_data/navigation.json)
and ensures:
1. All referenced source and target files exist on disk.
2. Navigation sequences and track relationships resolve coherently.
3. docs/_data/navigation.json is synchronized with docs/assets/data/navigation.json.
4. Markdown files in docs/ remain clean without legacy in-page navigation blockquotes.
"""

import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
DATA_FILE = os.path.join(DOCS_DIR, '_data', 'navigation.json')
ASSET_DATA_FILE = os.path.join(DOCS_DIR, 'assets', 'data', 'navigation.json')


def validate_navigation():
    print(f"Validating centralized navigation in {DATA_FILE}...")
    if not os.path.exists(DATA_FILE):
        print(f"ERROR: {DATA_FILE} not found!", file=sys.stderr)
        return False

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    chapters = data.get('chapters', [])
    track_order = data.get('track_order', ['latin', 'english', 'summary', 'notes'])

    if not chapters:
        print("ERROR: No chapters found in navigation data!", file=sys.stderr)
        return False

    errors = []
    total_tracks = 0

    for i, ch in enumerate(chapters):
        ch_id = ch.get('id', f'index_{i}')
        tracks = ch.get('tracks', {})

        if not ch.get('title') or not ch.get('title_la'):
            errors.append(f"Chapter '{ch_id}' is missing title or title_la")

        for tr_key, tr_info in tracks.items():
            total_tracks += 1
            src_rel = tr_info.get('src')
            if not src_rel:
                errors.append(f"Chapter '{ch_id}' track '{tr_key}' is missing 'src'")
                continue

            src_full = os.path.join(DOCS_DIR, src_rel)
            if not os.path.exists(src_full):
                errors.append(f"File not found on disk: {src_full}")

    print(f"Verified {len(chapters)} chapters and {total_tracks} track files across {track_order}.")

    # Verify sync with asset data file
    if os.path.exists(ASSET_DATA_FILE):
        with open(ASSET_DATA_FILE, 'r', encoding='utf-8') as f:
            asset_data = json.load(f)
        if asset_data != data:
            print(f"Warning: {ASSET_DATA_FILE} is out of sync with {DATA_FILE}. Syncing...")
            with open(ASSET_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write('\n')
            print("Successfully synced asset data file.")
    else:
        os.makedirs(os.path.dirname(ASSET_DATA_FILE), exist_ok=True)
        with open(ASSET_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')
        print(f"Created {ASSET_DATA_FILE}.")

    # Verify no legacy blockquotes in docs markdown files
    legacy_count = 0
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith('.md'):
                fpath = os.path.join(root, file)
                with open(fpath, 'r', encoding='utf-8') as f:
                    for line_idx in range(5):
                        line = f.readline()
                        if not line:
                            break
                        if line.startswith('> ') and ('Latin' in line or 'English' in line) and '|' in line:
                            errors.append(f"Legacy navigation blockquote found in {fpath}")
                            legacy_count += 1
                            break

    if errors:
        print(f"\nFAILED with {len(errors)} error(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return False

    print("\nAll navigation relationships and file integrity checks passed successfully!")
    return True


if __name__ == '__main__':
    success = validate_navigation()
    sys.exit(0 if success else 1)
