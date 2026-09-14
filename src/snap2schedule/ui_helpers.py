"""
ui_helpers.py
Exact Frutiger Aero mockup implementation for Snap2Schedule.
"""

import base64
import os
import textwrap
import streamlit as st
from datetime import date
from .schema import ExtractedEvent

# ─────────────────────────────────────────
# Image encoding helper
# ─────────────────────────────────────────

@st.cache_data
def _get_base64_of_bin_file(bin_file: str) -> str:
    """Reads a file and returns its base64 string."""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return ""

def safe_html(html_str: str) -> None:
    """Strips leading whitespace to prevent Streamlit from rendering HTML as a Markdown code block."""
    cleaned = "\n".join(line.strip() for line in html_str.split("\n"))
    st.markdown(cleaned, unsafe_allow_html=True)

# ─────────────────────────────────────────
# CSS (Exact Mockup Match)
# ─────────────────────────────────────────

def inject_css() -> None:
    bg_path = os.path.join(os.path.dirname(__file__), "..", "..", "background.png")
    bg_b64 = _get_base64_of_bin_file(bg_path)
    
    bg_css = ""
    if bg_b64:
        bg_css = f"""
        .stApp {{
            background: linear-gradient(rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.4)), 
                        url("data:image/png;base64,{bg_b64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        """
    else:
        bg_css = """
        .stApp {{
            background: linear-gradient(135deg, #EAF7FF 0%, #F7FCFF 100%);
        }}
        """

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
        color: #102A66;
    }}
    
    {bg_css}

    [data-testid="stSidebar"] {{ display: none !important; }}
    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1400px;
        background: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(12px) !important;
        border-radius: 32px !important;
        margin-top: 2rem !important;
        margin-bottom: 2rem !important;
        box-shadow: 0 20px 40px rgba(16, 42, 102, 0.08) !important;
    }}

    /* Make native containers look like glass cards */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(255, 255, 255, 0.85) !important;
        border: 1px solid rgba(70, 150, 220, 0.2) !important;
        border-radius: 22px !important;
        padding: 1.5rem !important;
        backdrop-filter: blur(24px) !important;
        box-shadow: 0 10px 30px rgba(16, 42, 102, 0.05), inset 0 1px 3px rgba(255,255,255,0.9) !important;
        margin-bottom: 1.25rem !important;
    }}

    .glass-card {{
        background: rgba(255, 255, 255, 0.78);
        border: 1px solid rgba(70, 150, 220, 0.18);
        border-radius: 22px;
        padding: 1.5rem;
        backdrop-filter: blur(20px);
        box-shadow: 0 10px 30px rgba(16, 42, 102, 0.05),
                    inset 0 1px 3px rgba(255,255,255,0.9);
        margin-bottom: 1.25rem;
    }}
    .glass-card-warn {{
        background: rgba(255, 255, 255, 0.78);
        border: 1px solid rgba(255, 184, 77, 0.3);
        border-radius: 22px;
        padding: 1.5rem;
        backdrop-filter: blur(20px);
        box-shadow: 0 10px 30px rgba(255, 184, 77, 0.1),
                    inset 0 1px 3px rgba(255,255,255,0.9);
        margin-bottom: 1.25rem;
    }}

    .hero-label {{
        font-size: 0.8rem;
        font-weight: 700;
        color: #168BFF;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    .hero-title {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 2.6rem;
        font-weight: 800;
        color: #102A66;
        line-height: 1.1;
        margin-bottom: 0.25rem;
        letter-spacing: -0.02em;
    }}
    .hero-title span {{
        color: #2FA9FF;
        background: linear-gradient(90deg, #168BFF, #2FA9FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .hero-sub {{
        font-size: 1.0rem;
        color: #52709F;
        margin-bottom: 1.0rem;
        font-weight: 500;
    }}
    .card-section-title {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.25rem;
        font-weight: 800;
        color: #102A66;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}

    .feature-pills-container {{
        display: flex;
        gap: 0.75rem;
        margin-bottom: 2rem;
    }}
    .feature-pill {{
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(70, 150, 220, 0.18);
        padding: 0.4rem 1rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #168BFF;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        box-shadow: 0 2px 10px rgba(16, 42, 102, 0.04);
    }}

    .event-title {{
        font-size: 1.8rem;
        font-weight: 800;
        color: #102A66;
        margin-bottom: 1rem;
    }}
    .event-detail-row {{
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        color: #52709F;
        font-size: 1rem;
        margin-bottom: 0.6rem;
        font-weight: 500;
    }}
    .event-detail-row .icon {{
        color: #168BFF;
        font-size: 1.2rem;
        width: 24px;
        flex-shrink: 0;
        margin-top: 0.1rem;
    }}
    .event-detail-row .value {{
        color: #102A66;
    }}

    .status-badge {{
        background: #E1F8F0;
        color: #27C99A;
        border: 1px solid rgba(39, 201, 154, 0.3);
        padding: 0.3rem 0.8rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-left: 0.5rem;
    }}

    .trace-container {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        margin-top: 0.5rem;
        overflow-x: auto;
        padding-bottom: 0.5rem;
    }}
    .trace-step {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.4rem;
        flex: 1;
        position: relative;
        min-width: 70px;
    }}
    .trace-step:not(:last-child)::after {{
        content: '→';
        position: absolute;
        right: -10px;
        top: 20%;
        color: #A0B3C6;
        font-size: 0.9rem;
    }}
    .trace-icon {{
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.85rem;
        font-weight: bold;
    }}
    .trace-icon.done {{
        background: #27C99A; color: white;
        box-shadow: 0 4px 12px rgba(39, 201, 154, 0.4);
    }}
    .trace-icon.current {{
        background: #168BFF; color: white;
        box-shadow: 0 4px 12px rgba(22, 139, 255, 0.4);
    }}
    .trace-icon.pending {{
        background: white; border: 2px solid #DDEFFF; color: #A0B3C6;
    }}
    .trace-label {{
        font-size: 0.8rem;
        font-weight: 700;
        text-align: center;
        color: #52709F;
    }}
    .trace-label.current {{ color: #102A66; }}
    .trace-time {{
        font-size: 0.7rem;
        color: #A0B3C6;
    }}

    .stTextArea textarea, .stTextInput input {{
        background: #FFFFFF !important;
        border: 1px solid rgba(70, 150, 220, 0.2) !important;
        border-radius: 12px !important;
        color: #102A66 !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: inset 0 2px 4px rgba(16, 42, 102, 0.02) !important;
        padding: 1rem !important;
    }}
    .stTextArea textarea:focus, .stTextInput input:focus {{
        border-color: #168BFF !important;
        box-shadow: 0 0 0 3px rgba(22, 139, 255, 0.2) !important;
    }}

    .stButton > button {{
        background: linear-gradient(180deg, #2FA9FF 0%, #168BFF 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 999px !important;
        padding: 0.6rem 1.8rem !important;
        box-shadow: 0 6px 16px rgba(22, 139, 255, 0.3), inset 0 1px 1px rgba(255,255,255,0.4) !important;
        transition: all 0.2s ease !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(22, 139, 255, 0.4), inset 0 1px 1px rgba(255,255,255,0.4) !important;
    }}
    button[kind="secondary"] {{
        background: #FFFFFF !important;
        color: #52709F !important;
        border: 1px solid rgba(70, 150, 220, 0.3) !important;
        box-shadow: 0 4px 12px rgba(16, 42, 102, 0.04) !important;
        background-image: none !important;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        background: rgba(255, 255, 255, 0.6);
        border-radius: 999px;
        padding: 6px;
        gap: 6px;
        border: 1px solid rgba(70, 150, 220, 0.1);
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 999px !important;
        color: #52709F !important;
        font-weight: 700;
        padding: 0.5rem 1.5rem;
    }}
    .stTabs [aria-selected="true"] {{
        background: #168BFF !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(22, 139, 255, 0.3) !important;
    }}

    .sidebar-container {{
        padding: 0.5rem 0;
    }}
    .sidebar-nav-item {{
        padding: 0.8rem 1.2rem;
        border-radius: 999px;
        color: #52709F;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    .sidebar-nav-item:hover {{
        background: rgba(255, 255, 255, 0.8);
    }}
    .sidebar-nav-item.active {{
        background: #DDEFFF;
        color: #168BFF;
    }}
    /* Sidebar nav buttons via st.button secondary */
    [data-testid="column"]:first-child .stButton > button {{
        background: transparent !important;
        color: #52709F !important;
        border: none !important;
        border-radius: 999px !important;
        padding: 0.65rem 1.2rem !important;
        font-weight: 700 !important;
        box-shadow: none !important;
        text-align: left !important;
        justify-content: flex-start !important;
        transition: all 0.2s ease !important;
    }}
    [data-testid="column"]:first-child .stButton > button:hover {{
        background: rgba(255,255,255,0.8) !important;
        color: #168BFF !important;
        transform: none !important;
        box-shadow: none !important;
    }}
    [data-testid="column"]:first-child .stButton > button[kind="primary"] {{
        background: #DDEFFF !important;
        color: #168BFF !important;
        box-shadow: none !important;
    }}

    .note-item {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 0;
        border-bottom: 1px solid rgba(70, 150, 220, 0.1);
        font-size: 0.95rem;
        font-weight: 600;
        color: #52709F;
    }}
    .note-item:last-child {{ border-bottom: none; }}
    .note-check {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }}
    .note-date {{ font-size: 0.8rem; color: #A0B3C6; }}

    .example-chips {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }}
    .example-chip {{
        background: #F7FCFF;
        border: 1px solid rgba(70, 150, 220, 0.15);
        padding: 0.3rem 0.8rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #52709F;
        cursor: pointer;
    }}
    .example-chip:hover {{
        background: #DDEFFF;
        color: #168BFF;
    }}

    footer {{ display: none !important; }}
    #MainMenu {{ display: none !important; }}
    header {{ visibility: hidden !important; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


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
# Right Sidebar Widgets (Calendar & Notes)
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

def render_quick_notes() -> None:
    html = """
<div class="glass-card" style="padding: 1.25rem;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1rem;">
        <div style="font-family:'Plus Jakarta Sans'; font-weight:800; color:#102A66; display:flex; align-items:center; gap:0.5rem;">
            <span style="background:#DDEFFF; color:#168BFF; width:28px; height:28px; border-radius:8px; display:flex; align-items:center; justify-content:center;">📝</span> 
            Quick Notes
        </div>
        <span style="color:#168BFF; font-size:0.8rem; font-weight:700; background:#EAF7FF; border: 1px solid rgba(22, 139, 255, 0.2); padding:4px 10px; border-radius:999px; cursor:pointer;">
            + New
        </span>
    </div>
    <div class="note-item">
        <div class="note-check"><input type="checkbox" style="width:16px;height:16px;"> Mua sữa</div>
        <div class="note-date">Tomorrow</div>
    </div>
    <div class="note-item">
        <div class="note-check"><input type="checkbox" style="width:16px;height:16px;"> Chuẩn bị slide PRICAI</div>
        <div class="note-date">Sep 15</div>
    </div>
    <div class="note-item">
        <div class="note-check"><input type="checkbox" style="width:16px;height:16px;"> Gửi báo cáo cho thầy</div>
        <div class="note-date">Sep 18</div>
    </div>
    <div class="note-item">
        <div class="note-check"><input type="checkbox" style="width:16px;height:16px;"> Đặt vé máy bay</div>
        <div class="note-date">Sep 25</div>
    </div>
</div>
"""
    safe_html(html)

def render_right_decorative() -> None:
    html = """
<div class="glass-card" style="padding: 2rem 1.5rem; background: linear-gradient(135deg, rgba(22, 139, 255, 0.8), rgba(47, 169, 255, 0.8)); color: white; border:none; text-align:right;">
    <div style="font-family:'Plus Jakarta Sans'; font-weight:800; font-size:1.5rem; line-height:1.2; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        Organize<br>today.<br>Do more<br>tomorrow.
    </div>
</div>
"""
    safe_html(html)


# ─────────────────────────────────────────
# Example Chips Placeholder
# ─────────────────────────────────────────

def render_example_chips() -> None:
    html = """
<div class="example-chips">
    <div class="example-chip">Họp team mai 2h</div>
    <div class="example-chip">Review sprint thứ 6</div>
    <div class="example-chip">Meeting with John</div>
    <div class="example-chip">Workshop 22/8</div>
    <div class="example-chip">Ăn trưa với Minh</div>
</div>
"""
    safe_html(html)

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
        <div style="display:inline-block; padding:0.6rem 1.5rem; background:linear-gradient(180deg, #2FA9FF 0%, #168BFF 100%); color:white; border-radius:999px; font-weight:700; box-shadow:0 6px 16px rgba(22,139,255,0.3); cursor:pointer;">
            Open in Google Calendar ↗
        </div>
        <div style="font-size:0.85rem; color:#A0B3C6;">ID: {event_id}</div>
    </div>
</div>
"""
    safe_html(html)


# ─────────────────────────────────────────
# Interrupt type detection
# ─────────────────────────────────────────

def detect_interrupt_type(message: str) -> str:
    msg_lower = message.lower()
    if "xác nhận tạo sự kiện" in msg_lower: return "preview"
    if "trùng" in msg_lower or "anyway" in msg_lower: return "conflict"
    return "clarification"
