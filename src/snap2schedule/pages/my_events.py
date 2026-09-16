from datetime import datetime, timedelta, timezone
import streamlit as st

from ..ui_helpers import safe_html
from ..calendar.calendar_reader import get_events

def render_my_events_page() -> None:
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
