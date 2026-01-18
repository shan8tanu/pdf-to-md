# PDF-to-Context Bridge 🌉

> **Transform complex PDFs into clean, LLM-optimized Markdown using local CPU-based processing.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red) ![License](https://img.shields.io/badge/License-MIT-green)

## 📖 Overview

The **PDF-to-Context Bridge** is a local web application designed to solve the "Garbage In, Garbage Out" problem when feeding PDFs to Large Language Models. 

Standard PDF parsers often destroy document structure—merging headers into sentences, mangling tables, and losing reading order in multi-column layouts. This tool uses a 4-phase algorithmic pipeline to reconstruct the document logically, ensuring your LLM understands the *structure* of the data, not just the characters.

**Key capabilities:**
- 🔒 **100% Local Privacy**: Runs entirely on your machine. No APIs, no cloud.
- ⚡ **CPU Optimized**: No GPU required. Uses efficient algorithmic parsing (`pymupdf4llm`).
- 📊 **Table Recovery**: Detects and formats tables into Markdown grids.
- 📑 **Context Enrichment**: Injects page tags and metadata to help LLMs cite sources.

---

## 🚀 Quick Start (Windows)

### Prerequisites
- Python 3.10 or higher

### Installation
1. Clone or download this repository.
2. Double-click **`setup.bat`**. 
   - This will create a virtual environment and install all dependencies automatically.

### Running the App
1. Double-click **`run.bat`**.
2. The browser will open automatically (usually at `http://localhost:8501`).

---

## 🛠 Features & Pipeline

The application processes documents through 4 distinct phases (Documentation available in `docs/`):

### Phase 1: The Stitcher 🧵
> *Converts raw PDF draw commands into coherent words and sentences.*
- Reconstructs broken words (kerning issues).
- Stitches sentences across line breaks.

### Phase 2: The River 🌊
> *Intelligent Column & Layout Detection.*
- Identifies multi-column layouts using "White River" analysis.
- Ensures correct reading order (N-Path vs Z-Path) so text doesn't jump across columns.
- **Split View UI**: Compare original PDF vs. Output side-by-side.

### Phase 3: The Grid 🕸
> *Lattice-based Table Extraction.*
- Detects tables with explicit borders.
- Converts them into clean Markdown tables (`| Header | Value |`).
- **Table Debugger**: Inspect detected tables independently of the text.

### Phase 4: The Librarian 🏛
> *Context Injection & Cleaning.*
- **Header/Footer Removal**: Strips repetitive artifacts.
- **Page Tagging**: Injects `<!-- Page X -->` markers.
- **Frontmatter**: Adds YAML metadata (Title, Author, Date) for RAG systems.

---

## 📂 Project Structure

```text
pdf-to-context-bridge/
├── app.py                 # Main Streamlit UI Application
├── core/
│   └── processor.py       # The Logic Engine (Phases 1-4)
├── docs/                  # Technical Documentation & Design Specs
│   ├── prd.md             # Product Requirements Document
│   ├── td.md              # Technical Design Document
│   └── p1-p4.md           # Phase implementation details
├── temp/                  # Temporary storage for processing
├── requirements.txt       # Python dependencies
├── setup.bat              # One-click installer
└── run.bat                # One-click launcher
```

## 🤝 Contributing
This is a "Lite" version focused on speed and CPU efficiency. 
Feel free to fork and add GPU-based vision models for complex scanned documents!
