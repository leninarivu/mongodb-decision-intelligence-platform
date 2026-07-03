import asyncio
from collections.abc import Mapping

from app.core.config import get_settings
from app.db.mongodb import MongoDocument, mongodb_manager
from app.repositories import COLLECTION_REPOSITORIES
from app.services.embedding_service import EmbeddingService, get_embedding_service


def embedded_document(
    document: MongoDocument,
    embedding_service: EmbeddingService,
    text_fields: list[str],
) -> MongoDocument:
    text = " ".join(str(document.get(field, "")) for field in text_fields)
    return {**document, "embedding": embedding_service.embed_text(text)}


def demo_data(
    customer_profile: str,
    embedding_service: EmbeddingService | None = None,
) -> Mapping[str, list[MongoDocument]]:
    resolved_embedding_service = embedding_service or get_embedding_service()

    playbooks = [
        embedded_document(
            {
                "_id": "playbook-heatwave-beverage-demand-response",
                "customer_profile": customer_profile,
                "title": "Heatwave Response Playbook",
                "summary": (
                    "Protect priority retail accounts during heatwave beverage demand spikes."
                ),
                "content": (
                    "When temperatures exceed seasonal norms and hydration category demand "
                    "accelerates, protect priority retail accounts, review regional days "
                    "of supply daily, reallocate inventory from lower-risk adjacent nodes, "
                    "and escalate production review if demand persists beyond 7 days."
                ),
                "source_system": "MDIP Playbook Library",
                "scenario_type": "weather_driven_demand_spike",
                "product": "Gatorade",
                "region": "Texas",
                "recommended_actions": [
                    "Protect priority retail accounts",
                    "Review regional days of supply daily",
                    "Reallocate inventory from lower-risk adjacent nodes",
                    "Escalate production review if demand persists beyond 7 days",
                ],
                "approval_requirements": ["Supply Chain VP"],
            },
            resolved_embedding_service,
            ["title", "summary", "content", "scenario_type", "product", "region"],
        ),
        embedded_document(
            {
                "_id": "playbook-retail-promotion-replenishment-policy",
                "customer_profile": customer_profile,
                "title": "Retail Promotion Replenishment Policy",
                "summary": "Promotion-driven stock risk requires approval and daily monitoring.",
                "content": (
                    "When a major retailer promotion increases sell-through above forecast, "
                    "validate DC coverage, protect priority stores, confirm incremental "
                    "transportation capacity, and route material reallocation decisions "
                    "through supply chain approval."
                ),
                "source_system": "Retail Execution Policy Repository",
                "scenario_type": "retail_promotion_replenishment",
                "product": "Gatorade",
                "region": "Texas",
                "recommended_actions": [
                    "Validate promotion lift against inventory coverage",
                    "Prioritize replenishment for high-velocity retail accounts",
                    "Confirm transportation capacity before reallocating inventory",
                ],
                "approval_requirements": ["Supply Chain VP", "Logistics Manager"],
            },
            resolved_embedding_service,
            ["title", "summary", "content", "scenario_type", "product", "region"],
        ),
    ]

    historical_incidents = [
        embedded_document(
            {
                "_id": "incident-texas-beverage-demand-spike-2025",
                "customer_profile": customer_profile,
                "title": "2025 Texas Beverage Demand Spike Incident",
                "summary": "Heatwave and retail display activity lifted sports drink velocity.",
                "content": (
                    "A prior Texas heatwave combined with retail display activity created "
                    "a sports drink demand surge. Service levels stabilized within 72 "
                    "hours after inventory was reallocated from adjacent distribution "
                    "centers and daily sell-through monitoring was established."
                ),
                "source_system": "Supply Chain Incident Review",
                "scenario_type": "historical_heatwave_demand_spike",
                "product": "Gatorade",
                "region": "Texas",
                "products": ["Gatorade"],
                "regions": ["Texas", "Arizona", "New Mexico"],
                "drivers": ["heatwave", "promotion", "school_sports"],
                "actions_taken": ["inventory_reallocation", "daily_sell_through_monitoring"],
                "outcome": "Service levels stabilized within 72 hours.",
                "lessons_learned": (
                    "Adjacent DC transfers should begin before supply drops below 4 days."
                ),
            },
            resolved_embedding_service,
            ["title", "summary", "content", "scenario_type", "product", "region"],
        )
    ]

    decision_history = [
        embedded_document(
            {
                "_id": "decision-gatorade-texas-precedent-2025",
                "customer_profile": customer_profile,
                "title": "Prior heatwave demand response",
                "summary": "Approved replenishment response for prior heatwave demand spike.",
                "content": (
                    "The supply chain team prioritized replenishment to high-velocity "
                    "accounts, reallocated inventory from adjacent nodes, and monitored "
                    "supplier capacity until service levels stabilized."
                ),
                "source_system": "MDIP Decision Memory",
                "scenario_type": "approved_decision_memory",
                "product": "Gatorade",
                "region": "Texas",
                "business_question": "How did we respond to prior heatwave demand spikes?",
                "recommendation": "Prioritize replenishment to high-velocity accounts.",
                "business_impact": {
                    "revenue_protected_usd": 1200000,
                    "service_level_improvement_points": 4.5,
                    "decision_cycle_reduction_hours": 36,
                },
                "approval_status": "approved",
                "approver": "Supply Chain VP",
                "outcome": "Used as reusable precedent for future hydration demand spikes.",
            },
            resolved_embedding_service,
            ["title", "summary", "content", "scenario_type", "product", "region"],
        )
    ]

    return {
        "products": [
            {
                "_id": "prod-gatorade-20oz-fruit-punch",
                "customer_profile": customer_profile,
                "brand": "Gatorade",
                "sku": "GAT-20-FP",
                "name": "Gatorade Fruit Punch 20 oz",
                "category": "Sports Drink",
                "package_size": "20 oz bottle",
                "substitution_group": "gatorade-core-20oz",
                "active": True,
            },
            {
                "_id": "prod-gatorade-20oz-lemon-lime",
                "customer_profile": customer_profile,
                "brand": "Gatorade",
                "sku": "GAT-20-LL",
                "name": "Gatorade Lemon Lime 20 oz",
                "category": "Sports Drink",
                "package_size": "20 oz bottle",
                "substitution_group": "gatorade-core-20oz",
                "active": True,
            },
            {
                "_id": "prod-gatorade-zero-20oz-orange",
                "customer_profile": customer_profile,
                "brand": "Gatorade Zero",
                "sku": "GZ-20-ORG",
                "name": "Gatorade Zero Orange 20 oz",
                "category": "Sports Drink",
                "package_size": "20 oz bottle",
                "substitution_group": "gatorade-zero-20oz",
                "active": True,
            },
        ],
        "regions": [
            {
                "_id": "region-texas",
                "customer_profile": customer_profile,
                "name": "Texas",
                "state": "TX",
                "market_cluster": "South Central",
                "retail_territories": ["Dallas-Fort Worth", "Houston", "Austin", "San Antonio"],
                "distribution_zones": ["zone-dfw", "zone-houston", "zone-central-tx"],
            },
            {
                "_id": "region-oklahoma",
                "customer_profile": customer_profile,
                "name": "Oklahoma",
                "state": "OK",
                "market_cluster": "South Central",
                "retail_territories": ["Oklahoma City", "Tulsa"],
                "distribution_zones": ["zone-okc"],
            },
        ],
        "plants": [
            {
                "_id": "plant-dallas-beverage",
                "customer_profile": customer_profile,
                "name": "Dallas Beverage Plant",
                "region_id": "region-texas",
                "capacity_status": "elevated-utilization",
                "supported_products": ["prod-gatorade-20oz-fruit-punch"],
                "weekly_capacity_units": 1250000,
            },
            {
                "_id": "plant-tulsa-beverage",
                "customer_profile": customer_profile,
                "name": "Tulsa Beverage Plant",
                "region_id": "region-oklahoma",
                "capacity_status": "available-capacity",
                "supported_products": [
                    "prod-gatorade-20oz-lemon-lime",
                    "prod-gatorade-zero-20oz-orange",
                ],
                "weekly_capacity_units": 840000,
            },
        ],
        "warehouses": [
            {
                "_id": "wh-dfw-dc",
                "customer_profile": customer_profile,
                "name": "Dallas-Fort Worth Distribution Center",
                "region_id": "region-texas",
                "warehouse_type": "regional_dc",
                "service_level_risk": "medium",
            },
            {
                "_id": "wh-houston-dc",
                "customer_profile": customer_profile,
                "name": "Houston Distribution Center",
                "region_id": "region-texas",
                "warehouse_type": "regional_dc",
                "service_level_risk": "high",
            },
            {
                "_id": "wh-okc-dc",
                "customer_profile": customer_profile,
                "name": "Oklahoma City Distribution Center",
                "region_id": "region-oklahoma",
                "warehouse_type": "regional_dc",
                "service_level_risk": "low",
            },
        ],
        "inventory": [
            {
                "_id": "inv-gat-fp-dfw-2026-07-03",
                "customer_profile": customer_profile,
                "product_id": "prod-gatorade-20oz-fruit-punch",
                "warehouse_id": "wh-dfw-dc",
                "available_units": 184000,
                "committed_units": 126000,
                "days_of_supply": 5.4,
                "as_of": "2026-07-03T08:00:00Z",
            },
            {
                "_id": "inv-gat-ll-houston-2026-07-03",
                "customer_profile": customer_profile,
                "product_id": "prod-gatorade-20oz-lemon-lime",
                "warehouse_id": "wh-houston-dc",
                "available_units": 92000,
                "committed_units": 81000,
                "days_of_supply": 3.1,
                "as_of": "2026-07-03T08:00:00Z",
            },
            {
                "_id": "inv-gz-orange-okc-2026-07-03",
                "customer_profile": customer_profile,
                "product_id": "prod-gatorade-zero-20oz-orange",
                "warehouse_id": "wh-okc-dc",
                "available_units": 144000,
                "committed_units": 42000,
                "days_of_supply": 9.7,
                "as_of": "2026-07-03T08:00:00Z",
            },
        ],
        "suppliers": [
            {
                "_id": "supplier-pet-resin-gulf",
                "customer_profile": customer_profile,
                "name": "Gulf Coast PET Resin Supply",
                "supplier_type": "packaging_material",
                "risk_status": "normal",
                "supported_plants": ["plant-dallas-beverage", "plant-tulsa-beverage"],
            },
            {
                "_id": "supplier-electrolyte-blend-midwest",
                "customer_profile": customer_profile,
                "name": "Midwest Electrolyte Blend Co.",
                "supplier_type": "ingredient",
                "risk_status": "watch",
                "supported_plants": ["plant-dallas-beverage"],
            },
        ],
        "shipments": [
            {
                "_id": "ship-dfw-retail-2026-07-03-001",
                "customer_profile": customer_profile,
                "origin_id": "wh-dfw-dc",
                "destination": "DFW Priority Retail Accounts",
                "product_ids": ["prod-gatorade-20oz-fruit-punch"],
                "status": "in_transit",
                "units": 42000,
                "planned_delivery": "2026-07-04",
            },
            {
                "_id": "ship-okc-houston-transfer-2026-07-03",
                "customer_profile": customer_profile,
                "origin_id": "wh-okc-dc",
                "destination": "wh-houston-dc",
                "product_ids": ["prod-gatorade-zero-20oz-orange"],
                "status": "planned",
                "units": 36000,
                "planned_delivery": "2026-07-05",
            },
        ],
        "logistics_partners": [
            {
                "_id": "carrier-lonestar-freight",
                "customer_profile": customer_profile,
                "name": "Lone Star Freight",
                "mode": "truckload",
                "lane_coverage": ["DFW", "Houston", "Austin", "San Antonio"],
                "capacity_status": "tight",
            },
            {
                "_id": "carrier-red-river-logistics",
                "customer_profile": customer_profile,
                "name": "Red River Logistics",
                "mode": "regional_truckload",
                "lane_coverage": ["Oklahoma City", "Dallas-Fort Worth", "Houston"],
                "capacity_status": "available",
            },
        ],
        "demand_signals": [
            {
                "_id": "signal-gatorade-texas-heatwave-2026-07-03",
                "customer_profile": customer_profile,
                "product_ids": [
                    "prod-gatorade-20oz-fruit-punch",
                    "prod-gatorade-20oz-lemon-lime",
                ],
                "region_id": "region-texas",
                "time_window": "2026-07-01/2026-07-07",
                "baseline_units": 510000,
                "observed_units": 734000,
                "variance_percent": 43.9,
                "confidence_score": 0.91,
                "detected_drivers": ["heatwave", "retail_promotion"],
            }
        ],
        "weather_events": [
            {
                "_id": "weather-texas-heatwave-2026-07",
                "customer_profile": customer_profile,
                "region_id": "region-texas",
                "event_type": "heatwave",
                "severity": "high",
                "start_date": "2026-07-01",
                "end_date": "2026-07-08",
                "temperature_delta_f": 9.4,
                "source": "synthetic-weather-feed",
            }
        ],
        "promotions": [
            {
                "_id": "promo-gatorade-texas-summer-retail-2026",
                "customer_profile": customer_profile,
                "retailer": "Large Format Grocery - Texas Region",
                "product_ids": [
                    "prod-gatorade-20oz-fruit-punch",
                    "prod-gatorade-20oz-lemon-lime",
                ],
                "region_ids": ["region-texas"],
                "promotion_type": "endcap_and_price_reduction",
                "start_date": "2026-06-29",
                "end_date": "2026-07-06",
                "expected_lift_percent": 18,
                "execution_status": "active",
            }
        ],
        "retail_sales": [
            {
                "_id": "sales-dfw-gatorade-2026-07-03",
                "customer_profile": customer_profile,
                "region_id": "region-texas",
                "retailer": "DFW Priority Retail Accounts",
                "product_id": "prod-gatorade-20oz-fruit-punch",
                "units_sold": 118000,
                "sales_date": "2026-07-03",
                "sell_through_status": "above_forecast",
            },
            {
                "_id": "sales-houston-gatorade-2026-07-03",
                "customer_profile": customer_profile,
                "region_id": "region-texas",
                "retailer": "Houston Priority Retail Accounts",
                "product_id": "prod-gatorade-20oz-lemon-lime",
                "units_sold": 96000,
                "sales_date": "2026-07-03",
                "sell_through_status": "above_forecast",
            },
        ],
        "playbooks": playbooks,
        "historical_incidents": historical_incidents,
        "decision_history": decision_history,
        "graph_nodes": [
            {
                "_id": "node-gatorade-sku",
                "customer_profile": customer_profile,
                "node_id": "node-gatorade-sku",
                "entity_type": "product",
                "node_type": "product",
                "entity_id": "prod-gatorade-20oz-fruit-punch",
                "label": "Gatorade SKU",
                "description": "High-velocity Gatorade SKUs affected by Texas demand lift.",
                "business_context": "Product demand is 38% above baseline in Texas.",
            },
            {
                "_id": "node-houston-plant",
                "customer_profile": customer_profile,
                "node_id": "node-houston-plant",
                "entity_type": "plant",
                "node_type": "plant",
                "entity_id": "plant-dallas-beverage",
                "label": "Houston Plant",
                "description": "Regional beverage production capacity serving Texas demand.",
                "business_context": "Production can be increased to restore downstream supply.",
            },
            {
                "_id": "node-dallas-dc",
                "customer_profile": customer_profile,
                "node_id": "node-dallas-dc",
                "entity_type": "warehouse",
                "node_type": "distribution_center",
                "entity_id": "wh-houston-dc",
                "label": "Dallas DC",
                "description": "Distribution center serving priority Texas retailers.",
                "business_context": (
                    "Inventory is at 2.1 days of supply with elevated stockout risk."
                ),
            },
            {
                "_id": "node-texas-retailers",
                "customer_profile": customer_profile,
                "node_id": "node-texas-retailers",
                "entity_type": "retailer_group",
                "node_type": "retailer_group",
                "entity_id": "retailers-texas-priority",
                "label": "Texas Retailers",
                "description": "Priority retailers experiencing elevated Gatorade sell-through.",
                "business_context": "Retail service levels must be protected during demand surge.",
            },
            {
                "_id": "node-walmart-promotion",
                "customer_profile": customer_profile,
                "node_id": "node-walmart-promotion",
                "entity_type": "promotion",
                "node_type": "promotion",
                "entity_id": "promo-gatorade-texas-summer-retail-2026",
                "label": "Walmart Promotion",
                "description": "Active retail promotion increasing Gatorade sales velocity.",
                "business_context": "Promotion lift is amplifying heatwave-driven demand.",
            },
            {
                "_id": "node-texas-heatwave",
                "customer_profile": customer_profile,
                "node_id": "node-texas-heatwave",
                "entity_type": "weather_event",
                "node_type": "weather",
                "entity_id": "weather-texas-heatwave-2026-07",
                "label": "Texas Heatwave",
                "description": "High-severity heatwave affecting Texas hydration demand.",
                "business_context": "105°F temperatures are increasing sports drink demand.",
            },
            {
                "_id": "node-demand-spike",
                "customer_profile": customer_profile,
                "node_id": "node-demand-spike",
                "entity_type": "demand_signal",
                "node_type": "demand_signal",
                "entity_id": "signal-gatorade-texas-heatwave-2026-07-03",
                "label": "Demand Spike",
                "description": "Detected Texas Gatorade demand increase above baseline.",
                "business_context": (
                    "Demand is up 38%, creating revenue and service-level exposure."
                ),
            },
            {
                "_id": "node-recommended-decision",
                "customer_profile": customer_profile,
                "node_id": "node-recommended-decision",
                "entity_type": "decision",
                "node_type": "recommended_decision",
                "entity_id": "decision-package-gatorade-texas",
                "label": "Recommended Decision",
                "description": "Recommended response to protect service and revenue.",
                "business_context": (
                    "Increase Houston production, reallocate inventory, add trucks, "
                    "and monitor resin supply."
                ),
            },
        ],
        "graph_edges": [
            {
                "_id": "edge-gatorade-produced-houston",
                "customer_profile": customer_profile,
                "from_node_id": "node-gatorade-sku",
                "to_node_id": "node-houston-plant",
                "relationship_type": "PRODUCED_BY",
                "weight": 0.96,
                "business_reason": "Houston Plant produces replenishment supply for Gatorade SKUs.",
                "business_impact": "Production increase can add supply against the Texas spike.",
                "constraints": ["Plant schedule must support a 22% production increase"],
            },
            {
                "_id": "edge-houston-replenishes-dallas",
                "customer_profile": customer_profile,
                "from_node_id": "node-houston-plant",
                "to_node_id": "node-dallas-dc",
                "relationship_type": "REPLENISHES",
                "weight": 0.93,
                "business_reason": "Houston Plant currently replenishes Dallas DC.",
                "business_impact": "Dallas inventory can be restored within 24 hours.",
                "constraints": ["Line capacity", "Packaging material availability"],
            },
            {
                "_id": "edge-dallas-serves-texas-retailers",
                "customer_profile": customer_profile,
                "from_node_id": "node-dallas-dc",
                "to_node_id": "node-texas-retailers",
                "relationship_type": "SERVES",
                "weight": 0.91,
                "business_reason": "Dallas DC serves priority Texas retail accounts.",
                "business_impact": "Low Dallas coverage raises stockout risk for retailers.",
                "constraints": ["Dallas DC inventory is at 2.1 days of supply"],
            },
            {
                "_id": "edge-texas-retailers-walmart-promotion",
                "customer_profile": customer_profile,
                "from_node_id": "node-texas-retailers",
                "to_node_id": "node-walmart-promotion",
                "relationship_type": "PROMOTED_BY",
                "weight": 0.89,
                "business_reason": "Walmart promotion is active across affected Texas stores.",
                "business_impact": (
                    "Promotion lift increases sell-through and replenishment pressure."
                ),
                "constraints": ["Promotion lift may exceed forecast"],
            },
            {
                "_id": "edge-walmart-promotion-texas-heatwave",
                "customer_profile": customer_profile,
                "from_node_id": "node-walmart-promotion",
                "to_node_id": "node-texas-heatwave",
                "relationship_type": "AMPLIFIED_BY",
                "weight": 0.88,
                "business_reason": "Heatwave conditions amplify promotion-driven hydration demand.",
                "business_impact": (
                    "Demand is rising faster than promotion forecast alone would predict."
                ),
                "constraints": ["Heatwave duration may extend demand beyond current plan"],
            },
            {
                "_id": "edge-texas-heatwave-demand-spike",
                "customer_profile": customer_profile,
                "from_node_id": "node-texas-heatwave",
                "to_node_id": "node-demand-spike",
                "relationship_type": "DRIVES",
                "weight": 0.94,
                "business_reason": (
                    "105°F temperatures are driving incremental hydration purchases."
                ),
                "business_impact": "Demand is 38% above baseline with elevated revenue exposure.",
                "constraints": ["Weather severity must be monitored daily"],
            },
            {
                "_id": "edge-demand-spike-recommended-decision",
                "customer_profile": customer_profile,
                "from_node_id": "node-demand-spike",
                "to_node_id": "node-recommended-decision",
                "relationship_type": "REQUIRES_DECISION",
                "weight": 0.97,
                "business_reason": (
                    "Demand spike and inventory risk require governed supply response."
                ),
                "business_impact": (
                    "Recommended action protects $4.2M revenue and 98% service level."
                ),
                "constraints": [
                    "Transportation availability must hold for 5 days",
                    "Supplier resin capacity must remain stable",
                ],
            },
        ],
        "agent_memory": [
            {
                "_id": "memory-gatorade-texas-demo-scope",
                "customer_profile": customer_profile,
                "memory_type": "demo_context",
                "summary": "Sprint 1 operational foundation for the Gatorade Texas scenario.",
                "source": "seed_demo_data.py",
            }
        ],
    }


async def seed() -> None:
    settings = get_settings()
    embedding_service = get_embedding_service(settings)
    await mongodb_manager.connect(settings)

    try:
        database = mongodb_manager.get_database()
        data = demo_data(settings.customer_profile, embedding_service)

        for repository_class in COLLECTION_REPOSITORIES:
            repository = repository_class(database)
            await repository.ensure_collection_exists()
            await repository.upsert_many(data[repository.collection_name])
            count = await repository.count()
            print(f"{repository.collection_name}: {count} documents")
    finally:
        await mongodb_manager.close()


if __name__ == "__main__":
    asyncio.run(seed())
