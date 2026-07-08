# OSF Standard Pre-Registration

This file follows the OSF Standard Pre-Registration template (the
"OSF Pre-Reg Form"). Each numbered section maps to a field in the
OSF form; paste the content of each section into the matching field
when you submit on osf.io.

---

## A. Study information

### A1. Title
A comparative evaluation of the Boundary-Layer Explainer (BLE)
renderer for app-store privacy labels.

### A2. Authorship
*(Anonymised for IJHCS review. Camera-ready will list each author with
ORCID.)*

### A3. Description
We compare the current Google Play Data Safety renderer against a
Boundary-Layer Explainer (BLE) renderer that adds, per contested
flag, a one-line rule clause, a community signal (% accept / %
unsure measured in a prior survey), and a one-tap counter-factual
toggle. The companion paper introduces the BLE design pattern from
a measurement study of 87 Android users on Google Play's nine
boundary cases. This pre-registration covers the **mixed-method
evaluation** of the BLE pattern: an online between-subjects vignette
experiment (Arm A) and an in-lab think-aloud study (Arm B).

### A4. Hypotheses

| # | Statement | Pre-registered effect | Test |
|---|---|---|---|
| H1 | BLE participants score higher on a boundary-case comprehension MCQ than current-condition participants. | Cohen's $d \geq 0.30$ | One-sided Welch $t$ |
| H2 | BLE participants rate the label as more accurately describing the app's data practices. | $d \geq 0.30$ | One-sided Welch $t$ |
| H3 | BLE participants rate the label as giving them enough information to decide. | $d \geq 0.30$ | One-sided Welch $t$ |
| H4 | Within BLE arm, drawer-opening rate per boundary case correlates positively with the case's Maybe-rate in the prior survey. | Spearman $\rho \geq 0.50$ | Spearman with permutation $p$ |
| H5 | Installation intent does **not** differ between conditions (equivalence). | $|d| < 0.30$ (SESOI) | TOST against $d_{SESOI}{=}0.30$ |

Decision rules: each hypothesis is pre-classified as
*supported / refuted / no decision* using the rules in
`hypotheses.md` (also released as supplementary material).

---

## B. Design plan

### B1. Study type
Mixed-method evaluation.
- Arm A: between-subjects vignette experiment (online).
- Arm B: think-aloud study (in-lab/remote video).

### B2. Blinding
Participants are not told the names of the conditions and cannot
infer the manipulation from the recruitment text. The label-text
content of both conditions is held constant; only the renderer
differs.

### B3. Study design
- IV (between-subjects): renderer = {current, ble}.
- Within-participant factor: app (4 of 12 sampled per participant,
  stratified to cover the three typology families).
- DVs:
  - Comprehension MCQ (binary), one per app.
  - Three 7-point Likerts per app (perceived accuracy, perceived
    comprehensiveness, installation intent).
  - One open-ended free-text per app.
  - BLE-condition only: drawer-opening rate, counter-factual toggle
    use, post-task usefulness rating.

### B4. Randomisation
- Condition assignment: by `fnv1a(pid + ":cond:" + STUDY_ID) % 2`.
  Yields ~50/50 with no need for a randomiser.
- App subset: by `mulberry32(fnv1a(pid + "::" + STUDY_ID))` with a
  greedy stratification step ensuring each of the three typology
  families is represented at least once.
- MCQ option order: shuffled per participant per app.

---

## C. Sampling plan

### C1. Existing data
This pre-registration is for new data collection. We do reference
aggregate Yes/Maybe percentages from the companion paper's survey
($N{=}87$) to set the prior on the community signal embedded in the
BLE drawer. Those reference percentages are fixed at lock time.

### C2. Data collection procedures
- Arm A: Prolific posting; eligible participants complete the
  single-page-app at `https://YOUR-DOMAIN/study.html?pid=PROLIFIC_ID`.
  Each session ends with a completion code paste-back into Prolific.
