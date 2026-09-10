from datetime import datetime
from zoneinfo import ZoneInfo
import sys
sys.path.append(".")

from src.snap2schedule.calendar.calendar_reader import get_events


tz = ZoneInfo("Asia/Ho_Chi_Minh")

events = get_events(
    datetime(2026, 9, 1, 0, 0, tzinfo=tz),
    datetime(2026, 9, 30, 23, 59, tzinfo=tz),
)

for event in events:
    print(event)