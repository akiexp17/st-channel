---
name: PDFToMarkdown
description: Converts PDF documents to structured Markdown by first converting pages to images and then visually analyzing them with AI. This approach ensures high fidelity for complex layouts, tables, and figures.
license: MIT
---

# PDFToMarkdown

This skill converts PDF documents into structured Markdown files using a visual approach. It is particularly effective for PDFs with complex layouts, tables, and figures that traditional text extraction tools often mishandle.

## Usage

This skill follows a multi-step workflow:
1.  **Convert PDF to Images**: Split the PDF into individual image files.
2.  **Visual Analysis**: The AI visually "reads" each page image to extract text, tables, and structure.
3.  **Markdown Generation**: Compile the analyzed content into a single Markdown document.

### Step 1: Convert PDF to Images

Use the provided Python script to convert the PDF into a series of PNG images.

```bash
# Basic usage
python .agent/skills/PDFToMarkdown/scripts/pdf_to_images.py /path/to/document.pdf

# Specify output directory and DPI
python .agent/skills/PDFToMarkdown/scripts/pdf_to_images.py /path/to/document.pdf /path/to/output_dir 300
```

This will create a directory (defaulting to the PDF filename) containing `page_001.png`, `page_002.png`, etc.

### Step 2: Visual Analysis & Markdown Generation

Once the images are generated, instruct the AI to process them. **For large documents (>10 pages), process in batches to ensure high quality and avoid context limits.**

**Prompt Template:**

> "I have converted a PDF into images in the directory `{output_dir}`. Please visually analyze `page_{start}` to `page_{end}` and convert them into a structured Markdown format. Preserve all headings, tables, and figures. Output the result as a Markdown file."

**Rules for AI Analysis:**
*   **Tables**: Reconstruct tables using Markdown syntax. Do not flatten them into text.
*   **Figures**: Describe the content of charts and diagrams in detail.
*   **Headings**: Use appropriate `#` header levels to match the visual hierarchy.
*   **Accuracy**: Do not summarize; aim for a faithful transcription of the content.

### Step 3: Combine References (Optional)

If processing in batches, you may finish with multiple Markdown files (e.g., `part1.md`, `part2.md`). Use `cat` or a simple script to combine them if needed, or keep them separate for modularity.

## Dependencies

*   **Python Libraries**: `pdf2image`, `Pillow`
    *   `pip install pdf2image Pillow`
*   **System Utility**: `poppler`
    *   **macOS**: `brew install poppler`
    *   **Linux**: `sudo apt-get install poppler-utils`
    *   **Windows**: Download from [poppler releases](https://github.com/oschwartz10612/poppler-windows/releases) and add to PATH.
