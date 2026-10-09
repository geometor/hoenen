> [← Table of Contents](../index.md)

---

# PDF Parsing & Scan Processing Guide

This document details the exact methodology, tooling, and reproduction instructions used to convert raw PDF scans of Peter Hoenen's *De Noetica Geometriae* (1954) into standardized, high-contrast, single-page images organized by chapter.

---

## 1. Scanner & Source Specifications

### Standard 2-Page Spread
- **Physical Size:** $11 \times 8.5\text{ inches}$ (Standard US Letter in Landscape orientation).
- **Resolution:** 300 DPI $\rightarrow 3300 \times 2550\text{ pixels}$.
- **Page Layout:** Two book pages per scan:
  - **Left page:** Even printed page number (verso).
  - **Right page:** Odd printed page number (recto).
  - **Spine gutter:** Vertical shadow crease near the horizontal center ($x \approx 1600\text{--}1650\text{ px}$).

### Observed Scan Anomalies
1. **Portrait Orientation Misscans:**
   - **Dimensions:** $2550 \times 3300\text{ pixels}$ ($8.5 \times 11\text{ inches}$ portrait).
   - **Effect:** The scanner bed width was restricted to 8.5 inches instead of 11 inches. The right-hand page was fully captured, but the left-hand page was vertically truncated (~50% width lost).
   - **Occurrences:** Chapter 5 (p. 176), Chapter 6 (pp. 212, 216, 222), Chapter 7 (pp. 224, 226, 230, 232, 234, 238, 240, 242, 244, 246), Appendix (p. 268).
2. **Legal Paper Size Scans:**
   - **Dimensions:** $4200 \times 2550\text{ pixels}$ ($14 \times 8.5\text{ inches}$ landscape).
   - **Effect:** Extra white margins on the sides. Spine gutter shifted to $x \approx 2250\text{ px}$.
   - **Occurrences:** `appendix-end-and-index.pdf` (Spread 4).

---

## 2. Processing Pipeline Architecture

The extraction and splitting process is fully automated via [`src/geometor/hoenen/split_scans.py`](../../src/geometor/hoenen/split_scans.py).

```
   Source PDF (pdfs/)
          │
          ▼  (pdftoppm -png -r 300)
   Raw 300 DPI Spread Image
          │
          ▼  (convert -crop 100%x50%+0+25% -scale 100%x1! txt:-)
   Horizontal Intensity Profile & Spine Gutter Detection
          │
     ┌────┴───────────────────────────┐
     ▼                                ▼
Left Page Crop                   Right Page Crop
(0 to Gutter)                    (Gutter to Width)
     │                                │
     ▼  (-colorspace Gray -contrast-stretch 1%x1%)
Optimized Single Page PNG       Optimized Single Page PNG
(chapter-XX/page-NNN.png)       (chapter-XX/page-NNN.png)
```

### Core Algorithms & Tooling

#### A. High-Resolution Rendering
Rendered using Poppler's `pdftoppm` at native 300 DPI:
```bash
pdftoppm -png -r 300 -f <page_num> -l <page_num> input.pdf output_prefix
```

#### B. Dynamic Spine Gutter Detection
Rather than splitting at a fixed 50% coordinate (which risks clipping text when scans are slightly off-center), the script inspects the vertical center 50% strip of the spread, compresses it vertically to a 1-pixel high intensity map, and identifies the spine shadow minimum:
- **Portrait Spreads ($w < h$):** Search window is $x \in [0.25w, 0.42w]$.
- **Normal Landscape ($w \approx 3300$):** Search window is $x \in [0.44w, 0.56w]$.
- **Legal Landscape ($w \approx 4200$):** Search window is $x \in [0.50w, 0.60w]$.

#### C. Grayscale & Contrast Enhancement
To maximize readability and prepare the pages for optimal OCR:
```bash
convert <cropped_page.png> -colorspace Gray -contrast-stretch 1%x1% <output.png>
```
This maps the darkest 1% of pixels to pure black and the brightest 1% to pure white, eliminating yellowing, paper grain, and scan shadow without degrading font weight.

