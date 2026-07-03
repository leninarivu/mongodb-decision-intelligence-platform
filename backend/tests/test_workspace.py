from fastapi.testclient import TestClient

from app.main import create_app


def test_dashboard_endpoint_returns_attention_summary() -> None:
    app = create_app()
    client = TestClient(app)

    response = client.get("/api/dashboard")

    assert response.status_code == 200
    body = response.json()
    assert body["question"] == "What needs my attention today?"
    assert body["alert"]["title"] == "Texas Gatorade Demand Spike"
    assert body["alert"]["demand_change"] == "+38%"
    assert len(body["metrics"]) == 5


def test_decision_package_endpoint_returns_required_recommendation() -> None:
    app = create_app()
    client = TestClient(app)

    response = client.get("/api/decision-package/gatorade-texas")

    assert response.status_code == 200
    body = response.json()
    assert body["business_question"] == (
        "Why is Gatorade demand increasing in Texas and what should we do?"
    )
    assert "Increase Houston production by 22%" in body["recommended_decision"]
    assert body["confidence"] == "92%"


def test_recent_decisions_endpoint_returns_memory_items() -> None:
    app = create_app()
    client = TestClient(app)

    response = client.get("/api/decisions/recent")

    assert response.status_code == 200
    body = response.json()
    assert len(body) >= 1
    assert body[0]["owner"] == "Supply Chain VP"
