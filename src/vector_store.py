from langchain_core.embeddings import Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

from database import get_connection_string
from settings import settings

_vector_store: PGVector | None = None

def get_vector_store(embeddings: Embeddings | None = None) -> PGVector:
    global _vector_store
    if _vector_store is None:
        if embeddings is None:
            if settings.google_embedding_model:
                embeddings = GoogleGenerativeAIEmbeddings(model=settings.google_embedding_model)
            elif settings.openai_embedding_model:
                embeddings = OpenAIEmbeddings(model=settings.openai_embedding_model)
            else:
                raise ValueError("Uma das seguintes variáveis de ambiente GOOGLE_EMBEDDING_MODEL ou OPENAI_EMBEDDING_MODEL deve ser definida.")
        _vector_store = PGVector(
            embeddings=embeddings,
            collection_name=settings.pg_vector_collection_name,
            connection=get_connection_string(),
        )
    return _vector_store
