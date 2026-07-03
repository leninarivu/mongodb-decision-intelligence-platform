from fastapi.testclient import TestClient
from pytest import MonkeyPatch

from app.core.config import get_settings
from app.db.mongodb import mongodb_manager
from app.main import create_app


def test_health_endpoint_reports_connection_metadata(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("CUSTOMER_PROFILE", "PepsiCo")
    monkeypatch.setenv("MONGODB_DATABASE", "mdip_demo")
    get_settings.cache_clear()

    async def connected() -> bool:
        return True

    monkeypatch.setattr(mongodb_manager, "ping", connected)
    app = create_app()
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "mongodb": "connected",
        "database": "mdip_demo",
        "customer": "PepsiCo",
    }


def test_health_endpoint_reports_unavailable_mongodb(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("CUSTOMER_PROFILE", "PepsiCo")
    monkeypatch.setenv("MONGODB_DATABASE", "mdip_demo")
    get_settings.cache_clear()

    async def disconnected() -> bool:
        return False

    monkeypatch.setattr(mongodb_manager, "ping", disconnected)
    app = create_app()
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 503
    assert response.json() == {"detail": "MongoDB is not connected"}
