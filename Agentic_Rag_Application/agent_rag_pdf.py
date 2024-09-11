import os
import sys
from typing import List
import asyncio
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.node_parser import SimpleNodeParser
from llama_index.embeddings import OpenAIEmbedding
from llama_index.postprocessor import MetadataReplacementPostProcessor, SimilarityPostprocessor
from llama_index.indices.postprocessor import SentenceTransformerRerank
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.schema import Document
from dotenv import load_dotenv
import PyPDF2
import camelot

# Load environment variables
load_dotenv()

async def parse_pdf(file_path: str) -> str:
    """Parse a PDF file and return its content as a string."""
    content = ""

    # Extract text using PyPDF2
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            content += page.extract_text() + "\n"

    # Extract tables using Camelot
    tables = camelot.read_pdf(file_path)
    for table in tables:
        content += table.df.to_string(index=False) + "\n\n"

    return content

async def ingest_pdfs(directory: str) -> VectorStoreIndex:
    """Ingest PDFs from a directory and create a VectorStoreIndex."""
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]

    documents = []
    for pdf_file in pdf_files:
        file_path = os.path.join(directory, pdf_file)
        content = await parse_pdf(file_path)
        documents.append(Document(text=content))

    # Create a custom ServiceContext
    embed_model = OpenAIEmbedding()
    service_context = ServiceContext.from_defaults(
        llm=None,
        embed_model=embed_model,
        node_parser=SimpleNodeParser.from_defaults()
    )

    # Create and return the index
    return VectorStoreIndex.from_documents(
        documents,
        service_context=service_context
    )

class RAGQueryEngine:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    async def retrieve_nodes(self) -> RetrieverQueryEngine:
        embedding_model = OpenAIEmbedding()
        service_context = ServiceContext.from_defaults(
            llm=None,
            embed_model=embedding_model
        )
        index = VectorStoreIndex.from_vector_store(
            self.vector_store,
            service_context=service_context
        )
        postproc = MetadataReplacementPostProcessor(
            target_metadata_key="window"
        )
        rerank = SentenceTransformerRerank(
            top_n=5,
            model="BAAI/bge-reranker-base"
        )
        score = SimilarityPostprocessor(similarity_cutoff=0.60)
        query_engine = index.as_query_engine(
            similarity_top_k=10,
            alpha=0.5,
            node_postprocessors=[postproc, rerank, score],
        )
        return query_engine

async def query_index(index: VectorStoreIndex, query: str) -> str:
    """Query the index and return the result."""
    rag_engine = RAGQueryEngine(index.vector_store)
    query_engine = await rag_engine.retrieve_nodes()
    response = await query_engine.aquery(query)
    return str(response)

async def main():
    print("Welcome to the RAG-based Tabular PDF Ingestion Application!")

    # Get the directory path from the user
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
        print("\nResult:")
        print(result)

    print("Thank you for using the RAG-based Tabular PDF Ingestion Application!")

if __name__ == "__main__":
    asyncio.run(main())