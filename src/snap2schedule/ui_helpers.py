"""
ui_helpers.py
Base UI utilities and CSS injection for Snap2Schedule.
"""

import base64
import os
import streamlit as st

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
# Interrupt type detection
# ─────────────────────────────────────────

def detect_interrupt_type(message: str) -> str:
    msg_lower = message.lower()
    if "xác nhận tạo sự kiện" in msg_lower: return "preview"
    if "trùng" in msg_lower or "anyway" in msg_lower: return "conflict"
    return "clarification"

# Re-export ui components for backward compatibility
from .ui.layout import render_header, render_sidebar_nav, render_calendar_widget
from .ui.components import render_event_card, render_ocr_badge, render_success, render_trace

__all__ = [
    "safe_html",
    "inject_css",
    "detect_interrupt_type",
    "render_header",
    "render_sidebar_nav",
    "render_calendar_widget",
    "render_event_card",
    "render_ocr_badge",
    "render_success",
    "render_trace",
]
