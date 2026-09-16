from datetime import datetime

from ..schema import CalendarEventSummary


def check_conflict(
    start: datetime,
    end: datetime,
    existing_events: list[CalendarEventSummary],
) -> bool:
    for event in existing_events:
        event_start = datetime.fromisoformat(event.start)
        event_end = datetime.fromisoformat(event.end)

        if max(start, event_start) < min(end, event_end):
            return True

    return False