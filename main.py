from src.snap2schedule.config import MODEL
from src.snap2schedule.llm_client import client
from src.snap2schedule.prompts.event_extraction import EXTRACTION_SYSTEM_PROMPT
from src.snap2schedule.schema import ExtractedEvent
from datetime import datetime, timezone


USER_INPUT = "Mai 2h chiều họp team ở B201 khoảng 1 tiếng, review OCR sprint."

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": EXTRACTION_SYSTEM_PROMPT.format(
                current_datetime=datetime.now(timezone.utc).isoformat(),
                timezone="Asia/Ho_Chi_Minh",
            ),
        },
        {
            "role": "user",
            "content": USER_INPUT
        }
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

print(content)
print(type(content))

event = ExtractedEvent.model_validate_json(content)
print(event)
print(event.title)
print(event.start_date)
print(event.start_time)