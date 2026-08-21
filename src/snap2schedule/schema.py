from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date
from typing import Literal

class CalendarEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: str | None = None
    start_datetime: datetime
    end_datetime: datetime | None = None
    location: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)

class ExtractedEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None
    description: str | None
    start_date: date | None
    start_time: str | None
    start_day_part: Literal["morning", "afternoon", "evening"] | None
    end_date: date | None
    end_time: str | None
    end_day_part: Literal["morning", "afternoon", "evening"] | None
    location: str | None
    confidence: float | None = Field(ge=0.0, le=1.0)

class ValidationResult(BaseModel):
    status: Literal[
        "valid",
        "needs_clarification",
        "invalid",
    ]
    errors: list[str] = []
    missing_fields: list[str] = []
