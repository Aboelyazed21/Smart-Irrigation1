"""
CSC4103 Intelligent Systems | Practical Sheet 1
Exercise 3 — Levels of autonomy L0–L3: thermostat (10 marks)

One function `thermostat(temp_c, level, human_available)` implements:
  L0 MANUAL     : never acts; only reports + suggests (human does everything).
  L1 ASSISTED   : suggests an action, asks for confirmation, human executes.
  L2 PARTIAL    : acts automatically INSIDE safe envelope [10,35]C;
                  outside -> escalates for confirmation (no silent action).
  L3 CONDITIONAL: acts automatically; if temp outside [10,35]C it requests
                  human takeover; if no human available -> SAFE MODE
                  (HVAC off + alert) instead of acting blindly.

Comfort band: 20–24 C (heat if <20, cool if >24, hold otherwise).
Safety envelope: [10, 35] C per the sheet.

Test: temps {22, 27, 38} C x levels {L0..L3}, plus L3 with/without human at 38C.
"""
from __future__ import annotations

SAFE_LO, SAFE_HI = 10.0, 35.0
COMFORT_LO, COMFORT_HI = 20.0, 24.0

LEVELS = {
    0: "L0-MANUAL (human does all)",
    1: "L1-ASSISTED (system suggests, human confirms/executes)",
    2: "L2-PARTIAL (auto inside safe envelope, escalate outside)",
    3: "L3-CONDITIONAL (auto + human takeover outside envelope; safe-mode fallback)",
}


def comfort_action(temp_c: float) -> str:
    if temp_c < COMFORT_LO:
        return f"HEAT to {COMFORT_LO:.0f}C"
    if temp_c > COMFORT_HI:
        return f"COOL to {COMFORT_HI:.0f}C"
    return "HOLD (comfort OK)"


def thermostat(temp_c: float, level: int, human_available: bool = True) -> dict:
    """Single thermostat implementing L0..L3. Returns {action, authority, message}."""
    if level not in (0, 1, 2, 3):
        raise ValueError("level must be 0..3")
    suggestion = comfort_action(temp_c)
    in_envelope = SAFE_LO <= temp_c <= SAFE_HI

    if level == 0:
        return {"action": "NO-ACTION",
                "authority": "human",
                "message": f"L0 @ {temp_c}C: display {temp_c}C, suggest [{suggestion}]; operator must act."}
    if level == 1:
        return {"action": "AWAITING-CONFIRMATION",
                "authority": "human (system advises)",
                "message": f"L1 @ {temp_c}C: recommend [{suggestion}]; execute only after human confirms."}
    if level == 2:
        if in_envelope:
            return {"action": suggestion,
                    "authority": "system (supervised)",
                    "message": f"L2 @ {temp_c}C: inside [{SAFE_LO:.0f},{SAFE_HI:.0f}] -> auto [{suggestion}]."}
        return {"action": "ESCALATED — no auto action",
                "authority": "human",
                "message": f"L2 @ {temp_c}C: OUTSIDE safe envelope -> escalate, await human (no silent action)."}
    # L3
    if in_envelope:
        return {"action": suggestion,
                "authority": "system (conditional)",
                "message": f"L3 @ {temp_c}C: nominal -> auto [{suggestion}]; human on standby."}
    if human_available:
        return {"action": "HUMAN-TAKEOVER-REQUESTED",
                "authority": "human (takeover)",
                "message": f"L3 @ {temp_c}C: OUTSIDE envelope -> REQUEST HUMAN TAKEOVER; hold last safe state meanwhile."}
    return {"action": "SAFE-MODE (HVAC OFF + ALERT)",
            "authority": "system fail-safe",
            "message": f"L3 @ {temp_c}C: OUTSIDE envelope + NO HUMAN -> SAFE MODE (HVAC off, alert sent)."}


def main():
    print("=" * 86)
    print("Exercise 3 — Levels of autonomy (thermostat, safe envelope [10,35]C)")
    print("=" * 86)
    for temp in [22, 27, 38]:
        print(f"\n-- temp = {temp}C --")
        for lvl in [0, 1, 2, 3]:
            # at 38C also show the no-human fallback for L3
            r = thermostat(float(temp), lvl, human_available=True)
            print(f"  {LEVELS[lvl].split(' ')[0]:3s} | action={r['action']:32s} | {r['message']}")
        if temp == 38:
            r = thermostat(38.0, 3, human_available=False)
            print(f"  L3* | action={r['action']:32s} | {r['message']}  [human_available=False]")
    print("\nDiscussion: autonomy rises L0->L3 (human load falls, speed rises) but so does")
    print("responsibility risk. The envelope guard is the key: L2 never acts outside it,")
    print("L3 explicitly hands over or fails safe. 22C=HOLD at every auto level; 27C=COOL;")
    print("38C=unsafe -> must NOT auto-cool blindly (compressor/pipe risk), hence takeover/safe-mode.")
    print("=" * 86)


if __name__ == "__main__":
    main()
