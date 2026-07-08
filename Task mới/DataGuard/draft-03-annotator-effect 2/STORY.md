# Draft 3 — "Who Audits the Auditor?"
## Reviewer Heterogeneity and the Social Construction of Privacy-Label Audit

**Target venue.** International Journal of Human-Computer Studies (Q1).

**Status.** Standalone paper. Uses only the existing DataGuard corpus.
Zero new experiments needed — all evidence is already in
`data-labels.xlsx`.

---

## The story in one paragraph

The privacy-audit literature treats reviewers as interchangeable noise
sources around a hidden ground truth. Our DataGuard corpus shows that
this assumption is wrong: seven trained annotators reviewing the same
material with the same interface produced verdict rates that span a
**15× range** (acc 7: 3.2% incorrect; acc 6: 50.1% incorrect on data
sharing). Pasted-evidence length differs by **6×** between the PhD
auditor (median 608 chars) and the most lenient student (median 100
chars). Pair-wise agreement varies between annotator pairs from 22.7% to
63.6%. Reviewer background — role (PhD vs student), declared interest
(IA vs AI vs .NET) and engagement style — explains a large share of the
disagreement that Draft 1 attributed to "interpretive ambiguity". The
paper reframes privacy-label audit as a *sociotechnical* task and gives
the field a vocabulary for reviewer-effect that κ alone cannot capture.

## Why this is interesting/novel

| Existing assumption | What we observe |
|---|---|
| κ reflects ambiguity of policy text | κ also reflects reviewer style |
| Trained annotators converge | Same training, 15× verdict spread |
| Evidence is a uniform act of citation | PhD pastes 3× longer evidence than students |
| Audit is a single-axis task | Annotators differ on *what kind* of audit they do |

No prior privacy-disclosure work disaggregates reviewer effects at this
granularity. The closest comparison is the OPP-115 corpus, where three
law students annotated 115 policies and reported aggregated κ —
**without analysing inter-coder differences**~\citep{wilson2016creation}.
Our annotators carry richer metadata (role, age, major, declared
interest), which lets us model the gradient.

## Headline empirical findings (from existing data)

1. **Verdict-rate heterogeneity.**
   - Acc 7 (SE/IA, age 22): 3.2% share-incorrect, 11.1% collect-incorrect
   - Acc 6 (SE/AI, age 20): **50.1%** share-incorrect, **58.3%** collect-incorrect
   - **15.7× ratio** on sharing; **5.3× ratio** on collection.

2. **Completeness style.**
   - Acc 4 (SE/.NET): 79.0% collect-incomplete
   - Acc 6 (SE/AI): 14.1% collect-incomplete
   - **5.6× ratio** on completeness perception.

3. **Evidence-length style.**
   - PhD (acc 1): median 608 chars per evidence excerpt
   - Students mean 100–216 chars
   - PhD pastes **~3× longer** evidence text.

4. **Pair-wise agreement.**
   - (acc 1, 5): 49.4% share, 52.9% collect
   - (acc 1, 6): 45.5% share, **63.6%** collect
   - (acc 5, 6): 48.1% share, 50.6% collect
   - (acc 5, 7): **22.7%** share, 40.9% collect
   - Spread of 41 pp on share agreement; clear "reviewer-pair" effect.

5. **Domain interest predicts style.**
   - Two annotators declared interest "IA" (information assurance).
     One is the PhD (high engagement; long evidence); the other is the
     most lenient student. Domain interest alone does not predict
     vigilance; role does.

## Contributions (four)

1. **Empirical.** First quantitative reviewer-heterogeneity audit of
   privacy-label review: 1,506 judgments by 7 annotators with role/major/
   interest metadata.
2. **Conceptual.** A two-axis reviewer-style model: *vigilance*
   (incorrect-rate) × *engagement* (evidence length and presence). The
   axes are weakly correlated and partition annotators into four styles.
3. **Methodological.** A *reviewer-aware κ* that decomposes raw κ into
   ambiguity-driven and reviewer-driven components.
4. **Design.** Three interface implications: (i) onboarding annotators
   with calibration tasks; (ii) requiring evidence pasting for
   negative verdicts; (iii) ambiguity-aware aggregation that weights
   reviewers by demonstrated calibration.

## Why IJHCS

The reviewer is a human-computer system. The audit interface is the
HCI artefact mediating the task. Reviewer heterogeneity is a *property
of the system*, not a residual. IJHCS readers care about both halves.

## Section plan

1. Introduction — the assumption-of-interchangeability gap.
2. Related work — OPP-115 inter-coder reports; crowdsourcing kappa
   literature; calibration in human-AI review (Cai 2019, Liao 2020).
3. Data — DataGuard corpus; annotator metadata (role, age, major,
   interest); collection protocol.
4. Reviewer-effect findings — per-annotator verdict, evidence, agreement.
5. The two-axis reviewer-style model.
6. Reviewer-aware κ and decomposition.
7. Design implications — calibration, mandatory evidence,
   reviewer-weighted aggregation.
8. Discussion + Limitations + Conclusion.

## Figures (all colourful TikZ)

- F1 Annotator quadrant (vigilance × engagement), scatter with 7 points
- F2 Per-annotator incorrect-rate bar chart
- F3 Evidence-length distribution per annotator (violin / box)
- F4 Pairwise agreement matrix as a 7×7 heat-map
- F5 Reviewer-aware κ decomposition diagram

## What is NOT in the paper

- No new audit task. No new annotators. No user study. All from the
  existing 1,506-row labels sheet.

## Files in this folder

- `STORY.md` — this file
- `skeleton.tex` — compileable LaTeX shell with figure placeholders
- `references.bib` — symlinked to draft-01's verified bibliography
