import logging

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.mongodb import MongoDocument, mongodb_manager
from app.models.workspace import (
    DashboardAlert,
    DashboardMetric,
    DashboardResponse,
    DecisionPackageMetric,
    DecisionPackageResponse,
    DecisionPackageSection,
    EvidenceCard,
    RecentDecision,
)

logger = logging.getLogger(__name__)


class WorkspaceService:
    async def get_dashboard(self) -> DashboardResponse:
        counts = await self._collection_counts()
        recent_decisions = await self.get_recent_decisions()

        return DashboardResponse(
            question="What needs my attention today?",
            alert=DashboardAlert(
                title="Texas Gatorade Demand Spike",
                demand_change="+38%",
                revenue_at_risk="$4.2M",
                priority="High",
                package_url="/decision-package/gatorade-texas",
            ),
            metrics=[
                DashboardMetric(
                    label="Demand Signal",
                    value="+38%",
                    status="Attention",
                    detail="Texas Gatorade velocity is concentrated in Dallas and Houston.",
                ),
                DashboardMetric(
                    label="Weather Event",
                    value=str(max(counts.get("weather_events", 0), 1)),
                    status="105°F heatwave",
                    detail="High temperatures are increasing hydration demand.",
                ),
                DashboardMetric(
                    label="Promotion",
                    value=str(max(counts.get("promotions", 0), 1)),
                    status="Walmart lift",
                    detail="Retail promotion is increasing store-level movement.",
                ),
                DashboardMetric(
                    label="Inventory Risk",
                    value="2.1 days",
                    status="Dallas DC",
                    detail="Coverage is below target during the promotion window.",
                ),
                DashboardMetric(
                    label="Logistics Capacity",
                    value="18 trucks",
                    status="Needed",
                    detail="Additional capacity protects priority retail service levels.",
                ),
            ],
            recent_decisions=recent_decisions,
        )

    async def get_recent_decisions(self) -> list[RecentDecision]:
        database = self._database_or_none()
        if database is None:
            return self._fallback_recent_decisions()

        try:
            cursor = database["decision_history"].find({}).limit(5)
            documents = await cursor.to_list(length=5)
        except Exception:
            logger.debug("Falling back to deterministic recent decisions", exc_info=True)
            return self._fallback_recent_decisions()

        if not documents:
            return self._fallback_recent_decisions()

        decisions: list[RecentDecision] = [
            RecentDecision(
                decision_id=str(document.get("_id", "decision-unknown")),
                title=str(document.get("business_question", "Prior decision")),
                status=str(document.get("approval_status", "approved")).title(),
                owner=str(document.get("approver", "Supply Chain VP")),
                impact=self._decision_impact(document),
                updated="Stored in enterprise memory",
            )
            for document in documents
        ]
        return decisions

    async def get_decision_package(self, package_id: str) -> DecisionPackageResponse:
        if package_id != "gatorade-texas":
            return self._gatorade_texas_package(seed_status="deterministic scenario")

        seed_status = await self._seed_status()
        return self._gatorade_texas_package(seed_status=seed_status)

    def _database_or_none(self) -> AsyncIOMotorDatabase[MongoDocument] | None:
        try:
            return mongodb_manager.get_database()
        except RuntimeError:
            return None

    async def _collection_counts(self) -> dict[str, int]:
        database = self._database_or_none()
        if database is None:
            return {}

        counts: dict[str, int] = {}
        for collection_name in (
            "demand_signals",
            "weather_events",
            "promotions",
            "decision_history",
        ):
            try:
                counts[collection_name] = await database[collection_name].count_documents({})
            except Exception:
                logger.debug("Unable to count %s", collection_name, exc_info=True)
        return counts

    async def _seed_status(self) -> str:
        database = self._database_or_none()
        if database is None:
            return "deterministic scenario"

        required_ids = {
            "demand_signals": "signal-gatorade-texas-heatwave-2026-07-03",
            "weather_events": "weather-texas-heatwave-2026-07",
            "promotions": "promo-gatorade-texas-summer-retail-2026",
            "playbooks": "playbook-heatwave-beverage-demand-response",
            "historical_incidents": "incident-southwest-heatwave-sports-drink-2025",
        }

        available = 0
        for collection_name, document_id in required_ids.items():
            try:
                document = await database[collection_name].find_one({"_id": document_id})
            except Exception:
                logger.debug("Unable to read %s", collection_name, exc_info=True)
                continue
            if document is not None:
                available += 1

        if available == len(required_ids):
            return "seeded MongoDB scenario"
        return "deterministic scenario with seeded-data fallback"

    def _decision_impact(self, document: MongoDocument) -> str:
        business_impact = document.get("business_impact")
        if isinstance(business_impact, dict):
            protected = business_impact.get("revenue_protected_usd")
            if isinstance(protected, int | float):
                return f"${protected / 1_000_000:.1f}M revenue protected"
        return "Decision memory available"

    def _fallback_recent_decisions(self) -> list[RecentDecision]:
        return [
            RecentDecision(
                decision_id="decision-gatorade-texas-precedent-2025",
                title="Prior heatwave demand response",
                status="Approved",
                owner="Supply Chain VP",
                impact="$1.2M revenue protected",
                updated="Stored in enterprise memory",
            ),
            RecentDecision(
                decision_id="decision-inventory-rebalance-south-central",
                title="South Central inventory rebalancing",
                status="Completed",
                owner="Logistics Manager",
                impact="Service level stabilized",
                updated="Reusable operating precedent",
            ),
            RecentDecision(
                decision_id="decision-supplier-capacity-watch",
                title="Supplier capacity watch initiated",
                status="Monitoring",
                owner="Procurement Manager",
                impact="Supply risk reduced",
                updated="Active memory item",
            ),
        ]

    def _gatorade_texas_package(self, seed_status: str) -> DecisionPackageResponse:
        return DecisionPackageResponse(
            package_id="gatorade-texas",
            title="Texas Gatorade Demand Spike",
            business_question="Why is Gatorade demand increasing in Texas and what should we do?",
            current_situation_chain=[
                "Texas Heatwave 105°F",
                "Demand +38%",
                "Walmart Promotion Active",
                "Dallas DC Inventory 2.1 days",
                "Stockout risk elevated",
            ],
            current_situation=[
                (
                    "Gatorade demand in Texas is materially above baseline during a "
                    "high-severity heatwave."
                ),
                "Retail promotion activity is amplifying demand across priority accounts.",
                "Houston inventory coverage is below target and requires coordinated response.",
                f"Decision package generated from {seed_status}.",
            ],
            operational_context=[
                DecisionPackageSection(
                    title="Demand",
                    items=[
                        "Texas Gatorade demand is up 38% versus baseline.",
                        "Demand concentration is highest in Dallas-Fort Worth and Houston.",
                    ],
                ),
                DecisionPackageSection(
                    title="Inventory",
                    items=[
                        "Houston DC coverage is below target for the promotion window.",
                        "Oklahoma City DC has available inventory for controlled reallocation.",
                    ],
                ),
                DecisionPackageSection(
                    title="Market Conditions",
                    items=[
                        "Heatwave conditions are increasing hydration demand.",
                        "Active retail promotion is increasing store-level velocity.",
                    ],
                ),
            ],
            enterprise_knowledge=[
                DecisionPackageSection(
                    title="Playbook",
                    items=[
                        (
                            "Heatwave beverage response guidance recommends protecting "
                            "priority accounts."
                        ),
                        "Daily sell-through monitoring is required while demand remains elevated.",
                    ],
                ),
                DecisionPackageSection(
                    title="Historical Incident",
                    items=[
                        (
                            "A prior Southwest sports drink surge stabilized after "
                            "inventory reallocation."
                        ),
                        (
                            "Previous learning: transfers should begin before coverage "
                            "drops below four days."
                        ),
                    ],
                ),
            ],
            evidence_cards=[
                EvidenceCard(
                    title="Heatwave Response Playbook",
                    detail="Protect priority retail accounts and review regional coverage daily.",
                ),
                EvidenceCard(
                    title="2025 Texas Beverage Demand Spike Incident",
                    detail="Prior demand surge stabilized after controlled inventory reallocation.",
                ),
                EvidenceCard(
                    title="Retail Promotion Replenishment Policy",
                    detail=(
                        "Promotion-driven stock risk requires supply chain approval "
                        "and monitoring."
                    ),
                ),
            ],
            relationship_intelligence=[
                DecisionPackageSection(
                    title="Supply Chain Dependencies",
                    items=[
                        "Dallas and Houston distribution centers serve the affected Texas market.",
                        (
                            "Tulsa production and Oklahoma City inventory can support "
                            "regional balancing."
                        ),
                    ],
                ),
                DecisionPackageSection(
                    title="Supplier And Logistics Exposure",
                    items=[
                        (
                            "PET resin supply should be monitored daily during the "
                            "production increase."
                        ),
                        "Additional truck capacity is required to protect service levels.",
                    ],
                ),
            ],
            relationship_path=[
                "Gatorade SKUs",
                "Houston Plant",
                "Dallas DC",
                "Texas Retailers",
                "Walmart Promotion",
                "Texas Heatwave",
            ],
            recommended_decision=[
                "Increase Houston production by 22%",
                "Reallocate inventory from Oklahoma City DC to Dallas DC",
                "Allocate 18 additional trucks",
                "Monitor resin supplier capacity daily",
            ],
            business_impact=[
                DecisionPackageMetric(
                    label="Estimated revenue protected",
                    value="$4.2M",
                    detail="Protects priority retail availability during the promotion window.",
                ),
                DecisionPackageMetric(
                    label="Expected service level",
                    value="98%",
                    detail="Maintains target service for affected Texas accounts.",
                ),
                DecisionPackageMetric(
                    label="Stockout risk reduction",
                    value="High",
                    detail="Reduces exposure in Dallas-Fort Worth and Houston.",
                ),
                DecisionPackageMetric(
                    label="Confidence",
                    value="92%",
                    detail="Based on operational signals and seeded enterprise context.",
                ),
            ],
            confidence="92%",
            risks=[
                "Supplier resin capacity must remain stable",
                "Transportation availability must hold for 5 days",
                "Promotion lift may exceed forecast",
            ],
            approval_actions=[
                "Approve",
                "Modify",
                "Reject",
            ],
            enterprise_memory=[
                "Prior heatwave demand response",
                "South Central inventory rebalancing",
                "Supplier capacity watch initiated",
            ],
        )


workspace_service = WorkspaceService()
