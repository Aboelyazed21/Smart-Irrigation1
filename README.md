# CSC4103 Intelligent Systems — Practical Sheet 1 (Parts B + C)

**Foundations and Applications of Intelligent Systems** — Prof. Abdel-Rahman Hedar, BUA, Fall 2026

Solved: Exercise 1 (robust controller) + Exercise 2 (human-in-the-loop gate) + Exercise 3 (L0–L3 autonomy) + Part C Mini-Project (Smart Irrigation System).

## Structure

```text
CSC4103_PS01/
├── ps01/
│   ├── ex1_robust_controller.py   # Ex1: naive vs Kalman-style filtered (σ=0.05,0.15,0.25 × 30 runs)
│   ├── ex2_human_approval.py     # Ex2: risk gate, 20 proposals, escalation rate
│   ├── ex3_autonomy_levels.py     # Ex3: thermostat L0–L3, tests at 22/27/38°C
│   └── irrigation.py              # Part C: Field + SmartIrrigator, 90 days × 25 seeds vs timer
├── assets/                        # generated figures (ex1, Part C trajectory/water/architecture)
├── CSC4103_PS01_PartsBC_Report.pdf
├── make_assets.py                 # regenerates assets/*.png
├── build_report.py                # regenerates the PDF (reportlab)
└── requirements.txt
```

## Run

```bash
cd ps01
python ex1_robust_controller.py
python ex2_human_approval.py
python ex3_autonomy_levels.py
python irrigation.py
```

Requirements: `pip install -r requirements.txt` (numpy, matplotlib, reportlab).

## Headline results (measured, seeded)

| Task | Result |
|---|---|
| Ex1 σ=0.05 | stress 1.17 → **0.07** d/60d, water +1.1% |
| Ex1 σ=0.15 | stress 2.30 → **0.63** d/60d, water −1.0% |
| Ex1 σ=0.25 | stress 1.60 → **1.07** d/60d, water −4.2% |
| Ex2 τ=0.50 | escalation **55%** (9 auto / 11 escalated: 2 approved, 9 rejected) |
| Ex3 | 22°C HOLD, 27°C COOL, 38°C takeover / safe-mode (no silent action) |
| Part C 90d×25 | timer 5.40 water / 0.00 stress → smart **2.95 / 0.24** (−45.4% water, ≈zero stress) |

Full tables, figures, 12-element case study, and discussion: see `CSC4103_PS01_PartsBC_Report.pdf`.
