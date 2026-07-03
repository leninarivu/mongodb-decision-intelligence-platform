import hashlib
import math
from abc import ABC, abstractmethod

from app.core.config import Settings, get_settings


class EmbeddingService(ABC):
    @abstractmethod
    def embed_text(self, text: str) -> list[float]:
        raise NotImplementedError


class LocalMockEmbeddingService(EmbeddingService):
    def __init__(self, dimensions: int) -> None:
        self._dimensions = dimensions

    def embed_text(self, text: str) -> list[float]:
        tokens = [token.strip().lower() for token in text.split() if token.strip()]
        vector = [0.0] * self._dimensions

        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], byteorder="big") % self._dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign

        magnitude = math.sqrt(sum(value * value for value in vector))
        if magnitude == 0:
            return vector

        return [value / magnitude for value in vector]


class ExternalEmbeddingServicePlaceholder(EmbeddingService):
    def __init__(self, provider: str) -> None:
        self._provider = provider

    def embed_text(self, text: str) -> list[float]:
        raise NotImplementedError(
            f"Embedding provider '{self._provider}' is not configured in this sprint."
        )


def get_embedding_service(settings: Settings | None = None) -> EmbeddingService:
    resolved_settings = settings or get_settings()
    provider = resolved_settings.embedding_provider.lower()

    if provider in {"local", "local_mock", "mock"}:
        return LocalMockEmbeddingService(resolved_settings.embedding_dimensions)

    return ExternalEmbeddingServicePlaceholder(provider)
