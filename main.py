# from src.snap2schedule.extractor import extract_event

# USER_INPUT = "Mai 14h họp, kết thúc 13h30."

# event = extract_event(USER_INPUT)
# print(event)
from datetime import datetime
from zoneinfo import ZoneInfo

from src.snap2schedule.extractor import extract_event
from src.snap2schedule.time_context import TimeContext
from src.snap2schedule.validator import validate_extracted_event


fixed = datetime(
    2026,
    8,
    20,
    10,
    0,
    tzinfo=ZoneInfo("Asia/Ho_Chi_Minh"),
)

ctx = TimeContext(fixed_datetime=fixed)

event = extract_event(
    "Tomorrow at 12 PM review the demo.",
    time_context=ctx,
)

validation_result = validate_extracted_event(event)

print(event)
print(validation_result)