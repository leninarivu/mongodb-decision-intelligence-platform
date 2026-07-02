from fastapi import APIRouter, status

from app.db.mongodb import ping_mongodb
from app.models.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health() -> HealthResponse:
    database = "ok" if await ping_mongodb() else "unavailable"
    service = "ok" if database == "ok" else "degraded"

    return HealthResponse(service=service, database=database)
