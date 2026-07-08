# Pre-registration — PRISM workbench user evaluation
**Format:** AsPredicted-style. Hosted on OSF (Open Science Framework).
**Project title.** *PRISM: A Rationale-Grounded Mismatch Taxonomy for Android Data-Safety Label and Privacy-Policy Disclosures — User evaluation*
**Registered:** [DATE — fill on submission]
**Registry:** OSF Registries (`https://osf.io/registries/`)

---

## 1. Have any data been collected for this study already?
No. This pre-registration is filed before any participant begins the study. A four-participant feasibility pilot ($n=4$) will run in Week 2 to debug the workbench and the timing of the protocol; pilot data is reported but excluded from confirmatory analyses, per pre-registration §6.

## 2. What's the main question being asked or hypothesis being tested?
Does a code-aware audit workbench (PRISM) that surfaces the seven-code mismatch taxonomy in-context — through the eight design implications D1–D8 from the parent paper — produce a measurable improvement in audit task quality and a measurable reduction in cognitive load, relative to a legacy binary-verdict workbench, on a stratified sample of $40$ Google Play apps audited by $24$ trained reviewers (Arm A, within-subjects), and does the D8 ambiguity badge specifically reduce over-flagging by $30$ data-protection practitioners (Arm B, between-subjects)?

## 3. Describe the key dependent variable(s) specifying how they will be measured.

**Primary outcomes.**

| DV | Measurement |
|---|---|
| Cognitive load | NASA-TLX (Hart 2006) total weighted score, 0–100, computed per 20-app block. Lower is better. |
| Task-completion time | Median seconds per app, computed from server-side `start_app` → `submit_verdict` timestamps. Lower is better. |
| Verdict agreement | Cohen's κ between each participant's verdicts and the expert-consensus gold set, on the 35 non-tutorial apps. Higher is better. |
| Reasoning quality | Two blind raters score the rationale text 0–3 per code on a rubric (see `rationale_quality_rubric.md`). Inter-rater κ reported. Higher is better. |

**Secondary outcomes.**
- Per-affordance helpfulness (7-point Likert, exit-interview Q2/Q3)
- Self-reported confidence per verdict (7-point Likert, optional radio attached to verdict form)
- Click-stream feature usage (which D-affordance was inspected per app)
- D8 badge over-flagging rate (Arm B): proportion of M1/M3 cases the practitioner flags as "incorrect" when the gold-set verdict is "correct"

## 4. How many and which conditions will participants be assigned to?

**Arm A (within-subjects, $n=24$).** Two conditions presented in 20-app blocks separated by a NASA-TLX form: Legacy (binary-verdict, no taxonomy affordances) and PRISM (D1–D8 affordances). Order is counterbalanced via Latin square across the 24 participants. Each participant audits each app once; assignment of apps to blocks is randomized per participant.

**Arm B (between-subjects, $n=30$).** Two between-subjects conditions: PRISM-without-D8 (badge bar hidden) and PRISM-with-D8 (badge bar visible). Random assignment 15:15. Stimuli identical across conditions.

## 5. Specify exactly which analyses will be conducted for each question.

**H1 (primary):** Median NASA-TLX is ≥15% lower in PRISM than in Legacy on Arm A.
- Test: one-sided Wilcoxon signed-rank, paired by participant, $\alpha=0.05$.
- Effect size: matched-pairs rank-biserial correlation $r$.
- 95% CI: bootstrap, 10,000 resamples, percentile method.

**H2 (primary):** Inter-rater κ vs gold is ≥0.10 higher in PRISM than in Legacy on Arm A.
- Test: paired permutation test on per-participant κ-vs-gold difference, $\alpha=0.05$.
- Effect size: mean κ-difference with 95% bootstrap CI.

**H3 (primary):** Median task-completion time per app is non-inferior in PRISM relative to Legacy on Arm A, with non-inferiority margin $\delta=10$%.
- Test: two one-sided tests (TOST) on the log-transformed completion time, $\alpha=0.05$.
- Reported alongside H1 to ensure the cognitive-load gain is not bought through speed cost.

