import logging
from typing import Any, cast

from pymongo.errors import OperationFailure

from app.core.config import get_settings
from app.db.mongodb import MongoDocument, mongodb_manager
from app.models.knowledge import KnowledgeSearchResponse, KnowledgeSearchResult
from app.services.embedding_service import get_embedding_service

logger = logging.getLogger(__name__)


class KnowledgeSearchService:
    async def search(self, query: str) -> KnowledgeSearchResponse:
        settings = get_settings()
        embedding = get_embedding_service(settings).embed_text(query)

        try:
            database = mongodb_manager.get_database()
        except RuntimeError:
            return self._not_configured_response(query)

        try:
            playbook_results = await self._vector_search_collection(
                database["playbooks"],
                settings.atlas_vector_search_index,
                embedding,
                result_limit=3,
            )
            incident_results = await self._vector_search_collection(
                database["historical_incidents"],
                settings.atlas_vector_search_index,
                embedding,
                result_limit=3,
            )
        except OperationFailure:
            logger.info("Atlas Vector Search index is not configured", exc_info=True)
            return self._not_configured_response(query)
        except Exception:
            logger.exception("Knowledge vector search failed")
            return self._not_configured_response(query)

        results = [
            self._to_result(document)
            for document in sorted(
                [*playbook_results, *incident_results],
                key=self._score_value,
                reverse=True,
            )[:5]
        ]

        return KnowledgeSearchResponse(query=query, configured=True, results=results)

    async def _vector_search_collection(
        self,
        collection: Any,
        index_name: str,
        embedding: list[float],
        *,
        result_limit: int,
    ) -> list[MongoDocument]:
        pipeline = [
            {
                "$vectorSearch": {
                    "index": index_name,
                    "path": "embedding",
                    "queryVector": embedding,
                    "numCandidates": 50,
                    "limit": result_limit,
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "title": 1,
                    "summary": 1,
                    "content": 1,
                    "source_system": 1,
                    "scenario_type": 1,
                    "product": 1,
                    "region": 1,
                    "similarity_score": {"$meta": "vectorSearchScore"},
                }
            },
        ]
        documents = await collection.aggregate(pipeline).to_list(length=result_limit)
        return cast(list[MongoDocument], documents)

    def _to_result(self, document: MongoDocument) -> KnowledgeSearchResult:
        title = str(document.get("title", "Untitled knowledge record"))
        product = str(document.get("product", "the product"))
        region = str(document.get("region", "the region"))
        scenario_type = str(document.get("scenario_type", "decision context"))

        return KnowledgeSearchResult(
            title=title,
            summary=str(
                document.get("summary") or document.get("content") or "No summary available."
            ),
            source_system=str(document.get("source_system", "Unknown source")),
            similarity_score=round(self._score_value(document), 4),
            reason_retrieved=(
                f"Matched {product}, {region}, and {scenario_type.replace('_', ' ')} context."
            ),
        )

    def _score_value(self, document: MongoDocument) -> float:
        score = document.get("similarity_score", 0.0)
        if isinstance(score, int | float | str):
            return float(score)
        return 0.0

    def _not_configured_response(self, query: str) -> KnowledgeSearchResponse:
        return KnowledgeSearchResponse(
            query=query,
            configured=False,
            message="Vector Search index not configured yet",
            results=[],
        )


knowledge_search_service = KnowledgeSearchService()
