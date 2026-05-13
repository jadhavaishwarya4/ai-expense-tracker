# components/ui_components.py
# ============================================================
# Reusable UI Components
# Cards, metric displays, alerts, progress bars, etc.
# ============================================================

import streamlit as st
from datetime import datetime


def inject_custom_css(theme: str = "dark"):
    """Inject global CSS for theming and custom components."""
    is_dark = theme == "dark"

    colors = {
        "bg": "#0f1117" if is_dark else "#f8fafc",
        "card": "#1a1d2e" if is_dark else "#ffffff",
        "surface": "#1e2235" if is_dark else "#f1f5f9",
        "border": "#2a2d3e" if is_dark else "#e2e8f0",
        "text": "#e2e8f0" if is_dark else "#0f172a",
        "subtext": "#94a3b8" if is_dark else "#64748b",
        "accent": "#6366f1",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "sidebar": "#0d1017" if is_dark else "#f1f5f9",
    }

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

    /* ---- GLOBAL RESET ---- */
    :root {{
        --bg: {colors['bg']};
        --card: {colors['card']};
        --surface: {colors['surface']};
        --border: {colors['border']};
        --text: {colors['text']};
        --subtext: {colors['subtext']};
        --accent: {colors['accent']};
        --success: {colors['success']};
        --warning: {colors['warning']};
        --danger: {colors['danger']};
    }}

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        background-color: var(--bg) !important;
        color: var(--text) !important;
    }}

    /* ---- MAIN APP LAYOUT ---- */
    .main .block-container {{
        padding: 1rem 1.5rem 2rem;
        max-width: 1400px;
    }}

    /* ---- SIDEBAR ---- */
    [data-testid="stSidebar"] {{
        background-color: {colors['sidebar']} !important;
        border-right: 1px solid var(--border) !important;
    }}

    /* ---- HIDE DEFAULT HEADER ---- */
    header[data-testid="stHeader"] {{ display: none; }}
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}

    /* ---- METRIC CARDS ---- */
    .metric-card {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.2rem;
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }}
    .metric-card:hover {{
        transform: translateY(-2px);
        border-color: var(--accent);
        box-shadow: 0 8px 24px rgba(99,102,241,0.15);
    }}
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
    }}
    .metric-card.income::before {{ background: var(--success); }}
    .metric-card.expense::before {{ background: var(--danger); }}
    .metric-card.savings::before {{ background: var(--accent); }}
    .metric-card.neutral::before {{ background: var(--warning); }}

    .metric-label {{
        font-size: 0.72rem;
        font-weight: 600;
        color: var(--subtext);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.4rem;
    }}
    .metric-value {{
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--text);
        font-family: 'Space Mono', monospace;
        line-height: 1.2;
    }}
    .metric-delta {{
        font-size: 0.75rem;
        margin-top: 0.3rem;
        display: flex;
        align-items: center;
        gap: 0.2rem;
    }}
    .metric-icon {{
        font-size: 1.5rem;
        position: absolute;
        top: 1rem;
        right: 1rem;
        opacity: 0.6;
    }}

    /* ---- INSIGHT CARDS ---- */
    .insight-card {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.6rem;
        border-left: 4px solid var(--accent);
        font-size: 0.88rem;
        color: var(--text);
    }}
    .insight-card.warning {{ border-left-color: var(--warning); }}
    .insight-card.success {{ border-left-color: var(--success); }}
    .insight-card.danger {{ border-left-color: var(--danger); }}

    /* ---- CHAT BUBBLES ---- */
    .chat-user {{
        background: var(--accent);
        color: white;
        border-radius: 16px 16px 4px 16px;
        padding: 0.6rem 1rem;
        margin: 0.4rem 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 0.88rem;
    }}
    .chat-bot {{
        background: var(--surface);
        color: var(--text);
        border-radius: 16px 16px 16px 4px;
        border: 1px solid var(--border);
        padding: 0.6rem 1rem;
        margin: 0.4rem 0;
        max-width: 85%;
        font-size: 0.88rem;
    }}

    /* ---- BUDGET PROGRESS BAR ---- */
    .budget-bar-container {{
        background: var(--surface);
        border-radius: 8px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.5rem;
        border: 1px solid var(--border);
    }}
    .budget-bar-track {{
        background: var(--border);
        border-radius: 999px;
        height: 8px;
        margin-top: 0.5rem;
    }}
    .budget-bar-fill {{
        height: 8px;
        border-radius: 999px;
        transition: width 0.5s ease;
    }}

    /* ---- BUTTONS ---- */
    .stButton > button {{
        background: var(--accent) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.2rem !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(99,102,241,0.3) !important;
    }}
    .stButton > button:hover {{
        filter: brightness(1.1) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(99,102,241,0.4) !important;
    }}

    /* ---- INPUTS ---- */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stDateInput > div > div > input,
    .stTextArea textarea {{
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--text) !important;
        font-size: 0.875rem !important;
    }}
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(99,102,241,0.2) !important;
    }}

    /* ---- TABS ---- */
    .stTabs [data-baseweb="tab-list"] {{
        background: var(--surface);
        border-radius: 10px;
        padding: 4px;
        gap: 4px;
        border-bottom: none !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        background: transparent !important;
        color: var(--subtext) !important;
        border-radius: 8px !important;
        font-weight: 500;
        font-size: 0.875rem;
    }}
    .stTabs [aria-selected="true"] {{
        background: var(--accent) !important;
        color: white !important;
    }}

    /* ---- DATAFRAME ---- */
    [data-testid="stDataFrame"] {{
        border-radius: 10px !important;
        overflow: hidden;
    }}

    /* ---- EXPANDER ---- */
    [data-testid="stExpander"] {{
        background: var(--card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
    }}

    /* ---- ALERTS ---- */
    .stAlert {{
        border-radius: 10px !important;
    }}

    /* ---- PAGE TITLE ---- */
    .page-title {{
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 0.2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    .page-subtitle {{
        font-size: 0.875rem;
        color: var(--subtext);
        margin-bottom: 1.5rem;
    }}

    /* ---- DIVIDER ---- */
    .custom-divider {{
        border: none;
        border-top: 1px solid var(--border);
        margin: 1rem 0;
    }}

    /* ---- NAV ITEMS ---- */
    .nav-item {{
        padding: 0.6rem 0.8rem;
        border-radius: 8px;
        margin: 2px 0;
        cursor: pointer;
        transition: all 0.15s ease;
        font-size: 0.875rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }}
    .nav-item:hover, .nav-item.active {{
        background: rgba(99,102,241,0.15);
        color: var(--accent);
    }}

    /* ---- SCORE BADGE ---- */
    .score-badge {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 64px; height: 64px;
        border-radius: 50%;
        font-size: 1.4rem;
        font-weight: 700;
        font-family: 'Space Mono', monospace;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def metric_card(label: str, value: str, delta: str = "", card_type: str = "neutral", icon: str = "💰"):
    """Render a styled metric card."""
    delta_html = ""
    if delta:
        color = "#10b981" if delta.startswith("+") or "less" in delta.lower() else "#ef4444"
        delta_html = f'<div class="metric-delta" style="color:{color}">{delta}</div>'

    html = f"""
    <div class="metric-card {card_type}">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def insight_card(message: str, severity: str = "info"):
    """Render an insight/alert card."""
    cls = "warning" if severity == "warning" else "success" if severity == "success" else "info"
    html = f'<div class="insight-card {cls}">{message}</div>'
    st.markdown(html, unsafe_allow_html=True)


def budget_progress_bar(category: str, spent: float, budget: float, currency: str = "₹", icon: str = "💰"):
    """Render a budget progress bar."""
    pct = min(100, (spent / budget * 100)) if budget > 0 else 0
    remaining = max(0, budget - spent)

    color = "#10b981" if pct < 70 else "#f59e0b" if pct < 90 else "#ef4444"
    status = "✅" if pct < 70 else "⚠️" if pct < 90 else "🔴"

    html = f"""
    <div class="budget-bar-container">
        <div style="display:flex; justify-content:space-between; align-items:center">
            <span style="font-weight:600; font-size:0.875rem;">{icon} {category}</span>
            <span style="font-size:0.75rem; color:var(--subtext)">{status} {pct:.0f}%</span>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:var(--subtext); margin-top:2px">
            <span>Spent: <b style="color:{color}">{currency}{spent:,.0f}</b></span>
            <span>Budget: {currency}{budget:,.0f}</span>
        </div>
        <div class="budget-bar-track">
            <div class="budget-bar-fill" style="width:{pct}%; background:{color};"></div>
        </div>
        <div style="font-size:0.72rem; color:var(--subtext); margin-top:4px">
            {"⚠️ Over budget by " + currency + f"{abs(spent - budget):,.0f}" if pct > 100 else "Remaining: " + currency + f"{remaining:,.0f}"}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = ""):
    """Render a page header with title and optional subtitle."""
    html = f"""
    <div style="margin-bottom: 1rem;">
        <div class="page-title">{title}</div>
        {"<div class='page-subtitle'>" + subtitle + "</div>" if subtitle else ""}
        <hr class="custom-divider"/>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def chat_bubble(message: str, role: str = "user"):
    """Render a chat message bubble."""
    if role == "user":
        html = f'<div class="chat-user">{message}</div>'
    else:
        html = f'<div class="chat-bot">🤖 {message}</div>'
    st.markdown(html, unsafe_allow_html=True)


def empty_state(icon: str = "📭", title: str = "Nothing here yet", subtitle: str = ""):
    """Render an empty state placeholder."""
    html = f"""
    <div style="text-align:center; padding:3rem 1rem; color:var(--subtext)">
        <div style="font-size:3rem; margin-bottom:1rem">{icon}</div>
        <div style="font-size:1.1rem; font-weight:600; color:var(--text)">{title}</div>
        {"<div style='font-size:0.875rem; margin-top:0.5rem'>" + subtitle + "</div>" if subtitle else ""}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def recommendation_card(rec: dict):
    """Render a recommendation card."""
    priority_color = "#ef4444" if rec.get("priority") == "high" else "#f59e0b" if rec.get("priority") == "medium" else "#6366f1"
    html = f"""
    <div style="background:var(--card); border:1px solid var(--border); border-radius:10px;
                padding:1rem; margin-bottom:0.6rem; border-left:4px solid {priority_color}">
        <div style="font-weight:600; font-size:0.9rem; color:var(--text)">{rec.get('icon','')} {rec.get('title','')}</div>
        <div style="font-size:0.82rem; color:var(--subtext); margin-top:4px">{rec.get('description','')}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
