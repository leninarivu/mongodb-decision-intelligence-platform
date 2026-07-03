from typing import Literal

from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    status: Literal["healthy"]
    mongodb: Literal["connected"]
    database: str
    customer: str

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "status": "healthy",
                    "mongodb": "connected",
                    "database": "mdip_demo",
                    "customer": "PepsiCo",
                }
            ]
        }
    )
