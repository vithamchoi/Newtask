# Study Protocol — DataGuard Controlled User Study

**Version:** 1.0 (locked at preregistration)
**Anticipated submission:** International Journal of Human-Computer Studies
**Linked paper:** *The Auditability Gap* (Study 5)

---

## 1. Title

A controlled comparison of raw, structured, and evidence-grounded
interfaces for auditing Google Play Data Safety disclosures against
privacy-policy evidence.

## 2. Research questions

**RQ1.** Does providing a structured, side-by-side comparison interface (C1)
improve human audit accuracy over the raw artefacts a regulator or motivated
end user has today (C0)?

**RQ2.** Does evidence-grounded AI assistance (C2) further improve accuracy
and confidence calibration without increasing over-trust?

**RQ3.** Where are the benefits of C1 and C2 largest — across categories,
across the four judgment axes, and on no-data versus disclosed labels?

## 3. Hypotheses (pre-registered)

| ID  | Statement | Endpoint | Test |
|-----|-----------|----------|------|
| H1  | Accuracy(C1) > Accuracy(C0) AND Accuracy(C2) > Accuracy(C0) | Per-trial 4-axis accuracy vs gold standard | Mixed-effects logistic |
| H2  | Workload(C2) < Workload(C0) AND Workload(C2) < Workload(C1) | NASA-TLX block-mean | Linear MEM |
| H3  | Brier(C2) < Brier(C0) | Confidence calibration | Paired bootstrap |
| H4  | Δ(C2−C0) is larger on no-data trials than on disclosed trials | Accuracy × trial-type interaction | MEM interaction term |

Two-sided tests at α = .05; FWER-adjusted via Holm–Bonferroni across H1–H4.

## 4. Design

- **Type:** within-subjects, repeated-measures, three conditions
- **Counterbalancing:** 3×3 Latin square for condition order × app block
- **Unit task:** judge one app on four labels + confidence per judgment
- **Block structure:** 8 stimulus apps per condition × 3 conditions = 24 trials per participant
- **Total study duration:** ≈ 60–75 minutes (target median ≤ 70 min)
- **Compensation:** local-currency equivalent of US$15 (consistent with our IRB ceiling)

## 5. Participants

- **Target N:** 30 (see `analysis/power_analysis.py` for justification).
- **Recruitment:** university and developer communities; convenience sampling.
- **Inclusion criteria:**
  - Adult (≥18)
  - Reads English at a college level (self-reported)
  - Has used an Android smartphone in the last 12 months
  - No prior involvement in the DataGuard annotation corpus
- **Exclusion criteria:**
  - Self-reported privacy-policy or app-store internal experience (developer-relations role) — would bias against C0
- **Screening:** brief web form (see `SCREENING.md`).

## 6. Materials and stimuli

- **Stimulus pool:** 24 Android apps (see `stimuli/stimuli_pool.json`).
- **Stratification (3 strata × 8 apps):**
  - **S1 — High-confidence cases** (gold standard unambiguous: clear support or clear contradiction in both axes).
  - **S2 — High-disagreement cases** (apps where the retrospective DataGuard κ on this app was lowest; ambiguous policy language).
  - **S3 — No-data cases** (Data Safety declares no sharing or no collection).
- **Per-stimulus artefacts:**
  - Cached HTML of the Google Play Data Safety page (frozen snapshot)
  - Cached privacy policy text (frozen snapshot)
  - Structured Data Safety JSON (parsed)
  - Adjudicated gold label (Supported / Contradicted / Omitted / Insufficient evidence) for each of the four judgment axes
  - Evidence span (for C2): policy fragment(s) flagged by the LLM-assisted locator
- **Gold standard:** two independent expert coders + consensus meeting; see
  `stimuli/gold_standard.json`.

## 7. Conditions

### C0 — Raw review (baseline)
A web page that mirrors what a motivated end user or regulator can see today:
the Google Play Data Safety panel screenshot on the left, and the full text of
the privacy policy on the right with the browser's native find-in-page
available. No section extraction; no AI; no evidence highlight.

### C1 — Structured side-by-side
The Data Safety panel is rendered as a structured table (categories,
types, purposes). The privacy policy is shown with the heuristically
extracted *Data Share* and *Data Collect* sections expanded by default; the
remaining policy is collapsible. No AI; no evidence highlight.

