import os
from langchain_core.embeddings import Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

from database import get_connection_string

_vector_store: PGVector | None = None

def get_vector_store(embeddings: Embeddings | None = None) -> PGVector:
  global _vector_store
  if _vector_store is None:
    if embeddings is None:
      embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL"))
    _vector_store = PGVector(
      embeddings=embeddings,
      collection_name="documents",
      connection=get_connection_string()
    )
  return _vector_store
