from pathlib import Path
from typing import Optional
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    google_api_key: Optional[SecretStr] = None
    google_embedding_model: Optional[str] = None
    google_chatbot_model: Optional[str] = None
    openai_api_key: Optional[SecretStr] = None
    openai_embedding_model: Optional[str] = None
    openai_chatbot_model: Optional[str] = None
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "rag"
    db_user: str = "postgres"
    db_password: SecretStr = "postgres"
    pg_vector_collection_name: str = "documents"
    pdf_path: str = ""
    chunk_size: int = 1000
    chunk_overlap: int = 150


settings = Settings()
