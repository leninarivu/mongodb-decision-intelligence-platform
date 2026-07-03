from typing import cast

from fastapi import HTTPException, status

from app.db.mongodb import MongoDocument, mongodb_manager
from app.models.relationship_intelligence import (
    RelationshipEdge,
    RelationshipIntelligenceResponse,
    RelationshipNode,
)

START_NODE_ID = "node-gatorade-sku"


def build_relationship_pipeline(start_node_id: str = START_NODE_ID) -> list[dict[str, object]]:
    return [
        {"$match": {"from_node_id": start_node_id}},
        {
            "$graphLookup": {
                "from": "graph_edges",
                "startWith": "$to_node_id",
                "connectFromField": "to_node_id",
                "connectToField": "from_node_id",
                "as": "traversed_edges",
                "depthField": "depth",
                "maxDepth": 8,
            }
        },
        {
            "$set": {
                "traversed_edges": {
                    "$sortArray": {"input": "$traversed_edges", "sortBy": {"depth": 1}}
                }
            }
        },
        {
            "$project": {
                "relationship_edges": {
                    "$concatArrays": [
                        [
                            {
                                "from_node_id": "$from_node_id",
                                "to_node_id": "$to_node_id",
                                "relationship_type": "$relationship_type",
                                "weight": "$weight",
                                "business_reason": "$business_reason",
                                "business_impact": "$business_impact",
                                "constraints": "$constraints",
                                "depth": -1,
                            }
                        ],
                        "$traversed_edges",
                    ]
                }
            }
        },
        {
            "$project": {
                "relationship_edges": 1,
                "node_ids": {
                    "$concatArrays": [
                        [{"$arrayElemAt": ["$relationship_edges.from_node_id", 0]}],
                        {
                            "$map": {
                                "input": "$relationship_edges",
                                "as": "edge",
                                "in": "$$edge.to_node_id",
                            }
                        },
                    ]
                },
            }
        },
        {
            "$lookup": {
                "from": "graph_nodes",
                "localField": "node_ids",
                "foreignField": "node_id",
                "as": "nodes",
            }
        },
        {"$limit": 1},
    ]


class RelationshipIntelligenceService:
    async def get_gatorade_texas_relationships(self) -> RelationshipIntelligenceResponse:
        try:
            database = mongodb_manager.get_database()
        except RuntimeError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="MongoDB is not connected",
            ) from exc

        pipeline = build_relationship_pipeline()
        documents = await database["graph_edges"].aggregate(pipeline).to_list(length=1)
        if not documents:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relationship graph for Gatorade Texas scenario was not found",
            )

        return self._format_response(documents[0])

    def _format_response(self, document: MongoDocument) -> RelationshipIntelligenceResponse:
        raw_nodes = self._list_of_documents(document.get("nodes"))
        raw_edges = self._list_of_documents(document.get("relationship_edges"))
        node_by_id = {str(node.get("node_id")): node for node in raw_nodes}

        relationship_path_ids = [START_NODE_ID]
        relationship_path_ids.extend(str(edge.get("to_node_id")) for edge in raw_edges)
        relationship_path = [
            self._node_label(node_by_id, node_id) for node_id in relationship_path_ids
        ]

        affected_nodes = [
            RelationshipNode(
                node_id=str(node.get("node_id", "")),
                node_type=str(node.get("node_type", "")),
                label=str(node.get("label", "")),
                description=str(node.get("description", "")),
                business_context=str(node.get("business_context", "")),
            )
            for node in sorted(
                raw_nodes,
                key=lambda node: relationship_path_ids.index(str(node.get("node_id")))
                if str(node.get("node_id")) in relationship_path_ids
                else 999,
            )
        ]

        relationships = [self._edge_response(edge, node_by_id) for edge in raw_edges]
        constraints = sorted(
            {
                str(constraint)
                for edge in raw_edges
                for constraint in self._list_of_strings(edge.get("constraints"))
                if str(constraint)
            }
        )

        return RelationshipIntelligenceResponse(
            business_summary=(
                "MongoDB traversed the Gatorade Texas operating graph to show how product, "
                "production, distribution, retail promotion, weather, demand, and decision "
                "entities are connected."
            ),
            relationship_path=relationship_path,
            nodes=affected_nodes,
            edges=relationships,
            affected_nodes=affected_nodes,
            impacted_entities=relationship_path,
            constraints=constraints,
            business_constraints=constraints,
            relationships=relationships,
            business_explanation=(
                "The demand spike is connected to a Texas heatwave and Walmart promotion, "
                "with Dallas DC inventory pressure requiring Houston production, Oklahoma "
                "City reallocation, additional truck capacity, and supplier monitoring."
            ),
            mongo_aggregation_used="$graphLookup",
        )

    def _edge_response(
        self,
        edge: MongoDocument,
        node_by_id: dict[str, MongoDocument],
    ) -> RelationshipEdge:
        from_node_id = str(edge.get("from_node_id", ""))
        to_node_id = str(edge.get("to_node_id", ""))
        from_label = self._node_label(node_by_id, from_node_id)
        to_label = self._node_label(node_by_id, to_node_id)
        weight = edge.get("weight", 0.0)

        return RelationshipEdge(
            from_node_id=from_node_id,
            to_node_id=to_node_id,
            relationship_type=str(edge.get("relationship_type", "")),
            relationship=f"{from_label} → {to_label}",
            why_it_exists=str(edge.get("business_reason", "")),
            business_impact=str(edge.get("business_impact", "")),
            weight=float(weight) if isinstance(weight, int | float | str) else 0.0,
            constraints=self._list_of_strings(edge.get("constraints")),
        )

    def _node_label(self, node_by_id: dict[str, MongoDocument], node_id: str) -> str:
        node = node_by_id.get(node_id)
        if node is None:
            return node_id
        return str(node.get("label", node_id))

    def _list_of_documents(self, value: object) -> list[MongoDocument]:
        if not isinstance(value, list):
            return []
        return [cast(MongoDocument, item) for item in value if isinstance(item, dict)]

    def _list_of_strings(self, value: object) -> list[str]:
        if not isinstance(value, list):
            return []
        return [str(item) for item in value]


relationship_intelligence_service = RelationshipIntelligenceService()
