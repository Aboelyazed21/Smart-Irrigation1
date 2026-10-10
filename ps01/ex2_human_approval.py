"""
CSC4103 Intelligent Systems | Practical Sheet 1
Exercise 2 — Human-in-the-loop approval gate (10 marks)

A smart pump proposes (volume, confidence). An explicit, bounded risk
function decides whether the action auto-executes or escalates to a
(simulated) farmer:

    risk = w_vol * (volume / V_MAX) + w_conf * (1 - confidence),  in [0,1]
    if risk <= TAU: execute automatically
    else:           escalate -> farmer approves / rejects

The farmer is simulated: a careful farmer who approves needed watering
but rejects wasteful/uncertain doses, with a small error rate and
occasional unavailability (then the action is safely rejected/held).

Protocol: 20 proposals (seeded), report escalation rate + outcomes.
Plus a threshold sensitivity sweep TAU in {0.30, 0.50, 0.70}.

Design discussion is printed at the end.
"""
from __future__ import annotations

import numpy as np

V_MAX = 0.20          # max single irrigation dose considered
W_VOL = 0.60          # weight of volume risk
W_CONF = 0.40         # weight of uncertainty risk
TAU = 0.50            # default approval threshold
N_PROPOSALS = 20
SEED = 7


def risk_score(volume: float, confidence: float) -> float:
    """Explicit bounded risk in [0,1]. High volume + low confidence = risky."""
    v = float(np.clip(volume / V_MAX, 0.0, 1.0))
    u = float(np.clip(1.0 - confidence, 0.0, 1.0))
    return float(np.clip(W_VOL * v + W_CONF * u, 0.0, 1.0))


def simulate_farmer(volume: float, confidence: float, rng: np.random.Generator) -> str:
    """
    Simulated farmer policy (ground-truth-ish heuristic + noise):
      - clearly wasteful doses (volume > 0.15 with low confidence) -> usually REJECT
      - small confident doses -> usually APPROVE
      - 10% human error flip; 5% farmer unavailable -> HOLD (safe reject).
    """
    if rng.random() < 0.05:
        return "HOLD (farmer unavailable -> safe reject)"
    if volume > 0.15 and confidence < 0.6:
        approve_prob = 0.15
    elif volume <= 0.08 and confidence >= 0.6:
        approve_prob = 0.95
    else:
        approve_prob = 0.60
    # 10% trembling-hand error
    if rng.random() < 0.10:
        approve_prob = 1.0 - approve_prob
    return "APPROVED by farmer" if rng.random() < approve_prob else "REJECTED by farmer"


def generate_proposals(n: int = N_PROPOSALS, seed: int = SEED):
    rng = np.random.default_rng(seed)
    volumes = rng.uniform(0.02, 0.20, size=n).round(3)
    confidences = rng.uniform(0.35, 0.98, size=n).round(2)
    return volumes, confidences


def run_gate(threshold: float = TAU, seed: int = SEED, verbose: bool = True):
    volumes, confidences = generate_proposals(seed=seed)
    rng = np.random.default_rng(seed + 1000)  # independent farmer stream
    rows = []
    n_auto = n_esc = n_approved = n_rejected = 0
    for i, (v, c) in enumerate(zip(volumes, confidences), start=1):
        r = risk_score(float(v), float(c))
        if r <= threshold:
            decision = "AUTO-EXECUTE"
            n_auto += 1
        else:
            decision = simulate_farmer(float(v), float(c), rng)
            n_esc += 1
            if "APPROVED" in decision:
                n_approved += 1
            else:
                n_rejected += 1
        rows.append((i, float(v), float(c), r, decision))
    esc_rate = n_esc / len(rows)
    if verbose:
        print(f"\n--- Approval gate | TAU={threshold:.2f} | seed={seed} ---")
        print(f"{'#':>3} {'vol':>6} {'conf':>6} {'risk':>6}  decision")
        for i, v, c, r, d in rows:
            flag = " *" if "AUTO" not in d else "  "
            print(f"{i:3d} {v:6.3f} {c:6.2f} {r:6.3f}  {d}{flag if 'HOLD' in d or 'REJECT' in d else ''}")
        print(f"=> auto={n_auto}, escalated={n_esc}, approved={n_approved}, "
              f"rejected/held={n_rejected}, ESCALATION RATE={esc_rate:.1%}")
    return {"threshold": threshold, "auto": n_auto, "escalated": n_esc,
            "approved": n_approved, "rejected": n_rejected, "esc_rate": esc_rate, "rows": rows}


def main():
    print("=" * 78)
    print("Exercise 2 — Human-in-the-loop approval gate (20 proposals)")
    print(f"risk = {W_VOL}*(vol/{V_MAX}) + {W_CONF}*(1-conf) in [0,1]; default TAU={TAU}")
    print("=" * 78)
    run_gate(TAU, verbose=True)
    print("\n--- Threshold sensitivity (design parameter) ---")
    for tau in [0.30, 0.50, 0.70]:
        s = run_gate(tau, verbose=False)
        print(f"  TAU={tau:.2f}: auto={s['auto']:2d} escalated={s['escalated']:2d} "
              f"(approved {s['approved']}, rejected {s['rejected']})  esc_rate={s['esc_rate']:.1%}")
    print("-" * 78)
    print("Discussion: raising TAU -> fewer escalations (less farmer load, faster loop)")
    print("but more high-risk auto-executions (over-watering / stress risk). Lowering TAU")
    print("-> safer but risks alarm fatigue + delays; farmer becomes the bottleneck.")
    print("TAU=0.50 balances both for this pump (see sweep above).")
    print("=" * 78)


if __name__ == "__main__":
    main()
