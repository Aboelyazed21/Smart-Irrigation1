"""Build professional PDF report for CSC4103 PS1 Parts B+C (reportlab)."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                Image, PageBreak, HRFlowable, KeepTogether, ListFlowable, ListItem)
from reportlab.lib.colors import HexColor
import os

OUT = r"C:\Users\EL.DAWLIA\Downloads\CSC4103_PS01\CSC4103_PS01_PartsBC_Report.pdf"
ASSETS = r"C:\Users\EL.DAWLIA\Downloads\CSC4103_PS01\assets"

NAVY = HexColor("#0F3B7A"); GREEN = HexColor("#1B7A4D"); LIGHT = HexColor("#EDF2F7")
MIDB = HexColor("#DCE6F1"); ACC = HexColor("#E8F5E9")

styles = getSampleStyleSheet()
sTitle = ParagraphStyle("Title2", parent=styles["Title"], textColor=NAVY, fontSize=22, leading=26, spaceAfter=2)
sSub = ParagraphStyle("Sub", parent=styles["Normal"], textColor=HexColor("#333333"), fontSize=10, leading=13, alignment=TA_CENTER)
sH1 = ParagraphStyle("H1", parent=styles["Heading1"], textColor=NAVY, fontSize=14, leading=16, spaceBefore=14, spaceAfter=6,
                     borderPadding=(0, 0, 4, 0))
sH2 = ParagraphStyle("H2", parent=styles["Heading2"], textColor=GREEN, fontSize=11, leading=14, spaceBefore=10, spaceAfter=4)
sB = ParagraphStyle("Body", parent=styles["Normal"], fontSize=9, leading=12.5, alignment=TA_JUSTIFY, spaceAfter=4)
sBsmall = ParagraphStyle("BodyS", parent=sB, fontSize=8.5, leading=11.5)
sCell = ParagraphStyle("Cell", parent=styles["Normal"], fontSize=7.8, leading=10)
sCellH = ParagraphStyle("CellH", parent=sCell, textColor=colors.white, fontName="Helvetica-Bold")
sCap = ParagraphStyle("Cap", parent=styles["Normal"], fontSize=8, leading=10, alignment=TA_CENTER, textColor=HexColor("#444444"), spaceBefore=3, spaceAfter=8)
sCode = ParagraphStyle("Code", parent=styles["Code"], fontSize=7.5, leading=10, backColor=HexColor("#F5F5F5"),
                       borderPadding=6, spaceAfter=6)
sBullet = ParagraphStyle("Bul", parent=sB, leftIndent=14, bulletIndent=6, spaceAfter=2)

def header_table(data, widths=None):
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, HexColor("#F2F6FB")]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t

def P(txt, style=sB):
    return Paragraph(txt, style)

story = []

# ================= COVER =================
story.append(Spacer(1, 1.2*cm))
story.append(P("CSC4103 Intelligent Systems — Practical Sheet 1", ParagraphStyle("c1", parent=sSub, textColor=NAVY, fontName="Helvetica-Bold", fontSize=11)))
story.append(P("Foundations and Applications of Intelligent Systems", sTitle))
story.append(P("Parts B (Exercises 1–3) + C (Smart Irrigation Mini-Project) — Solved Report with Reproducible Code", sSub))
story.append(Spacer(1, 0.3*cm))
story.append(HRFlowable(width="100%", thickness=1.2, color=GREEN))
story.append(Spacer(1, 0.3*cm))
story.append(P("Prof. Abdel-Rahman Hedar &nbsp;•&nbsp; School of Artificial Intelligence &amp; Data Management, Badr University in Assiut &nbsp;•&nbsp; Fall 2026", sSub))
story.append(Spacer(1, 0.5*cm))
info = [
    [P("<b>Name</b>: ___________________________", sB), P("<b>ID</b>: __________________", sB)],
    [P("<b>Course</b>: CSC4103 Intelligent Systems (CLO1)", sB), P("<b>Tools</b>: Python 3.10+, numpy, matplotlib", sB)],
    [P("<b>Folder</b>: <font face='Courier' size=8>CSC4103_PS01/ps01/</font> — ex1, ex2, ex3, irrigation.py", sBsmall),
     P("<b>Date</b>: October 2026 &nbsp;•&nbsp; Seeds fixed, paired evaluation", sBsmall)],
]
tinfo = Table(info, colWidths=[9*cm, 8*cm])
tinfo.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), LIGHT), ("BOX", (0, 0), (-1, -1), 0.6, NAVY),
                           ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.grey), ("TOPPADDING", (0, 0), (-1, -1), 5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 5), ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
story.append(tinfo)
story.append(Spacer(1, 0.4*cm))
story.append(P("<b>What this report contains.</b> Professional solutions for <b>Exercise 1</b> (robust Kalman-style controller), "
               "<b>Exercise 2</b> (human-in-the-loop approval gate), <b>Exercise 3</b> (L0–L3 autonomy thermostat), and the "
               "<b>Part-C Smart Irrigation System</b> (Field + SmartIrrigator with perceive/decide/act/learn, forecast knowledge, "
               "noise filtering, target adaptation, 90-day × 25-seed paired evaluation vs. fixed timer, and the 12-element case study). "
               "All numbers below are <b>measured outputs of the submitted .py files</b> (not estimates) and every figure is generated from the same seeds.",
               sB))
story.append(Spacer(1, 0.2*cm))
story.append(P("Reproduce in one line (from <font face='Courier'>ps01/</font>): &nbsp; <font face='Courier' size=8>python ex1_robust_controller.py &amp;&amp; "
               "python ex2_human_approval.py &amp;&amp; python ex3_autonomy_levels.py &amp;&amp; python irrigation.py</font>", sCode))
story.append(P("Figure 0 — Deliverables map. Code: <font face='Courier'>ex1_robust_controller.py</font>, <font face='Courier'>ex2_human_approval.py</font>, "
               "<font face='Courier'>ex3_autonomy_levels.py</font>, <font face='Courier'>irrigation.py</font> &nbsp;•&nbsp; Assets: <font face='Courier'>assets/*.png</font> "
               "&nbsp;•&nbsp; This PDF: <font face='Courier'>CSC4103_PS01_PartsBC_Report.pdf</font>", sCap))

# key results box
box = [
    [P("<b><font color='#0F3B7A'>Headline results (measured)</font></b>", sB)],
    [P("<b>Ex1:</b> filtered controller cuts stress from <b>1.17→0.07</b> (σ=0.05), <b>2.30→0.63</b> (σ=0.15), <b>1.60→1.07</b> (σ=0.25) days/60d, "
       "water change <b>+1.1% / −1.0% / −4.2%</b> — robustness without waste.<br/>"
       "<b>Ex2:</b> default threshold τ=0.50 → <b>escalation rate 55%</b> (9 auto, 11 escalated: 2 approved, 9 rejected/held); sweep 0.30→95%, 0.70→20%.<br/>"
       "<b>Ex3:</b> 22°C=HOLD, 27°C=COOL at L2/L3; 38°C correctly <b>refuses silent action</b> (L2 escalates, L3 take-over / safe-mode).<br/>"
       "<b>Part C:</b> Smart saves <b>45.4% water (5.40→2.95)</b> over 90d×25 seeds with stress <b>0.24 vs 0.00 d</b> (≈ zero) — farmer goal met; "
       "pump runs 54.8 vs 45.0 days but with micro-doses.", sBsmall)],
]
tb = Table(box, colWidths=[17*cm])
tb.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), MIDB), ("BACKGROUND", (0, 1), (-1, 1), ACC),
                        ("BOX", (0, 0), (-1, -1), 0.8, NAVY), ("TOPPADDING", (0, 0), (-1, -1), 6),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 6), ("LEFTPADDING", (0, 0), (-1, -1), 8),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 8)]))
story.append(tb)

# ================= EXERCISE 1 =================
story.append(P("Exercise 1 — A robust controller for noisy sensors (10 marks)", sH1))
story.append(P("<b>Task.</b> Modify the Example-3 feedback controller so it tolerates sensor noise. Compare <i>naive</i> (trusts every raw reading) "
               "with <i>filtered</i> for σ ∈ {0.05, 0.15, 0.25}, 30 runs each (60 days/run): total water + stress days (moisture &lt; 0.35). Explain the trade-off.", sB))
story.append(P("Design (Kalman idea)", sH2))
story.append(P("Naive: &nbsp;<font face='Courier'>irr = max(0, 0.50 − z)·0.9</font>, &nbsp;z = true + N(0,σ). &nbsp;Filtered perceive step fuses a process-model "
               "prediction with the reading:", sB))
story.append(P("pred = m̂ − 0.055 + last_irr &nbsp;&nbsp;(avg. evaporation model) &nbsp;&nbsp;→&nbsp;&nbsp; m̂ = pred + K(σ)·(z − pred), &nbsp;&nbsp;"
               "K(σ)=P/(P+σ<sup>2</sup>), P=0.01, clipped [0.30, 0.70] &nbsp;&nbsp;→&nbsp;&nbsp; irr = max(0, 0.50+margin(σ) − m̂)·1.0, "
               "margin(σ)=0.02+0.35σ.", sCode))
story.append(P("Two principled choices: (i) <b>K falls as σ rises</b> — trust the model more when the sensor is unreliable (0.70 → 0.31 → 0.30); "
               "(ii) <b>safety stock grows with σ</b> (0.037 → 0.072 → 0.107) — the more uncertain we are, the more cautiously high we aim. "
               "Gain 1.0 compensates filter lag. Evaluation is <b>paired</b>: identical heat/noise tapes per seed for both controllers, so differences are controller effects, not weather luck.", sB))
story.append(P("Results (measured, 60 days × 30 seeds)", sH2))
ex1data = [
    [P("<b>σ</b>", sCellH), P("<b>Naive water<br/>(mean±sd)</b>", sCellH), P("<b>Naive stress d<br/>(mean±sd)</b>", sCellH),
     P("<b>Filtered water<br/>(mean±sd)</b>", sCellH), P("<b>Filtered stress d<br/>(mean±sd)</b>", sCellH), P("<b>Effect</b>", sCellH)],
    [P("0.05", sCell), P("3.22 ± 0.15", sCell), P("1.17 ± 1.12", sCell), P("3.25 ± 0.15", sCell), P("<b>0.07 ± 0.25</b>", sCell), P("−94% stress, +1.1% water", sCell)],
    [P("0.15", sCell), P("3.33 ± 0.17", sCell), P("2.30 ± 2.10", sCell), P("3.29 ± 0.15", sCell), P("<b>0.63 ± 1.00</b>", sCell), P("−73% stress, −1.0% water", sCell)],
    [P("0.25", sCell), P("3.50 ± 0.23", sCell), P("1.60 ± 2.27", sCell), P("3.36 ± 0.17", sCell), P("<b>1.07 ± 2.18</b>", sCell), P("−33% stress, −4.2% water", sCell)],
]
story.append(header_table(ex1data, widths=[1.8*cm, 3*cm, 3*cm, 3.2*cm, 3.2*cm, 2.8*cm]))
story.append(P("Table 1 — Ex1 paired comparison. Filtered dominates on effectiveness (stress) at every σ while efficiency (water) is equal-or-better except a negligible +1.1% at σ=0.05.", sCap))
story.append(Image(os.path.join(ASSETS, "ex1_comparison.png"), width=16*cm, height=6.4*cm))
story.append(P("Figure 1 — Left: mean water is flat for the filter (≈3.3) while naive over-waters increasingly with noise (Jensen bias of max(0,·)). "
               "Right: stress collapses under filtering at every noise level.", sCap))
story.append(P("Discussion — the trade-off", sH2))
story.append(P("The naive controller's flaw is trusting <i>every</i> reading: a single upward noise spike causes under-irrigation (stress next day); a downward spike "
               "causes over-irrigation (waste). Because max(0,·) is convex, noise creates a systematic over-watering bias — visible as naive water rising 3.22→3.50 with σ. "
               "The filter removes most of that variance via the prediction term, and the σ-proportional margin converts the remaining uncertainty into a <i>small, controlled</i> "
               "safety stock instead of random waste. Cost: at very clean sensing (σ=0.05) we pay +0.03 water (+1%) for −1.10 stress days — an overwhelmingly favourable exchange. "
               "At σ=0.25 we save 4.2% water <i>and</i> cut stress by a third. Robustness here does not mean 'use more water'; it means 'use water <i>conditionally on uncertainty</i>'. "
               "Limitation: if σ grew beyond ~0.35 the fixed process model (avg. evaporation 0.055) would itself become the bottleneck — the next step is a full Kalman filter estimating P online, or fusing a second sensor.", sB))

# ================= EXERCISE 2 =================
story.append(P("Exercise 2 — Human-in-the-loop approval gate (10 marks)", sH1))
story.append(P("<b>Task.</b> A smart pump proposes (volume, confidence). Compute a risk score; low-risk actions auto-execute, high-risk ones escalate to a "
               "(simulated) farmer who approves/rejects. Run 20 proposals, report the escalation rate.", sB))
story.append(P("Design", sH2))
story.append(P("risk = 0.6·(volume/0.20) + 0.4·(1 − confidence) &nbsp;∈ [0,1]. &nbsp;Volume risk and uncertainty risk are explicit, weighted, and normalised; "
               "τ=0.50 is the design threshold (risk ≤ τ → AUTO, else escalate). &nbsp;Simulated farmer: careful heuristic (rejects big+uncertain doses, approves small+confident ones) "
               "with 10% trembling-hand error and 5% unavailability → HOLD (safe reject). Proposals: volume∼U(0.02,0.20), confidence∼U(0.35,0.98), seed=7.", sCode))
story.append(P("Results — 20 proposals at τ = 0.50 (measured)", sH2))
rows = [
    (1, "0.133", "0.49", "0.603", "REJECTED"), (2, "0.181", "0.45", "0.763", "REJECTED"),
    (3, "0.160", "0.74", "0.584", "APPROVED"), (4, "0.061", "0.38", "0.431", "AUTO"),
    (5, "0.074", "0.37", "0.474", "AUTO"), (6, "0.177", "0.67", "0.663", "HOLD"),
    (7, "0.021", "0.64", "0.207", "AUTO"), (8, "0.168", "0.93", "0.532", "REJECTED"),
    (9, "0.163", "0.75", "0.589", "REJECTED"), (10, "0.104", "0.67", "0.444", "AUTO"),
    (11, "0.075", "0.66", "0.361", "AUTO"), (12, "0.070", "0.51", "0.406", "AUTO"),
    (13, "0.066", "0.36", "0.454", "AUTO"), (14, "0.100", "0.47", "0.512", "REJECTED"),
    (15, "0.111", "0.79", "0.417", "AUTO"), (16, "0.120", "0.48", "0.568", "REJECTED"),
    (17, "0.199", "0.58", "0.765", "REJECTED"), (18, "0.163", "0.35", "0.749", "APPROVED"),
    (19, "0.132", "0.87", "0.448", "AUTO"), (20, "0.198", "0.45", "0.814", "REJECTED"),
]
tdata = [[P("<b>#</b>", sCellH), P("<b>vol</b>", sCellH), P("<b>conf</b>", sCellH), P("<b>risk</b>", sCellH), P("<b>decision</b>", sCellH)]]
for r in rows:
    tdata.append([P(str(r[0]), sCell), P(r[1], sCell), P(r[2], sCell), P(r[3], sCell), P(r[4], sCell)])
story.append(header_table(tdata, widths=[1.2*cm, 2*cm, 2*cm, 2*cm, 9.8*cm]))
story.append(P("Table 2 — All 20 proposals. Outcome: auto = 9, escalated = 11 (approved 2, rejected/held 9) → <b>escalation rate 55.0%</b>. "
               "Note proposal #8: high confidence (0.93) but large volume (0.168) still escalates — volume risk alone can trip the gate, by design.", sCap))
sens = [
    [P("<b>τ</b>", sCellH), P("<b>auto</b>", sCellH), P("<b>escalated</b>", sCellH), P("<b>esc. rate</b>", sCellH), P("<b>meaning</b>", sCellH)],
    [P("0.30", sCell), P("1", sCell), P("19 (3 ok / 16 no)", sCell), P("95%", sCell), P("paranoid: farmer overloaded", sCell)],
    [P("0.50", sCell), P("9", sCell), P("11 (2 ok / 9 no)", sCell), P("<b>55%</b>", sCell), P("balanced (recommended)", sCell)],
    [P("0.70", sCell), P("16", sCell), P("4 (0 ok / 4 no)", sCell), P("20%", sCell), P("permissive: fast but risky", sCell)],
]
story.append(header_table(sens, widths=[1.8*cm, 2*cm, 4*cm, 2.2*cm, 7*cm]))
story.append(P("Table 3 — Threshold sensitivity. τ is the autonomy dial.", sCap))
story.append(P("Discussion", sH2))
story.append(P("Raising τ automates more (20% escalation at 0.70) — faster loop, less farmer fatigue — but high-risk doses (#2, #17, #20, risk > 0.75) would then auto-execute, "
               "risking waterlogging and pump energy waste. Lowering τ (95% at 0.30) is safest per-action but makes the farmer the bottleneck and invites alarm fatigue "
               "(ignored escalations). τ=0.50 keeps the gate informative: roughly every second proposal needs a human, and the farmer still rejects 9/11 escalations — "
               "evidence the gate is catching genuinely risky actions, not spamming. A production step would be <i>adaptive</i> τ (tighter at night / when the tank is low) and logging overrides to learn farmer preferences.", sB))

# ================= EXERCISE 3 =================
story.append(P("Exercise 3 — Levels of autonomy L0–L3: thermostat (10 marks)", sH1))
story.append(P("<b>Task.</b> One <font face='Courier'>thermostat(temp, level, human_available)</font> function implementing L0 manual, L1 assisted, L2 partial, L3 conditional. "
               "At L3, outside [10, 35]°C it must request human takeover (or safe mode if no human). Test at 22, 27, 38°C.", sB))
story.append(P("Design", sH2))
story.append(P("Comfort band 20–24°C (HEAT / COOL / HOLD); safety envelope [10, 35]°C hard-gates autonomy. L0 never acts; L1 only advises; L2 auto-acts <i>inside</i> the envelope "
               "and escalates silently-never outside it; L3 auto-acts inside, requests takeover outside, and fails safe (HVAC OFF + alert) when no human answers.", sB))
lv = [
    [P("<b>Level</b>", sCellH), P("<b>Authority</b>", sCellH), P("<b>Behaviour</b>", sCellH)],
    [P("L0 manual", sCell), P("human", sCell), P("Display + suggest only; NO-ACTION by system.", sCell)],
    [P("L1 assisted", sCell), P("human (advised)", sCell), P("Recommend action; execute only after confirmation.", sCell)],
    [P("L2 partial", sCell), P("system (supervised)", sCell), P("Auto inside [10,35]; ESCALATE (no silent action) outside.", sCell)],
    [P("L3 conditional", sCell), P("system ↔ human", sCell), P("Auto inside; HUMAN-TAKEOVER outside; SAFE-MODE if nobody answers.", sCell)],
]
story.append(header_table(lv, widths=[3*cm, 3.5*cm, 10.5*cm]))
story.append(P("Table 4 — Autonomy contract.", sCap))
story.append(P("Test matrix (measured program output, abbreviated)", sH2))
tm3 = [
    [P("<b>temp</b>", sCellH), P("<b>L0</b>", sCellH), P("<b>L1</b>", sCellH), P("<b>L2</b>", sCellH), P("<b>L3</b>", sCellH)],
    [P("22°C", sCell), P("NO-ACTION<br/>suggest HOLD", sCell), P("AWAIT-CONFIRM<br/>HOLD", sCell), P("HOLD (auto)", sCell), P("HOLD (auto)", sCell)],
    [P("27°C", sCell), P("NO-ACTION<br/>suggest COOL", sCell), P("AWAIT-CONFIRM<br/>COOL", sCell), P("COOL to 24 (auto)", sCell), P("COOL to 24 (auto)", sCell)],
    [P("38°C", sCell), P("NO-ACTION<br/>suggest COOL", sCell), P("AWAIT-CONFIRM<br/>COOL", sCell), P("ESCALATED<br/>no auto action", sCell), P("TAKEOVER req.<br/>/ SAFE-MODE*", sCell)],
]
story.append(header_table(tm3, widths=[2*cm, 3.75*cm, 3.75*cm, 3.75*cm, 3.75*cm]))
story.append(P("Table 5 — *L3 at 38°C with human → HUMAN-TAKEOVER-REQUESTED (hold last safe state); without human → SAFE-MODE (HVAC OFF + ALERT). Full verbatim log is printed by ex3_autonomy_levels.py.", sCap))
story.append(P("Discussion", sH2))
story.append(P("Autonomy rises L0→L3 (human load and latency fall) but so does delegated risk. 22°C exercises the comfort deadband (correct HOLD everywhere — no chattering); "
               "27°C exercises proportional response (COOL); 38°C exercises the <i>safety envelope</i>: blindly auto-cooling an overheated loop risks compressor damage or masking a fire/fault, "
               "so L2/L3 correctly refuse. The envelope is the difference between automation and intelligence: the system knows <i>when not to act</i>. A real deployment adds sensor-validity checks "
               "(a stuck 22.0°C reading must not imply safety) and a takeover timer (if the human does not answer in N minutes, L3 auto-enters safe mode).", sB))

# ================= PART C =================
story.append(P("Part C — Mini-Project: Smart Irrigation System (25 marks)", sH1))
story.append(P("<b>Scenario.</b> A farm near Assiut replaces a fixed timer with an intelligent controller. Soil sensing is noisy (σ=0.08), a rain forecast exists but is right only "
               "80% of the time, and the farmer wants <i>less water and (essentially) no crop stress</i> over 90 simulated days.", sB))
story.append(Image(os.path.join(ASSETS, "partC_arch.png"), width=16*cm, height=5.1*cm))
story.append(P("Figure 2 — System architecture: the perceive–decide–act–learn loop with forecast as explicit knowledge and stress days as learning feedback. "
               "The fixed timer (baseline) bypasses every block — pure automation.", sCap))
story.append(P("Implementation (starter completed: <font face='Courier'>ps01/irrigation.py</font>)", sH2))
story.append(P("<b>Field</b> (environment): moisture ∈ [0,1], step(m) = min(1, m − heat + rain + irr), heat∼U(0.02,0.09), rain∈{0,0.15} w.p. 15%. "
               "Weather tapes are <b>pre-generated per seed and replayed</b> to both controllers — paired, fair comparison.<br/>"
               "<b>SmartIrrigator.perceive</b>: z = true+N(0,0.08); pred = m̂−0.055+last; m̂ = pred+0.40·(z−pred); attach 80%-accurate binary rain forecast.<br/>"
               "<b>decide</b>: effective_target = target − (0.05 if rain forecast else 0); dose = min(max(0, eff−m̂)·1.0, 0.16) — <i>wait-for-rain</i> discount uses knowledge to skip.<br/>"
               "<b>act</b>: clip + apply to Field. <b>learn</b>: rolling 14-day stress window; stress → target=min(0.62, +0.012); 14 healthy days → target=max(0.48, −0.008). "
               "Initial target 0.55 (safety stock for noise + 20% forecast error).", sB))
story.append(P("12-element case-study description (Problem … Ethics)", sH2))
elems = [
    ("1. Problem", "Keep root-zone moisture above the stress threshold (0.35) for 90 days while minimising pumped water, under noisy sensing and imperfect forecasts."),
    ("2. Goal / utility", "Minimise Σ irrigation subject to stress-days ≈ 0. Pump-on days reported as energy proxy (many micro-doses vs few floods)."),
    ("3. Environment", "Assiut field: stochastic heat/rain (15% rain days, 0.15 events), soil clipping at 1.0, fully observable only in simulation — partially observable in reality."),
    ("4. Sensors / perception", "One noisy moisture probe (σ=0.08) + binary rain forecast (80%). Complementary filter (K=0.40) fuses model prediction with reading; forecast is knowledge, not truth."),
    ("5. Actuators / action", "Dimmable pump: continuous dose [0, 0.16]/day. Timer baseline: 0.12 every 2nd day (45 pump-days, 5.40 water/90d by construction)."),
    ("6. Knowledge / model", "Avg. evaporation 0.055, last dose (process model); forecast semantics ('rain likely → lower effective target by 0.05'); stress threshold 0.35."),
    ("7. Decision-making", "Deficit rule toward adaptive target with wait-for-rain discount and max-dose cap — a one-step myopic optimiser, transparent and auditable."),
    ("8. Learning / adaptation", "Parameter-level: target adapts from stress feedback (+0.012 on stress, −0.008 after 14 healthy days, bounded [0.48, 0.62]). No structure learning."),
    ("9. Performance measure", "Paired 25-seed means: water, stress days, pump-days. Effectiveness = stress ≈ 0; efficiency = water saved; robustness = std across seeds + behaviour under noise/forecast error."),
    ("10. Baseline &amp; fairness", "Fixed timer on identical weather tapes. Smart: 2.95±0.57 water, 0.24±0.52 stress, 54.8±8.7 pump-days vs timer 5.40±0.00 / 0.00±0.00 / 45.0 — saves 45.4% water at ≈zero stress."),
    ("11. Limitations", "Forecast is binary & memoryless (no intensity/timing); single soil layer; no pump failures/clogging; evaporation model is a constant mean; 20% forecast error + σ=0.08 still cause ~1 stress day in unlucky seeds (#7: 2 d). Needs field calibration before deployment."),
    ("12. Ethics / safety / HITL", "Over-irrigation wastes Nile water and leaches fertiliser; under-irrigation threatens livelihood. Design keeps a human gate for large doses (Ex2 pattern), fails safe (never floods on uncertain sensing), logs every dose for audit, and must not disadvantage smallholders if water pricing follows automation."),
]
edata = []
for title, desc in elems:
    edata.append([P(f"<b>{title}</b>", sCell), P(desc, sCell)])
t12 = Table(edata, colWidths=[3.2*cm, 13.8*cm])
t12.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.grey), ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, HexColor("#F2F6FB")]),
                         ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                         ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6)]))
story.append(t12)
story.append(P("Evaluation — 90 days × 25 seeds, paired (measured)", sH2))
story.append(Image(os.path.join(ASSETS, "partC_water.png"), width=9*cm, height=6*cm))
story.append(P("Figure 3 — Mean water: timer 5.40 vs smart 2.95 (−45.4%) with stress 0.00 vs 0.24 d.", sCap))
pev = [
    [P("<b>Controller</b>", sCellH), P("<b>Water (mean±sd)</b>", sCellH), P("<b>Stress days (mean±sd)</b>", sCellH), P("<b>Pump-days (mean±sd)</b>", sCellH)],
    [P("Fixed timer", sCell), P("5.40 ± 0.00", sCell), P("0.00 ± 0.00", sCell), P("45.0 ± 0.0", sCell)],
    [P("<b>Smart</b>", sCell), P("<b>2.95 ± 0.57</b>", sCell), P("<b>0.24 ± 0.52</b>", sCell), P("<b>54.8 ± 8.7</b>", sCell)],
]
story.append(header_table(pev, widths=[4*cm, 4*cm, 4.5*cm, 4.5*cm]))
story.append(P("Table 6 — Summary. Smart saves 2.45 water units (45.4%) at the cost of 0.24 stress days per 90-day season (≈ one stress day every four seasons) — the farmer's 'less water and no stress' goal is met within noise. "
               "Pump runs ~10 days more but with micro-doses (avg 0.054/dose vs timer 0.12) — energy per m³ is the next metric to log.", sCap))
story.append(Image(os.path.join(ASSETS, "partC_trajectory.png"), width=16*cm, height=9.6*cm))
story.append(P("Figure 4 — Paired 90-day trace (seed=3): smart moisture rides just above the target band, doses shrink/skip ahead of (forecast) rain; "
               "timer floods on schedule regardless. Red dashed = stress line; blue ticks = true rain days.", sCap))
story.append(P("Per-seed excerpt (first 8 of 25; full log printed by <font face='Courier'>irrigation.py</font>) — water / stress / pump-days:", sBsmall))
story.append(P("<font face='Courier' size=7.5>seed 0: timer 5.40/0/45 vs smart 1.88/0/40 (saved +3.52) &nbsp;•&nbsp; 1: 5.40/0/45 vs 3.77/0/65 (+1.63) &nbsp;•&nbsp; "
               "2: 5.40/0/45 vs 2.45/0/53 (+2.95) &nbsp;•&nbsp; 3: 5.40/0/45 vs 3.67/1/64 (+1.73)<br/>"
               "4: 5.40/0/45 vs 3.12/1/61 (+2.28) &nbsp;•&nbsp; 5: 5.40/0/45 vs 3.04/0/57 (+2.36) &nbsp;•&nbsp; 6: 5.40/0/45 vs 2.12/0/43 (+3.28) &nbsp;•&nbsp; "
               "7: 5.40/0/45 vs 2.61/2/52 (+2.79) — worst seed still saves 2.79 water.</font>", sCode))
story.append(P("Discussion — why it works; limitations", sH2))
story.append(P("Three mechanisms stack: (i) <b>filtering</b> stops chasing noise (cf. Ex1); (ii) <b>forecast knowledge</b> avoids watering before rain (≈15% of days) — the single biggest saver versus the blind timer; "
               "(iii) <b>target adaptation</b> closes the loop on the true objective (stress) rather than a proxy. The timer's zero stress is purchased with 83% more water — effective but not <i>efficient</i>, and in a water-scarce region efficiency <i>is</i> effectiveness at scale.<br/>"
               "<b>Limitations &amp; next steps:</b> binary forecast ignores amount/timing (a 0.15 event vs drizzle); σ=0.08 and 20% forecast error are assumed known — real deployment needs online estimation; "
               "soil is one bucket (no depth, no spatial variation); pump energy is counted in days, not kWh; evaluation is simulation-only. Recommended extensions: probabilistic forecast (expected-rain value), "
               "two-layer soil + crop-coefficient, Ex2-style approval gate for doses &gt; 0.12, and a field-calibration week before trusting the 0.55 target.", sB))

# ================= APPENDIX =================
story.append(P("Appendix — reproducibility & files", sH1))
story.append(P("All code is commented, seeded, and dependency-light (numpy + matplotlib only for figures). Run from <font face='Courier'>CSC4103_PS01/ps01/</font>:", sB))
story.append(P("<font face='Courier' size=8>python ex1_robust_controller.py &nbsp;&nbsp;# 60d × 30 runs × 3 σ → Table 1 + Fig.1<br/>"
               "python ex2_human_approval.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 20 proposals + τ sweep → Tables 2–3<br/>"
               "python ex3_autonomy_levels.py &nbsp;&nbsp;&nbsp;&nbsp;# 22/27/38°C × L0–L3 → Table 5<br/>"
               "python irrigation.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 90d × 25 seeds paired → Table 6 + Figs.3–4<br/>"
               "python ../make_assets.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# regenerates assets/*.png</font>", sCode))
story.append(P("Assessment mapping: environment+agent design (§Part C implementation + Fig.2); forecast &amp; noise handling (perceive/decide + Ex1 filter); "
               "adaptation from feedback (learn rule + target trace); fair multi-seed evaluation (paired tapes, 25 seeds, mean±sd); "
               "12-element case study + limitations/ethics (numbered list above).", sB))
story.append(P("Note on honesty of results: stress is reported as mean±sd over seeds, never a cherry-picked run; the worst smart seed (#7: 2 stress days) is disclosed alongside the mean (0.24). "
               "That is the robustness claim — not 'zero stress everywhere' but 'near-zero on average with bounded worst case while saving 45% water'.", sB))
story.append(Spacer(1, 0.4*cm))
story.append(HRFlowable(width="100%", thickness=0.8, color=NAVY))
story.append(P("End of report — CSC4103 PS1 Parts B+C &nbsp;•&nbsp; Code + figures + this PDF are saved under <font face='Courier'>Downloads/CSC4103_PS01/</font>.", sCap))

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=1.5*cm, rightMargin=1.5*cm, topMargin=1.4*cm, bottomMargin=1.4*cm,
                        title="CSC4103 PS1 Parts B+C Report", author="CSC4103")
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5); canvas.setFillColor(NAVY)
    canvas.drawString(1.5*cm, 1.0*cm, "CSC4103 Intelligent Systems — PS1 Parts B+C  •  BUA Fall 2026")
    canvas.drawRightString(A4[0]-1.5*cm, 1.0*cm, f"Page {doc.page}")
    canvas.restoreState()
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("PDF saved:", OUT)
