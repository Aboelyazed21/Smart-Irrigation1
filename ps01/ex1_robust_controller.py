"""
CSC4103 Intelligent Systems | Practical Sheet 1
Exercise 1 — A robust controller for noisy sensors (10 marks)

Compares:
  * NAIVE controller : trusts every noisy reading  irr = max(0, TARGET - z) * 0.9
  * FILTERED controller (complementary / steady-state Kalman idea):
        pred  = m_hat - AVG_EVAP + last_irr        (simple process model)
        m_hat = pred + K(sigma) * (z - pred)       (fuse prediction + measurement)
        irr   = max(0, TARGET + margin(sigma) - m_hat) * 1.0

K(sigma) = P/(P+R), R = sigma^2, clipped to [0.30, 0.70] (trust model more
when the sensor is noisier). margin(sigma) = 0.02 + 0.35*sigma is an
uncertainty-proportional safety stock: the noisier the sensor, the more
cautiously high we aim. Gain 1.0 compensates filter lag.

Protocol (fair, paired): sigma in {0.05, 0.15, 0.25}, 30 seeds each,
60 days per run, identical weather per seed for both controllers.
Metrics: mean ± std of total water used and crop-stress days (m < 0.35).

Author: CSC4103 Lab solution — reproducible (fixed seeds).
"""
from __future__ import annotations

import numpy as np

TARGET = 0.50
NAIVE_GAIN = 0.9
FILT_GAIN = 1.0
AVG_EVAP = 0.055               # mean of Uniform(0.02, 0.09)
PROCESS_VAR = 0.01             # assumed process variance for Kalman-style gain
DAYS = 60
STRESS_THRESHOLD = 0.35
SIGMAS = [0.05, 0.15, 0.25]
N_RUNS = 30


def kalman_gain(noise_sigma: float) -> float:
    """Steady-state gain K = P/(P+R), clipped to [0.30, 0.70]."""
    R = noise_sigma ** 2
    K = PROCESS_VAR / (PROCESS_VAR + R + 1e-12)
    return float(np.clip(K, 0.30, 0.70))


def safety_margin(noise_sigma: float) -> float:
    """Uncertainty-proportional safety stock."""
    return 0.02 + 0.35 * noise_sigma


def run_naive(noise_sigma: float, seed: int, days: int = DAYS):
    """Naive feedback controller trusting the raw noisy reading."""
    rng = np.random.default_rng(seed)
    m, water, stress = 0.55, 0.0, 0
    for _ in range(days):
        heat = rng.uniform(0.02, 0.09)
        z = m + rng.normal(0, noise_sigma)          # noisy sensor
        irr = max(0.0, TARGET - z) * NAIVE_GAIN
        m = min(1.0, m - heat + irr)                # (same dynamics as Sheet Ex.3: evaporation only)
        water += irr
        stress += m < STRESS_THRESHOLD
    return water, stress


def run_filtered(noise_sigma: float, seed: int, days: int = DAYS):
    """Filtered controller: process-model prediction + measurement fusion."""
    rng = np.random.default_rng(seed)
    K = kalman_gain(noise_sigma)
    margin = safety_margin(noise_sigma)
    m, m_hat = 0.55, 0.55
    last_irr = 0.0
    water, stress = 0.0, 0
    for _ in range(days):
        heat = rng.uniform(0.02, 0.09)
        z = m + rng.normal(0, noise_sigma)
        # -- perceive (estimate) --
        pred = m_hat - AVG_EVAP + last_irr
        pred = float(np.clip(pred, 0.0, 1.0))
        m_hat = pred + K * (z - pred)
        m_hat = float(np.clip(m_hat, 0.0, 1.0))
        # -- decide --
        irr = max(0.0, (TARGET + margin) - m_hat) * FILT_GAIN
        # -- act (environment step) --
        m = min(1.0, m - heat + irr)
        last_irr = irr
        water += irr
        stress += m < STRESS_THRESHOLD
    return water, stress


def evaluate():
    print("=" * 78)
    print("Exercise 1 — Robust vs Naive controller (60 days, 30 runs per sigma)")
    print("=" * 78)
    print(f"TARGET={TARGET}  AVG_EVAP={AVG_EVAP}  FILT_GAIN={FILT_GAIN}")
    print("K(sigma), margin(sigma): " +
          ", ".join(f"s={s:.2f}->K={kalman_gain(s):.3f},m={safety_margin(s):.3f}" for s in SIGMAS))
    print("-" * 78)
    header = f"{'sigma':>6} | {'NAIVE water':>16} | {'NAIVE stress':>16} | {'FILT water':>16} | {'FILT stress':>16}"
    print(header)
    print("-" * len(header))
    results = {}
    for sigma in SIGMAS:
        naive = np.array([run_naive(sigma, s) for s in range(N_RUNS)])
        filt = np.array([run_filtered(sigma, s) for s in range(N_RUNS)])
        results[sigma] = (naive, filt)
        print(f"{sigma:6.2f} | "
              f"{naive[:, 0].mean():6.2f}±{naive[:, 0].std(ddof=1):4.2f}     | "
              f"{naive[:, 1].mean():6.2f}±{naive[:, 1].std(ddof=1):4.2f}     | "
              f"{filt[:, 0].mean():6.2f}±{filt[:, 0].std(ddof=1):4.2f}     | "
              f"{filt[:, 1].mean():6.2f}±{filt[:, 1].std(ddof=1):4.2f}")
    print("-" * 78)
    print("Trade-off summary (filtered vs naive):")
    for sigma in SIGMAS:
        naive, filt = results[sigma]
        dw = (filt[:, 0].mean() - naive[:, 0].mean()) / max(naive[:, 0].mean(), 1e-9) * 100
        ds = naive[:, 1].mean() - filt[:, 1].mean()
        print(f"  sigma={sigma:.2f}: stress reduced by {ds:5.2f} days/run "
              f"({naive[:,1].mean():.2f}->{filt[:,1].mean():.2f}), "
              f"water change {dw:+5.1f}% ({naive[:,0].mean():.2f}->{filt[:,0].mean():.2f})")
    print("=" * 78)
    return results


if __name__ == "__main__":
    evaluate()
