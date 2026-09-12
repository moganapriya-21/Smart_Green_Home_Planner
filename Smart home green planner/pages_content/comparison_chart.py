# pages_content/comparison_chart.py
# Tab 3 — Comparison Chart: bar chart of generation vs consumption.

import streamlit as st
import pandas as pd


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
    """Render the Comparison Chart tab."""

    st.subheader("📈 Generation vs Consumption")

    if st.session_state.result is None:
        _no_results()
        return

    r = st.session_state.result

    st.markdown(
        "The chart compares how much solar energy your panels generate "
        "against your household's total energy consumption today."
    )
    st.markdown("")

    chart_data = pd.DataFrame(
        {"kWh": [r["solar_generation_kWh"], r["consumption_kWh"]]},
        index=["Solar Generation", "Home Consumption"],
    )
    st.bar_chart(chart_data, color="#2e7d32")

    # Surplus / deficit callout
    surplus = r["solar_generation_kWh"] - r["consumption_kWh"]
    if surplus >= 0:
        st.success(
            f"🔋 Solar surplus today: **+{surplus:.1f} kWh** — great for battery charging!"
        )
    else:
        st.warning(
            f"⚡ Energy deficit today: **{surplus:.1f} kWh** needs to come from the grid."
        )
