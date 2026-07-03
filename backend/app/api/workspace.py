from fastapi import APIRouter, status

from app.models.workspace import DashboardResponse, DecisionPackageResponse, RecentDecision
from app.services.workspace import workspace_service

router = APIRouter(prefix="/api", tags=["workspace"])


@router.get("/dashboard", response_model=DashboardResponse, status_code=status.HTTP_200_OK)
async def dashboard() -> DashboardResponse:
    return await workspace_service.get_dashboard()


@router.get(
    "/decision-package/gatorade-texas",
    response_model=DecisionPackageResponse,
    status_code=status.HTTP_200_OK,
)
async def gatorade_texas_decision_package() -> DecisionPackageResponse:
    return await workspace_service.get_decision_package("gatorade-texas")


@router.get(
    "/decisions/recent",
    response_model=list[RecentDecision],
    status_code=status.HTTP_200_OK,
)
async def recent_decisions() -> list[RecentDecision]:
    return await workspace_service.get_recent_decisions()
