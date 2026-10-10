"""
CSC4103 Intelligent Systems | Practical Sheet 1
Part C Mini-Project — Smart Irrigation System (Assiut farm, 90 days)

Architecture:  Field (environment) + SmartIrrigator (agent: perceive/decide/act/learn)
Knowledge used: noisy soil sensor (sigma=0.08) + rain forecast (80% accurate).
  - perceive : complementary/Kalman-style filter fusing process-model
               prediction with the noisy reading; attaches forecast.
  - decide   : deficit irrigation toward an adaptive target; if rain is
               forecast, the effective target is lowered (wait-for-rain).
  - learn    : adapts the moisture target from stress feedback
               (stress -> raise target; long healthy stretch -> lower target
               to save water). Bounded in [0.45, 0.60].
  - act      : clips + applies the dose to the field.

Evaluation: paired comparison vs fixed timer (0.12 every 2nd day) over
>=20 random seeds, 90 days each. Metrics: total water, stress days
(moisture<0.35), pump-on days (dose>0.005).

Reproducible: all randomness is seeded.
"""
from __future__ import annotations

import numpy as np

DAYS = 90
N_SEEDS = 25
NOISE_SIGMA = 0.08
FORECAST_ACCURACY = 0.80
AVG_EVAP = 0.055
STRESS_TH = 0.35
PUMP_TH = 0.005


# ---------------------------------------------------------------- Environment
class Field:
    """Soil-moisture environment. Weather is replayed from a pre-generated series
    so baseline and smart controller face IDENTICAL conditions per seed (fair)."""

    def __init__(self, moisture: float = 0.55):
        self.moisture = moisture
        self.day = 0

    def step(self, irrigation: float, heat: float, rain: float):
        self.moisture = min(1.0, self.moisture - heat + rain + irrigation)
        self.day += 1
        return self.moisture


def generate_weather(seed: int, days: int = DAYS):
    """Fixed weather tape per seed: heat ~ U(0.02,0.09), rain in {0,0.15} (15%)."""
    rng = np.random.default_rng(seed)
    heats = rng.uniform(0.02, 0.09, size=days)
    rains = rng.choice([0.0, 0.15], size=days, p=[0.85, 0.15])
    return heats, rains


def make_forecast(actual_rain: float, rng: np.random.Generator,
                  accuracy: float = FORECAST_ACCURACY) -> bool:
    """80%-accurate binary rain forecast for *today* (given before irrigation)."""
    actual = actual_rain > 0
    return actual if rng.random() < accuracy else (not actual)


# ---------------------------------------------------------------- Agent
class SmartIrrigator:
    """Perceive–Decide–Act–Learn irrigation agent."""

    def __init__(self, target: float = 0.55, gain: float = 1.0,
                 noise_sigma: float = NOISE_SIGMA, k: float = 0.40,
                 forecast_saving: float = 0.05, max_dose: float = 0.16):
        self.target = target
        self.gain = gain
        self.noise_sigma = noise_sigma
        self.k = k                                  # filter gain (Kalman idea)
        self.forecast_saving = forecast_saving      # how much target drops if rain expected
        self.max_dose = max_dose
        self.m_hat = 0.55
        self.last_irr = 0.0
        self.recent_stress: list[int] = []           # rolling feedback window
        self.target_history: list[float] = [target]

    # -- PERCEIVE: noisy sensor + process-model filter + forecast knowledge --
    def perceive(self, true_moisture: float, forecast_rain: bool,
                 sensor_rng: np.random.Generator) -> dict:
        z = true_moisture + sensor_rng.normal(0, self.noise_sigma)
        pred = self.m_hat - AVG_EVAP + self.last_irr
        pred = float(np.clip(pred, 0.0, 1.0))
        self.m_hat = float(np.clip(pred + self.k * (z - pred), 0.0, 1.0))
        return {"m_hat": self.m_hat, "z_raw": float(z),
                "forecast_rain": bool(forecast_rain)}

    # -- DECIDE: deficit rule modulated by forecast knowledge --
    def decide(self, percept: dict) -> float:
        eff_target = self.target - (self.forecast_saving if percept["forecast_rain"] else 0.0)
        dose = max(0.0, eff_target - percept["m_hat"]) * self.gain
        return float(min(dose, self.max_dose))

    def act(self, field: Field, dose: float, heat: float, rain: float) -> float:
        self.last_irr = dose
        return field.step(dose, heat, rain)

    # -- LEARN: adapt target from stress feedback (parameter-level adaptation) --
    def learn(self, stressed: bool):
        self.recent_stress.append(1 if stressed else 0)
        if len(self.recent_stress) > 14:
            self.recent_stress.pop(0)
        if stressed:
            self.target = min(0.62, self.target + 0.012)      # cautious: raise safety stock
        elif len(self.recent_stress) == 14 and sum(self.recent_stress) == 0:
            self.target = max(0.48, self.target - 0.008)      # efficient: relax when healthy
            self.recent_stress = []                           # avoid repeated decay
        self.target_history.append(self.target)


