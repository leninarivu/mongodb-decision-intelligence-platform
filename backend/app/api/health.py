from fastapi import APIRouter, HTTPException, status

from app.db.mongodb import mongodb_manager
from app.models.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health() -> HealthResponse:
    if not await mongodb_manager.ping():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="MongoDB is not connected",
        )

    return HealthResponse(
        status="healthy",
        mongodb="connected",
        database=mongodb_manager.database_name,
        customer=mongodb_manager.customer_profile,
    )
