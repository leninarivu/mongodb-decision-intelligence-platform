from typing import Literal

from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    service: Literal["ok", "degraded"]
    database: Literal["ok", "unavailable"]

    model_config = ConfigDict(json_schema_extra={"examples": [{"service": "ok", "database": "ok"}]})