# ---------------------------------------------------------------- Runners
def run_smart(seed: int, days: int = DAYS, track: bool = False):
    heats, rains = generate_weather(seed, days)
    sensor_rng = np.random.default_rng(seed + 10_000)
    fc_rng = np.random.default_rng(seed + 20_000)
    field, agent = Field(), SmartIrrigator()
    water, stress_days, pump_days = 0.0, 0, 0
    traj = [] if track else None
    for t in range(days):
        fc = make_forecast(rains[t], fc_rng)
        percept = agent.perceive(field.moisture, fc, sensor_rng)
        dose = agent.decide(percept)
        field.step(dose, heats[t], rains[t])
        agent.last_irr = dose
        stressed = field.moisture < STRESS_TH
        agent.learn(stressed)
        water += dose
        stress_days += stressed
        pump_days += dose > PUMP_TH
        if track:
            traj.append((field.moisture, dose, agent.target, fc, rains[t]))
    out = {"water": water, "stress": stress_days, "pump_days": pump_days,
           "final_target": agent.target}
    if track:
        out["traj"] = traj
    return out


def run_timer(seed: int, days: int = DAYS):
    heats, rains = generate_weather(seed, days)
    field = Field()
    water, stress_days, pump_days = 0.0, 0, 0
    traj = []
    for t in range(days):
        dose = 0.12 if t % 2 == 0 else 0.0
        field.step(dose, heats[t], rains[t])
        water += dose
        stress_days += field.moisture < STRESS_TH
        pump_days += dose > PUMP_TH
        traj.append(field.moisture)
    return {"water": water, "stress": stress_days, "pump_days": pump_days, "traj": traj}


def evaluate(n_seeds: int = N_SEEDS, days: int = DAYS):
    print("=" * 80)
    print(f"Part C — Smart Irrigation vs Fixed Timer | {days} days x {n_seeds} seeds (paired)")
    print(f"sensor sigma={NOISE_SIGMA}, forecast accuracy={FORECAST_ACCURACY:.0%}, stress< {STRESS_TH}")
    print("=" * 80)
    print(f"{'seed':>5} | {'TIMER wat/str/pump':>22} | {'SMART wat/str/pump':>22} | {'saved':>7}")
    smart_all, timer_all = [], []
    for s in range(n_seeds):
        tm = run_timer(s, days)
        sm = run_smart(s, days)
        smart_all.append([sm["water"], sm["stress"], sm["pump_days"]])
        timer_all.append([tm["water"], tm["stress"], tm["pump_days"]])
        saved = tm["water"] - sm["water"]
        print(f"{s:5d} | {tm['water']:5.2f}/{tm['stress']:3d}/{tm['pump_days']:3d} "
              f"         | {sm['water']:5.2f}/{sm['stress']:3d}/{sm['pump_days']:3d}          | {saved:+6.2f}")
    smart_all = np.array(smart_all)
    timer_all = np.array(timer_all)
    print("-" * 80)
    for name, arr in [("TIMER", timer_all), ("SMART", smart_all)]:
        print(f"{name:6s} mean water={arr[:,0].mean():5.2f}±{arr[:,0].std(ddof=1):4.2f}  "
              f"stress={arr[:,1].mean():5.2f}±{arr[:,1].std(ddof=1):4.2f}  "
              f"pump-days={arr[:,2].mean():5.1f}±{arr[:,2].std(ddof=1):4.1f}")
    w_saved = timer_all[:,0].mean() - smart_all[:,0].mean()
    pct = w_saved / timer_all[:,0].mean() * 100
    print(f"=> SMART saves {w_saved:.2f} water units ({pct:.1f}%) with "
          f"stress {smart_all[:,1].mean():.2f} vs {timer_all[:,1].mean():.2f} days; "
          f"pump-days {smart_all[:,2].mean():.1f} vs {timer_all[:,2].mean():.1f}.")
    print("=" * 80)
    return timer_all, smart_all


if __name__ == "__main__":
    evaluate()
