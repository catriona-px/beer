# 🍺 Pint or Half? A Computational Approach to a Heated Pub Debate

This repo contains the code for our aims of exploring a simple but loaded question: Half or Pint? Which stays colder...
---

## What It Does

- Simulates how the beer temperature evolves in a pint or half pint over time
- Includes conduction from the ambient air
- Accounts for contact heating from your hand (based on surface area and assumed temperature)
- Adjusts how fast you're drinking depending on how warm the beer is
- Calculates cumulative consumption and average temperatures
- Produces clear plots comparing full and half pints

---

## What's in the Model

The model is run via `simulate_warming_with_conduction`, and includes:

| Parameter                   | Description                                     |
|----------------------------|-------------------------------------------------|
| `T_initial`                | Beer starting temperature (default 4°C)         |
| `T_air`                    | Air temperature (default 30°C)                  |
| `T_hand`                   | Hand temperature (default 37°C)                 |
| `heat_transfer_coefficient`| Convective heat transfer from air               |
| `heat_transfer_coefficient_hand` | Convective heat transfer from hand     |
| `glass_thermal_conductivity`| Conductive heating through glass               |
| `glass_thickness`          | Wall thickness of the glass                     |
| `consumption_rate_function`| Variable drinking speed, depending on beer temp|

The simulation runs with small time steps (default: 0.0001 minutes = 0.006 s) for better accuracy.

---

## Output

After 30 minutes of simulated pub time (or more, if you're that way inclined), you'll get:

- A plot showing:
  - Temperature curves for both pint and half pint
  - Corresponding average temperatures
  - Total "pints" consumed over time
- Optional: fine-grain insight from returned variables (volumes, heights, temperature arrays)

You can adjust the consumption function to experiment with behaviour changes (e.g. drink warmer beer faster or slower, drink less if the beer gets bad, etc.)

---

## 📎 Requirements

- Python 3.x
- `numpy`
- `matplotlib`
