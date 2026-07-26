import streamlit as st

COLORS = {
    "bg": "#0A0E14",
    "panel": "#0F1521",
    "panel_hover": "#131B2B",
    "border": "#1E2A3F",
    "border_bright": "#2B4C7E",
    "accent_blue": "#4A7FBF",
    "accent_gold": "#C9A227",
    "text": "#E8EDF4",
    "text_muted": "#6B7A94",
    "status_green": "#3FA66A",
    "status_amber": "#C9A227",
    "status_red": "#C24444",
}

PLOTLY_TEMPLATE = {
    "paper_bgcolor": COLORS["panel"],
    "plot_bgcolor": COLORS["panel"],
    "font": {"family": "JetBrains Mono, monospace", "color": COLORS["text_muted"], "size": 12},
    "colorway": [COLORS["accent_blue"], COLORS["accent_gold"], "#7A93B8", "#8A5A2E"],
}


def apply_plotly_theme(fig, height=None):
    fig.update_layout(
        paper_bgcolor=COLORS["panel"],
        plot_bgcolor=COLORS["panel"],
        font=dict(family="JetBrains Mono, monospace", color=COLORS["text_muted"], size=12),
        title_font=dict(family="Rajdhani, sans-serif", color=COLORS["text"], size=18),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text_muted"])),
        margin=dict(l=10, r=10, t=50, b=10),
        colorway=[COLORS["accent_blue"], COLORS["accent_gold"], "#7A93B8", "#8A5A2E", "#5C7CA8"],
    )
    fig.update_xaxes(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"], linecolor=COLORS["border_bright"])
    fig.update_yaxes(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"], linecolor=COLORS["border_bright"])
    if height:
        fig.update_layout(height=height)
    return fig


def inject_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Inter:wght@400;500;600&display=swap');

        :root {
            --bg: #0A0E14;
            --panel: #0F1521;
            --panel-hover: #131B2B;
            --border: #1E2A3F;
            --border-bright: #2B4C7E;
            --accent-blue: #4A7FBF;
            --accent-gold: #C9A227;
            --text: #E8EDF4;
            --text-muted: #6B7A94;
        }

        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        /* ---- App shell ---- */
        .stApp {
            background-color: var(--bg);
            background-image:
                linear-gradient(rgba(30,42,63,0.35) 1px, transparent 1px),
                linear-gradient(90deg, rgba(30,42,63,0.35) 1px, transparent 1px);
            background-size: 42px 42px;
            background-position: -1px -1px;
        }
        section[data-testid="stSidebar"] {
            background-color: #080B10;
            border-right: 1px solid var(--border);
        }
        section[data-testid="stSidebar"] * { color: var(--text-muted) !important; }
        section[data-testid="stSidebar"] a { font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; }

        #MainMenu, footer { visibility: hidden; }
        header { background: transparent !important; }
        header [data-testid="stHeaderActionElements"] { visibility: hidden; }
        button[kind="header"] { visibility: visible !important; color: var(--text) !important; }

        /* ---- Typography ---- */
        h1, h2, h3 {
            font-family: 'Rajdhani', sans-serif !important;
            color: var(--text) !important;
            letter-spacing: 0.02em;
            text-transform: uppercase;
            font-weight: 700 !important;
        }
        p, span, label, div { color: var(--text); }
        .stMarkdown, .stCaption { color: var(--text-muted); }

        /* ---- Eyebrow / status labels ---- */
        .hud-eyebrow {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            color: var(--accent-gold);
            border-left: 2px solid var(--accent-gold);
            padding-left: 10px;
            margin-bottom: 6px;
        }

        .hud-title {
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            font-size: 2.6rem;
            letter-spacing: 0.01em;
            color: var(--text);
            text-transform: uppercase;
            line-height: 1.05;
            margin: 4px 0 8px 0;
        }

        .hud-subtitle {
            font-family: 'Inter', sans-serif;
            color: var(--text-muted);
            font-size: 0.95rem;
            max-width: 680px;
            margin-bottom: 4px;
        }

        .hud-rule {
            border: none;
            border-top: 1px solid var(--border);
            margin: 22px 0;
        }

        /* ---- Boxy corner-bracket panel ---- */
        .hud-panel {
            position: relative;
            background: var(--panel);
            border: 1px solid var(--border);
            padding: 20px 22px;
            margin-bottom: 4px;
        }
        .hud-panel::before, .hud-panel::after {
            content: "";
            position: absolute;
            width: 14px;
            height: 14px;
            pointer-events: none;
        }
        .hud-panel::before {
            top: -1px; left: -1px;
            border-top: 2px solid var(--accent-gold);
            border-left: 2px solid var(--accent-gold);
        }
        .hud-panel::after {
            bottom: -1px; right: -1px;
            border-bottom: 2px solid var(--accent-gold);
            border-right: 2px solid var(--accent-gold);
        }

        /* ---- KPI stat block ---- */
        .hud-kpi-label {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 6px;
        }
        .hud-kpi-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 2.1rem;
            font-weight: 600;
            color: var(--text);
            letter-spacing: 0.01em;
        }
        .hud-kpi-value.gold { color: var(--accent-gold); }
        .hud-kpi-value.blue { color: var(--accent-blue); }

        /* ---- Status pill ---- */
        .hud-status {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--text-muted);
        }
        .hud-dot {
            width: 7px; height: 7px;
            background: var(--accent-gold);
            box-shadow: 0 0 6px var(--accent-gold);
        }
        .hud-dot.green { background: #3FA66A; box-shadow: 0 0 6px #3FA66A; }

        /* ---- CTA panel ---- */
        .hud-cta {
            position: relative;
            background: var(--panel);
            border: 1px solid var(--border-bright);
            padding: 18px 22px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            letter-spacing: 0.04em;
            color: var(--text);
        }
        .hud-cta::before {
            content: "";
            position: absolute;
            top: -1px; left: -1px;
            width: 14px; height: 14px;
            border-top: 2px solid var(--accent-blue);
            border-left: 2px solid var(--accent-blue);
        }
        .hud-cta::after {
            content: "";
            position: absolute;
            bottom: -1px; right: -1px;
            width: 14px; height: 14px;
            border-bottom: 2px solid var(--accent-blue);
            border-right: 2px solid var(--accent-blue);
        }
        .hud-cta b { color: var(--accent-gold); }

        /* ---- Module index rows (app.py landing) ---- */
        .hud-module {
            display: flex;
            align-items: baseline;
            gap: 14px;
            padding: 12px 4px;
            border-bottom: 1px solid var(--border);
            font-family: 'JetBrains Mono', monospace;
        }
        .hud-module:last-child { border-bottom: none; }
        .hud-module .idx { color: var(--accent-gold); font-size: 0.85rem; width: 26px; }
        .hud-module .name { color: var(--text); font-family: 'Rajdhani', sans-serif; text-transform: uppercase; font-size: 1.05rem; letter-spacing: 0.03em; font-weight: 600; }
        .hud-module .desc { color: var(--text-muted); font-size: 0.8rem; margin-left: auto; text-align: right; }

        /* ---- Streamlit native widget restyle ---- */
        div[data-testid="stMetric"] {
            background: var(--panel);
            border: 1px solid var(--border);
            padding: 14px 16px;
        }
        div[data-testid="stMetricLabel"] { color: var(--text-muted) !important; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; font-size: 0.7rem !important; letter-spacing: 0.14em; }
        div[data-testid="stMetricValue"] { color: var(--text) !important; font-family: 'JetBrains Mono', monospace; }

        .stButton > button {
            background: var(--panel);
            color: var(--text);
            border: 1px solid var(--border-bright);
            border-radius: 0;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-size: 0.78rem;
            padding: 10px 18px;
        }
        .stButton > button:hover {
            border-color: var(--accent-gold);
            color: var(--accent-gold);
        }

        div[data-testid="stDataFrame"] { border: 1px solid var(--border); }

        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg); }
        ::-webkit-scrollbar-thumb { background: var(--border-bright); }
        </style>
        """,
        unsafe_allow_html=True,
    )


def eyebrow(text: str):
    st.markdown(f'<div class="hud-eyebrow">{text}</div>', unsafe_allow_html=True)


def hud_title(title: str, subtitle: str = ""):
    st.markdown(f'<div class="hud-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="hud-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def rule():
    st.markdown('<hr class="hud-rule">', unsafe_allow_html=True)


def status_pill(text: str, ok: bool = True):
    dot_class = "hud-dot green" if ok else "hud-dot"
    st.markdown(
        f'<div class="hud-status"><span class="{dot_class}"></span>{text}</div>',
        unsafe_allow_html=True,
    )


def kpi_panel(label: str, value: str, accent: str = ""):
    """Render one boxy KPI card. accent: '' | 'gold' | 'blue'"""
    st.markdown(
        f"""
        <div class="hud-panel">
            <div class="hud-kpi-label">{label}</div>
            <div class="hud-kpi-value {accent}">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def cta(text_html: str):
    st.markdown(f'<div class="hud-cta">{text_html}</div>', unsafe_allow_html=True)

def panel_open(padding: str = "20px 22px"):
    """Open a boxy corner-bracket panel. Pair with panel_close() around any
    Streamlit content (charts, dataframes, forms) you want framed."""
    st.markdown(f'<div class="hud-panel" style="padding:{padding};">', unsafe_allow_html=True)


def panel_close():
    st.markdown('</div>', unsafe_allow_html=True)


def status_panel(label: str, message: str, level: str = "ok"):
    """Color-coded result panel. level: 'ok' (green) | 'warn' (gold) | 'bad' (red)."""
    color = {
        "ok": COLORS["status_green"],
        "warn": COLORS["accent_gold"],
        "bad": COLORS["status_red"],
    }.get(level, COLORS["accent_gold"])
    st.markdown(
        f"""
        <div class="hud-panel" style="border-left:3px solid {color};">
            <div class="hud-kpi-label">{label}</div>
            <div class="hud-kpi-value" style="color:{color};">{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )