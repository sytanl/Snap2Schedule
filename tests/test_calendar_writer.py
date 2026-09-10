from datetime import datetime
from zoneinfo import ZoneInfo
import sys
sys.path.append(".")

from src.snap2schedule.calendar.calendar_writer import create_event


tz = ZoneInfo("Asia/Ho_Chi_Minh")

event_id = create_event(
    title="Test Snap2Schedule Create",
    start=datetime(2026, 9, 10, 14, 0, tzinfo=tz),
    end=datetime(2026, 9, 10, 15, 0, tzinfo=tz),
    description="Test create_event()",
    location="B201",
)

print("Created event:", event_id)