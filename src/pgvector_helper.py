import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

from database import get_connection_string

def get_pgvector():
    return PGVector(
        embeddings=GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL")),
        collection_name="documents",
        connection=get_connection_string()
    )