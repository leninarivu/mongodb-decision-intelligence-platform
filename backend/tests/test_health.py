from fastapi.testclient import TestClient

from app.main import create_app


def test_health_endpoint_reports_degraded_without_lifespan() -> None:
    app = create_app()
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"service": "degraded", "database": "unavailable"}
