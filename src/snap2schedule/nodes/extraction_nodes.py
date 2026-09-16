from ..schema import ExtractedEvent, ValidationResult
from ..state import CalendarState
from ..extractor import extract_event
from ..validator import validate_extracted_event
from ..clarification import build_clarification
from langgraph.types import interrupt
from ..trace import print_trace

def extract_event_node(
    state: CalendarState,
) -> dict[str, ExtractedEvent]:
    """
    Extract an event from user input and return a partial state update.
    """
    extracted_event = extract_event(state["user_input"])

    result = {
        "extracted_event": extracted_event,
    }

    print_trace(
        "extract_event_node",
        {
            **state,
            **result,
        },
    )

    return result


def validate_event_node(
    state: CalendarState,
) -> dict[str, ValidationResult]:

    if "extracted_event" not in state:
        raise ValueError(
            "extracted_event is required before validation"
        )

    validation_result = validate_extracted_event(state["extracted_event"])

    result = {
        "validation_result": validation_result,
    }

    print_trace(
        "validate_event_node",
        {
            **state,
            **result,
        },
    )

    return result

def clarification_node(
    state: CalendarState,
) -> dict[str, str]:

    if "extracted_event" not in state:
        raise ValueError(
            "extracted_event is required before clarification"
        )

    if "validation_result" not in state:
        raise ValueError(
            "validation_result is required before clarification"
        )

    clarification_question = build_clarification(
        state["extracted_event"],
        state["validation_result"],
    )

    if clarification_question is None:
        raise ValueError(
            "clarification_question is required before clarification"
        )

    print_trace(
        "clarification_node",
        {
            **state,
            "clarification_message": clarification_question,
        },
    )

    user_response = interrupt(clarification_question)

    if not isinstance(user_response, str) or not user_response.strip():
        raise ValueError(
            "user_response must be a non-empty string"
        )

    updated_user_input = (
        state["user_input"]
        + "\nThông tin bổ sung từ user: "
        + user_response.strip()
    )

    return {
        "clarification_message": clarification_question,
        "user_input": updated_user_input,
    }
