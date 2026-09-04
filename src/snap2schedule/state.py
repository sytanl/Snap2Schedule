from typing import TypedDict, NotRequired
from .schema import ExtractedEvent, ValidationResult

class CalendarState(TypedDict):
    # Workflow state of the whole LangGraph
    user_input: str
    extracted_event: NotRequired[ExtractedEvent]
    validation_result: NotRequired[ValidationResult]
    clarification_message: NotRequired[str]