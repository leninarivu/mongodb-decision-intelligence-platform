from pydantic import BaseModel, ConfigDict


class KnowledgeSearchResult(BaseModel):
    title: str
    summary: str
    source_system: str
    similarity_score: float
    reason_retrieved: str


class KnowledgeSearchResponse(BaseModel):
    query: str
    configured: bool
    message: str | None = None
    setup_documentation: str = "docs/08-Atlas-Vector-Search-Setup.md"
    results: list[KnowledgeSearchResult]

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "query": "Why is Gatorade demand increasing in Texas?",
                    "configured": True,
                    "results": [
                        {
                            "title": "Heatwave Response Playbook",
                            "summary": (
                                "Protect priority retail accounts during heatwave demand spikes."
                            ),
                            "source_system": "MDIP Playbook Library",
                            "similarity_score": 0.92,
                            "reason_retrieved": (
                                "Matched heatwave, Gatorade, Texas, and demand spike context."
                            ),
                        }
                    ],
                }
            ]
        }
    )
