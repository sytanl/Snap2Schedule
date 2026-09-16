import sys
sys.path.append(".")

from src.snap2schedule.calendar.auth import get_calendar_service


service = get_calendar_service()

print("Google Calendar service created successfully")
print(type(service))