# pages_content/recommendation.py
# Tab 5 — Recommendation: colour-coded box + Green Score.

import streamlit as st
from utils.green_score import calculate_green_score


def _no_results() -> None:
    st.markdown(
        '<div class="no-results-box">'
        "📋 <strong>No results yet.</strong><br>"
        "Head to the <strong>🏠 Home Details</strong> tab, fill in your home details, "
        "and press <em>⚡ Calculate my energy plan</em> to see results here."
        "</div>",
        unsafe_allow_html=True,
    )


def render() -> None:
    """Render the Recommendation tab."""

    st.subheader("💡 Personalised Recommendation")

    if st.session_state.result is None:
        _no_results()
        return

    r = st.session_state.result

    grid               = r["grid_reliance_kWh"]
    consumption        = r["consumption_kWh"]
    moderate_threshold = consumption * 0.4

    # ── Colour-coded recommendation box ─────────────────────────────────────
    if grid <= 0:
        st.success(r["recommendation"])
    elif grid <= moderate_threshold:
        st.warning(r["recommendation"])
    else:
        st.error(r["recommendation"])

    st.divider()

    # ── Green Score ──────────────────────────────────────────────────────────
    gs = calculate_green_score(r["solar_generation_kWh"], consumption)

    st.markdown("#### 🏆 Your Green Score")

    score_col, badge_col = st.columns([2, 1])
    with score_col:
        st.progress(gs["score"] / 100)
        st.markdown(f"**Score: {gs['score']} / 100**")
    with badge_col:
        st.markdown(
            f"<div style='font-size:1.4rem; font-weight:700; color:#1b5e20; "
            f"padding-top:0.4rem;'>{gs['badge']}</div>",
            unsafe_allow_html=True,
        )

    st.markdown(gs["message"])

    st.divider()

    # ── General green tips ───────────────────────────────────────────────────
    st.markdown("#### 🌱 General Green Tips")

    t1, t2 = st.columns(2)
    with t1:
        st.markdown(
            "- Run dishwashers & washing machines **during peak solar hours** (10am–3pm)\n"
            "- Use a **smart thermostat** to reduce heating/cooling load\n"
            "- Switch to **LED lighting** throughout your home\n"
            "- **Unplug idle devices** — standby power adds up"
        )
    with t2:
        st.markdown(
            "- Charge EVs and batteries **when solar generation is highest**\n"
            "- Install **roof insulation** to cut heating and cooling demands\n"
            "- Consider a **home battery** to store surplus solar energy\n"
            "- Monitor usage with a **smart energy meter**"
        )
