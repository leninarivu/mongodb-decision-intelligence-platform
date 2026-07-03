from pydantic import BaseModel, ConfigDict


class RelationshipNode(BaseModel):
    node_id: str
    node_type: str
    label: str
    description: str
    business_context: str


class RelationshipEdge(BaseModel):
    from_node_id: str
    to_node_id: str
    relationship_type: str
    relationship: str
    why_it_exists: str
    business_impact: str
    weight: float
    constraints: list[str]


class RelationshipIntelligenceResponse(BaseModel):
    business_summary: str
    relationship_path: list[str]
    nodes: list[RelationshipNode]
    edges: list[RelationshipEdge]
    affected_nodes: list[RelationshipNode]
    impacted_entities: list[str]
    constraints: list[str]
    business_constraints: list[str]
    relationships: list[RelationshipEdge]
    business_explanation: str
    mongo_aggregation_used: str

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "business_summary": "MongoDB traversed the Gatorade Texas supply chain graph.",
                    "relationship_path": ["Gatorade SKU", "Houston Plant", "Dallas DC"],
                    "mongo_aggregation_used": "$graphLookup",
                }
            ]
        }
    )
