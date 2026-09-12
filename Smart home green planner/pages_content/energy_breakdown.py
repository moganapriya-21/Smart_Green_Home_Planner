# pages_content/energy_breakdown.py
# Tab 2 — Energy Breakdown: metric cards, cost summary, CO2 footprint.

import streamlit as st
from utils.cost_calculator import calculate_costs
from utils.co2_tracker import calculate_co2

WEATHER_LABELS = {"sunny": "☀️ Sunny", "cloudy": "☁️ Cloudy", "rainy": "🌧️ Rainy"}


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
    """Render the Energy Breakdown tab."""

    st.subheader("⚡ Energy Breakdown")

    if st.session_state.result is None:
        _no_results()
        return

    r = st.session_state.result

    st.markdown(
        f"Results for **{WEATHER_LABELS[r['weather_condition']]}** weather · "
        "Values are daily estimates based on your home details."
    )
    st.markdown("")

    # ── Energy metric cards ──────────────────────────────────────────────────
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(
            label="☀️ Solar Generation",
            value=f"{r['solar_generation_kWh']:.1f} kWh",
            help="Estimated energy your solar panels will produce today.",
        )
    with m2:
        st.metric(
            label="🏠 Home Consumption",
            value=f"{r['consumption_kWh']:.1f} kWh",
            help="Estimated total energy your household will use today.",
        )
    with m3:
        st.metric(
            label="🔌 Grid Reliance",
            value=f"{r['grid_reliance_kWh']:.1f} kWh",
            help="How much extra energy you'll need to draw from the grid.",
        )

    # Coverage note
    solar = r["solar_generation_kWh"]
    cons  = r["consumption_kWh"]
    grid  = r["grid_reliance_kWh"]
    pct   = (solar / cons * 100) if cons > 0 else 0.0

    if grid <= 0:
        st.info("🌟 Your panels cover **100%** of today's energy needs. Any surplus is available for battery storage or grid export.")
    else:
        st.info(
            f"☀️ Solar covers **{pct:.0f}%** of today's consumption. "
            f"The remaining **{grid:.1f} kWh** ({100 - pct:.0f}%) will come from the grid."
        )

    st.divider()

    # ── Cost summary ─────────────────────────────────────────────────────────
    st.markdown("#### 💰 Electricity Cost Estimate")
    costs = calculate_costs(grid)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(
            label="Today's Grid Cost",
            value=f"₹{costs['daily_cost_inr']:.0f}",
            help="Cost of today's grid electricity at ₹8/kWh.",
        )
    with c2:
        st.metric(
            label="Monthly Estimate",
            value=f"₹{costs['monthly_cost_inr']:.0f}",
            help="Projected monthly electricity bill (daily × 30).",
        )
    with c3:
        st.metric(
            label="Saving per Extra Panel",
            value=f"₹{costs['monthly_savings_per_panel_inr']:.0f}/mo",
            help="Estimated monthly saving by adding one more solar panel.",
        )

    st.divider()

    # ── CO2 footprint ────────────────────────────────────────────────────────
    st.markdown("#### 🌍 CO₂ Footprint")
    co2 = calculate_co2(grid, solar)

    d1, d2, d3 = st.columns(3)
    with d1:
        st.metric(
            label="Grid CO₂ Emitted",
            value=f"{co2['grid_co2_kg']:.2f} kg",
            help="CO₂ emitted from today's grid electricity use (0.82 kg/kWh).",
        )
    with d2:
        st.metric(
            label="CO₂ Saved by Solar",
            value=f"{co2['solar_co2_saved_kg']:.2f} kg",
            help="CO₂ avoided by generating from solar instead of the grid.",
        )
    with d3:
        st.metric(
            label="Car Equivalent",
            value=f"{co2['car_km_equivalent']:.1f} km",
            help="Equivalent km driven in a petrol car for today's grid CO₂.",
        )
