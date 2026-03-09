import sys
from pathlib import Path
from google import genai

def format_section(section_name: str):
    print(f"Formatting {section_name}...")
    docsrc = Path("docsrc")
    
    # Get all txt files for this section
    files = sorted(docsrc.glob(f"{section_name}*.txt"))
    # Filter out anything that's not part of the sequence, e.g. -en.txt
    files = [f for f in files if not f.name.endswith("-en.txt")]
    
    if not files:
        print(f"No files found for {section_name}")
        return
        
    compiled_text = ""
    for f in files:
        compiled_text += f"\n\n--- Page {f.stem} ---\n\n"
        compiled_text += f.read_text(encoding="utf-8")
        
    prompt = f"""
I have extracted OCR text from a Latin philosophical/mathematical book. The text is provided below, with pages separated by '--- Page ... ---'.

Please process this text and output a single, clean Markdown version of the text with the following instructions:
1. Organize the text using proper Markdown section headings (e.g., #, ##).
2. Format the footnotes using proper Markdown syntax (e.g., [^1] in the text and [^1]: footnote text at the bottom).
3. De-hyphenate words that were split across line breaks, so the text is continuous and clean.
4. Remove any top-of-page headings (headers) and page numbers that appear at the top of the pages.
5. Maintain the original Latin language. Do NOT translate.
6. Return ONLY the Markdown content without any introduction, markdown tags (```markdown) or conclusion. Just the raw markdown text.

Text to format:
{compiled_text}
"""
    
    client = genai.Client()
    response = client.models.generate_content(
        model='gemini-2.5-pro',
        contents=prompt,
    )
    
    out_path = docsrc / f"{section_name}.md"
    out_text = response.text
    if out_text.startswith("```markdown"):
        out_text = out_text[11:]
    if out_text.endswith("```"):
        out_text = out_text[:-3]
    out_path.write_text(out_text.strip(), encoding="utf-8")
    print(f"Saved formatted markdown to {out_path.name}")

def main():
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            format_section(arg)
    else:
        format_section("preface")
        format_section("caput-1")
        
if __name__ == "__main__":
    main()
