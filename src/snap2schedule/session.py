import os
import uuid
import streamlit as st

def init_session() -> None:
    defaults: dict = {
        "thread_id": str(uuid.uuid4()),
        "graph_result": None,       # last CalendarState dict
        "stage": "idle",            # idle | interrupted | done | cancelled | error
        "interrupt_value": None,    # str message from interrupt()
        "interrupt_type": None,     # clarification | conflict | preview
        "temp_image_path": None,    # path of saved upload
        "error_msg": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def reset_session() -> None:
    """Clear all conversation state and generate a fresh thread_id."""
    cleanup_temp_image()
    keys_to_clear = [
        "thread_id", "graph_result", "stage",
        "interrupt_value", "interrupt_type",
        "temp_image_path", "error_msg",
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    init_session()

def cleanup_temp_image() -> None:
    path = st.session_state.get("temp_image_path")
    if path and os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            pass
