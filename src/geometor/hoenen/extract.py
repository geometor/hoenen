import os
import sys
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image

def extract_text(image_path: Path) -> str:
    print(f"Extracting text from {image_path.name}...")
    # Initialize the Gemini client. It automatically picks up the GEMINI_API_KEY env var
    client = genai.Client()
    
    # Open the image using PIL
    image = Image.open(image_path)
    
    # Prompt the model to extract the Latin text
    prompt = """
    Please extract all the text from this image exactly as it is written.
    The text is in Latin. 
    Preserve paragraph structure and line breaks where appropriate.
    Do not add any additional commentary, just output the raw transcribed text.
    """
    
    # Use gemini-2.5-pro for best OCR results
    response = client.models.generate_content(
        model='gemini-2.5-pro',
        contents=[image, prompt]
    )
    
    return response.text

def process_directory(directory: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    
    extensions = ['*.png', '*.jpg', '*.jpeg']
    files = []
    for ext in extensions:
        files.extend(directory.glob(ext))
    files.sort()
    
    for file_path in files:
        if file_path.name == "title.jpg":
            continue
            
        output_file = output_dir / f"{file_path.stem}.txt"
        
        # skip if already exists
        if output_file.exists():
            continue
            
        text = extract_text(file_path)
        output_file.write_text(text, encoding='utf-8')
        print(f"Saved extracted text to {output_file}")

if __name__ == '__main__':
    base_dir = Path("/home/phi/PROJECTS/geometor/hoenen")
    output_dir = base_dir / "extracted_text"
    
    # Run a test on a single file first
    test_file = base_dir / "caput-1-01.png"
    if test_file.exists():
        try:
            text = extract_text(test_file)
            print("--- Extracted Text Preview ---")
            print(text[:500])
            print("------------------------------")
            
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"{test_file.stem}.txt"
            output_file.write_text(text, encoding='utf-8')
            print(f"Saved to {output_file}")
            
        except Exception as e:
            print(f"Error during extraction: {e}")
    else:
        print("Test file not found.")
