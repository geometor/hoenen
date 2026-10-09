#!/usr/bin/env python3
"""
geometor.hoenen.split_scans
Processes raw scan PDFs into individual, contrast-enhanced grayscale page images
organized into chapter folders, preserving original scans and reporting status.
"""

import os
import shutil
import subprocess
import re
from pathlib import Path

BASE_DIR = Path("/home/phi/PROJECTS/geometor/hoenen")
PDFS_DIR = BASE_DIR / "archive" / "pdfs"
SCRATCH_DIR = Path("/home/phi/.gemini/antigravity/brain/9c7a701e-6b20-4b45-ab5e-f6b00f1a38fb/scratch/split_work")
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)

# Global inventory registry: page_num -> dict of info
INVENTORY = {}

def move_original_file(src: Path, dst: Path):
    """Move a file using git mv if tracked, else shutil.move."""
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    res = subprocess.run(['git', 'mv', str(src), str(dst)], capture_output=True, text=True)
    if res.returncode != 0:
        shutil.move(src, dst)

def find_gutter(img_path):
    """Detect vertical spine gutter in the center region of a 300 dpi spread image."""
    try:
        ident = subprocess.check_output(['identify', '-format', '%w %h', str(img_path)], text=True).strip()
        w, h = map(int, ident.split())
        
        out = subprocess.check_output([
            'convert', str(img_path),
            '-crop', '100%x50%+0+25%',
            '-colorspace', 'Gray',
            '-scale', '100%x1!',
            'txt:-'
        ], text=True)
        vals = []
        for line in out.splitlines()[1:]:
            m = re.match(r'(\d+),0:\s*\(\s*(\d+)', line)
            if m:
                vals.append((int(m.group(1)), int(m.group(2))))
        
        if w < h:
            min_x, max_x = int(w * 0.25), int(w * 0.42)
        elif w > 3600:
            min_x, max_x = int(w * 0.50), int(w * 0.60)
        else:
            min_x, max_x = int(w * 0.44), int(w * 0.56)
            
        gutters = [(v, x) for x, v in vals if min_x <= x <= max_x]
        if gutters:
            gutters.sort()
            val, gx = gutters[0]
            return gx, w
        return int(w * 0.33) if w < h else w // 2, w
    except Exception as e:
        print(f"Gutter detection error for {img_path}: {e}")
        return 1650, 3300

def render_pdf_page(pdf_path, page_num, out_prefix):
    """Render a single page from a PDF at 300 dpi to PNG."""
    parent = Path(out_prefix).parent
    stem = Path(out_prefix).name
    for old in parent.glob(f"{stem}*.png"):
        old.unlink()
        
    cmd = ['pdftoppm', '-png', '-r', '300', '-f', str(page_num), '-l', str(page_num), str(pdf_path), str(out_prefix)]
    subprocess.run(cmd, check=True)
    matches = sorted(parent.glob(f"{stem}*.png"))
    if matches:
        return matches[-1]
    raise RuntimeError(f"Could not render page {page_num} of {pdf_path}")

