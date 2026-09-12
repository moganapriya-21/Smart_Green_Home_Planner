# pages_content/weekly_trend.py
# Tab 4 — Weekly Trend: 7-day simulated line chart.

import streamlit as st
import pandas as pd
from utils.weekly_trend import simulate_weekly_trend


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
    """Render the Weekly Trend tab."""

    st.subheader("📅 7-Day Energy Trend")

    if st.session_state.result is None:
        _no_results()
        return

    r = st.session_state.result

    trend = simulate_weekly_trend(
        solar_generation_kWh=r["solar_generation_kWh"],
        consumption_kWh=r["consumption_kWh"],
    )

    # Disclaimer banner
    st.info(trend["note"])
    st.markdown("")

    # Build a tidy DataFrame for the line chart
    df = pd.DataFrame(
        {
            "Solar Generation (kWh)": trend["generation"],
            "Home Consumption (kWh)": trend["consumption"],
            "Grid Reliance (kWh)":    trend["grid_reliance"],
        },
        index=trend["days"],
    )

    st.line_chart(df)

    # Quick summary below the chart
    avg_gen  = round(sum(trend["generation"])  / 7, 2)
    avg_cons = round(sum(trend["consumption"]) / 7, 2)
    avg_grid = round(sum(trend["grid_reliance"]) / 7, 2)

    st.markdown("**7-day averages (simulated)**")
    s1, s2, s3 = st.columns(3)
    with s1:
        st.metric("Avg Solar", f"{avg_gen:.1f} kWh")
    with s2:
        st.metric("Avg Consumption", f"{avg_cons:.1f} kWh")
    with s3:
        st.metric("Avg Grid Reliance", f"{avg_grid:.1f} kWh")
