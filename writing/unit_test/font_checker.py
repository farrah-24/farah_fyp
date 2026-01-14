import pymupdf  # Correct import for PyMuPDF
import os
from collections import defaultdict

def extract_fonts_from_pdf(pdf_path):
    """Extracts font types from each page of a PDF."""

    # Check if the file exists
    if not os.path.exists(pdf_path):
        print(f"Error: The file '{pdf_path}' was not found.")
        return None

    # Open the PDF
    doc = pymupdf.open(pdf_path)
    fonts_per_page = defaultdict(set)

    for page_num in range(len(doc)):
        page = doc[page_num]
        font_info = page.get_fonts(full=True)  # Extract all fonts on the page

        # Process font information
        for font in font_info:
            font_name = font[3]  # Font name is at index 3
            fonts_per_page[page_num + 1].add(font_name)  # Page numbers start from 1

    return fonts_per_page

if __name__ == "__main__":
    # Change this to your actual PDF file path
    pdf_path = r"C:\Users\balan\Downloads\fyp_draft_template-2.pdf"

    fonts = extract_fonts_from_pdf(pdf_path)

    if fonts:
        print("\n--- Font Report Per Page ---\n")
        for page, font_set in fonts.items():
            print(f"Page {page}: {', '.join(font_set)}")
    else:
        print("No fonts found or PDF could not be processed.")
