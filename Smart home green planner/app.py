# app.py
# Smart Home Green Planner — main entry point.
# Handles page config, global CSS, session state, tab layout, and sidebar.
# All tab content is delegated to pages_content/; all logic lives in utils/.
#
# Run with:  streamlit run app.py

import streamlit as st

import pages_content.home_details    as pg_home
import pages_content.energy_breakdown as pg_energy
import pages_content.comparison_chart as pg_chart
import pages_content.weekly_trend     as pg_trend
import pages_content.recommendation   as pg_rec
from utils.chat_assistant import get_response

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Smart Home Green Planner",
    page_icon="🌿",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Global CSS — green and white elegant theme
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        /* ── Base app background ── */
        .stApp { background-color: #f4f8f4; }

        /* ── Top toolbar (the dark header bar Streamlit renders at the top) ── */
        header[data-testid="stHeader"] {
            background-color: #ffffff !important;
            border-bottom: 2px solid #c8e6c9 !important;
        }
        /* Toolbar icon buttons (hamburger, settings, etc.) */
        header[data-testid="stHeader"] button,
        header[data-testid="stHeader"] button svg {
            color: #2e7d32 !important;
            fill: #2e7d32 !important;
        }
        header[data-testid="stHeader"] button:hover {
            background-color: #e8f5e9 !important;
        }
        /* "Deploy" button */
        header[data-testid="stHeader"] [data-testid="stToolbarActionButtonLabel"],
        header[data-testid="stHeader"] [data-testid="stToolbarActionButton"] {
            color: #1b5e20 !important;
            background-color: #e8f5e9 !important;
            border: 1px solid #a5d6a7 !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
        }
        header[data-testid="stHeader"] [data-testid="stToolbarActionButton"]:hover {
            background-color: #c8e6c9 !important;
        }
        /* Streamlit logo / decoration in the toolbar */
        header[data-testid="stHeader"] [data-testid="stDecoration"] {
            background-image: none !important;
            background-color: #a5d6a7 !important;
        }

        /* ── Remove excessive top padding ── */
        .block-container { padding-top: 1.5rem !important; }

        /* ── Force full-opacity text — main area ── */
        .stApp h1,
        .stApp [data-testid="stHeading"] h1 {
            color: #1b2e1b !important;
            opacity: 1 !important;
            font-weight: 700 !important;
        }
        .stApp p,
        .stApp [data-testid="stMarkdownContainer"] p,
        .stApp [data-testid="stText"] {
            color: #1f2d1f !important;
            opacity: 1 !important;
        }
        .stApp .stMarkdown,
        .stApp .stMarkdown * {
            color: #1f2d1f !important;
            opacity: 1 !important;
        }
        .stApp h2, .stApp h3, .stApp h4 {
            color: #1b5e20 !important;
            opacity: 1 !important;
            font-weight: 700 !important;
        }
        .stApp [data-testid="stCaptionContainer"],
        .stApp [data-testid="stCaptionContainer"] * {
            color: #3a5a3a !important;
            opacity: 1 !important;
        }

        /* ── Tab bar ── */
        div[data-baseweb="tab-list"] {
            gap: 4px;
            background: #e8f5e9;
            border-radius: 10px;
            padding: 4px;
        }
        div[data-baseweb="tab-list"] button,
        div[data-baseweb="tab-list"] button * {
            border-radius: 8px !important;
            font-weight: 700 !important;
            font-size: 0.9rem !important;
            color: #1b5e20 !important;
            opacity: 1 !important;
        }
        div[data-baseweb="tab-list"] button[aria-selected="true"],
        div[data-baseweb="tab-list"] button[aria-selected="true"] * {
            background-color: #2e7d32 !important;
            color: #ffffff !important;
            opacity: 1 !important;
        }

        /* ── Tab panel backgrounds ── */
        /* Tab 1 — Home Details: warm off-white/beige */
        div[data-baseweb="tab-panel"]:nth-of-type(1) {
            background: #fffdf7;
            border-radius: 0 12px 12px 12px;
            padding: 1.5rem;
            border: 1px solid #e8e0cc;
        }
        /* Tab 2 — Energy Breakdown: light yellow-green */
        div[data-baseweb="tab-panel"]:nth-of-type(2) {
            background: #f1f8e9;
            border-radius: 0 12px 12px 12px;
            padding: 1.5rem;
            border: 1px solid #c5e1a5;
        }
        /* Tab 3 — Comparison Chart: clean white */
        div[data-baseweb="tab-panel"]:nth-of-type(3) {
            background: #ffffff;
            border-radius: 0 12px 12px 12px;
            padding: 1.5rem;
            border: 1px solid #c8e6c9;
        }
        /* Tab 4 — Weekly Trend: soft green tint */
        div[data-baseweb="tab-panel"]:nth-of-type(4) {
            background: #f4faf4;
            border-radius: 0 12px 12px 12px;
            padding: 1.5rem;
            border: 1px solid #c8e6c9;
        }
        /* Tab 5 — Recommendation: white/green */
        div[data-baseweb="tab-panel"]:nth-of-type(5) {
            background: #f9fbf9;
            border-radius: 0 12px 12px 12px;
            padding: 1.5rem;
            border: 1px solid #c8e6c9;
        }

        /* ── Form card ── */
        div.stForm {
            background: #ffffff;
            border: 1px solid #d4e8d4;
            border-radius: 12px;
            padding: 1.25rem 1.5rem 0.75rem;
        }

        /* ── Submit buttons ── */
        div[data-testid="stFormSubmitButton"] > button {
            background-color: #2e7d32 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }
        div[data-testid="stFormSubmitButton"] > button:hover {
            background-color: #1b5e20 !important;
        }

        /* ── Metric cards ── */
        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #a5d6a7;
            border-radius: 12px;
            padding: 1rem 1.25rem;
        }
        div[data-testid="stMetricLabel"] { color: #2e7d32 !important; font-weight: 600 !important; }
        div[data-testid="stMetricValue"] { color: #1b5e20 !important; font-size: 1.6rem !important; }

        /* ── Sidebar ── */
        section[data-testid="stSidebar"] {
            background: #e8f5e9;
            border-right: 2px solid #a5d6a7;
        }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #1b5e20 !important;
        }

        /* ── Chat messages ── */
        div[data-testid="stChatMessage"] {
            border-radius: 10px;
            margin-bottom: 0.4rem;
        }

        /* ── "No results yet" placeholder ── */
        .no-results-box {
            background: #f1f8e9;
            border: 1px solid #aed581;
            border-radius: 10px;
            padding: 1.25rem 1.5rem;
            color: #33691e;
            font-size: 0.95rem;
            text-align: center;
            margin-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------
if "weather" not in st.session_state:
    st.session_state.weather = "sunny"

if "result" not in st.session_state:
    st.session_state.result = None          # None until first calculation

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []      # list of {"role": str, "content": str}

# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------
st.title("🌿 Smart Home Green Planner")
st.markdown(
    "Enter your home details, pick today's weather, and get a personalised "
    "solar energy breakdown — plus a smart assistant to guide you."
)
st.divider()

# ---------------------------------------------------------------------------
# 5 Tabs — each delegates entirely to its pages_content module
# ---------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Home Details",
    "⚡ Energy Breakdown",
    "📈 Comparison Chart",
    "📅 Weekly Trend",
    "💡 Recommendation",
])

with tab1:
    pg_home.render()

with tab2:
    pg_energy.render()

with tab3:
    pg_chart.render()

with tab4:
    pg_trend.render()

with tab5:
    pg_rec.render()

# ---------------------------------------------------------------------------
# Persistent sidebar — AI Smart Home Assistant
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🤖 Your Smart Home Assistant")
    st.markdown(
        "👋 Hi! I'm here to help. May I assist you with your energy plan today?"
    )
    st.divider()

    # Render chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask me about your energy plan…")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        response = get_response(user_input, st.session_state.result)

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

    st.divider()
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.divider()
st.caption("Smart Home Green Planner · Built with Streamlit · College Project Demo")
