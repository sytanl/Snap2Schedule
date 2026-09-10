from .schema import ExtractedEvent, ValidationResult
from .state import CalendarState
from .extractor import extract_event
from .validator import validate_extracted_event
from .clarification import build_clarification
from langgraph.types import interrupt
from .calendar.calendar_writer import create_event
from .trace import print_trace
from .calendar.conflict_checker import check_conflict
from .calendar.calendar_reader import get_events
from datetime import datetime
from zoneinfo import ZoneInfo

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
    
def preview_event_node(
    state: CalendarState,
) -> dict[str, str | bool]:

    event = state["extracted_event"]

    message = (
        "Xác nhận tạo sự kiện\n\n"
        f"Tiêu đề: {event.title}\n"
        f"Ngày: {event.start_date}\n"
        f"Thời gian: {event.start_time} - {event.end_time}\n"
        f"Địa điểm: {event.location}\n\n"
        "Bạn có muốn tạo sự kiện này vào Google Calendar không?"
    )

    user_response = interrupt(message)

    approved = user_response.strip().lower() in {
        "yes",
        "y",
        "có",
        "ok",
        "đồng ý",
    }

    return {
        "preview_message": message,
        "approval": approved,
    }

def create_event_node(
    state: CalendarState,
) -> dict[str, str]:

    event = state["extracted_event"]

    if (
        event.start_date is None
        or event.start_time is None
        or event.end_date is None
        or event.end_time is None
    ):
        raise ValueError(
            "Event must have start and end date/time before creation"
        )

    tz = ZoneInfo("Asia/Ho_Chi_Minh")
    start = datetime.combine(
        event.start_date,
        datetime.strptime(event.start_time, "%H:%M").time(),
        tzinfo=tz,
    )

    end = datetime.combine(
        event.end_date,
        datetime.strptime(event.end_time, "%H:%M").time(),
        tzinfo=tz,
    )

    event_id = create_event(
        title=event.title,
        start=start,
        end=end,
        description=event.description,
        location=event.location,
    )

    result = {
        "event_id": event_id,
    }

    print_trace(
        "create_event_node",
        {
            **state,
            **result,
        },
    )

    return result

def check_conflict_node(
    state: CalendarState,
) -> dict[str, bool]:
    event = state["extracted_event"]
    tz = ZoneInfo("Asia/Ho_Chi_Minh")
    start = datetime.combine(
        event.start_date,
        datetime.strptime(event.start_time, "%H:%M").time(),
        tzinfo=tz,
    )
    end = datetime.combine(
        event.end_date,
        datetime.strptime(event.end_time, "%H:%M").time(),
        tzinfo=tz,
    )

    existing_events = get_events(start, end)

    conflict = check_conflict(start, end, existing_events)
    
    result = {"conflict": conflict}

    print_trace(
        "check_conflict_node",
        {
            **state,
            **result,
        },
    )

    return result

def conflict_warning_node(
    state: CalendarState,
) -> dict[str, bool]:

    response = interrupt(
        "Lịch này đang bị trùng với một sự kiện hiện có. "
        "Bạn có muốn tạo sự kiện này anyway không?"
    )

    create_anyway = (
        response.strip().lower()
        in {"có", "yes", "y", "ok"}
    )

    return {
        "create_anyway": create_anyway,
    }