def process_spread(pdf_path, pdf_page, out_dir, left_page_num=None, right_page_num=None, is_partial_left=False, is_partial_right=False):
    """Extract spread, detect gutter, enhance contrast/grayscale, and save left/right pages."""
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp_prefix = SCRATCH_DIR / f"spread_{pdf_path.stem}_p{pdf_page}"
    spread_png = render_pdf_page(pdf_path, pdf_page, tmp_prefix)
    
    ident = subprocess.check_output(['identify', '-format', '%w %h', str(spread_png)], text=True).strip()
    w, h = map(int, ident.split())
    gx, _ = find_gutter(spread_png)
    
    # Process left page
    if left_page_num is not None:
        left_out = out_dir / f"page-{left_page_num:03d}.png"
        if is_partial_left:
            left_partial = out_dir / f"page-{left_page_num:03d}-partial.png"
            target_file = left_partial
        else:
            target_file = left_out
        
        if w > 3600:
            lx0 = max(0, gx - 1650)
            lw = gx - lx0
            subprocess.run([
                'convert', str(spread_png),
                '-crop', f'{lw}x{h}+{lx0}+0', '+repage',
                '-colorspace', 'Gray',
                '-contrast-stretch', '1%x1%',
                str(target_file)
            ], check=True)
        else:
            subprocess.run([
                'convert', str(spread_png),
                '-crop', f'{gx}x{h}+0+0', '+repage',
                '-colorspace', 'Gray',
                '-contrast-stretch', '1%x1%',
                str(target_file)
            ], check=True)
            
        if is_partial_left:
            if left_out.exists() or left_out.is_symlink():
                left_out.unlink()
            left_out.symlink_to(left_partial.name)
            
        status = "PARTIAL" if is_partial_left else "OK"
        print(f"  [+] {target_file.name} ({status})")
        INVENTORY[left_page_num] = {
            "section": out_dir.name,
            "source": f"{pdf_path.name} (p. {pdf_page}, left)",
            "status": status,
            "filename": left_out.name if not is_partial_left else left_partial.name
        }

    # Process right page
    if right_page_num is not None:
        right_out = out_dir / f"page-{right_page_num:03d}.png"
        if is_partial_right:
            right_partial = out_dir / f"page-{right_page_num:03d}-partial.png"
            target_file = right_partial
        else:
            target_file = right_out
            
        if w > 3600:
            rw = min(w - gx, 1650)
            subprocess.run([
                'convert', str(spread_png),
                '-crop', f'{rw}x{h}+{gx}+0', '+repage',
                '-colorspace', 'Gray',
                '-contrast-stretch', '1%x1%',
                str(target_file)
            ], check=True)
        else:
            rw = w - gx
            subprocess.run([
                'convert', str(spread_png),
                '-crop', f'{rw}x{h}+{gx}+0', '+repage',
                '-colorspace', 'Gray',
                '-contrast-stretch', '1%x1%',
                str(target_file)
            ], check=True)
            
        if is_partial_right:
            if right_out.exists() or right_out.is_symlink():
                right_out.unlink()
            right_out.symlink_to(right_partial.name)
            
        status = "PARTIAL" if is_partial_right else "OK"
        print(f"  [+] {target_file.name} ({status})")
        INVENTORY[right_page_num] = {
            "section": out_dir.name,
            "source": f"{pdf_path.name} (p. {pdf_page}, right)",
            "status": status,
            "filename": right_out.name if not is_partial_right else right_partial.name
        }
        
    spread_png.unlink()

