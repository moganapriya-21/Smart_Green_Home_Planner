# utils/chat_assistant.py
# Rule-based response logic for the sidebar AI assistant.
# Reads live values from a result dict; no Streamlit imports.


def get_response(user_input: str, result: dict | None) -> str:
    """
    Return a plain-text (Markdown-safe) assistant response.

    Parameters:
        user_input (str):        Raw message typed by the user.
        result     (dict|None):  st.session_state.result — None if not yet calculated.

    Returns:
        str: Markdown-formatted assistant reply.
    """
    q = user_input.strip().lower()

    # ── No results yet ───────────────────────────────────────────────────────
    if result is None:
        return (
            "It looks like you haven't calculated your energy plan yet. "
            "Head over to the **🏠 Home Details** tab, fill in your details, "
            "and press **⚡ Calculate** — then I can give you personalised answers! 😊"
        )

    # Unpack common values once
    solar  = result["solar_generation_kWh"]
    cons   = result["consumption_kWh"]
    grid   = result["grid_reliance_kWh"]
    weather = result["weather_condition"]
    pct_solar = (solar / cons * 100) if cons > 0 else 0.0

    # ── Green score (check before CO2 branch which also matches "green") ─────
    if any(kw in q for kw in ["green score", "score", "badge", "champion", "rating"]):
        score = min(100, round((solar / cons * 100) if cons > 0 else 100))
        if score >= 80:
            badge = "🌟 Eco Champion"
        elif score >= 50:
            badge = "🌿 Green Achiever"
        else:
            badge = "🌱 Getting Started"
        return (
            f"Your current Green Score is **{score}/100** — {badge}. "
            "The score measures what percentage of your consumption is covered by solar. "
            "Boost it by adding panels or reducing consumption on cloudy and rainy days."
        )

    # ── Grid reliance ────────────────────────────────────────────────────────
    if any(kw in q for kw in ["grid", "grid reliance", "why is my grid", "high grid"]):
        if grid <= 0:
            return (
                "Your grid reliance is **zero** right now — your solar panels "
                f"generate **{solar:.1f} kWh**, which fully covers your "
                f"**{cons:.1f} kWh** consumption. Excellent! 🌞"
            )
        return (
            f"Your grid reliance is **{grid:.1f} kWh** because your panels only generate "
            f"**{solar:.1f} kWh** ({pct_solar:.0f}% of needs), while your home consumes "
            f"**{cons:.1f} kWh** today under **{weather}** conditions. "
            "Adding more panels or shifting heavy appliance use to peak solar hours can help."
        )

    # ── Energy saving tips ───────────────────────────────────────────────────
    if any(kw in q for kw in ["save energy", "reduce", "cut", "lower consumption", "tips", "advice"]):
        return (
            "Here are practical ways to cut your energy use:\n\n"
            "- 🕙 Run appliances (dishwasher, washing machine) **10am–3pm** when solar peaks\n"
            "- 💡 Replace all bulbs with **LED lights** (up to 80% less energy)\n"
            "- 🌡️ Drop your thermostat **1–2 °C** — saves ~10% on heating\n"
            "- 🔌 **Unplug idle devices** — standby power drains silently 24/7\n"
            "- 🔋 A **home battery** stores surplus solar for evening use"
        )

    # ── Cost ─────────────────────────────────────────────────────────────────
    if any(kw in q for kw in ["cost", "bill", "money", "rupee", "₹", "price", "expensive"]):
        daily  = round(grid * 8.0, 2)
        monthly = round(daily * 30, 2)
        return (
            f"At ₹8/kWh your grid draw of **{grid:.1f} kWh** costs roughly "
            f"**₹{daily:.0f} today** and **₹{monthly:.0f}/month**. "
            "Each extra solar panel saves about ₹5.60/day (₹168/month) on your bill."
        )

    # ── CO2 / environment ────────────────────────────────────────────────────
    if any(kw in q for kw in ["co2", "carbon", "emission", "environment", "footprint", "green", "eco"]):
        grid_co2  = round(grid  * 0.82, 2)
        solar_saved = round(solar * (0.82 - 0.05), 2)
        car_km    = round(grid_co2 * 4.6, 1)
        return (
            f"Your grid usage emits about **{grid_co2:.2f} kg CO₂** today "
            f"(≈ driving **{car_km:.0f} km** in a petrol car). "
            f"Meanwhile your solar panels are saving **{solar_saved:.2f} kg CO₂** "
            "compared to drawing the same energy from the grid. 🌍"
        )

    # ── Recommendation ───────────────────────────────────────────────────────
    if any(kw in q for kw in ["recommendation", "what does", "mean", "explain"]):
        return (
            f"Your recommendation is colour-coded by how much grid power you need:\n\n"
            f"- 🟢 **Green**: Solar covers 100% — no grid needed\n"
            f"- 🟡 **Yellow**: Moderate — up to 40% of consumption from grid\n"
            f"- 🔴 **Red**: High reliance — more than 40% from grid\n\n"
            f"Today you're drawing **{grid:.1f} kWh** ({100 - pct_solar:.0f}% of needs) from the grid."
        )

    # ── Solar / generation ───────────────────────────────────────────────────
    if any(kw in q for kw in ["solar", "panels", "generation", "how much solar"]):
        return (
            f"Your panels generate an estimated **{solar:.1f} kWh** today under "
            f"**{weather}** conditions. "
            "Output scales directly with panel count — a 10-panel system produces ~7 kWh on a sunny day."
        )

    # ── Consumption ──────────────────────────────────────────────────────────
    if any(kw in q for kw in ["consumption", "use", "how much energy", "using"]):
        return (
            f"Your home consumes an estimated **{cons:.1f} kWh** today. "
            "This accounts for your home size, number of family members, "
            "and weather (more lighting and heating on cloudy/rainy days)."
        )

    # ── Greetings ────────────────────────────────────────────────────────────
    if any(kw in q for kw in ["hello", "hi", "hey", "good morning", "good afternoon"]):
        return (
            "Hello! 👋 I'm your Smart Home Assistant. I can help with:\n\n"
            "- Grid reliance questions\n"
            "- Energy saving tips\n"
            "- Cost & bill estimates\n"
            "- CO₂ footprint\n"
            "- Your Green Score\n\n"
            "What would you like to know?"
        )

    # ── Thanks ───────────────────────────────────────────────────────────────
    if any(kw in q for kw in ["thank", "thanks", "cheers", "great", "awesome"]):
        return "You're welcome! 😊 Feel free to ask anything else about your energy plan."

    # ── Fallback ─────────────────────────────────────────────────────────────
    return (
        "I'm not sure about that — here are things I can help with:\n\n"
        "- *Why is my grid reliance high?*\n"
        "- *How can I save energy?*\n"
        "- *What is my electricity cost?*\n"
        "- *What is my CO₂ footprint?*\n"
        "- *What is my Green Score?*\n"
        "- *What does the recommendation mean?*\n\n"
        "Try rephrasing or pick one of the above!"
    )
