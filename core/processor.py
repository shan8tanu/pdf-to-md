import pymupdf4llm
import fitz # PyMuPDF
from pathlib import Path
import datetime

def convert_pdf_to_md(file_path: str) -> str:
    """
    Phase 1, 2, & 4: Full Conversion Pipeline
    
    Updated for Phase 4:
    - Uses page_chunks=True to get per-page granularity.
    - Calls post_process_markdown to handle 'Janitor' and 'Librarian' tasks.
    """
    try:
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Phase 1 & 2: Core Extraction (with chunks for Phase 4)
        # invalidating 'write_images' to keep it text-only for now
        data_chunks = pymupdf4llm.to_markdown(file_path, page_chunks=True, write_images=False)
        
        # Phase 4: Context Injection & Cleaning
        full_markdown = post_process_markdown(data_chunks, file_path)
        
        return full_markdown
        
    except Exception as e:
        raise RuntimeError(f"Extraction Failed: {str(e)}")

def post_process_markdown(chunks: list, file_path: str) -> str:
    """
    Phase 4: The Janitor & The Librarian
    
    Args:
        chunks: List of dicts from pymupdf4llm [{'text': str, 'metadata': ...}, ...]
        file_path: Path to original file for metadata extraction
    """
    cleaned_pages = []
    
    # 1. Metadata Extraction (The Librarian - Frontmatter)
    doc = fitz.open(file_path)
    meta = doc.metadata
    page_count = doc.page_count
    doc.close()
    
    title = meta.get('title', 'Untitled Document')
    author = meta.get('author', 'Unknown Author')
    date_processed = datetime.date.today().isoformat()
    filename = Path(file_path).name
    
    frontmatter = f"""---
filename: "{filename}"
title: "{title}"
author: "{author}"
processed_date: "{date_processed}"
page_count: {page_count}
---

"""

    # 2. Page Iteration (The Janitor & Context Injection)
    for i, chunk in enumerate(chunks):
        page_num = i + 1
        text = chunk['text']
        
        # --- A. The Janitor (Cleaning) ---
        # Simple heuristic: If real-world app, we'd use coordinate checking here.
        # For 'Lite' version, we rely on pymupdf4llm's default cleaning, but we can
        # add specific string filters if needed.
        # e.g., removal of "Page X of Y" if it leaked through (optional)
        
        # --- B. The Librarian (Page Tags) ---
        # We explicitly wrap pages so the LLM knows boundaries.
        page_header = f"\n\n<!-- Page {page_num} -->\n## Page {page_num}\n"
        
        cleaned_pages.append(page_header + text)

    # 3. Assembly
    final_output = frontmatter + "".join(cleaned_pages)
    return final_output

def inspect_tables(file_path: str) -> list:
    """
    Phase 3: Table Extraction Debugger
    """
    doc = fitz.open(file_path)
    debug_data = []

    for page_index, page in enumerate(doc):
        tables = page.find_tables(strategy="lines_strict")
        if tables:
            for i, table in enumerate(tables):
                data = table.extract()
                debug_data.append({
                    "page": page_index + 1,
                    "index": i + 1,
                    "content": data,
                    "bbox": table.bbox
                })
    
    doc.close()
    return debug_data
