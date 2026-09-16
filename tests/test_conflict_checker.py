from datetime import datetime
from zoneinfo import ZoneInfo
import sys
sys.path.append(".")

from src.snap2schedule.schema import CalendarEventSummary
from src.snap2schedule.calendar.conflict_checker import check_conflict


tz = ZoneInfo("Asia/Ho_Chi_Minh")


existing = [
    CalendarEventSummary(
        id="1",
        title="Existing meeting",
        start="2026-09-10T14:00:00+07:00",
        end="2026-09-10T15:00:00+07:00",
    )
]


# T01: Overlap a part → True
result = check_conflict(
    datetime(2026, 9, 10, 14, 30, tzinfo=tz),
    datetime(2026, 9, 10, 15, 30, tzinfo=tz),
    existing,
)
print("T01:", result)


# T02: No overlap → False
result = check_conflict(
    datetime(2026, 9, 10, 15, 0, tzinfo=tz),
    datetime(2026, 9, 10, 16, 0, tzinfo=tz),
    existing,
)
print("T02:", result)


# T03: Reach boundary → False
result = check_conflict(
    datetime(2026, 9, 10, 15, 0, tzinfo=tz),
    datetime(2026, 9, 10, 15, 30, tzinfo=tz),
    existing,
)
print("T03:", result)


# T04: Completely inside old event → True
result = check_conflict(
    datetime(2026, 9, 10, 14, 15, tzinfo=tz),
    datetime(2026, 9, 10, 14, 45, tzinfo=tz),
    existing,
)
print("T04:", result)