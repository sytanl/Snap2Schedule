import streamlit as st
from langgraph.types import Command
from .graph import graph
from .errors import OCRServiceError, CalendarServiceError
from .logging_config import get_logger
from .ui_helpers import detect_interrupt_type

logger = get_logger("snap2schedule.graph_runner")

def _config() -> dict:
    return {"configurable": {"thread_id": st.session_state.thread_id}}

def handle_result(result: dict) -> None:
    """Update session state from a graph.invoke() result."""
    st.session_state.graph_result = result

    interrupts = result.get("__interrupt__", [])
    if interrupts:
        msg = interrupts[0].value
        st.session_state.interrupt_value = msg
        st.session_state.interrupt_type = detect_interrupt_type(msg)
        st.session_state.stage = "interrupted"
    else:
        st.session_state.interrupt_value = None
        st.session_state.interrupt_type = None
        st.session_state.stage = "done"

def invoke_initial(user_input: str, image_path: str | None = None) -> None:
    """Start a fresh graph invocation."""
    initial_state: dict = {
        "user_input": user_input,
    }
    if image_path:
        initial_state["image_path"] = image_path

    try:
        result = graph.invoke(initial_state, config=_config())
        handle_result(result)
    except OCRServiceError as exc:
        logger.exception("OCR service error")
        st.session_state.stage = "error"
        st.session_state.error_msg = (
            "Couldn't read this image. Try a clearer screenshot."
        )
    except CalendarServiceError as exc:
        logger.exception("Calendar service error")
        st.session_state.stage = "error"
        st.session_state.error_msg = (
            "Google Calendar is temporarily unavailable. Please try again."
        )
    except Exception as exc:
        logger.exception("Unexpected error during graph invocation")
        st.session_state.stage = "error"
        st.session_state.error_msg = (
            "Something went wrong while processing this event."
        )

def invoke_resume(response: str) -> None:
    """Resume graph from an interrupt checkpoint."""
    try:
        result = graph.invoke(Command(resume=response), config=_config())
        handle_result(result)
    except CalendarServiceError:
        logger.exception("Calendar service error on resume")
        st.session_state.stage = "error"
        st.session_state.error_msg = (
            "Google Calendar is temporarily unavailable. Please try again."
        )
    except Exception:
        logger.exception("Unexpected error during graph resume")
        st.session_state.stage = "error"
        st.session_state.error_msg = (
            "Something went wrong while processing this event."
        )
