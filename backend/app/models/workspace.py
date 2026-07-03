from pydantic import BaseModel, ConfigDict


class DashboardAlert(BaseModel):
    title: str
    demand_change: str
    revenue_at_risk: str
    priority: str
    package_url: str


class DashboardMetric(BaseModel):
    label: str
    value: str
    status: str
    detail: str


class RecentDecision(BaseModel):
    decision_id: str
    title: str
    status: str
    owner: str
    impact: str
    updated: str


class DashboardResponse(BaseModel):
    question: str
    alert: DashboardAlert
    metrics: list[DashboardMetric]
    recent_decisions: list[RecentDecision]


class DecisionPackageSection(BaseModel):
    title: str
    items: list[str]


class DecisionPackageMetric(BaseModel):
    label: str
    value: str
    detail: str


class EvidenceCard(BaseModel):
    title: str
    detail: str


class DecisionPackageResponse(BaseModel):
    package_id: str
    title: str
    business_question: str
    current_situation_chain: list[str]
    current_situation: list[str]
    operational_context: list[DecisionPackageSection]
    enterprise_knowledge: list[DecisionPackageSection]
    evidence_cards: list[EvidenceCard]
    relationship_intelligence: list[DecisionPackageSection]
    relationship_path: list[str]
    recommended_decision: list[str]
    business_impact: list[DecisionPackageMetric]
    confidence: str
    risks: list[str]
    approval_actions: list[str]
    enterprise_memory: list[str]

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "package_id": "gatorade-texas",
                    "title": "Texas Gatorade Demand Spike",
                    "business_question": (
                        "Why is Gatorade demand increasing in Texas and what should we do?"
                    ),
                    "confidence": "92%",
                }
            ]
        }
    )