- Arm B: Prolific posting filtered to participants who consent to a
  Zoom session. Sessions recorded audio + screen with consent.

### C3. Sample size
- Arm A: $N=200$ recruited, $\geq 80$ valid per condition expected
  after exclusions. Powered for $d{=}0.40$, $\alpha{=}0.05$, power
  $0.80$ on the primary DV (H1).
- Arm B: 12--15 participants, stopping at thematic saturation
  (operationalised as no new axial code in the last two transcripts).

### C4. Sample size rationale
See `sample_size.md` in the same folder. H5 is explicitly
under-powered at $N{=}200$ and is reported as an exploratory
equivalence test.

### C5. Stopping rule
Stop at $N{=}200$ recruited or $N{=}80$ valid per condition,
whichever is later. No interim analyses on the primary contrast.

---

## D. Variables

### D1. Manipulated variables
Renderer condition: `current` (binary flag list, mimicking Google
Play Data Safety) versus `ble` (same flag list plus a BLE drawer per
contested flag).

### D2. Measured variables
Per app (within-participant): comprehension MCQ (binary),
$L_{3.2}$ accuracy (1--7), $L_{3.3}$ comprehensiveness (1--7),
$L_{3.4}$ installation intent (1--7), open-ended rationale.

Pre-task: Android usage duration, prior Data Safety inspection,
IUIPC privacy-concern item (1--10).

Post-task (both conditions): attention check, honesty item,
demographics. BLE-only: drawer-engagement item, post-task
usefulness Likert, improvement suggestion.

Logged automatically: time-on-page, drawer-open events,
counter-factual-toggle events.

### D3. Indices
Per-participant primary score = arithmetic mean of the four
per-app values for each DV.

---

## E. Analysis plan

### E1. Statistical models
- H1, H2, H3: one-sided Welch's $t$ on participant-level means,
  Bonferroni-corrected ($\alpha_{\text{adj}}{=}0.0167$).
- H4: Spearman $\rho$ across the 9 boundary cases between
  drawer-opening rate and the published Maybe-rate; 10{,}000
  permutations for $p$.
- H5: TOST against SESOI $d{=}0.30$ on installation intent.

### E2. Effect-size and CI reporting
Cohen's $d$ with 10{,}000-resample bootstrap 95\% CIs. For TOST,
the 90\% CI on $d$.

### E3. Inference criteria
Pre-classified per hypothesis in `hypotheses.md`.

### E4. Data exclusion
Pre-registered exclusions: attention-check failure; completion
time $< 4$ min; honest self-report of rushing (Q6.1 = "rushed");
straight-lining on the 12 Likerts (variance $\leq 0.1$).

### E5. Missing data
Cases that drop out mid-study are excluded from the primary
analysis but reported in a CONSORT-style flow diagram. We will
report per-participant completion rate by condition.

### E6. Robustness
Re-run all primary contrasts as mixed-effects models with
participant random intercept and app fixed effect.

### E7. Exploratory analyses
Demographic moderators (age, gender, country, IT background).
Drawer-opening rate as moderator. Free-text content analysis. All
labelled exploratory.

---

## F. Other

### F1. Other information
A working browser-based prototype, the analysis pipeline, the
consent and recruitment text, the moderator protocol for Arm B,
and the inductive coding book are released in the `UserStudy/`
folder of the supplementary material.

### F2. Funding
*(Anonymised for review.)*

### F3. Conflicts of interest
None declared.

### F4. Citations
Companion paper: *Where the Policy Ends and the User Begins: A
Boundary-Case Mismatch in App-Store Privacy Labels*.
Submitted to the International Journal of Human-Computer Studies.

---

## Lock

This pre-registration will be locked on OSF prior to recruitment.
The SHA-256 hash of the locked PDF will be appended here:

`SHA-256: [to be filled at lock]`

Date of lock: `[to be filled]`
