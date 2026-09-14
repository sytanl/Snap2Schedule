from ..schema import ExtractedEvent
from ..state import CalendarState
from ..trace import print_trace
from langgraph.types import interrupt
from ..calendar.conflict_checker import has_conflict
from ..calendar.calendar_writer import create_event_in_gcal
from datetime import datetime, timezone
import json

def preview_event_node(
    state: CalendarState,
) -> dict[str, bool]:

    if "extracted_event" not in state:
        raise ValueError(
            "extracted_event is required before previewing"
        )
    extracted_event = state["extracted_event"]
    preview_message = (
        "Xác nhận tạo sự kiện sau?\n"
        f"Tiêu đề: {extracted_event.title}\n"
        f"Mô tả: {extracted_event.description}\n"
        f"Bắt đầu: {extracted_event.start_date} {extracted_event.start_time}\n"
        f"Kết thúc: {extracted_event.end_date} {extracted_event.end_time}\n"
        f"Địa điểm: {extracted_event.location}"
    )

    print_trace(
        "preview_event_node",
        {
            **state,
        },
    )

    user_response = interrupt(preview_message)

    if not isinstance(user_response, str) or not user_response.strip():
        raise ValueError(
            "user_response must be a non-empty string"
        )

    if user_response.strip().lower() in ["yes", "có", "y", "ok", "được"]:
        return {"approval": True}
    return {"approval": False}

def create_event_node(
    state: CalendarState,
) -> dict:

    if "extracted_event" not in state:
        raise ValueError(
            "extracted_event is required before creating"
        )
    extracted_event = state["extracted_event"]

    print_trace(
        "create_event_node",
        {
            **state,
        },
    )

    try:
        event_id = create_event_in_gcal(extracted_event)
        
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
    except Exception as e:
        print_trace(
            "create_event_node",
            {
                **state,
            },
        )
        # Note: If it fails, graph runner catches CalendarServiceError
        from ..errors import CalendarServiceError
        raise CalendarServiceError(f"Failed to create event: {e}")

def check_conflict_node(
    state: CalendarState,
) -> dict[str, bool]:
    
    if "extracted_event" not in state:
        raise ValueError(
            "extracted_event is required before checking for conflicts"
        )
    extracted_event = state["extracted_event"]
    
    conflict = has_conflict(extracted_event)
    
    result = {
        "conflict": conflict,
    }
    
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
    
    conflict_message = (
        "Trùng lịch! Bạn có muốn tạo sự kiện này anyway không?\n"
    )
    
    print_trace(
        "conflict_warning_node",
        {
            **state,
        },
    )
    
    user_response = interrupt(conflict_message)
    
    if not isinstance(user_response, str) or not user_response.strip():
        raise ValueError(
            "user_response must be a non-empty string"
        )
    
    if user_response.strip().lower() in ["yes", "có", "y", "ok", "được", "anyway"]:
        return {"approval": True}
    return {"approval": False}
