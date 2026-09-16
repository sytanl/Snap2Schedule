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
