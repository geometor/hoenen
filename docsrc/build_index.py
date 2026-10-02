import os

docsrc = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(docsrc)

index_dir = os.path.join(root, 'index')

all_lines = ["# INDEX ANALYTICUS", ""]

for p in range(289, 294):
    fn = os.path.join(index_dir, f'page-{p:03d}.txt')
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    lines = content.split('\n')
    for line in lines:
        line_s = line.strip()
        # Skip the title and PAG. headers from individual pages
        if line_s == "# INDEX ANALYTICUS" or line_s == "PAG.":
            continue
        all_lines.append(line)

out_text = "\n".join(all_lines).strip() + "\n"

out_path = os.path.join(root, "docs", "end_index.md")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(out_text)

print(f"Wrote {out_path} successfully ({len(out_text)} bytes).")
