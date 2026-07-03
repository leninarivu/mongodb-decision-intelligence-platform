from fastapi.testclient import TestClient

from app.main import create_app
from app.services.embedding_service import get_embedding_service


def test_local_mock_embedding_is_deterministic() -> None:
    service = get_embedding_service()

    first = service.embed_text("Gatorade Texas heatwave")
    second = service.embed_text("Gatorade Texas heatwave")

    assert first == second
    assert len(first) == 128


def test_knowledge_search_gracefully_reports_missing_vector_index() -> None:
    app = create_app()
    client = TestClient(app)

    response = client.get(
        "/api/knowledge/search",
        params={"query": "Why is Gatorade demand increasing in Texas?"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["configured"] is False
    assert body["message"] == "Vector Search index not configured yet"
    assert body["setup_documentation"] == "docs/08-Atlas-Vector-Search-Setup.md"
    assert body["results"] == []