#### D. Partial Page Handling & Symlinks
For pages with truncated content (the 15 portrait pages):
1. The image is saved as `page-NNN-partial.png` so it is immediately identifiable.
2. A relative symlink `page-NNN.png -> page-NNN-partial.png` is generated so numerical sequential access remains intact for automated pipelines.

---

## 3. Directory Organization

Each section of the work is self-contained:
```
hoenen/
├── preface/
│   ├── title.jpg
│   ├── preface-1.png .. preface-3.png    (Original scans)
│   ├── page-005.png .. page-007.png     (Standardized pages)
│   └── page-005.txt .. page-007.txt     (Transcribed text)
├── chapter-01/
│   ├── caput-1-01.png .. caput-1-17.png  (Original scans)
│   ├── page-009.png .. page-025.png     (Standardized pages)
│   └── page-009.txt .. page-025.txt     (Transcribed text)
├── chapter-02/
│   ├── chapter-2.pdf                    (Source PDF)
│   ├── page-027.png .. page-064.png     (Standardized pages)
│   └── page-027.txt .. page-064.txt     (Transcribed text)
├── chapter-03/
│   ├── chapter-3.pdf, page-fills.pdf    (Source PDFs)
│   └── page-065.png .. page-094.png
├── chapter-04/
│   ├── chapter-4.pdf, page-fills.pdf
│   └── page-095.png .. page-156.png
├── chapter-05/
│   ├── chapter-5.pdf, page-fills.pdf
│   ├── page-176-partial.png, page-176.png (symlink)
│   └── page-157.png .. page-194.png
├── chapter-06/
│   ├── chapter-6.pdf, page-fills.pdf
│   ├── page-212-partial.png, page-216-partial.png, page-222-partial.png
│   └── page-195.png .. page-222.png
├── chapter-07/
│   ├── chapter-7.pdf, appendix-2.pdf
│   ├── page-224-partial.png, ... (10 partial pages)
│   └── page-223.png .. page-248.png
├── appendix/
│   ├── appendix-2.pdf, appendix-end-and-index.pdf
│   ├── page-268-partial.png
│   └── page-249.png .. page-288.png
└── index/
    ├── index.pdf, appendix-end-and-index.pdf
    └── page-289.png .. page-293.png
```

---

## 4. How to Process Rescans / Fill Pages

When replacement scans for the 15 partial pages are acquired:

### Scanning Guidelines for Replacements
1. **Orientation:** Set scanner to **Landscape** (11 in wide $\times$ 8.5 in tall) or ensure the scan width covers both pages (or at least full 5.5 in width for single page).
2. **Resolution:** 300 DPI.
3. **Format:** Single-page or two-page spread PDF/PNG.

### Ingestion Procedure
If rescanned as a new fill PDF (e.g. `pdfs/rescans.pdf`):
1. Place `rescans.pdf` in `pdfs/`.
2. Extract the specific replacement page:
   ```bash
   pdftoppm -png -r 300 -f <page> -l <page> pdfs/rescans.pdf /tmp/rescan
   ```
3. If it is a two-page spread, split using:
   ```bash
   python3 -c "
   from geometor.hoenen.split_scans import process_spread
   from pathlib import Path
   process_spread(Path('pdfs/rescans.pdf'), <spread_num>, Path('<target_chapter_dir>'), left_page_num=<LP>, right_page_num=<RP>)
   "
   ```
4. If it is an individual single page:
   ```bash
   convert /tmp/rescan-*.png -colorspace Gray -contrast-stretch 1%x1% <target_chapter_dir>/page-<NNN>.png
   ```
5. Remove the obsolete `-partial.png` and update `docs/scan-inventory.md`.

---

> [← Table of Contents](../index.md)
