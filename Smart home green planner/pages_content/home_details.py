# pages_content/home_details.py
# Tab 1 — Home Details input form.

import streamlit as st
from utils.energy_calculator import predict_energy_needs

WEATHER_LABELS = {"sunny": "☀️ Sunny", "cloudy": "☁️ Cloudy", "rainy": "🌧️ Rainy"}


def render() -> None:
    """Render the Home Details tab: form inputs + calculate button."""

    st.subheader("🏡 Tell us about your home")
    st.markdown(
        "Fill in the details below and press **Calculate** to generate your energy plan."
    )

    with st.form("home_details_form"):

        # Row 1 — home size and family members
        col_a, col_b = st.columns(2)
        with col_a:
            home_sq_ft = st.number_input(
                "Home size (sq ft)",
                min_value=100,
                max_value=10_000,
                value=1500,
                step=50,
                help="Total floor area of your home in square feet.",
            )
        with col_b:
            num_members = st.number_input(
                "Family members",
                min_value=1,
                max_value=20,
                value=2,
                step=1,
                help="Number of people living in the household.",
            )

        # Row 2 — solar panels
        num_panels = st.number_input(
            "Solar panels installed",
            min_value=0,
            max_value=100,
            value=10,
            step=1,
            help="Number of solar panels on your roof. Enter 0 if you have none.",
        )

        # Row 3 — weather selection
        st.markdown("**Today's weather condition**")
        st.caption("Click a weather button to select it — the form will recalculate instantly.")
        w1, w2, w3 = st.columns(3)
        with w1:
            sunny_btn  = st.form_submit_button("☀️  Sunny",  use_container_width=True)
        with w2:
            cloudy_btn = st.form_submit_button("☁️  Cloudy", use_container_width=True)
        with w3:
            rainy_btn  = st.form_submit_button("🌧️  Rainy",  use_container_width=True)

        st.markdown("")

        # Main calculate button
        calculate = st.form_submit_button(
            "⚡  Calculate my energy plan",
            use_container_width=False,
        )

    # -- Resolve weather selection --
    if sunny_btn:
        st.session_state.weather = "sunny"
    elif cloudy_btn:
        st.session_state.weather = "cloudy"
    elif rainy_btn:
        st.session_state.weather = "rainy"

    selected_condition = st.session_state.weather

    # -- Run calculation on any form submission --
    if calculate or sunny_btn or cloudy_btn or rainy_btn:
        try:
            st.session_state.result = predict_energy_needs(
                st.session_state.weather,
                home_sq_ft=home_sq_ft,
                num_panels=num_panels,
                num_members=num_members,
            )
        except ValueError as e:
            st.error(str(e))

    # -- Status caption --
    st.caption(
        f"Selected: **{WEATHER_LABELS[selected_condition]}** · "
        f"{int(home_sq_ft):,} sq ft · {int(num_panels)} panels · "
        f"{int(num_members)} {'person' if num_members == 1 else 'people'}"
    )

    # -- Success confirmation once results exist --
    if st.session_state.result is not None:
        r = st.session_state.result
        st.success(
            f"✅ Plan calculated!  Solar: **{r['solar_generation_kWh']:.1f} kWh** · "
            f"Consumption: **{r['consumption_kWh']:.1f} kWh** · "
            f"Grid: **{r['grid_reliance_kWh']:.1f} kWh**  "
            "— Switch to the other tabs to explore your results."
        )
