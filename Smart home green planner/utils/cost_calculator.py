# utils/cost_calculator.py
# Electricity cost calculations based on grid reliance.
# No Streamlit imports — pure Python calculation.

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
RATE_PER_KWH      = 8.0    # ₹ per kWh — standard Indian residential tariff
DAYS_PER_MONTH    = 30
EXTRA_PANEL_KWH   = 0.7    # kWh saved per additional panel per day (sunny baseline)


def calculate_costs(grid_reliance_kWh: float, num_panels: int = 0) -> dict:
    """
    Calculate daily/monthly electricity costs and potential savings.

    Parameters:
        grid_reliance_kWh (float): kWh drawn from the grid today.
        num_panels (int):          Current number of solar panels installed.

    Returns:
        dict with keys:
            daily_cost_inr        — today's grid electricity cost (₹)
            monthly_cost_inr      — estimated monthly cost (₹)
            savings_per_panel_inr — daily ₹ saved by adding one more panel
            monthly_savings_per_panel_inr
    """
    daily_cost   = round(grid_reliance_kWh * RATE_PER_KWH, 2)
    monthly_cost = round(daily_cost * DAYS_PER_MONTH, 2)

    # Marginal saving from one extra panel
    panel_daily_saving   = round(EXTRA_PANEL_KWH * RATE_PER_KWH, 2)
    panel_monthly_saving = round(panel_daily_saving * DAYS_PER_MONTH, 2)

    return {
        "daily_cost_inr":               daily_cost,
        "monthly_cost_inr":             monthly_cost,
        "savings_per_panel_inr":        panel_daily_saving,
        "monthly_savings_per_panel_inr": panel_monthly_saving,
    }
