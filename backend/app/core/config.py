from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "MongoDB Decision Intelligence Platform API"
    environment: str = "local"
    log_level: str = "info"
    backend_cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_database: str = "mdip_demo"
    customer_profile: str = "PepsiCo"
    embedding_provider: str = "local_mock"
    embedding_dimensions: int = 128
    atlas_vector_search_index: str = "mdip_knowledge_vector_index"

    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
