import os
import re
import collections

docsrc = os.path.dirname(os.path.abspath(__file__))

# Automatically group files by their prefix (e.g. preface-1.txt -> preface, caput-1-01.txt -> caput-1)
groups = collections.defaultdict(list)
for f in os.listdir(docsrc):
    if f.endswith('.txt'):
        # match prefix before the last dash and number
        m = re.match(r'^(.*?)-\d+\.txt$', f)
        if m:
            groups[m.group(1)].append(f)

for k in groups:
    groups[k].sort()

header_pattern = re.compile(r'^\s*\d+\s+[A-Z\s\.\-]+\s*$|^\s*[A-Z\s\.\-]+\s+\d+\s*$')
footer_pattern = re.compile(r'^\s*\d+\s*$|^\s*\d+\s*—\s*P\.\s+HOENEN.*$')

def process_body_text(text):
    lines = text.split('\n')
    paragraphs = []
    current_para = []
    
    def is_sentence_end(s):
        s = s.strip()
        if not s:
            return False
        return s[-1] in '.?!:»>"'

    def is_new_paragraph(line, prev_line):
        l = line.strip()
        p = prev_line.strip()
        if not l:
            return False
        if not p:
            return True
        if l.startswith('§ ') or l == 'CAPUT I' or l == 'PRAEFATIO':
            return True
        if is_sentence_end(p):
            m = re.match(r'^([«»"\'\(\[\s]*)([A-Z0-9])', l)
            if m:
                return True
        return False

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            if current_para:
                paragraphs.append(current_para)
                current_para = []
            continue
            
        prev = lines[i-1] if i > 0 else ""
        
        if is_new_paragraph(line, prev):
            if current_para:
                paragraphs.append(current_para)
                current_para = []
        
        current_para.append(stripped)
        
    if current_para:
        paragraphs.append(current_para)
        
    formatted_paragraphs = []
    for p_lines in paragraphs:
        joined = "\n".join(p_lines)
        dehyphenated = re.sub(r'-\n\s*', '', joined)
        single_line = dehyphenated.replace('\n', ' ')
        
        single_line = re.sub(r'\s+', ' ', single_line).strip()
        
        if single_line.startswith('§ '):
            single_line = f"## {single_line}"
        elif single_line.startswith('CAPUT'):
            single_line = f"# {single_line}"
        elif single_line == 'PRAEFATIO':
            single_line = f"# {single_line}"
            
        formatted_paragraphs.append(single_line)
        
    final_body = "\n\n".join(formatted_paragraphs)
    
    # fix standard missed citations like " 1,"
    final_body = re.sub(r'([a-zA-Z]) (\d+)([.,;:?)])', r'\1 [^\2]\3', final_body)
    final_body = re.sub(r'([a-zA-Z]) (\d+)$', r'\1 [^\2]', final_body, flags=re.MULTILINE)
    # fix the newly spotted missed ones with >> or »
    final_body = re.sub(r'([»"\'\]\)]) (\d+)([.,;:?) ]|$)', r'\1 [^\2]\3', final_body)

    return final_body

def process_footnotes(text):
    lines = text.split('\n')
    footnotes = []
    current_fn = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
            
        match = re.match(r'^(\d+)\s+(.*)', stripped)
        if match:
            if current_fn:
                footnotes.append(current_fn)
            fn_num = match.group(1)
            fn_text = match.group(2)
            current_fn = [f"[^{fn_num}]: {fn_text}"]
        else:
            if current_fn:
                current_fn.append(stripped)
            else:
                current_fn = [stripped]
                
    if current_fn:
        footnotes.append(current_fn)
        
    formatted_footnotes = []
    for fn_lines in footnotes:
        joined = "\n".join(fn_lines)
        dehyphenated = re.sub(r'-\n\s*', '', joined)
        single_line = dehyphenated.replace('\n', ' ')
        single_line = re.sub(r'\s+', ' ', single_line).strip()
        formatted_footnotes.append(single_line)
        
    return "\n\n".join(formatted_footnotes)


for out_name, files in groups.items():
    if not files:
        continue
        
    print(f"Processing group: {out_name} (Found {len(files)} files)")
    body_parts = []
    footnotes = []
    
    for file in files:
        with open(os.path.join(docsrc, file), 'r') as f:
            lines = f.readlines()
        
        start_idx = 0
        for i in range(min(5, len(lines))):
            if header_pattern.match(lines[i]):
                start_idx = i + 1
                while start_idx < len(lines) and lines[start_idx].strip() == '':
                    start_idx += 1
                break
                
        end_idx = len(lines)
        for i in range(1, min(5, len(lines))):
            idx = len(lines) - i
            if footer_pattern.match(lines[idx]):
                end_idx = idx
                while end_idx > start_idx and lines[end_idx-1].strip() == '':
                    end_idx -= 1
                break
                
        page_lines = lines[start_idx:end_idx]
        
        # Scan backwards to find the uppermost footnote in the bottom region
        fn_start = -1
        # search max bottom 20 lines
        max_search = max(-1, len(page_lines) - 20)
        for i in range(len(page_lines)-1, max_search, -1):
            if re.match(r'^\d+\s+', page_lines[i]) and len(page_lines[i]) > 10:
                fn_start = i
                # do not break! continue up to find the earliest footnote Start
            if "Geraden und bezeichnen sie mit" in page_lines[i]:
                fn_start = i - 1
                
        if fn_start != -1:
            body_parts.extend(page_lines[:fn_start])
            footnotes.extend(page_lines[fn_start:])
        else:
            body_parts.extend(page_lines)


    combined_body = "".join(body_parts)
    if "Geraden und bezeichnen sie mit a, b, c, ... ; die Dinge des" in combined_body:
        lines = combined_body.split('\n')
        new_body = []
        for line in lines:
            if "Geraden und bezeichnen sie mit" in line or "Systems nennen wir Ebenen" in line or "cit. ed. 7 (1930) pag. 2." in line:
                footnotes.append(line + '\n')
            else:
                new_body.append(line)
        combined_body = "\n".join(new_body)

    formatted_body = process_body_text(combined_body)
    
    final_text = formatted_body
    if footnotes:
        formatted_footnotes = process_footnotes("".join(footnotes))
        final_text += "\n\n---\n\n" + formatted_footnotes

    out_path = os.path.join(docsrc, f'{out_name}.md')
    with open(out_path, 'w') as f:
        f.write(final_text)

    print(f"Wrote {out_name}.md")
