"""
app.py
Snap2Schedule — Streamlit UI (Frutiger Aero)

Run with:
    streamlit run src/snap2schedule/app.py
"""

from __future__ import annotations

import os
import sys
import tempfile
import uuid
from pathlib import Path

import streamlit as st
from langgraph.types import Command

# ── Path setup so relative imports work when run as script ──────────────────
_ROOT = Path(__file__).parent.parent.parent  # d:/Snap2Schedule
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# ── Page config (must be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="Snap2Schedule",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Local imports (after path setup) ─────────────────────────────────────────
from src.snap2schedule.graph import graph  # noqa: E402
from src.snap2schedule.errors import OCRServiceError, CalendarServiceError  # noqa: E402
from src.snap2schedule.logging_config import get_logger  # noqa: E402
from src.snap2schedule.ui_helpers import (  # noqa: E402
    inject_css,
    render_header,
    render_sidebar_nav,
    render_calendar_widget,
    render_event_card,
    render_trace,
    render_success,
    render_ocr_badge,
    detect_interrupt_type,
    safe_html,
)
from src.snap2schedule.calendar.calendar_reader import get_events  # noqa: E402

logger = get_logger("snap2schedule.app")


# ─────────────────────────────────────────
# Session state
# ─────────────────────────────────────────

def _init_session() -> None:
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