def run_all():
    print("==================================================")
    print("HOENEN SCAN PROCESSOR & PARSER")
    print("==================================================")
    
    # 1. Preface
    preface_dir = BASE_DIR / "archive" / "preface"
    preface_dir.mkdir(exist_ok=True)
    if (BASE_DIR / "title.jpg").exists():
        move_original_file(BASE_DIR / "title.jpg", preface_dir / "title.jpg")
    for i, p in enumerate([5, 6, 7], 1):
        src = BASE_DIR / f"preface-{i}.png"
        dst = preface_dir / f"preface-{i}.png"
        if src.exists():
            move_original_file(src, dst)
        if dst.exists():
            out_img = preface_dir / f"page-{p:03d}.png"
            subprocess.run([
                'convert', str(dst),
                '-colorspace', 'Gray',
                '-contrast-stretch', '1%x1%',
                str(out_img)
            ], check=True)
            print(f"  [+] preface/page-{p:03d}.png (OK)")
            INVENTORY[p] = {
                "section": "preface",
                "source": f"preface-{i}.png",
                "status": "OK",
                "filename": f"page-{p:03d}.png"
            }
            
    # 2. Chapter 1
    ch1_dir = BASE_DIR / "archive" / "chapter-01"
    ch1_dir.mkdir(exist_ok=True)
    print("\n--- Processing Chapter 1 ---")
    for i in range(1, 18):
        src = BASE_DIR / f"caput-1-{i:02d}.png"
        dst = ch1_dir / f"caput-1-{i:02d}.png"
        if src.exists():
            move_original_file(src, dst)
        if dst.exists():
            page_num = 8 + i
            out_img = ch1_dir / f"page-{page_num:03d}.png"
            subprocess.run([
                'convert', str(dst),
                '-colorspace', 'Gray',
                '-contrast-stretch', '1%x1%',
                str(out_img)
            ], check=True)
            print(f"  [+] chapter-01/page-{page_num:03d}.png (OK)")
            INVENTORY[page_num] = {
                "section": "chapter-01",
                "source": f"caput-1-{i:02d}.png",
                "status": "OK",
                "filename": f"page-{page_num:03d}.png"
            }

    # 3. Chapter 2
    ch2_dir = BASE_DIR / "archive" / "chapter-02"
    ch2_dir.mkdir(exist_ok=True)
    c2_pdf = PDFS_DIR / "chapter-2.pdf"
    shutil.copy(c2_pdf, ch2_dir / "chapter-2.pdf")
    print("\n--- Processing Chapter 2 ---")
    process_spread(c2_pdf, 1, ch2_dir, left_page_num=None, right_page_num=27)
    for p in range(2, 20):
        lp = 28 + (p - 2) * 2
        rp = lp + 1
        process_spread(c2_pdf, p, ch2_dir, left_page_num=lp, right_page_num=rp)
    process_spread(c2_pdf, 20, ch2_dir, left_page_num=64, right_page_num=None)

    # 4. Chapter 3
    ch3_dir = BASE_DIR / "archive" / "chapter-03"
    ch3_dir.mkdir(exist_ok=True)
    c3_pdf = PDFS_DIR / "chapter-3.pdf"
    shutil.copy(c3_pdf, ch3_dir / "chapter-3.pdf")
    fills_pdf = PDFS_DIR / "page-fills.pdf"
    shutil.copy(fills_pdf, ch3_dir / "page-fills.pdf")
    print("\n--- Processing Chapter 3 ---")
    process_spread(c3_pdf, 1, ch3_dir, left_page_num=None, right_page_num=65)
    for p in range(2, 9):
        lp = 66 + (p - 2) * 2
        rp = lp + 1
        process_spread(c3_pdf, p, ch3_dir, left_page_num=lp, right_page_num=rp)
    # page 80-81 from page-fills p. 1
    process_spread(fills_pdf, 1, ch3_dir, left_page_num=80, right_page_num=81)
    for p in range(10, 16):
        lp = 82 + (p - 10) * 2
        rp = lp + 1
        process_spread(c3_pdf, p, ch3_dir, left_page_num=lp, right_page_num=rp)
    process_spread(c3_pdf, 16, ch3_dir, left_page_num=94, right_page_num=None)

    # 5. Chapter 4
    ch4_dir = BASE_DIR / "archive" / "chapter-04"
    ch4_dir.mkdir(exist_ok=True)
    c4_pdf = PDFS_DIR / "chapter-4.pdf"
    shutil.copy(c4_pdf, ch4_dir / "chapter-4.pdf")
    shutil.copy(fills_pdf, ch4_dir / "page-fills.pdf")
    print("\n--- Processing Chapter 4 ---")
    process_spread(c4_pdf, 1, ch4_dir, left_page_num=None, right_page_num=95)
    process_spread(c4_pdf, 2, ch4_dir, left_page_num=96, right_page_num=97)
    # spread 3 replaced by page-fills p. 3 (98-99) to avoid top margin cropping
    process_spread(fills_pdf, 3, ch4_dir, left_page_num=98, right_page_num=99)
    for p in range(4, 6):
        lp = 96 + (p - 2) * 2
        rp = lp + 1
        process_spread(c4_pdf, p, ch4_dir, left_page_num=lp, right_page_num=rp)
    # spread 6 replaced by page-fills p. 5 (104-105)
    process_spread(fills_pdf, 5, ch4_dir, left_page_num=104, right_page_num=105)
    for p in range(7, 11):
        lp = 106 + (p - 7) * 2
        rp = lp + 1
        process_spread(c4_pdf, p, ch4_dir, left_page_num=lp, right_page_num=rp)
    # spread 11 replaced by page-fills p. 6 (114-115)
    process_spread(fills_pdf, 6, ch4_dir, left_page_num=114, right_page_num=115)
    for p in range(12, 27):
        lp = 116 + (p - 12) * 2
        rp = lp + 1
        process_spread(c4_pdf, p, ch4_dir, left_page_num=lp, right_page_num=rp)
    # spread 27 replaced by page-fills p. 7 (146-147)
    process_spread(fills_pdf, 7, ch4_dir, left_page_num=146, right_page_num=147)
    for p in range(28, 32):
        lp = 148 + (p - 28) * 2
        rp = lp + 1
        process_spread(c4_pdf, p, ch4_dir, left_page_num=lp, right_page_num=rp)
    process_spread(c4_pdf, 32, ch4_dir, left_page_num=156, right_page_num=None)

    # 6. Chapter 5
    ch5_dir = BASE_DIR / "archive" / "chapter-05"
    ch5_dir.mkdir(exist_ok=True)
    c5_pdf = PDFS_DIR / "chapter-5.pdf"
    shutil.copy(c5_pdf, ch5_dir / "chapter-5.pdf")
    shutil.copy(fills_pdf, ch5_dir / "page-fills.pdf")
    print("\n--- Processing Chapter 5 ---")
    process_spread(c5_pdf, 1, ch5_dir, left_page_num=None, right_page_num=157)
    for p in range(2, 7):
        lp = 158 + (p - 2) * 2
        rp = lp + 1
        process_spread(c5_pdf, p, ch5_dir, left_page_num=lp, right_page_num=rp)
    # 168-169 from page-fills p. 8
    process_spread(fills_pdf, 8, ch5_dir, left_page_num=168, right_page_num=169)
    # 170-171 from page-fills p. 9
    process_spread(fills_pdf, 9, ch5_dir, left_page_num=170, right_page_num=171)
    # 172-173 from chapter-5 p. 9
    process_spread(c5_pdf, 9, ch5_dir, left_page_num=172, right_page_num=173)
    # 174-175 from page-fills p. 10
    process_spread(fills_pdf, 10, ch5_dir, left_page_num=174, right_page_num=175)
    fills2_pdf = PDFS_DIR / "page-fills-2.pdf"
    if fills2_pdf.exists():
        # 176-177 from page-fills-2 p. 1 (complete, fixing partial 176)
        process_spread(fills2_pdf, 1, ch5_dir, left_page_num=176, right_page_num=177, is_partial_left=False)
    else:
        # 176 (partial) and 177 from chapter-5 p. 11
        process_spread(c5_pdf, 11, ch5_dir, left_page_num=176, right_page_num=177, is_partial_left=True)
    # 178-179 from chapter-5 p. 12
    process_spread(c5_pdf, 12, ch5_dir, left_page_num=178, right_page_num=179)
    # 180-181 from chapter-5 p. 13
    process_spread(c5_pdf, 13, ch5_dir, left_page_num=180, right_page_num=181)
    # 182-183 from page-fills p. 11
    process_spread(fills_pdf, 11, ch5_dir, left_page_num=182, right_page_num=183)
    for p in range(15, 20):
        lp = 184 + (p - 15) * 2
        rp = lp + 1
        process_spread(c5_pdf, p, ch5_dir, left_page_num=lp, right_page_num=rp)
    process_spread(c5_pdf, 20, ch5_dir, left_page_num=194, right_page_num=None)

    # 7. Chapter 6
    ch6_dir = BASE_DIR / "archive" / "chapter-06"
    ch6_dir.mkdir(exist_ok=True)
    c6_pdf = PDFS_DIR / "chapter-6.pdf"
    shutil.copy(c6_pdf, ch6_dir / "chapter-6.pdf")
    shutil.copy(fills_pdf, ch6_dir / "page-fills.pdf")
    print("\n--- Processing Chapter 6 ---")
    process_spread(c6_pdf, 1, ch6_dir, left_page_num=None, right_page_num=195)
    for p in range(2, 7):
        lp = 196 + (p - 2) * 2
        rp = lp + 1
        process_spread(c6_pdf, p, ch6_dir, left_page_num=lp, right_page_num=rp)
    # 206-207 from page-fills p. 12
    process_spread(fills_pdf, 12, ch6_dir, left_page_num=206, right_page_num=207)
    # 208-209 from chapter-6 p. 8
    process_spread(c6_pdf, 8, ch6_dir, left_page_num=208, right_page_num=209)
    # 210-211 from page-fills p. 13
    process_spread(fills_pdf, 13, ch6_dir, left_page_num=210, right_page_num=211)
    if fills2_pdf.exists():
        # 212-213 from page-fills-2 p. 2 (complete, fixing partial 212)
        process_spread(fills2_pdf, 2, ch6_dir, left_page_num=212, right_page_num=213, is_partial_left=False)
    else:
        # 212 (partial) and 213 from chapter-6 p. 11
        process_spread(c6_pdf, 11, ch6_dir, left_page_num=212, right_page_num=213, is_partial_left=True)
    # 214-215 from chapter-6 p. 12
    process_spread(c6_pdf, 12, ch6_dir, left_page_num=214, right_page_num=215)
    if fills2_pdf.exists():
        # 216-217 from page-fills-2 p. 4 (complete, fixing partial 216)
        process_spread(fills2_pdf, 4, ch6_dir, left_page_num=216, right_page_num=217, is_partial_left=False)
    else:
        # 216 (partial) and 217 from chapter-6 p. 13
        process_spread(c6_pdf, 13, ch6_dir, left_page_num=216, right_page_num=217, is_partial_left=True)
    # 218-219 from chapter-6 p. 14
    process_spread(c6_pdf, 14, ch6_dir, left_page_num=218, right_page_num=219)
    # 220-221 from chapter-6 p. 15
    process_spread(c6_pdf, 15, ch6_dir, left_page_num=220, right_page_num=221)
    if fills2_pdf.exists():
        # 222 from page-fills-2 p. 12 (complete, fixing partial 222)
        process_spread(fills2_pdf, 12, ch6_dir, left_page_num=222, right_page_num=None, is_partial_left=False)
    else:
        # 222 (partial) from chapter-6 p. 16
        process_spread(c6_pdf, 16, ch6_dir, left_page_num=222, right_page_num=None, is_partial_left=True)

    # 8. Chapter 7
    ch7_dir = BASE_DIR / "archive" / "chapter-07"
    ch7_dir.mkdir(exist_ok=True)
    c7_pdf = PDFS_DIR / "chapter-7.pdf"
    shutil.copy(c7_pdf, ch7_dir / "chapter-7.pdf")
    app2_pdf = PDFS_DIR / "appendix-2.pdf"
    print("\n--- Processing Chapter 7 ---")
    process_spread(c7_pdf, 1, ch7_dir, left_page_num=None, right_page_num=223)
    process_spread(c7_pdf, 2, ch7_dir, left_page_num=224, right_page_num=225, is_partial_left=True)
    process_spread(c7_pdf, 3, ch7_dir, left_page_num=226, right_page_num=227, is_partial_left=True)
    process_spread(c7_pdf, 4, ch7_dir, left_page_num=228, right_page_num=229)
    process_spread(c7_pdf, 5, ch7_dir, left_page_num=230, right_page_num=231, is_partial_left=True)
    process_spread(c7_pdf, 6, ch7_dir, left_page_num=232, right_page_num=233, is_partial_left=True)
    process_spread(c7_pdf, 7, ch7_dir, left_page_num=234, right_page_num=235, is_partial_left=True)
    process_spread(c7_pdf, 8, ch7_dir, left_page_num=236, right_page_num=237)
    process_spread(c7_pdf, 9, ch7_dir, left_page_num=238, right_page_num=239, is_partial_left=True)
    process_spread(c7_pdf, 10, ch7_dir, left_page_num=240, right_page_num=241, is_partial_left=True)
    process_spread(c7_pdf, 11, ch7_dir, left_page_num=242, right_page_num=243, is_partial_left=True)
    process_spread(c7_pdf, 12, ch7_dir, left_page_num=244, right_page_num=245, is_partial_left=True)
    process_spread(c7_pdf, 13, ch7_dir, left_page_num=246, right_page_num=247, is_partial_left=True)
    # Page 248 is complete on spread 2 of appendix-2.pdf
    process_spread(app2_pdf, 2, ch7_dir, left_page_num=248, right_page_num=None)

    # 9. Appendix
    app_dir = BASE_DIR / "archive" / "appendix"
    app_dir.mkdir(exist_ok=True)
    app_end_pdf = PDFS_DIR / "appendix-end-and-index.pdf"
    shutil.copy(app2_pdf, app_dir / "appendix-2.pdf")
    shutil.copy(app_end_pdf, app_dir / "appendix-end-and-index.pdf")
    print("\n--- Processing Appendix ---")
    process_spread(app2_pdf, 2, app_dir, left_page_num=None, right_page_num=249)
    for p in range(3, 8):
        lp = 250 + (p - 3) * 2
        rp = lp + 1
        process_spread(app2_pdf, p, app_dir, left_page_num=lp, right_page_num=rp)
    process_spread(app2_pdf, 9, app_dir, left_page_num=260, right_page_num=261)
    process_spread(app2_pdf, 13, app_dir, left_page_num=262, right_page_num=263)
    process_spread(app2_pdf, 14, app_dir, left_page_num=264, right_page_num=265)
    process_spread(app2_pdf, 15, app_dir, left_page_num=266, right_page_num=267)
    # 268 is partial in spread 16
    process_spread(app2_pdf, 16, app_dir, left_page_num=268, right_page_num=269, is_partial_left=True)
    process_spread(app2_pdf, 17, app_dir, left_page_num=270, right_page_num=271)
    process_spread(app2_pdf, 19, app_dir, left_page_num=272, right_page_num=273)
    process_spread(app2_pdf, 20, app_dir, left_page_num=274, right_page_num=275)
    process_spread(app2_pdf, 22, app_dir, left_page_num=276, right_page_num=277)
    process_spread(app2_pdf, 23, app_dir, left_page_num=278, right_page_num=279)
    process_spread(app2_pdf, 26, app_dir, left_page_num=280, right_page_num=281)
    # 282-287 from appendix-end-and-index.pdf
    process_spread(app_end_pdf, 1, app_dir, left_page_num=282, right_page_num=283)
    process_spread(app_end_pdf, 2, app_dir, left_page_num=284, right_page_num=285)
    process_spread(app_end_pdf, 3, app_dir, left_page_num=286, right_page_num=287)
    process_spread(app_end_pdf, 4, app_dir, left_page_num=288, right_page_num=None)

    # 10. Index
    idx_dir = BASE_DIR / "archive" / "index"
    idx_dir.mkdir(exist_ok=True)
    idx_pdf = PDFS_DIR / "index.pdf"
    shutil.copy(idx_pdf, idx_dir / "index.pdf")
    print("\n--- Processing Index ---")
    process_spread(app_end_pdf, 4, idx_dir, left_page_num=None, right_page_num=289)
    process_spread(app_end_pdf, 5, idx_dir, left_page_num=290, right_page_num=291)
    process_spread(app_end_pdf, 8, idx_dir, left_page_num=292, right_page_num=293)

    print("\n==================================================")
    print("ALL SECTIONS SUCCESSFULLY PROCESSED AND SPLIT!")
    print("==================================================")
    
    # Write inventory report to docs/scan-inventory.md
    write_inventory_report()

