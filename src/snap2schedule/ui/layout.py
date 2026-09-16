from ..ui_helpers import safe_html
from ..schema import ExtractedEvent

# ─────────────────────────────────────────
# Header / Hero
# ─────────────────────────────────────────

def render_header() -> None:
    html = """
<div class="hero-title">Turn messy plans into<br><span>calendar events.</span></div>
<div class="hero-sub">Text or screenshot in. Clean calendar event out.</div>

<div class="feature-pills-container">
    <div class="feature-pill">✨ AI-Powered</div>
    <div class="feature-pill">📷 Screenshot → Event</div>
    <div class="feature-pill">📅 Google Calendar</div>
</div>
"""
    safe_html(html)


# ─────────────────────────────────────────
# Sidebar Mock
# ─────────────────────────────────────────

def render_sidebar_nav() -> None:
    html = """
<div class="sidebar-container">
    <div style="display:flex; align-items:center; gap:10px; margin-bottom: 1.5rem; margin-top: 0.5rem;">
        <div style="background:#168BFF; color:white; width:36px; height:36px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1.2rem; box-shadow:0 4px 12px rgba(22, 139, 255, 0.3);">
            📅
        </div>
        <div>
            <div style="font-family:'Plus Jakarta Sans'; font-weight:800; font-size:1.1rem; color:#102A66; line-height:1;">Snap2Schedule</div>
            <div style="font-size:0.7rem; color:#52709F; font-weight:600; margin-top:2px;">From plans to progress.</div>
        </div>
    </div>
</div>
"""
    safe_html(html)


# ─────────────────────────────────────────
# Right Sidebar Widgets (Calendar)
# ─────────────────────────────────────────

def render_calendar_widget(event: ExtractedEvent = None) -> None:
    target_day = event.start_date.day if event and getattr(event, "start_date", None) and event.start_date.month == 9 and event.start_date.year == 2026 else None
    
    def render_cell(day: int, is_target: bool) -> str:
        if is_target:
            return f'<td style="padding:5px 2px;"><div style="background:#168BFF; color:white; width:26px; height:26px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto; font-size:0.8rem; font-weight:800; box-shadow:0 3px 8px rgba(22,139,255,0.4);">{day}</div></td>'
        return f'<td style="padding:5px 2px;">{day}</td>'

    html = f"""<div class="glass-card" style="padding: 1rem; overflow: hidden;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1rem;">
        <div style="font-family:'Plus Jakarta Sans'; font-weight:800; font-size:0.9rem; color:#102A66; display:flex; align-items:center; gap:0.4rem;">
            <span style="color:#168BFF;">✦</span> September 2026
        </div>
        <div style="color:#52709F; font-size:0.85rem; font-weight:800; cursor:pointer; display:flex; gap:0.6rem;">
            <span>❮</span><span>❯</span>
        </div>
    </div>
    <table style="width:100%; table-layout:fixed; text-align:center; border-collapse:collapse; font-size:0.78rem;">
        <tr style="color:#A0B3C6; font-weight:700; font-size:0.7rem;">
            <td style="padding-bottom:8px;">Mo</td>
            <td>Tu</td><td>We</td><td>Th</td><td>Fr</td>
            <td style="color:#FFB84D;">Sa</td>
            <td style="color:#FFB84D;">Su</td>
        </tr>
        <tr style="color:#A0B3C6; font-weight:500; font-size:0.76rem;">
            <td style="padding:5px 2px;">1</td>
            <td style="padding:5px 2px;">2</td>
            <td style="padding:5px 2px;">3</td>
            <td style="padding:5px 2px;">4</td>
            <td style="padding:5px 2px;">5</td>
            <td style="padding:5px 2px;">6</td>
            <td style="padding:5px 2px;">7</td>
        </tr>
        <tr style="color:#102A66; font-weight:600;">
            {render_cell(8, target_day == 8)}
            {render_cell(9, target_day == 9)}
            {render_cell(10, target_day == 10)}
            {render_cell(11, target_day == 11 or target_day is None)}
            {render_cell(12, target_day == 12)}
            {render_cell(13, target_day == 13)}
            {render_cell(14, target_day == 14)}
        </tr>
        <tr style="color:#102A66; font-weight:600;">
            {render_cell(15, target_day == 15)}
            {render_cell(16, target_day == 16)}
            {render_cell(17, target_day == 17)}
            {render_cell(18, target_day == 18)}
            {render_cell(19, target_day == 19)}
            {render_cell(20, target_day == 20)}
            {render_cell(21, target_day == 21)}
        </tr>
        <tr style="color:#102A66; font-weight:600;">
            {render_cell(22, target_day == 22)}
            {render_cell(23, target_day == 23)}
            {render_cell(24, target_day == 24)}
            {render_cell(25, target_day == 25)}
            {render_cell(26, target_day == 26)}
            {render_cell(27, target_day == 27)}
            {render_cell(28, target_day == 28)}
        </tr>
        <tr style="color:#102A66; font-weight:600;">
            {render_cell(29, target_day == 29)}
            {render_cell(30, target_day == 30)}
            <td style="padding:5px 2px; color:#A0B3C6;">1</td>
            <td style="padding:5px 2px; color:#A0B3C6;">2</td>
            <td style="padding:5px 2px; color:#A0B3C6;">3</td>
            <td style="padding:5px 2px; color:#A0B3C6;">4</td>
            <td style="padding:5px 2px; color:#A0B3C6;">5</td>
        </tr>
    </table>

    <div style="margin-top:1.25rem;">
        <div style="font-size:0.72rem; font-weight:700; color:#A0B3C6; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:0.5rem;">Upcoming</div>
        <div style="display:flex; align-items:center; gap:0.5rem; padding:0.5rem 0.75rem; background:rgba(22,139,255,0.06); border-radius:10px; margin-bottom:0.4rem;">
            <div style="width:8px; height:8px; background:#168BFF; border-radius:50%; flex-shrink:0;"></div>
            <div style="font-size:0.82rem; font-weight:600; color:#102A66;">Họp team sprint</div>
            <div style="font-size:0.75rem; color:#A0B3C6; margin-left:auto;">2:00 PM</div>
        </div>
        <div style="display:flex; align-items:center; gap:0.5rem; padding:0.5rem 0.75rem; background:rgba(255,184,77,0.08); border-radius:10px;">
            <div style="width:8px; height:8px; background:#FFB84D; border-radius:50%; flex-shrink:0;"></div>
            <div style="font-size:0.82rem; font-weight:600; color:#102A66;">Workshop 22/9</div>
            <div style="font-size:0.75rem; color:#A0B3C6; margin-left:auto;">Sep 22</div>
        </div>
    </div>

    <div style="margin-top:1.25rem; text-align:center;">
        <div style="display:inline-block; padding:0.4rem 1rem; background:rgba(22, 139, 255, 0.1); color:#168BFF; border-radius:999px; font-weight:700; font-size:0.8rem; cursor:pointer;">
            📅 Open in Google Calendar ↗
        </div>
    </div>
</div>
"""
    safe_html(html)