def _reset() -> None:
    """Clear all conversation state and generate a fresh thread_id."""
    _cleanup_temp_image()
    keys_to_clear = [
        "thread_id", "graph_result", "stage",
        "interrupt_value", "interrupt_type",
        "temp_image_path", "error_msg",
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    _init_session()


def _cleanup_temp_image() -> None:
    path = st.session_state.get("temp_image_path")
    if path and os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            pass


# ─────────────────────────────────────────
# Graph helpers
# ─────────────────────────────────────────

def _config() -> dict:
    return {"configurable": {"thread_id": st.session_state.thread_id}}


def _handle_result(result: dict) -> None:
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


def _invoke_initial(user_input: str, image_path: str | None = None) -> None:
    """Start a fresh graph invocation."""
    initial_state: dict = {
        "user_input": user_input,
    }
    if image_path:
        initial_state["image_path"] = image_path

    try:
        result = graph.invoke(initial_state, config=_config())
        _handle_result(result)
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


def _invoke_resume(response: str) -> None:
    """Resume graph from an interrupt checkpoint."""
    try:
        result = graph.invoke(Command(resume=response), config=_config())
        _handle_result(result)
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


# ─────────────────────────────────────────
# UI rendering
# ─────────────────────────────────────────

def _render_input_card() -> None:
    st.markdown(
        '<div class="card-section-title" style="margin-bottom: 0.5rem;">✨ Create an event</div>',
        unsafe_allow_html=True,
    )

    mode = st.radio(
        "Input mode",
        options=["Text", "Screenshot"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if mode == "Text":
        example = st.pills(
            "Examples",
            ["Họp team mai 2h", "Review sprint thứ 6", "Meeting with John", "Workshop 22/8", "Ăn trưa với Minh"],
            label_visibility="collapsed",
            key="example_pills"
        )
        if example and example != st.session_state.get("last_selected_example"):
            st.session_state.input_text = example
            st.session_state.last_selected_example = example
            st.rerun()
        user_text = st.text_area(
            label="Event description",
            label_visibility="collapsed",
            placeholder=(
                "e.g. Mai 2h chiều họp team ở B201 khoảng 1 tiếng."
            ),
            height=110,
            key="input_text",
        )
        
        st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
        if st.button("✦ Extract event →", key="btn_extract_text", type="primary"):
            if not user_text.strip():
                st.warning("Please describe your event first.")
            else:
                _reset()
                _invoke_initial(user_input=user_text.strip())
                st.rerun()

    elif mode == "Screenshot":
        uploaded = st.file_uploader(
            label="Upload screenshot",
            label_visibility="collapsed",
            type=["png", "jpg", "jpeg"],
            key="input_image",
        )
        if uploaded:
            st.image(uploaded, caption=uploaded.name, use_container_width=True)

        st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
        if st.button("✦ Extract event →", key="btn_extract_img", type="primary"):
            if not uploaded:
                st.warning("Please upload a screenshot first.")
            else:
                # Save to temp file so PaddleOCR / Tesseract can read from disk
                suffix = Path(uploaded.name).suffix or ".png"
                tmp = tempfile.NamedTemporaryFile(
                    delete=False, suffix=suffix, dir=tempfile.gettempdir()
                )
                tmp.write(uploaded.getvalue())
                tmp.close()

                _reset()
                st.session_state.temp_image_path = tmp.name
                _invoke_initial(user_input="", image_path=tmp.name)
                st.rerun()


def _render_result_area() -> None:
    state: dict = st.session_state.graph_result or {}
    stage: str = st.session_state.stage

    # ── Error state
    if stage == "error":
        st.error(st.session_state.error_msg)
        if st.button("Start over", key="btn_reset_err"):
            _reset()
            st.rerun()
        return

    # ── Cancelled
    if stage == "cancelled":
        st.markdown(
            """
            <div class="glass-card">
                <div style="color:#4B5563; font-size:0.95rem; font-weight:500;">
                    Event creation cancelled.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Start over", key="btn_reset_cancel"):
            _reset()
            st.rerun()
        return

    if not state:
        return

    # ── OCR Badge ──
    if state.get("ocr_engine") and state.get("ocr_confidence") is not None:
        render_ocr_badge(state["ocr_engine"], state["ocr_confidence"])
        st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

    # ── Consolidated Event Preview ──
    event = state.get("extracted_event")
    if event and stage not in ("done", "cancelled", "error"):
        with st.container(border=True):
            render_event_card(event)
            
            # Conflict Check inside the card
            if "conflict" in state:
                if state["conflict"]:
                    st.markdown(
                        """
                        <div style="color:#D97706; font-size:0.95rem; font-weight:700; margin-bottom:1rem;">
                            ⚠ Schedule conflict detected<br>
                            <span style="font-size:0.85rem; font-weight:500; color:#6B7280;">Another event overlaps this time slot.</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        """
                        <div style="color:#059669; font-size:0.95rem; font-weight:700; margin-bottom:1rem;">
                            ✓ No schedule conflict detected<br>
                            <span style="font-size:0.85rem; font-weight:500; color:#064E3B;">You're good to go!</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            
            # Action Buttons inside the card
            if stage == "interrupted":
                itype = st.session_state.interrupt_type
                msg = st.session_state.interrupt_value or ""

                if itype == "clarification":
                    st.markdown(
                        f"""
                        <div style="margin-top:1rem; padding-top:1rem; border-top:1px solid rgba(70,150,220,0.1);">
                            <div style="font-weight:700; color:#102A66; margin-bottom:0.5rem;">One detail is missing:</div>
                            <div style="color:#1E3A5F; font-size:0.95rem; margin-bottom:0.5rem;">{msg}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    answer = st.text_input("Your answer", label_visibility="collapsed", key="clarification_answer")
                    if st.button("Continue →", key="btn_clarify"):
                        if answer.strip():
                            _invoke_resume(answer.strip())
                            st.rerun()
                elif itype == "conflict":
                    col_a, col_b, _ = st.columns([1.2, 1, 2])
                    with col_a:
                        if st.button("Create anyway", key="btn_conflict_yes", type="primary"):
                            _invoke_resume("có")
                            st.rerun()
                    with col_b:
                        if st.button("Cancel", key="btn_conflict_no"):
                            _invoke_resume("không")
                            st.session_state.stage = "cancelled"
                            st.rerun()
                elif itype == "preview":
                    col_a, col_b, _ = st.columns([1.5, 1, 2])
                    with col_a:
                        if st.button("Approve & create", key="btn_approve", type="primary"):
                            _invoke_resume("có")
                            st.rerun()
                    with col_b:
                        if st.button("Cancel", key="btn_cancel"):
                            _invoke_resume("không")
                            st.session_state.stage = "cancelled"
                            st.rerun()

    # ── Success
    if stage == "done":
        event_id = state.get("event_id")
        if event_id:
            render_success(event_id, event)
        if st.button("Create another event", key="btn_reset_done"):
            _reset()
            st.rerun()

    # ── Trace
    if state:
        render_trace(state)


# ─────────────────────────────────────────
# My Events page
# ─────────────────────────────────────────

def _render_my_events_page() -> None:
    from datetime import datetime, timedelta, timezone

    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

    # Date range selector
    col_l, col_r = st.columns([1, 1])
    with col_l:
        days_back = st.selectbox(
            "Show events from",
            options=[7, 14, 30, 60, 90],
            format_func=lambda x: f"Past {x} days",
            index=1,
            key="my_events_days_back",
            label_visibility="collapsed",
        )
    with col_r:
        if st.button("🔄 Refresh", key="btn_refresh_events"):
            st.cache_data.clear()
            st.rerun()

    now = datetime.now(timezone.utc)
    start_dt = now - timedelta(days=days_back)

    try:
        with st.spinner("Loading events from Google Calendar…"):
            events = get_events(start_dt, now + timedelta(days=30))
    except Exception as e:
        st.error(f"Could not load events: {e}")
        return

    if not events:
        safe_html("""
<div class="glass-card" style="text-align:center; padding: 3rem 2rem;">
    <div style="font-size:2.5rem; margin-bottom:1rem;">📅</div>
    <div style="font-family:'Plus Jakarta Sans'; font-weight:800; font-size:1.2rem; color:#102A66; margin-bottom:0.5rem;">No events found</div>
    <div style="color:#52709F; font-size:0.9rem;">No events in the selected date range.</div>
</div>""")
        return

    # Header
    safe_html(f"""
<div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:1rem;">
    <div style="font-family:'Plus Jakarta Sans'; font-weight:800; font-size:1.25rem; color:#102A66;">
        📅 My Events
        <span style="background:#DDEFFF; color:#168BFF; font-size:0.75rem; font-weight:700;
                     padding:3px 10px; border-radius:999px; margin-left:0.5rem;">{len(events)} events</span>
    </div>
</div>""")

    # Event cards
    for ev in sorted(events, key=lambda e: e.start, reverse=True):
        try:
            dt_start = datetime.fromisoformat(ev.start)
            dt_end   = datetime.fromisoformat(ev.end)
            date_str = dt_start.strftime("%a, %d %b %Y")
            time_str = f"{dt_start.strftime('%H:%M')} → {dt_end.strftime('%H:%M')}"
        except Exception:
            date_str = ev.start[:10]
            time_str = ""

        gcal_link = f"https://calendar.google.com/calendar/r/eventedit/{ev.id}"

        safe_html(f"""
<div class="glass-card" style="padding:1rem 1.25rem; margin-bottom:0.75rem;
     display:flex; align-items:center; gap:1.25rem;">
    <div style="background:#DDEFFF; color:#168BFF; width:44px; height:44px; border-radius:12px;
                display:flex; align-items:center; justify-content:center; font-size:1.3rem;
                flex-shrink:0;">📌</div>
    <div style="flex:1; min-width:0;">
        <div style="font-weight:800; font-size:1rem; color:#102A66;
                    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{ev.title}</div>
        <div style="font-size:0.82rem; color:#52709F; margin-top:2px;">
            🗓 {date_str} &nbsp;·&nbsp; 🕐 {time_str}
        </div>
    </div>
    <a href="{gcal_link}" target="_blank"
       style="padding:0.4rem 1rem; background:rgba(22,139,255,0.1); color:#168BFF;
              border-radius:999px; font-weight:700; font-size:0.8rem;
              text-decoration:none; white-space:nowrap; flex-shrink:0;">
        Open ↗
    </a>
</div>""")

# ─────────────────────────────────────────

def main() -> None:
    _init_session()
    inject_css()

    col_nav, col_main, col_side = st.columns([1.8, 5.8, 2.4], gap="large")
    nav_active = st.session_state.get("nav_active", "nav_home")

    with col_nav:
        render_sidebar_nav()
        st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
        nav_items = [
            ("🏠", "Home",      "nav_home"),
            ("📅", "My Events", "nav_events"),
            ("🕒", "History",   "nav_history"),
            ("⚙️", "Settings",  "nav_settings"),
        ]
        for icon, label, key in nav_items:
            active = nav_active == key
            if st.button(
                f"{icon} {label}",
                key=key,
                type="primary" if active else "secondary",
                use_container_width=True,
            ):
                st.session_state["nav_active"] = key
                if key == "nav_home":
                    _reset()
                else:
                    st.toast(f"{icon} {label} — Coming soon!", icon="🚧")
                st.rerun()

    with col_main:
        render_header()

        if nav_active == "nav_events":
            _render_my_events_page()
        elif nav_active == "nav_history":
            safe_html("""
<div class="glass-card" style="text-align:center; padding: 3rem 2rem;">
    <div style="font-size:2.5rem; margin-bottom:1rem;">🕒</div>
    <div style="font-family:'Plus Jakarta Sans'; font-weight:800; font-size:1.3rem; color:#102A66; margin-bottom:0.5rem;">History</div>
    <div style="color:#52709F; font-size:0.95rem;">Your past extractions and scheduling history.</div>
    <div style="margin-top:1.5rem; display:inline-block; padding:0.5rem 1.5rem; background:rgba(22,139,255,0.1); color:#168BFF; border-radius:999px; font-weight:700; font-size:0.85rem;">Coming soon</div>
</div>""")
        elif nav_active == "nav_settings":
            safe_html("""
<div class="glass-card" style="text-align:center; padding: 3rem 2rem;">
    <div style="font-size:2.5rem; margin-bottom:1rem;">⚙️</div>
    <div style="font-family:'Plus Jakarta Sans'; font-weight:800; font-size:1.3rem; color:#102A66; margin-bottom:0.5rem;">Settings</div>
    <div style="color:#52709F; font-size:0.95rem;">Configure OCR engine, calendar accounts, and preferences.</div>
    <div style="margin-top:1.5rem; display:inline-block; padding:0.5rem 1.5rem; background:rgba(22,139,255,0.1); color:#168BFF; border-radius:999px; font-weight:700; font-size:0.85rem;">Coming soon</div>
</div>""")
        else:
            # Home
            if st.session_state.stage == "idle":
                _render_input_card()
            else:
                _render_result_area()
                if st.session_state.stage not in {"done", "cancelled", "error"}:
                    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
                    if st.button("↩ Start over", key="btn_reset_mid"):
                        _reset()
                        st.rerun()

    with col_side:
        state: dict = st.session_state.graph_result or {}
        event = state.get("extracted_event") if st.session_state.stage not in ("idle", "cancelled", "error") else None
        render_calendar_widget(event)

if __name__ == "__main__":
    main()