**H4 (secondary):** D8 ambiguity badge reduces over-flagging of M1/M3 cases by ≥30% on Arm B.
- Test: one-sided Mann-Whitney $U$ on per-participant over-flag rate, $\alpha=0.05$.
- Effect size: rank-biserial.

**H5 (secondary):** Per-code reasoning-quality scores increase by ≥0.5 scale points (out of 3) on M1, M2, M6 in PRISM relative to Legacy.
- Test: paired-bootstrap CIs on per-code mean difference; H5 holds if all three CIs exclude 0.

**Multiple comparisons.** Bonferroni correction across H1–H3 ($\alpha_\text{adj}=0.0167$). H4 and H5 are pre-specified secondary and reported uncorrected.

**Power analysis.** With $n=24$ paired observations, a paired Wilcoxon signed-rank at $\alpha_\text{adj}=0.0167$ has $\ge 0.80$ power to detect a Cohen's $d_z \ge 0.66$. For H4, $n=15+15$ Mann-Whitney has $\ge 0.80$ power for $d \ge 0.95$. Sample sizes are constrained by recruitment budget; we report effect-size CIs in all cases, not p-values alone.

## 6. Stopping rule and exclusion criteria.

**Stopping.** Fixed-$n$ design. No interim analyses. We will stop once $n=24$ (Arm A) and $n=30$ (Arm B) participants have completed the full protocol.

**Participant exclusion (pre-registered).** A participant is excluded if any of the following occurs:
1. Completes fewer than 80% of the 35 non-tutorial stimuli in either block.
2. Fails the comprehension-check item on the tutorial (must correctly identify the verdict radios after reading the tutorial script).
3. Submits a verdict in less than 5 seconds on more than 25% of stimuli (proxy for click-through behaviour).
4. Reports a serious technical issue (browser crash, lost session) that prevents continuation.

If an Arm-A participant is excluded, we recruit a replacement from the standby pool to preserve the balanced Latin square. We expect ≤10% exclusion based on prior similar audits.

**Stimulus exclusion (pre-registered).** A stimulus is excluded from any per-app analysis if it produced an identical verdict across more than 22 of 24 Arm-A participants (insufficient variance), but its inclusion in the participant-level aggregate (NASA-TLX, completion time) is retained.

## 7. What other analyses do you plan to conduct?

Exploratory, clearly labelled as such in the paper:
- Per-quadrant breakdown of H1 and H2 (does the effect differ across common-ambiguous vs rare-tractable apps?)
- Per-affordance log-regression of NASA-TLX on click-stream features (which D-affordance contributes most to the cognitive-load gain?)
- Thematic analysis of exit-interview Q1/Q2/Q3/Q4 transcripts (two coders, simple thematic codebook)
- Time-on-app distribution (median and IQR; histograms reported per condition)

## 8. Predictions (qualitative).

We expect PRISM to reduce NASA-TLX by ≈15% relative to Legacy, primarily driven by Mental and Effort subscales. We expect reasoning quality on M1, M2, M6 (the high-ambiguity codes) to improve by ≈0.5–0.8 scale points. We do not expect a meaningful completion-time difference; the eight affordances are designed to be lightweight. We expect D8 to reduce over-flagging on M1/M3 apps but to have no effect on M4 apps (where the no-data overclaim is unambiguous).

## 9. Confirmation of the timing.

By submitting this pre-registration on or before [DATE], we confirm that no data described in this study have been collected at the time of submission, and that the protocol below has been finalised prior to participant recruitment.

## 10. Anything else you want to pre-register?

- Protocol artifacts that go with this pre-registration are versioned on the project's private GitHub repository under tag `pre-reg-v1` and mirrored to OSF as a frozen archive.
- All analysis code (Python notebooks) will be released under MIT licence upon publication; data will be released under CC-BY-4.0 with participant-identifying fields scrubbed.
- The pre-registered analysis script (`analyze.py`) is also included in the OSF deposit; any deviation between the script and the published analysis is reported with full justification in the paper's Method section.

---

**Authors (signed off on pre-registration):** [CONFIRM WITH SUPERVISOR]
**OSF DOI:** [auto-assigned on registration]
**Contact:** [CORRESPONDING AUTHOR EMAIL]
