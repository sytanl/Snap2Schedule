from pydantic import BaseModel, Field
from datetime import datetime

class CalendarEvent(BaseModel):
    title: str
    description: str | None = None
    start_datetime: datetime
    end_datetime: datetime | None = None
    location: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)

calendar_event = CalendarEvent(
    title="Team Meeting",
    description="Discuss project updates and next steps.",
    start_datetime="2026-08-20T14:00:00+07:00",
    location="Conference Room",
    confidence=0.1
)


print(calendar_event.model_dump())