# Agentic Rag Application

This project provides a solution for parsing tabular data from PDFs and retrieve a relevant details. While it does not currently use a Large Language Model (LLM) for re-ranking, incorporating an LLM could significantly enhance the application's performance in terms of improving the quality of output data.

## Features

- An RAG application using Llama Index to handle tabular PDF ingestion.
- A user-friendly interface for querying and retrieving relevant information from the ingested PDFs.
- PDF parsing libraries (e.g., PyPDF2, Camelot).

## Prerequisites

- Python 3.11 or higher
- Poetry (for dependency management)

## Installation

To get started with this project, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/jawadahmed2/Coding-Agent-and-Rag-Application.git
   cd Agentic_Rag_Application
   ```

2. Install the dependencies using Poetry:

    Note: First deactivate the virtual or conda environments in the terminal

   ```bash
   pip install poetry
   poetry install
   ```

3. Activate the Poetry shell:

   ```bash
   poetry shell
   ```

## Usage

After installation, you can run the application by executing the `main.py` script:

```bash
python main.py
```

You can also modify `config.py` to adjust any configuration settings based on your needs, such as the path to PDF files.

## Notes

- This project **does not currently use a Large Language Model (LLM)**. However, incorporating an LLM for re-ranking the extracted data could enhance the accuracy and performance of the parser.

## File Structure

```bash
.
├── agent_rag_pdf.py           # Core logic for processing PDF files.
├── config.py                  # Configuration settings for the application.
├── main.py                    # Main script to run the application.
├── pdf_files/                 # Directory containing sample PDF files.
│   ├── data_tables_sample.pdf # Sample PDF with tabular data.
│   └── table.pdf              # Another sample PDF.
├── pdf_tabular_parser.py      # Module for handling the parsing of tabular data.
├── poetry.lock                # Poetry lock file for dependency management.
├── pyproject.toml             # Project configuration and dependencies.
├── README.md                  # This file.
```
