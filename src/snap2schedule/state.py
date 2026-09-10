from typing import TypedDict, NotRequired
from .schema import ExtractedEvent, ValidationResult

class CalendarState(TypedDict):
    # Workflow state of the whole LangGraph
    user_input: str
    raw_text: NotRequired[str]
    ocr_confidence: NotRequired[float]
    ocr_engine: NotRequired[str]
    extracted_event: NotRequired[ExtractedEvent]
    validation_result: NotRequired[ValidationResult]
    clarification_message: NotRequired[str]
    preview_message: NotRequired[str]
    approval: NotRequired[bool]
    conflict: NotRequired[bool]
    conflict_message: NotRequired[str]
    create_anyway: NotRequired[bool]
    event_id: NotRequired[str]