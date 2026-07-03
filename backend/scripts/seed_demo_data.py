import asyncio
from collections.abc import Mapping

from app.core.config import get_settings
from app.db.mongodb import MongoDocument, mongodb_manager
from app.repositories import COLLECTION_REPOSITORIES


def demo_data(customer_profile: str) -> Mapping[str, list[MongoDocument]]:
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
        "playbooks": [
            {
                "_id": "playbook-heatwave-beverage-demand-response",
                "customer_profile": customer_profile,
                "title": "Heatwave Beverage Demand Response",
                "scenario_type": "weather_driven_demand_spike",
                "recommended_actions": [
                    "Protect priority retail accounts",
                    "Review regional days of supply daily",
                    "Reallocate inventory from lower-risk adjacent nodes",
                    "Escalate production review if demand persists beyond 7 days",
                ],
                "approval_requirements": ["Supply Chain VP"],
                "content": "Synthetic playbook for heatwave-driven hydration category demand.",
            }
        ],
        "historical_incidents": [
            {
                "_id": "incident-southwest-heatwave-sports-drink-2025",
                "customer_profile": customer_profile,
                "title": "Southwest Sports Drink Demand Surge - 2025",
                "summary": "Heatwave and retail display activity lifted sports drink velocity.",
                "products": ["Gatorade"],
                "regions": ["Texas", "Arizona", "New Mexico"],
                "drivers": ["heatwave", "promotion", "school_sports"],
                "actions_taken": ["inventory_reallocation", "daily_sell_through_monitoring"],
                "outcome": "Service levels stabilized within 72 hours.",
                "lessons_learned": (
                    "Adjacent DC transfers should begin before supply drops below 4 days."
                ),
            }
        ],
        "decision_history": [
            {
                "_id": "decision-gatorade-texas-precedent-2025",
                "customer_profile": customer_profile,
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
            }
        ],
        "graph_nodes": [
            {
                "_id": "node-prod-gatorade-fruit-punch",
                "customer_profile": customer_profile,
                "entity_type": "product",
                "entity_id": "prod-gatorade-20oz-fruit-punch",
                "label": "Gatorade Fruit Punch 20 oz",
            },
            {
                "_id": "node-wh-houston-dc",
                "customer_profile": customer_profile,
                "entity_type": "warehouse",
                "entity_id": "wh-houston-dc",
                "label": "Houston Distribution Center",
            },
            {
                "_id": "node-region-texas",
                "customer_profile": customer_profile,
                "entity_type": "region",
                "entity_id": "region-texas",
                "label": "Texas",
            },
        ],
        "graph_edges": [
            {
                "_id": "edge-gatorade-stocked-houston",
                "customer_profile": customer_profile,
                "from_node_id": "node-prod-gatorade-fruit-punch",
                "to_node_id": "node-wh-houston-dc",
                "relationship_type": "STOCKED_AT",
                "weight": 0.92,
            },
            {
                "_id": "edge-houston-serves-texas",
                "customer_profile": customer_profile,
                "from_node_id": "node-wh-houston-dc",
                "to_node_id": "node-region-texas",
                "relationship_type": "SERVES_REGION",
                "weight": 0.87,
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
    await mongodb_manager.connect(settings)

    try:
        database = mongodb_manager.get_database()
        data = demo_data(settings.customer_profile)

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
