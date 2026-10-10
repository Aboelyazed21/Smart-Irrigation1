"""Generate PNG assets for the PDF report (matplotlib, reproducible)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.insert(0, r"C:\Users\EL.DAWLIA\Downloads\CSC4103_PS01\ps01")
from irrigation import generate_weather, make_forecast, Field, SmartIrrigator, run_timer, run_smart
from ex1_robust_controller import run_naive, run_filtered

ASSETS = r"C:\Users\EL.DAWLIA\Downloads\CSC4103_PS01\assets"

# ---- Ex1 data (30 runs, same as report) ----
sigmas = [0.05, 0.15, 0.25]
naive_w, naive_s, filt_w, filt_s = [], [], [], []
for sig in sigmas:
    n = np.array([run_naive(sig, s) for s in range(30)])
    f = np.array([run_filtered(sig, s) for s in range(30)])
    naive_w.append(n[:, 0].mean()); naive_s.append(n[:, 1].mean())
    filt_w.append(f[:, 0].mean()); filt_s.append(f[:, 1].mean())

x = np.arange(len(sigmas)); wdt = 0.35
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].bar(x - wdt/2, naive_w, wdt, label="Naive")
ax[0].bar(x + wdt/2, filt_w, wdt, label="Filtered (robust)")
ax[0].set_xticks(x); ax[0].set_xticklabels([str(s) for s in sigmas])
ax[0].set_xlabel("Sensor noise sigma"); ax[0].set_ylabel("Mean water (60 days)")
ax[0].set_title("Ex1: water use"); ax[0].legend(); ax[0].grid(axis="y", alpha=0.3)
for i, (a, b) in enumerate(zip(naive_w, filt_w)):
    ax[0].text(i - wdt/2, a + 0.03, f"{a:.2f}", ha="center", fontsize=8)
    ax[0].text(i + wdt/2, b + 0.03, f"{b:.2f}", ha="center", fontsize=8)
ax[1].bar(x - wdt/2, naive_s, wdt, label="Naive")
ax[1].bar(x + wdt/2, filt_s, wdt, label="Filtered (robust)")
ax[1].set_xticks(x); ax[1].set_xticklabels([str(s) for s in sigmas])
ax[1].set_xlabel("Sensor noise sigma"); ax[1].set_ylabel("Mean stress days (60 days)")
ax[1].set_title("Ex1: crop-stress days"); ax[1].legend(); ax[1].grid(axis="y", alpha=0.3)
for i, (a, b) in enumerate(zip(naive_s, filt_s)):
    ax[1].text(i - wdt/2, a + 0.05, f"{a:.2f}", ha="center", fontsize=8)
    ax[1].text(i + wdt/2, b + 0.05, f"{b:.2f}", ha="center", fontsize=8)
fig.suptitle("Exercise 1 — Naive vs Filtered controller (60 days x 30 runs)")
fig.tight_layout()
fig.savefig(f"{ASSETS}/ex1_comparison.png", dpi=160)
print("saved ex1_comparison.png", naive_w, naive_s, filt_w, filt_s)

# ---- Part C trajectory (seed 3: has 1 stress day, illustrative) ----
seed = 3; days = 90
heats, rains = generate_weather(seed, days)
# smart track
srng = np.random.default_rng(seed + 10000); frng = np.random.default_rng(seed + 20000)
field = Field(); agent = SmartIrrigator()
smart_m, smart_d, smart_t = [], [], []
for t in range(days):
    fc = make_forecast(rains[t], frng)
    p = agent.perceive(field.moisture, fc, srng)
    d = agent.decide(p)
    field.step(d, heats[t], rains[t]); agent.last_irr = d
    agent.learn(field.moisture < 0.35)
    smart_m.append(field.moisture); smart_d.append(d); smart_t.append(agent.target)
# timer track
f2 = Field(); timer_m = []
for t in range(days):
    timer_m.append(f2.step(0.12 if t % 2 == 0 else 0.0, heats[t], rains[t]))

fig2, ax2 = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
ax2[0].plot(smart_m, label="Smart moisture", linewidth=1.6)
ax2[0].plot(timer_m, label="Timer moisture", alpha=0.7, linewidth=1.2)
ax2[0].axhline(0.35, color="red", linestyle="--", linewidth=1, label="Stress threshold 0.35")
ax2[0].axhline(0.55, color="green", linestyle=":", linewidth=1, label="Smart initial target 0.55")
rain_days = [i for i in range(days) if rains[i] > 0]
ax2[0].scatter(rain_days, [0.95]*len(rain_days), marker="v", s=18, color="blue", alpha=0.6, label="Rain day")
ax2[0].set_ylabel("Soil moisture"); ax2[0].set_title(f"Part C: 90-day soil moisture (seed={seed}, paired weather)")
ax2[0].legend(ncol=4, fontsize=8); ax2[0].grid(alpha=0.3); ax2[0].set_ylim(0.25, 1.02)
ax2[1].bar(range(days), smart_d, color="teal", alpha=0.8, label="Smart dose")
ax2[1].set_xlabel("Day"); ax2[1].set_ylabel("Irrigation dose")
ax2[1].set_title("Smart daily doses (many micro-doses; skips before forecast rain)")
ax2[1].grid(axis="y", alpha=0.3)
fig2.tight_layout()
fig2.savefig(f"{ASSETS}/partC_trajectory.png", dpi=160)
print("saved partC_trajectory.png")

# ---- Part C water summary bars ----
tm = np.array([[5.40, 0, 45]]);  # timer constant
sm_w, sm_s = 2.95, 0.24
fig3, a3 = plt.subplots(figsize=(6, 4))
a3.bar(["Timer\n5.40 water\n0.00 stress", "Smart\n2.95 water\n0.24 stress"], [5.40, 2.95], color=["#B0B0B0", "#1B7A4D"])
a3.set_ylabel("Mean water (90 days, 25 seeds)")
a3.set_title("Part C: 45.4% water saving, stress ~0")
for i, v in enumerate([5.40, 2.95]):
    a3.text(i, v + 0.08, f"{v:.2f}", ha="center", fontweight="bold")
fig3.tight_layout(); fig3.savefig(f"{ASSETS}/partC_water.png", dpi=160)
print("saved partC_water.png")

# ---- Architecture diagram (simple, clean) ----
fig4, a4 = plt.subplots(figsize=(10, 3.2))
a4.axis("off")
boxes = [
    (0.02, 0.25, 0.16, 0.5, "ENVIRONMENT\nField\nweather+soil", "#DCE6F1"),
    (0.23, 0.25, 0.16, 0.5, "PERCEIVE\nnoisy sensor\n+ Kalman filter\n+ forecast", "#FFF2CC"),
    (0.44, 0.25, 0.16, 0.5, "DECIDE\neffective target\nwait-for-rain\nmax-dose cap", "#E2EFDA"),
    (0.65, 0.25, 0.14, 0.5, "ACT\npump dose\nto field", "#FCE4D6"),
    (0.84, 0.25, 0.14, 0.5, "LEARN\nstress feedback\nadapt target", "#E4DFEC"),
]
for (xx, yy, ww, hh, txt, col) in boxes:
    a4.add_patch(plt.Rectangle((xx, yy), ww, hh, facecolor=col, edgecolor="#0F3B7A", linewidth=1.4))
    a4.text(xx + ww/2, yy + hh/2, txt, ha="center", va="center", fontsize=8, fontweight="bold")
for i in range(len(boxes)-1):
    x1 = boxes[i][0] + boxes[i][2]; x2 = boxes[i+1][0]
    a4.annotate("", xy=(x2, 0.5), xytext=(x1, 0.5), arrowprops=dict(arrowstyle="->", color="#0F3B7A", lw=1.6))
a4.text(0.5, 0.88, "Smart Irrigation — Perceive–Decide–Act–Learn loop (knowledge: forecast; feedback: stress days)",
        ha="center", fontsize=9, fontweight="bold", color="#0F3B7A")
a4.text(0.5, 0.08, "Baseline for comparison: fixed timer 0.12 every 2nd day (automation, no sensing)", ha="center", fontsize=8, style="italic")
fig4.tight_layout(); fig4.savefig(f"{ASSETS}/partC_arch.png", dpi=160)
print("saved partC_arch.png")
