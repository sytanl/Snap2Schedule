from ..ui_helpers import safe_html
from ..schema import ExtractedEvent

# ─────────────────────────────────────────
# OCR Badge
# ─────────────────────────────────────────

def render_ocr_badge(engine: str, confidence: float) -> None:
    pct = int(confidence * 100)
    color = "#27C99A" if pct >= 80 else "#FFB84D" if pct >= 60 else "#EF4444"
    html = f"""
<div style="display:inline-flex; align-items:center; gap:0.5rem;
            background:rgba(255,255,255,0.8); border:1px solid rgba(70,150,220,0.2);
            border-radius:999px; padding:0.3rem 0.9rem;
            font-size:0.78rem; font-weight:700; color:#52709F;">
    <span style="color:{color};">&#9679;</span>
    OCR
    <span style="color:#102A66;">{engine}</span>
    <span style="background:{color}; color:white; padding:1px 7px; border-radius:999px; font-size:0.72rem;">{pct}%</span>
</div>
"""
    safe_html(html)

# ─────────────────────────────────────────
# Event Card
# ─────────────────────────────────────────

def render_event_card(event: ExtractedEvent) -> None:
    date_str = (
        event.start_date.strftime("%a %d tháng %m, %Y")
        if event.start_date
        else "—"
    )
    time_str = (
        f"{event.start_time} → {event.end_time}"
        if event.start_time and event.end_time
        else event.start_time or "—"
    )
    location_str = event.location or "—"
    desc_str = event.description

    rows_html = f"""
<div class="event-detail-row">
    <span class="icon">📅</span>
    <span class="value">{date_str}</span>
</div>
<div class="event-detail-row">
    <span class="icon">🕐</span>
    <span class="value">{time_str}</span>
</div>
<div class="event-detail-row">
    <span class="icon">📍</span>
    <span class="value">{location_str}</span>
</div>
"""

    if desc_str:
        rows_html += f"""
<div class="event-detail-row">
    <span class="icon">📝</span>
    <span class="value">{desc_str}</span>
</div>
"""

    html = f"""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1.5rem;">
    <div class="card-section-title" style="margin-bottom:0;">
        <div style="background:#27C99A; color:white; width:28px; height:28px; border-radius:8px; display:flex; align-items:center; justify-content:center; box-shadow:0 4px 10px rgba(39, 201, 154, 0.4);">✓</div> 
        Event Preview 
        <span class="status-badge">Ready to review</span>
    </div>
    <div style="color:#168BFF; font-weight:700; font-size:0.9rem; border:1px solid rgba(22, 139, 255, 0.3); padding:0.3rem 1rem; border-radius:999px; cursor:pointer;">
        ✏️ Edit
    </div>
</div>

<div style="display:flex; gap: 2rem; margin-bottom: 1.5rem;">
    <div style="flex:1;">
        <div class="event-title">{event.title or "(No title)"}</div>
        {rows_html}
    </div>
    <div style="width: 250px; background: linear-gradient(135deg, #A8E6CF, #DCEDC1); border-radius:16px; position:relative; overflow:hidden; display:flex; align-items:flex-end; padding:1rem; box-shadow:inset 0 2px 10px rgba(255,255,255,0.5);">
        <div style="font-weight:800; color:#102A66; font-size:1.2rem; background:rgba(255,255,255,0.6); padding:4px 12px; border-radius:8px; backdrop-filter:blur(8px);">
            {location_str if location_str != "—" else "Campus"}
        </div>
    </div>
</div>
"""
    safe_html(html)

# ─────────────────────────────────────────
# Agent Trace (Horizontal Stepper)
# ─────────────────────────────────────────

_TRACE_NODES = [
    ("image_path",        "ocr_input",        "Input"),
    ("extracted_event",   "extract",          "OCR"),
    ("validation_result", "validate",         "Extract"),
    ("conflict",          "check_conflict",   "Validate"),
    ("approval",          "preview",          "Conflict"),
    ("event_id",          "create",           "Preview"),
    ("done",              "done",             "Create"),
]

