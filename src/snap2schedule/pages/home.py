import tempfile
from pathlib import Path
import streamlit as st

from ..session import reset_session
from ..graph_runner import invoke_initial, invoke_resume
from ..ui import render_ocr_badge, render_event_card, render_trace, render_success

def render_input_card() -> None:
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
                reset_session()
                invoke_initial(user_input=user_text.strip())
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

                reset_session()
                st.session_state.temp_image_path = tmp.name
                invoke_initial(user_input="", image_path=tmp.name)
                st.rerun()

def render_result_area() -> None:
    state: dict = st.session_state.graph_result or {}
    stage: str = st.session_state.stage

    # ── Error state
    if stage == "error":
        st.error(st.session_state.error_msg)
        if st.button("Start over", key="btn_reset_err"):
            reset_session()
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
            reset_session()
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
                            invoke_resume(answer.strip())
                            st.rerun()
                elif itype == "conflict":
                    col_a, col_b, _ = st.columns([1.2, 1, 2])
                    with col_a:
                        if st.button("Create anyway", key="btn_conflict_yes", type="primary"):
                            invoke_resume("có")
                            st.rerun()
                    with col_b:
                        if st.button("Cancel", key="btn_conflict_no"):
                            invoke_resume("không")
                            st.session_state.stage = "cancelled"
                            st.rerun()
                elif itype == "preview":
                    col_a, col_b, _ = st.columns([1.5, 1, 2])
                    with col_a:
                        if st.button("Approve & create", key="btn_approve", type="primary"):
                            invoke_resume("có")
                            st.rerun()
                    with col_b:
                        if st.button("Cancel", key="btn_cancel"):
                            invoke_resume("không")
                            st.session_state.stage = "cancelled"
                            st.rerun()

    # ── Success
    if stage == "done":
        event_id = state.get("event_id")
        if event_id:
            render_success(event_id, event)
        if st.button("Create another event", key="btn_reset_done"):
            reset_session()
            st.rerun()

    # ── Trace
    if state:
        render_trace(state)
