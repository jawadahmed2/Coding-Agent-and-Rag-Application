import os
import sys
from agent_rag_pdf import ingest_pdfs, query_index

async def main():
    print("Welcome to the RAG-based Tabular PDF Ingestion Application!")

    pdf_directory = input("Enter the path to the directory containing PDF files: ")

    if not os.path.isdir(pdf_directory):
        print("Error: The specified directory does not exist.")
        sys.exit(1)

    print("Ingesting PDFs and creating index... This may take a while.")
    index = await ingest_pdfs(pdf_directory)
    print("Index created successfully!")

    while True:
        query = input("\nEnter your query (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break

        result = await query_index(index, query)
        print("\nResults:")
        for i, text in enumerate(result["results"]):
            print(f"\nResult {i+1}:")
            print(text)
        print("\nSources:")
        for source in result["sources"]:
            print(f"- {source}")

    print("Thank you for using the RAG-based Tabular PDF Ingestion Application!")


import nest_asyncio, asyncio
nest_asyncio.apply()

if __name__ == "__main__":
    asyncio.run(main())