def render_trace(state: dict) -> None:
    steps_html = ""
    for i, (state_key, _node_id, label) in enumerate(_TRACE_NODES):
        if state_key in state or (state_key == "done" and "event_id" in state):
            status_cls = "done"
            icon = "✓"
            time_lbl = "Done 16:20"
            label_cls = ""
        elif _is_current(state_key, state):
            status_cls = "current"
            icon = "■" if label == "Preview" else "●"
            time_lbl = "Current"
            label_cls = "current"
        else:
            status_cls = "pending"
            icon = "○"
            time_lbl = "Pending"
            label_cls = ""

        steps_html += f"""
<div class="trace-step">
    <div class="trace-icon {status_cls}">{icon}</div>
    <div class="trace-label {label_cls}">{label}</div>
    <div class="trace-time">{time_lbl}</div>
</div>
"""

    html = f"""
<div class="glass-card" style="padding: 1.5rem;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.5rem;">
        <div class="card-section-title" style="margin-bottom:0;">
            <span style="color:#168BFF; font-size:1.2rem;">⚙️</span> Agent Trace
        </div>
        <div style="font-size:0.8rem; font-weight:700; color:#52709F; cursor:pointer;">
            View details ⌄
        </div>
    </div>
    <div class="trace-container">
        {steps_html}
    </div>
</div>
"""
    safe_html(html)

def _is_current(key: str, state: dict) -> bool:
    order = [k for k, _, _ in _TRACE_NODES]
    try:
        idx = order.index(key)
    except ValueError:
        return False
    if idx == 0:
        return True
    prev = order[idx - 1]
    return prev in state and key not in state

# ─────────────────────────────────────────
# Success card
# ─────────────────────────────────────────

def render_success(event_id: str, event: ExtractedEvent = None) -> None:
    event_details = ""
    if event:
        time_str = ""
        if getattr(event, "start_time", None):
            time_str = event.start_time
            if getattr(event, "end_time", None):
                time_str += f" → {event.end_time}"
        
        date_str = event.start_date.strftime("%a %d %b %Y") if getattr(event, "start_date", None) else ""
        
        event_details = f"""
        <div style="background:rgba(255,255,255,0.6); padding:1rem; border-radius:12px; margin-bottom:1.5rem; border:1px solid rgba(70,150,220,0.1);">
            <div style="font-weight:700; color:#102A66; margin-bottom:0.25rem;">{event.title or "(No title)"}</div>
            <div style="font-size:0.9rem; color:#52709F; margin-bottom:0.15rem;">📅 {date_str}</div>
            <div style="font-size:0.9rem; color:#52709F; margin-bottom:0.15rem;">🕐 {time_str}</div>
            <div style="font-size:0.9rem; color:#52709F;">📍 {event.location or "—"}</div>
        </div>
        """

    html = f"""
<div class="glass-card">
    <div class="card-section-title" style="color:#27C99A;">
        <div style="background:#27C99A; color:white; width:28px; height:28px; border-radius:8px; display:flex; align-items:center; justify-content:center; box-shadow:0 4px 10px rgba(39, 201, 154, 0.4);">✓</div> 
        Event created
    </div>
    <div style="font-size:1.1rem; font-weight:700; color:#102A66; margin-bottom:1.5rem;">
        Your event has been added to Google Calendar.
    </div>
    
    {event_details}
    
    <div style="display:flex; gap:1rem; align-items:center;">
        <a href="https://calendar.google.com/calendar/r/eventedit/{event_id}" target="_blank" style="text-decoration:none; display:inline-block; padding:0.6rem 1.5rem; background:linear-gradient(180deg, #2FA9FF 0%, #168BFF 100%); color:white; border-radius:999px; font-weight:700; box-shadow:0 6px 16px rgba(22,139,255,0.3); cursor:pointer;">
            Open in Google Calendar ↗
        </a>
        <div style="font-size:0.85rem; color:#A0B3C6;">ID: {event_id}</div>
    </div>
</div>
"""
    safe_html(html)
