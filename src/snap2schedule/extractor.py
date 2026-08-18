from datetime import datetime, date, time
from pydantic import BaseModel, Field
from typing import Literal

class ExtractedEvent(BaseModel):
    title: str | None = None
    description: str | None = None
    start_date: date | None = None
    start_time: time | None = None
    start_day_part: Literal["morning", "afternoon", "evening"] | None = None
    end_date: date | None = None
    end_time: time | None = None
    end_day_part: Literal["morning", "afternoon", "evening"] | None = None
    location: str | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)

# Input: raw text
# Ouput: extracted event information
# Rules: relative date, missing exact time, missing optional fields, do not invent information

def extract_event(user_input: str, current_datetime: datetime, timezone: str) -> ExtractedEvent:
    # Use an LLM to extract the event information from the user input
    # Return an ExtractedEvent object with the extracted information, or an empty ExtractedEvent if no event information could be extracted
    # If any information is misssing, the object should contain None for that field
    # return ExtractedEvent()
    pass
    #     "description": None,  
    #     "start_date": None,
    #     "start_time": None,
    #     "start_day_part": None,
    #     "end_date": None,
    #     "end_time": None,
    #     "end_day_part": None,
    #     "location": None,
    #     "confidence": None
    # }
    return ExtractedEvent()

# A. extractor → CalendarEvent trực tiếp hoặc B. extractor → partial extraction → validation → CalendarEvent
# I will choose option B because it allows for more flexibility in handling missing or incomplete information. 
# The extractor can provide a partial extraction of the event details, which can then be validated and completed before creating a CalendarEvent object. 
# This approach ensures that we can handle various user inputs and still produce a valid CalendarEvent.

# TC01 expeted output:
# title = Họp team
# description = review OCR sprint
# start_date = 2026-08-19
# start_time = 14:00:00
# start_day_part = afternoon
# end_date = 2026-08-19
# end_time = 15:00:00
# end_day_part = None
# confidence = 0.95

# TC04 expected output:
# title = Họp với Minh
# description = None
# start_date = 2026-08-19
# start_time = None
# start_day_part = afternoon
# end_date = None
# end_time = None
# end_day_part = None
# location = None
# confidence = 0.80

# TC06 expected output:
# title = Họp
# description = None
# start_date = 2026-08-19
# start_time = 14:00:00
# start_day_part = None
# end_date = 2026-08-19
# end_time = 13:30:00
# end_day_part = None
# location = None
# confidence = 0.70