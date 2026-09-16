import sys
sys.path.append(".")

from src.snap2schedule.clarification import build_clarification
from src.snap2schedule.schema import ExtractedEvent, ValidationResult

event = ExtractedEvent(
    title=None,
    description=None,
    start_date=None,
    start_time=None,
    start_day_part=None,
    end_date=None,
    end_time=None,
    end_day_part=None,
    location=None,
    confidence=None,
)

# T01: Test case for missing fields
result = ValidationResult(
    status="needs_clarification",
    errors=[],
    missing_fields=["title", "start_date", "start_time"],
)

print("T01: ", build_clarification(event, result))

# T02: Test case for invalid time format
result = ValidationResult(
    status="invalid",
    errors=["INVALID_TIME_FORMAT"],
    missing_fields=[],
)

print("T02: ", build_clarification(event, result))

# T03: Test case for invalid datetime order
result = ValidationResult(
    status="invalid",
    errors=["INVALID_DATETIME_ORDER"],
    missing_fields=[],
)

print("T03: ", build_clarification(event, result))

# T04: Test case for valid
result = ValidationResult(  
    status="valid",
    errors=[],
    missing_fields=[],
)

print("T04: ",build_clarification(event, result))

# T05: Test case for end date before start date
result = ValidationResult(
    status="invalid",
    errors=["END_DATE_BEFORE_START_DATE"],
    missing_fields=[],
)

print("T05: ", build_clarification(event, result))