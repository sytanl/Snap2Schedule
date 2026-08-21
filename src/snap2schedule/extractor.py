from datetime import datetime
from .schema import ExtractedEvent
from .llm_client import client
from .prompts.event_extraction import EXTRACTION_SYSTEM_PROMPT
from .config import MODEL
from .time_context import TimeContext

def extract_event(user_input: str, time_context: TimeContext | None = None) -> ExtractedEvent:
    if not user_input.strip():
        raise ValueError("user_input must not be empty")

    if time_context is None:
        time_context = TimeContext()

    system_prompt = EXTRACTION_SYSTEM_PROMPT.format(
        current_datetime=time_context.now.isoformat(),
        timezone=time_context.timezone_name,
        current_weekday=time_context.weekday_name
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_input,
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "ExtractedEvent",
                "strict": True,
                "schema": ExtractedEvent.model_json_schema(),
            },
        },
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError("Groq returned an empty response")

    return ExtractedEvent.model_validate_json(content)

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