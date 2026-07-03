from fastapi import APIRouter, Query, status

from app.models.knowledge import KnowledgeSearchResponse
from app.services.knowledge import knowledge_search_service

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])


@router.get("/search", response_model=KnowledgeSearchResponse, status_code=status.HTTP_200_OK)
async def search_knowledge(query: str = Query(..., min_length=1)) -> KnowledgeSearchResponse:
    return await knowledge_search_service.search(query)
