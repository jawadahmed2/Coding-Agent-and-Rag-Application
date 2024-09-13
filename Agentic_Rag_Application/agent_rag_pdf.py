import os
from typing import List, Dict
from llama_index.core import VectorStoreIndex, Document, ServiceContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core import Settings
import chromadb
import pandas as pd
import tabula
from config import AppConfig
import fitz
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

embed_model_name = AppConfig.EMBEDDING_MODEL()[0]
Settings.llm = None  # Disable LLM for this application

def get_service_context():
    embed_model = HuggingFaceEmbedding(model_name=embed_model_name)
    node_parser = SimpleNodeParser.from_defaults(
        chunk_size=2000,  # Increased to capture more context
        chunk_overlap=400
    )
    return ServiceContext.from_defaults(
        llm=None,
        embed_model=embed_model,
        node_parser=node_parser
    )

def extract_tables_from_pdf(file_path: str) -> List[pd.DataFrame]:
    return tabula.read_pdf(file_path, pages='all', multiple_tables=True)

def process_tables(tables: List[pd.DataFrame]) -> str:
    return "\n\n".join(table.to_string(index=False) for table in tables)

def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text).strip()
    return text

async def ingest_pdfs(directory: str) -> VectorStoreIndex:
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]

    documents = []
    for pdf_file in pdf_files:
        file_path = os.path.join(directory, pdf_file)

        tables = extract_tables_from_pdf(file_path)
        table_content = process_tables(tables)

        with fitz.open(file_path) as doc:
            text_content = ""
            for page in doc:
                text_content += clean_text(page.get_text())

        combined_content = f"{text_content}\n\n{table_content}"
        documents.append(Document(text=combined_content, metadata={"source": pdf_file}))

    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name="pdf_docs")

    for i, doc in enumerate(documents):
        collection.add(
            ids=[str(i)],
            documents=[doc.text],
            metadatas=[{"source": doc.metadata["source"]}],
        )

    print(f"Added {len(documents)} documents to the collection.")

    vector_store = ChromaVectorStore(collection)
    service_context = get_service_context()

    return VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        service_context=service_context
    )

def get_most_relevant_chunk_with_context(text: str, query: str, context_size: int = 300) -> str:
    words = text.split()
    chunks = []
    current_chunk = []

    for i, word in enumerate(words):
        current_chunk.append(word)
        if i % 50 == 0 and i > 0:  # Create overlapping chunks of ~50 words
            chunks.append(' '.join(current_chunk))
            current_chunk = current_chunk[-10:]  # Keep last 10 words for overlap

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    vectorizer = TfidfVectorizer()
    chunk_vectors = vectorizer.fit_transform(chunks)
    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(query_vector, chunk_vectors)
    most_relevant_chunk_index = similarities.argmax()

    # Get the context around the most relevant chunk
    start_index = max(0, most_relevant_chunk_index * 40 - context_size // len(' '.join(words)) * 40)
    end_index = min(len(words), (most_relevant_chunk_index + 1) * 40 + context_size // len(' '.join(words)) * 40)

    relevant_text = ' '.join(words[start_index:end_index])

    # Highlight the query terms
    highlighted_text = re.sub(f'({"|".join(re.escape(term) for term in query.split())})', r'**\1**', relevant_text, flags=re.IGNORECASE)

    return highlighted_text

async def query_index(index: VectorStoreIndex, query: str) -> Dict:
    retriever = index.as_retriever(similarity_top_k=3)
    nodes = retriever.retrieve(query)

    results = []
    sources = []
    for node in nodes:
        relevant_chunk = get_most_relevant_chunk_with_context(node.text, query)
        results.append(relevant_chunk)
        sources.append(node.metadata.get("source", "Unknown"))

    return {
        "results": results,
        "sources": sources
    }