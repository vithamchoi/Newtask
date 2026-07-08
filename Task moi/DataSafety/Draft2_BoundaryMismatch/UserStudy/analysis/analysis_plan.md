# Analysis plan

This document operationalises the pre-registration into runnable steps.

## Tooling
- Python 3.11 with `pandas`, `scipy.stats`, `statsmodels`, `pingouin`.
- All analyses are version-pinned in `analysis.py` and
  `requirements.txt` (released as supplementary material).
- Plots use `matplotlib` (paper) + `seaborn` (exploratory).

## Pipeline (per dataset)
1. Load Qualtrics export (`raw_vignette.csv`) and prototype log
   export (`raw_prototype_log.csv`).
2. Apply pre-specified exclusions (`vignette/protocol.md` §Quality
   controls). Log $N$ retained per condition.
3. Compute participant-level aggregates per DV (mean of 4 trials).
4. Fit primary, secondary, and equivalence models in this order:
   - H1: Welch $t$ on MCQ accuracy.
   - H2: Welch $t$ on L3.2 (perceived accuracy).
   - H3: Welch $t$ on L3.3 (comprehensiveness).
   - H4: Spearman $\rho$ between per-case drawer-opening rate
     (BLE arm only) and the case's filtered Maybe-rate.
   - H5: TOST against $d{=}0.30$ on L3.4 (install intent).
5. Apply Bonferroni across H1, H2, H3
   ($\alpha_{\text{adj}}{=}0.0167$).
6. Robustness: re-fit each primary contrast as a mixed-effects
   model with participant random intercept and app fixed effect
   (`statsmodels` `mixedlm`).
7. Generate the Section 7 summary table and bar charts.

## Outputs (auto-generated)
- `results/summary_table.csv` — one row per hypothesis with $d$,
  CI, $p$, verdict.
- `results/figure_S1.pdf` — bar chart of comprehension accuracy
  per condition per app.
- `results/figure_S2.pdf` — drawer-opening rate vs Maybe-rate
  scatter (H4).
- `results/qualitative_codes_long.csv` — wide table of think-aloud
  code prevalence.

## Robustness checks
- Re-run primary with non-parametric Mann--Whitney for sanity.
- Re-run with `prolific_id` as random intercept to absorb any
  participant-level noise.
- Sensitivity analysis: vary the comprehension MCQ-correctness
  threshold from "first attempt" to "any attempt" and report both.

## Deviations log
Any deviation from the plan above is logged in `deviations.md` with
date, reason, and the alternative result.
