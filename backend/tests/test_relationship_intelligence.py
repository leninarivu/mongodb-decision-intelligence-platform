from collections.abc import Sequence
from typing import Any

from fastapi.testclient import TestClient
from pytest import MonkeyPatch

from app.db.mongodb import mongodb_manager
from app.main import create_app
from app.services.relationship_intelligence import build_relationship_pipeline


def contains_graph_lookup(value: object) -> bool:
    if isinstance(value, dict):
        return "$graphLookup" in value or any(
            contains_graph_lookup(item) for item in value.values()
        )
    if isinstance(value, list):
        return any(contains_graph_lookup(item) for item in value)
    return False


class FakeCursor:
    def __init__(self, documents: list[dict[str, object]]) -> None:
        self._documents = documents

    async def to_list(self, length: int) -> list[dict[str, object]]:
        return self._documents[:length]


class FakeCollection:
    def __init__(self, documents: list[dict[str, object]]) -> None:
        self.pipeline: Sequence[dict[str, object]] | None = None
        self._documents = documents

    def aggregate(self, pipeline: Sequence[dict[str, object]]) -> FakeCursor:
        self.pipeline = pipeline
        return FakeCursor(self._documents)


class FakeDatabase:
    def __init__(self, collection: FakeCollection) -> None:
        self._collection = collection

    def __getitem__(self, collection_name: str) -> FakeCollection:
        assert collection_name == "graph_edges"
        return self._collection


def relationship_document() -> dict[str, object]:
    nodes = [
        {
            "node_id": "node-gatorade-sku",
            "node_type": "product",
            "label": "Gatorade SKU",
            "description": "High-velocity Gatorade SKUs.",
            "business_context": "Product demand is 38% above baseline in Texas.",
        },
        {
            "node_id": "node-houston-plant",
            "node_type": "plant",
            "label": "Houston Plant",
            "description": "Regional beverage production capacity.",
            "business_context": "Production can be increased to restore downstream supply.",
        },
        {
            "node_id": "node-dallas-dc",
            "node_type": "distribution_center",
            "label": "Dallas DC",
            "description": "Distribution center serving Texas retailers.",
            "business_context": "Inventory is at 2.1 days of supply.",
        },
        {
            "node_id": "node-texas-retailers",
            "node_type": "retailer_group",
            "label": "Texas Retailers",
            "description": "Priority Texas retailers.",
            "business_context": "Retail service levels must be protected.",
        },
        {
            "node_id": "node-walmart-promotion",
            "node_type": "promotion",
            "label": "Walmart Promotion",
            "description": "Active retail promotion.",
            "business_context": "Promotion lift is amplifying demand.",
        },
        {
            "node_id": "node-texas-heatwave",
            "node_type": "weather",
            "label": "Texas Heatwave",
            "description": "High-severity heatwave.",
            "business_context": "105°F temperatures are increasing hydration demand.",
        },
        {
            "node_id": "node-demand-spike",
            "node_type": "demand_signal",
            "label": "Demand Spike",
            "description": "Detected demand increase.",
            "business_context": "Demand is up 38%.",
        },
        {
            "node_id": "node-recommended-decision",
            "node_type": "recommended_decision",
            "label": "Recommended Decision",
            "description": "Recommended response.",
            "business_context": "Protect service and revenue.",
        },
    ]
    edge_pairs = [
        ("node-gatorade-sku", "node-houston-plant"),
        ("node-houston-plant", "node-dallas-dc"),
        ("node-dallas-dc", "node-texas-retailers"),
        ("node-texas-retailers", "node-walmart-promotion"),
        ("node-walmart-promotion", "node-texas-heatwave"),
        ("node-texas-heatwave", "node-demand-spike"),
        ("node-demand-spike", "node-recommended-decision"),
    ]
    edges: list[dict[str, Any]] = [
        {
            "from_node_id": from_node_id,
            "to_node_id": to_node_id,
            "relationship_type": "CONNECTED_TO",
            "business_reason": f"{from_node_id} is connected to {to_node_id}.",
            "business_impact": "Relationship affects the recommended decision.",
            "weight": 0.9,
            "constraints": ["Capacity and timing must be monitored"],
        }
        for from_node_id, to_node_id in edge_pairs
    ]
    return {"nodes": nodes, "relationship_edges": edges}


def test_relationship_pipeline_contains_graph_lookup() -> None:
    pipeline = build_relationship_pipeline()

    assert contains_graph_lookup(pipeline)


def test_relationship_endpoint_returns_path_and_graph_lookup(monkeypatch: MonkeyPatch) -> None:
    fake_collection = FakeCollection([relationship_document()])
    monkeypatch.setattr(mongodb_manager, "get_database", lambda: FakeDatabase(fake_collection))

    app = create_app()
    client = TestClient(app)
    response = client.get("/api/relationship-intelligence/gatorade-texas")

    assert response.status_code == 200
    body = response.json()
    assert body["mongo_aggregation_used"] == "$graphLookup"
    assert body["relationship_path"] == [
        "Gatorade SKU",
        "Houston Plant",
        "Dallas DC",
        "Texas Retailers",
        "Walmart Promotion",
        "Texas Heatwave",
        "Demand Spike",
        "Recommended Decision",
    ]
    assert contains_graph_lookup(fake_collection.pipeline)
