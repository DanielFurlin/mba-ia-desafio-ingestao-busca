import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from database import setup_database
from pgvector_helper import get_pgvector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")

def ingest_pdf():
    raw_documents = load_pdf(PDF_PATH)[:1]
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,      # Maximum characters per chunk
        chunk_overlap=150,    # Overlap between consecutive chunks
    )
    splited_documents = text_splitter.split_documents(raw_documents)
    get_pgvector().from_documents(
        documents=splited_documents,
        collection_name="documents",
        pre_delete_collection=True
    )

def load_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    return documents

if __name__ == "__main__":
    conn = setup_database()
    print("Conexão com o banco de dados estabelecida com sucesso.")
    
    ingest_pdf()