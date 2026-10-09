import os
import re

docsrc = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(docsrc)

appendix_dir = os.path.join(root, 'archive', 'appendix')

hyphen_boundaries = {252, 257, 258, 265, 267, 273, 274, 281, 284}
same_para_boundaries = {250, 253, 254, 255, 256, 262, 263, 264, 266, 268, 270, 271, 272, 275, 277, 278, 282}
new_para_boundaries = {249, 251, 259, 260, 261, 269, 276, 279, 280, 283, 285, 286, 287}

pages_paras = {}
fn_definitions = {}

for p in range(249, 289):
    fn = os.path.join(appendix_dir, f'page-{p:03d}.txt')
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    raw_paras = [x.strip() for x in content.split('\n\n') if x.strip()]
    paras = []
    for para in raw_paras:
        if para.startswith('[^') and ']:' in para:
            sub_fns = re.split(r'\n(?=\[\^\d+\]:)', para)
            for fn_block in sub_fns:
                fn_block = fn_block.strip()
                if fn_block.startswith('[^') and ']:' in fn_block:
                    fn_id = int(fn_block[2:fn_block.index(']:')])
                    fn_definitions[fn_id] = fn_block
        else:
            paras.append(para)
    pages_paras[p] = paras

# Strip title block from page 249
p249 = pages_paras[249]
idx = 0
while idx < len(p249) and not p249[idx].startswith('### § 1.'):
    idx += 1
pages_paras[249] = p249[idx:]

all_paras = []
for p in range(249, 289):
    paras = pages_paras[p]
    if p > 249:
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
    '### § 1. « MOVETUR ERGO EST ».': '## § 1. « Movetur ergo est »',
    '### § 2. « HOC MOVETUR ERGO LOCUS EST ».': '## § 2. « Hoc movetur ergo locus est »',
    '### § 3. « HOC MOVETUR, ERGO ALIUD, MOVENS, EXISTIT ».': '## § 3. « Hoc movetur, ergo aliud, movens, existit »',
    '### § 4. DE FINALITATE IN MOTU.': '## § 4. De finalitate in motu',
    '*Recapitulatio.*': '### Recapitulatio',
    '### § 5. QUAEDAM ALIAE RELATIONES EXISTENTIALES.': '## § 5. Quaedam aliae relationes existentiales',
    '### § 6. ARISTOTELES DE ACTU EXISTENTIALI.': '## § 6. Aristoteles de actu existentiali',
    '### § 7. DE CONCEPTU IPSIUS ESSE.': '## § 7. De conceptu ipsius esse',
}

formatted_blocks = []
for para in all_paras:
    if para in heading_map:
        formatted_blocks.append(heading_map[para])
    else:
        para_clean = re.sub(r' +', ' ', para).strip()
        formatted_blocks.append(para_clean)

doc_header = [
    "# APPENDIX",
    "## De connexionibus necessariis inter actus existentiales"
]

footnotes = [fn_definitions[k] for k in sorted(fn_definitions.keys())]

full_md_blocks = doc_header + formatted_blocks
full_md = "\n\n".join(full_md_blocks) + "\n\n---\n\n" + "\n\n".join(footnotes) + "\n"

out_path = os.path.join(root, "docs", "appendix", "appendix.md")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(full_md)

print(f"Wrote {out_path} successfully ({len(full_md)} bytes, {len(full_md_blocks)} blocks, {len(footnotes)} footnotes).")