### C2 — Evidence-grounded AI assistance
C1 plus, for each structured claim, a highlighted policy span that the
evidence-locator model identified as the most likely supporting (or
contradicting) passage, along with the model's suggested judgment and a
displayed uncertainty band. The AI output is **always inspectable before
acceptance**: the participant must click the highlight to expand it.

## 8. Procedure

1. **Consent** (5 min). Online consent form (`ETHICS_CONSENT.md`); participants must read and tick each clause.
2. **Demographics & screening** (3 min). Age band, English self-rating, Android-use frequency, prior privacy-policy reading frequency, developer-experience flag.
3. **Tutorial** (8 min). One worked example per condition with an explained gold answer. Participants must reach a comprehension-check threshold (4/5) before proceeding.
4. **Blocks** (3 × 15 min). Each block = 8 stimulus apps under one condition. Order counterbalanced (Latin square).
5. **Post-block NASA-TLX** (≈2 min per block). Six standard sub-scales.
6. **Post-C2 trust survey** (≈2 min, after C2 block). 5-item TPA-derived trust scale.
7. **Debrief** (5 min). Free-text reflection + payment information.

## 9. Dependent measures

| Measure | Operationalisation | Capture | Analysis |
|---------|--------------------|---------|----------|
| **Accuracy** | 0/1 per axis × 4 axes per trial vs adjudicated gold | per trial | mixed-effects logistic |
| **Task time** | wall-clock from trial open → trial submit | per trial | linear MEM (log-transformed) |
| **Confidence** | 0–100 slider, four (one per axis) | per axis | linear MEM |
| **Calibration** | Brier score on confidence-weighted accuracy | per block | bootstrap CI |
| **Workload (TLX)** | NASA-TLX six sub-scales + global mean | per block | linear MEM |
| **Trust (C2 only)** | TPA-derived 5-item Likert | once | descriptive + correlation |
| **Free-text rationale** | open text | per trial | thematic coding (secondary) |

## 10. Statistical analysis plan

- **Primary model (accuracy, H1).**
  Mixed-effects logistic regression:
  `accuracy ~ condition * stratum + (1|participant) + (1|app)`
  with `condition` levels {C0, C1, C2}, contrasts {C1 vs C0, C2 vs C0, C2 vs C1}.

- **Workload (H2).**
  Linear MEM on NASA-TLX global mean:
  `tlx ~ condition + (1|participant)`

- **Calibration (H3).**
  Brier score per (participant, condition) cell; paired bootstrap on per-participant Δ(C2 − C0); 1,000 bootstrap iterations, BCa CI.

- **Interaction (H4).**
  Add `condition * stratum` interaction to the H1 model; predicted-margin contrasts at stratum = no-data vs other.

- **Multiplicity.** Holm–Bonferroni across H1–H4 family-wise.

- **Robustness checks.** Non-parametric Wilcoxon signed-rank on per-participant cell-means; sensitivity analysis with participant exclusions (RT outliers > 3 SD).

## 11. Ethics

- IRB / ethics-committee approval obtained prior to data collection (file ref. recorded separately).
- Adult participants only; informed consent online.
- Data are de-identified at collection; participant IDs are random UUIDs.
- No deception; participants are told that one condition includes AI assistance.
- Right to withdraw at any time without penalty.
- Compensation is unconditional on completion; partial-completion data are retained only with explicit consent.

## 12. Data management

- All raw responses stored in SQLite (`data/raw/responses.db`), encrypted at rest.
- Released artefacts (after IRB sign-off and de-identification):
  - Per-trial accuracy / time / confidence / workload (CSV)
  - Free-text rationales (manually de-identified)
  - Analysis scripts and figures
- Storage period: 5 years post-publication, then secure deletion.

## 13. Deviations from protocol

Any deviation will be logged in `docs/DEVIATIONS.md` with date, reason, and
impact on the preregistered analysis.

---

## Appendix A — Stopping rules

The study will stop when **all of**: N ≥ 30 complete sessions; ≥80% of cells
(participant × condition) have complete data; ≥80% completion rate on the
NASA-TLX. If at N = 30 fewer than 80% completion is observed, recruit up to
N = 40.

## Appendix B — Power

See `analysis/power_analysis.py`. Simulation-based power for the C2 vs C0
contrast on accuracy: with assumed marginal accuracy difference ≥0.10
(consistent with retrospective audit defect rates), N = 30 yields ≥0.85
power at α = .05.
