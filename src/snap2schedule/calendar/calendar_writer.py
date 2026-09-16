from datetime import datetime

from .auth import get_calendar_service


def create_event(
    title: str,
    start: datetime,
    end: datetime,
    description: str | None = None,
    location: str | None = None,
) -> str:
    service = get_calendar_service()

    event_body = {
        "summary": title,
        "start": {
            "dateTime": start.isoformat(),
        },
        "end": {
            "dateTime": end.isoformat(),
        },
    }

    if description is not None:
        event_body["description"] = description

    if location is not None:
        event_body["location"] = location

    created_event = service.events().insert(
        calendarId="primary",
        body=event_body,
    ).execute()

    return created_event["id"]