def write_inventory_report():
    docs_dir = BASE_DIR / "docs"
    docs_dir.mkdir(exist_ok=True)
    inv_file = docs_dir / "scan-inventory.md"
    
    partials = [p for p, info in sorted(INVENTORY.items()) if info['status'] == 'PARTIAL']
    complete = [p for p, info in sorted(INVENTORY.items()) if info['status'] == 'OK']
    
    lines = [
        "# De Noetica Geometriae: Scan Inventory & Rescan Manifest",
        "",
        f"- **Total Book Pages Processed:** {len(INVENTORY)}",
        f"- **Complete / High-Quality Pages:** {len(complete)}",
        f"- **Partial Pages Needing Rescan:** {len(partials)}",
        "",
        "## Urgent Rescan Needed (15 Pages)",
        "",
        "The following 15 pages were partially cut off on the left side due to vertical scanner alignment (scanned in portrait orientation instead of landscape):",
        "",
        "| Page | Section | Current File | Problem Description | Priority |",
        "|---|---|---|---|---|",
    ]
    
    for p in partials:
        info = INVENTORY[p]
        lines.append(f"| **Page {p}** | `{info['section']}` | `{info['filename']}` | Left margin / left column text cut off vertically | Rescan Required |")
        
    lines.extend([
        "",
        "---",
        "",
        "## Full Book Page Directory",
        "",
        "| Page | Section | Source Reference | Status | Extracted File |",
        "|---|---|---|---|---|",
    ])
    
    for p, info in sorted(INVENTORY.items()):
        status_badge = "🔴 PARTIAL" if info['status'] == 'PARTIAL' else "🟢 OK"
        lines.append(f"| {p:03d} | `{info['section']}` | {info['source']} | {status_badge} | `{info['filename']}` |")
        
    inv_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote inventory report to {inv_file}")

if __name__ == "__main__":
    run_all()
