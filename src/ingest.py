import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from database import setup_database
from vector_store import get_vector_store

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
MAX_PAGES = 1
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

def ingest_pdf() -> None:
  raw_documents = load_pdf(PDF_PATH)[:MAX_PAGES]
  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
  )
  split_documents = text_splitter.split_documents(raw_documents)
  get_vector_store().from_documents(
    documents=split_documents,
    collection_name="documents",
    pre_delete_collection=True
  )

def load_pdf(pdf_path: str) -> list[Document]:
  loader = PyPDFLoader(pdf_path)
  documents = loader.load()
  return documents

if __name__ == "__main__":
  conn = setup_database()
  print("Conexão com o banco de dados estabelecida com sucesso.")
  try:
    ingest_pdf()
  finally:
    conn.close()