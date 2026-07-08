# Hypotheses with falsifiers

This document is the single source of truth for what counts as
support, refutation, or "no decision" for each hypothesis in
the BLE evaluation. It pairs each hypothesis with (i) the prediction,
(ii) the analysis that adjudicates it, and (iii) the explicit
falsifier.

## H1 — Comprehension

- **Statement.** BLE participants score higher than current-condition
  participants on the boundary-case comprehension MCQ.
- **Prediction.** $\mu_{\text{BLE}}^{\text{MCQ}} > \mu_{\text{current}}^{\text{MCQ}}$
  with Cohen's $d \geq 0.30$.
- **Test.** One-sided Welch $t$ on participant-level MCQ accuracy.
- **Supported if.** $p_{\text{adj}} < 0.0167$ AND $d \geq 0.30$.
- **Refuted if.** 95\% CI on $d$ excludes $0.20$ (suggesting effect
  too small to matter even if statistically present).
- **No decision if.** $p_{\text{adj}} \geq 0.0167$ but CI on $d$ includes $0.30$.

## H2 — Perceived accuracy

- **Statement.** BLE participants rate L3.2 ("This label accurately
  describes...") higher than current-condition participants.
- **Prediction.** $\mu_{\text{BLE}}^{\text{L3.2}} > \mu_{\text{current}}^{\text{L3.2}}$
  with $d \geq 0.30$.
- **Test.** As H1.
- **Supported / refuted / no decision.** As H1.

## H3 — Perceived comprehensiveness

- **Statement.** BLE participants rate L3.3 higher.
- **Prediction, test, decision rules.** As H1.

## H4 — Community signal predicts engagement

- **Statement.** Within the BLE arm, drawer-opening rate per
  boundary case correlates with the case's Maybe-rate in our
  published filtered survey.
- **Prediction.** Spearman $\rho_{\text{open,Maybe}} \geq 0.50$ across the 9 cases.
- **Test.** Spearman $\rho$ with 10{,}000-permutation $p$ value.
- **Supported if.** $\rho \geq 0.50$ AND $p < 0.05$.
- **Refuted if.** $\rho \leq 0.10$ (suggests no relationship).
- **No decision if.** $0.10 < \rho < 0.50$.

## H5 — No global install-intent effect (equivalence)

- **Statement.** Installation intent does **not** differ between
  conditions. BLE moves comprehension and accuracy without moving
  the install decision itself; the effect is on quality of the
  decision, not the answer.
- **Prediction.** $|d_{\text{install}}| < 0.30$ (SESOI).
- **Test.** TOST procedure against SESOI $d{=}0.30$ on
  participant-level mean install intent.
- **Supported (equivalence) if.** TOST $p < 0.05$ on both bounds
  (the $90\%$ CI on $d$ lies entirely inside $\pm 0.30$).
- **Refuted if.** $90\%$ CI on $d$ excludes $0$ (a directional effect
  is present beyond the SESOI).
- **No decision if.** $90\%$ CI on $d$ straddles either SESOI bound.

## Pre-registered open exploration (not hypotheses)

- E1. Does BLE drawer-opening rate vary by age band?
- E2. Does prior Data Safety familiarity moderate H1?
- E3. Do think-aloud counts of B5 (rule-rejected) correlate with
  the published survey's $b_i$ No-rate?

These are explicitly exploratory; we will not adjust $\alpha$ for
them and we will not over-interpret null findings.

## Reporting standards

All hypotheses will be reported with effect size, 95\% CI (90\% for
TOST), exact $p$ values, and **a one-sentence verdict**: supported,
refuted, or no decision. The verdict cell will be the first item in
the Section 7 summary table of the manuscript.
