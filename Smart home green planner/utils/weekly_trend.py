# utils/weekly_trend.py
# Simulates a 7-day energy trend around today's calculated values.
# Clearly labelled as simulated / illustrative data.
# No Streamlit imports — pure Python calculation.

import random
from datetime import date, timedelta

# Variation applied to each daily value (±fraction of the base value)
GENERATION_JITTER = 0.18   # ±18 % variation in solar generation day to day
CONSUMPTION_JITTER = 0.10  # ±10 % variation in consumption day to day


def simulate_weekly_trend(
    solar_generation_kWh: float,
    consumption_kWh: float,
    seed: int = 42,
) -> dict:
    """
    Produce a simulated 7-day trend centred on today's calculated values.

    The values are deterministic for a given seed so the chart doesn't
    jump on every Streamlit re-run.

    Parameters:
        solar_generation_kWh (float): Today's solar generation (kWh).
        consumption_kWh      (float): Today's consumption (kWh).
        seed                 (int):   Random seed for reproducibility.

    Returns:
        dict with keys:
            days         (list[str])   — "Mon", "Tue", … labels (7 items)
            generation   (list[float]) — simulated daily solar generation
            consumption  (list[float]) — simulated daily consumption
            grid_reliance(list[float]) — max(0, consumption - generation)
            note         (str)         — disclaimer that data is simulated
    """
    rng = random.Random(seed)
    today = date.today()

    days        = []
    generation  = []
    consumption = []
    grid_reliance = []

    for offset in range(-6, 1):          # past 6 days + today
        day = today + timedelta(days=offset)
        days.append(day.strftime("%a %d"))

        # Apply symmetric random jitter
        gen  = round(max(0.0, solar_generation_kWh * (1 + rng.uniform(-GENERATION_JITTER,  GENERATION_JITTER))), 2)
        cons = round(max(0.1, consumption_kWh      * (1 + rng.uniform(-CONSUMPTION_JITTER, CONSUMPTION_JITTER))), 2)
        grid = round(max(0.0, cons - gen), 2)

        generation.append(gen)
        consumption.append(cons)
        grid_reliance.append(grid)

    return {
        "days":          days,
        "generation":    generation,
        "consumption":   consumption,
        "grid_reliance": grid_reliance,
        "note": (
            "⚠️ Simulated data — values are illustrative variations around "
            "today's calculated figures and do not reflect actual historical readings."
        ),
    }
