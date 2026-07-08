# Pre-registration — DataGuard Controlled User Study

This file mirrors the OSF preregistration template (As Predicted: 9-question
version). It is a working copy of the registered record. The registered
version is timestamped on OSF and is the canonical reference.

---

## 1. What's the main question being asked or hypothesis being tested in this study?

Does an evidence-grounded AI-assisted privacy-label audit interface (C2)
improve human audit accuracy and calibration over a structured side-by-side
interface (C1) and a raw-artefact baseline (C0), without increasing perceived
workload?

## 2. Describe the key dependent variable(s) specifying how they will be measured.

- **Accuracy.** Per-trial 4-axis correctness (sharing correctness, sharing completeness, collection correctness, collection completeness) against an adjudicated four-state gold label (Supported / Contradicted / Omitted / Insufficient evidence). Score = number of axes (0–4) matching gold.
- **Confidence calibration.** Brier score on confidence-weighted accuracy per (participant, condition).
- **Workload.** NASA-TLX six sub-scales + global mean, after each condition block.
- **Time on task.** Wall-clock from trial open → submit, log-transformed for linear modelling.

## 3. How many and which conditions will participants be assigned to?

Three within-subject conditions: C0 (raw), C1 (structured), C2 (evidence-grounded AI). Order counterbalanced via 3×3 Latin square. Each participant completes 8 stimulus apps per condition (24 trials total).

## 4. Specify exactly which analyses you will conduct to examine the main question/hypothesis.

- **H1 (accuracy).** Mixed-effects logistic regression:
  `correct ~ condition + (1|participant) + (1|app)`
  Pre-specified contrasts: C1 vs C0, C2 vs C0, C2 vs C1.

- **H2 (workload).** Linear MEM on NASA-TLX global:
  `tlx ~ condition + (1|participant)`

- **H3 (calibration).** Per-(participant,condition) Brier scores; paired bootstrap (BCa, 1,000 iterations) on Δ(C2 − C0).

- **H4 (interaction).** Extend H1 model with `condition * stratum`; predicted-margin contrasts at stratum = no-data.

Multiplicity: Holm–Bonferroni across H1–H4.

## 5. Any secondary analyses?

- Per-axis breakdown of accuracy.
- Per-category breakdown of accuracy.
- Time × condition interaction.
- Trust (TPA) → C2 acceptance-rate correlation.
- Qualitative thematic coding of free-text rationales (independent coding by two researchers; Cohen's κ reported).

## 6. How many observations will be collected or what determines sample size?

Target N = 30 complete participants (24 trials × 30 = 720 trials per condition; 2,160 trials total). Stop when both (i) N ≥ 30 and (ii) ≥80% completion across cells. If at N = 30 completion < 80%, recruit up to N = 40.

Power justification: simulation-based, assuming marginal accuracy difference Δ(C2 − C0) ≥ 0.10 and participant-level SD = 0.18 → power ≥ 0.85 at α = .05 (see `analysis/power_analysis.py`).

## 7. Anything else you would like to pre-register?

- Stimulus selection rule: 24 apps stratified into 3 strata × 8 apps:
  S1 high-confidence, S2 high-disagreement, S3 no-data (see `stimuli/README.md`).
- Exclusions:
  - Sessions with median trial time < 8 seconds (signals random clicking).
  - Sessions with completion < 80% of trials.
  - Participants who fail the tutorial comprehension check after two attempts.
- Outlier handling: trial-level RT outliers > 3 SD log-transformed will be Winsorised at the 99th percentile.
- Deviations from protocol will be logged in `docs/DEVIATIONS.md` and reported in the manuscript.

## 8. Have any data been collected for this study already?

No. All analyses below are pre-specified.

## 9. Name suggested by Submitter

DataGuard Controlled Audit Study v1.

---

## Reproducibility

- All code is in this repository, pinned by Git commit hash at the registration timestamp.
- The OSF record DOI will be inserted here on submission.
