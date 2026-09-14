"""
app.py
Snap2Schedule — Streamlit UI (Frutiger Aero)

Run with:
    python -m snap2schedule
    or
    streamlit run src/snap2schedule/app.py
"""

import streamlit as st

# ── Page config (must be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="Snap2Schedule",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="expanded",
)

import sys
from pathlib import Path

# When run via `streamlit run`, this file executes as a script.
# Streamlit adds the script's directory to sys.path, which shadows the stdlib 'calendar' module
# because of our local 'calendar' package. We must remove it and add 'src' instead.
script_dir = str(Path(__file__).parent.resolve())
if script_dir in sys.path:
    sys.path.remove(script_dir)

src_dir = str(Path(__file__).parent.parent.resolve())
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# ── Local imports ─────────────────────────────────────────
from snap2schedule.session import init_session, reset_session
from snap2schedule.ui_helpers import inject_css, safe_html
from snap2schedule.ui import render_header, render_sidebar_nav, render_calendar_widget
from snap2schedule.pages.home import render_input_card, render_result_area
from snap2schedule.pages.my_events import render_my_events_page


def main() -> None:
    init_session()
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
                    reset_session()
                else:
                    st.toast(f"{icon} {label} — Coming soon!", icon="🚧")
                st.rerun()

    with col_main:
        render_header()

        if nav_active == "nav_events":
            render_my_events_page()
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
                render_input_card()
            else:
                render_result_area()
                if st.session_state.stage not in {"done", "cancelled", "error"}:
                    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
                    if st.button("↩ Start over", key="btn_reset_mid"):
                        reset_session()
                        st.rerun()

    with col_side:
        state: dict = st.session_state.graph_result or {}
        event = state.get("extracted_event") if st.session_state.stage not in ("idle", "cancelled", "error") else None
        render_calendar_widget(event)

if __name__ == "__main__":
    main()
