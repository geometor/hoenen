import os
import re

docsrc = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(docsrc)

chapter7_dir = os.path.join(root, 'archive', 'chapter-07')

hyphen_boundaries = {226, 231, 234, 236, 237, 240, 242, 243}
same_para_boundaries = {223, 224, 225, 227, 228, 229, 230, 232, 233, 235, 239, 241, 244, 245, 246, 247}
new_para_boundaries = {238}

pages_paras = {}
fn_definitions = {}

for p in range(223, 249):
    fn = os.path.join(chapter7_dir, f'page-{p:03d}.txt')
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    raw_paras = [x.strip() for x in content.split('\n\n') if x.strip()]
    paras = []
    for para in raw_paras:
        if para.startswith('[^') and ']:' in para:
            fn_id = int(para[2:para.index(']:')])
            fn_definitions[fn_id] = para
        else:
            paras.append(para)
    pages_paras[p] = paras

# Strip title block from page 223
p223 = pages_paras[223]
idx = 0
while idx < len(p223) and not p223[idx].startswith('### § 1.'):
    idx += 1
pages_paras[223] = p223[idx:]

all_paras = []
for p in range(223, 249):
    paras = pages_paras[p]
    if p > 223:
        prev_p = p - 1
        if prev_p in hyphen_boundaries:
            prev_last = all_paras.pop()
            assert prev_last.endswith('-'), f'Expected hyphen at end of P{prev_p}: {prev_last}'
            joined = prev_last[:-1] + paras[0]
            all_paras.append(joined)
            paras = paras[1:]
        elif prev_p in same_para_boundaries:
            prev_last = all_paras.pop()
            joined = prev_last + ' ' + paras[0]
            all_paras.append(joined)
            paras = paras[1:]
        elif prev_p in new_para_boundaries:
            pass
    all_paras.extend(paras)

heading_map = {
    '### § 1. De constructione figurarum geometricarum.': '## § 1. De constructione figurarum geometricarum.',
    '### § 2. De duplici intelligibilitate materiae intelligibilis.': '## § 2. De duplici intelligibilitate materiae intelligibilis.',
    '#### 1. De intelligibilitate passivitatis materiae intelligibilis.': '### 1. De intelligibilitate passivitatis materiae intelligibilis.',
    '#### 2. De intelligibilitate activitatis nostrae.': '### 2. De intelligibilitate activitatis nostrae.',
    '### § 3. De origine noeticae generalis.': '## § 3. De origine noeticae generalis.',
    '#### 1. Conspectus generalis.': '### 1. Conspectus generalis.',
    '2. *De casibus mathematicis.*': '### 2. De casibus mathematicis.',
    '3. *De casibus physicis.*': '### 3. De casibus physicis.',
}

formatted_blocks = []
for para in all_paras:
    if para in heading_map:
        formatted_blocks.append(heading_map[para])
    else:
        para_clean = re.sub(r' +', ' ', para).strip()
        formatted_blocks.append(para_clean)

doc_header = [
    "# CAPUT VII",
    "DE EXTENSIONE UT EST MATERIA INTELLIGIBILIS"
]

footnotes = [fn_definitions[k] for k in sorted(fn_definitions.keys())]

full_md_blocks = doc_header + formatted_blocks
full_md = "\n\n".join(full_md_blocks) + "\n\n---\n\n" + "\n\n".join(footnotes) + "\n"

out_path = os.path.join(root, "docs", "caput-7", "caput-7.md")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(full_md)

print(f"Wrote {out_path} successfully ({len(full_md)} bytes, {len(full_md_blocks)} blocks).")
