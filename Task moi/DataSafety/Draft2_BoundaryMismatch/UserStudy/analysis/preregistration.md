# Pre-registration — BLE mixed-method evaluation

This document is filed on the Open Science Framework **before** any
data collection. All deviations from this plan will be reported in
the manuscript with rationale.

---

## 1. Study identifiers
- **Title:** Comparative evaluation of the Boundary-Layer Explainer
  renderer.
- **Researchers:** [anonymised for review]
- **OSF link:** [populated at OSF lock]
- **Date of pre-registration:** [to be filled at OSF lock]

## 2. Design summary
- **Quantitative arm:** Online vignette experiment.
  - IV: renderer (current vs BLE), between-subjects.
  - DVs: comprehension, perceived accuracy, perceived
    comprehensiveness, installation intent.
- **Qualitative arm:** Think-aloud sessions (12--15 participants,
  recruited separately to avoid contamination).

## 3. Sample sizes (and stopping rules)
- Quantitative: target $N{=}200$ recruited, $\geq 80$ per condition
  after exclusions. Stopping rule: stop at $N{=}200$ recruited or
  $N{=}80$ valid per condition, whichever is later.
- Qualitative: 12 baseline, with the option to extend to 15 if
  thematic saturation is not reached at 12 (operationalised as
  no new axial code in the last two transcripts).

## 4. Hypotheses
- **H1 (comprehension).** BLE participants score higher on the
  boundary-case comprehension MCQ than current participants.
  $H_0: \mu_{\text{BLE}} \leq \mu_{\text{current}}$.
  Test: one-sided independent $t$.
- **H2 (perceived accuracy).** BLE participants rate
  the label higher on L3.2.
  $H_0: \mu_{\text{BLE}} \leq \mu_{\text{current}}$.
- **H3 (comprehensiveness).** BLE participants rate the label
  higher on L3.3.
- **H4 (community-signal predicts engagement).** Within the BLE
  condition, drawer-opening rate per case correlates positively
  ($\rho \geq 0.5$) with the case's Maybe-rate in the published
  survey.
- **H5 (no install-intent effect — exploratory equivalence).**
  Installation intent does not differ between conditions; tested
  with TOST against SESOI $d{=}0.30$.

## 5. Analyses

### Primary (H1, H2, H3)
- Pre-screen: exclusions per `vignette/protocol.md` §Quality controls.
- Compute participant-level mean of the 4 within-participant trials
  per DV.
- For each of H1, H2, H3: independent-samples $t$ test (one-sided)
  with Welch's correction.
- Bonferroni correction across H1--H3 ($\alpha_{\text{adj}}{=}0.0167$).
- Effect size: Cohen's $d$ with 95\% CI (bootstrap, 10{,}000
  resamples).
- Robustness: re-fit a mixed-effects model with participant random
  intercept and app fixed effect; report fixed effect of condition.

### Secondary (H4)
- Within the BLE condition, compute per-participant drawer-opening
  rate (count of distinct boundary cases opened / count of distinct
  boundary cases presented).
- Spearman $\rho$ between drawer-opening rate per case and the
  filtered-sample Maybe-rate for that case.
- Significance via 10{,}000 permutations.

### Equivalence (H5)
- TOST procedure (Lakens 2017) against SESOI $d{=}0.30$.
- Report TOST $p$ value plus the two-sided $90\%$ CI for the raw mean
  difference. We will refrain from claiming "no effect" if the CI
  includes $d{=}0.30$.

### Qualitative analysis
- Transcripts coded with the code book in `thinkaloud/coding_book.md`.
- Cohen's $\kappa$ on a 20\% calibration sample; target $\kappa \geq
  0.70$ per code.
- Reported counts plus quotes; no inferential test.

## 6. Pre-specified exclusions
- Attention check failure.
- Completion time $< 4$ min.
- Straight-lining on the 12 Likert items.
- Self-report of rushed completion (Q6.1 = "No, I rushed some").

## 7. Outcomes that will be **explored but not pre-registered**
- Demographic moderators (age, gender, country, IT-background).
- Drawer-opening rate as a moderator of H1.
- Free-text reasoning patterns from T3.5.

These exploratory analyses will be clearly labelled in the manuscript
as exploratory.

## 8. Deviations
Any deviation from this plan will be reported in the manuscript with
(i) what was deviated, (ii) why, (iii) the alternative result we would
have obtained had we not deviated.

## 9. Lock
This document will be locked on OSF prior to recruitment for the
pilot. The hash of the locked file will be appended here:

`SHA-256: [to be filled]`
