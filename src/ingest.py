from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from database import get_connection_string
from vector_store import get_vector_store
from settings import settings

from dotenv import load_dotenv
load_dotenv()

def ingest_pdf() -> None:
    raw_documents = load_pdf()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    split_documents = text_splitter.split_documents(raw_documents)
    vector_store = get_vector_store()
    vector_store.from_documents(
        embedding=vector_store.embeddings,
        connection=get_connection_string(),
        documents=split_documents,
        collection_name=settings.pg_vector_collection_name,
        pre_delete_collection=True,
    )


def load_pdf() -> list[Document]:
    if not settings.pdf_path:
        raise ValueError("A variável de ambiente PDF_PATH não está definida.")
    pdf_path = Path(settings.pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_path}")
    loader = PyPDFLoader(str(pdf_path))
    return loader.load()


if __name__ == "__main__":
    ingest_pdf()
    print("Ingestão concluída com sucesso.")