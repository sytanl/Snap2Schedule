from datetime import datetime

from .auth import get_calendar_service
from ..schema import CalendarEventSummary


def get_events(
    start: datetime,
    end: datetime,
) -> list[CalendarEventSummary]:

    service = get_calendar_service()

    events_result = service.events().list(
        calendarId='primary',
        timeMin=start.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True,
        orderBy="startTime",
        maxResults=100,
    ).execute()

    events = []
    for event in events_result.get("items", []):
        event_start = event["start"].get("dateTime")
        event_end = event["end"].get("dateTime")

        if event_start is None or event_end is None:
            continue

        events.append(
            CalendarEventSummary(
                id=event["id"],
                title=event.get("summary", "(No title)"),
                start=event_start,
                end=event_end,
            )
        )

    return events
