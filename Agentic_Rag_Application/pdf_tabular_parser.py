import PyPDF2
import camelot
import pandas as pd
import re
from typing import List, Tuple

def clean_text(text: str) -> str:
    """Clean and normalize the extracted text."""
    # Remove excessive whitespace and normalize newlines
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

def extract_tables(file_path: str) -> List[Tuple[int, pd.DataFrame]]:
    """Extract tables from the PDF using Camelot."""
    tables = camelot.read_pdf(file_path, pages='all', flavor='stream')
    return [(table.page, table.df) for table in tables]

def is_text_in_table(text: str, table: pd.DataFrame) -> bool:
    """Check if the given text significantly overlaps with the table content."""
    table_text = ' '.join(table.values.flatten().astype(str))
    return len(set(text.split()) & set(table_text.split())) / len(set(text.split())) > 0.5

async def parse_pdf(file_path: str) -> str:
    """Parse a PDF file and return its content as a string without repetition."""
    content = []
    extracted_tables = extract_tables(file_path)

    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num, page in enumerate(reader.pages, start=1):
            page_text = clean_text(page.extract_text())
            page_tables = [table for p, table in extracted_tables if p == page_num]

            # Split page text into paragraphs
            paragraphs = re.split(r'\n\s*\n', page_text)

            for para in paragraphs:
                if not any(is_text_in_table(para, table) for table in page_tables):
                    content.append(f"Page {page_num}:\n{para}\n")

            # Add tables for this page
            for table in page_tables:
                table_str = table.to_string(index=False, header=False)
                content.append(f"Table on Page {page_num}:\n{table_str}\n")

    return '\n'.join(content)

# Example usage
# if __name__ == "__main__":
#     import asyncio
#     result = asyncio.run(parse_pdf("table.pdf"))
#     print(result)