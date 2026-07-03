from fastapi import APIRouter, status

from app.models.relationship_intelligence import RelationshipIntelligenceResponse
from app.services.relationship_intelligence import relationship_intelligence_service

router = APIRouter(prefix="/api/relationship-intelligence", tags=["relationship-intelligence"])


@router.get(
    "/gatorade-texas",
    response_model=RelationshipIntelligenceResponse,
    status_code=status.HTTP_200_OK,
)
async def gatorade_texas_relationship_intelligence() -> RelationshipIntelligenceResponse:
    return await relationship_intelligence_service.get_gatorade_texas_relationships()
