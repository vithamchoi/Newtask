# Draft 2 — "Reading the Other Document"
## A Rationale-Grounded Taxonomy of Label–Policy Mismatch in Android Privacy Disclosures

**Target venue.** International Journal of Human-Computer Studies (Elsevier, Q1).

**Status.** Companion paper to Draft 1. Shares the DataGuard corpus but
reframes the contribution around a *qualitative-quantitative mixed-methods
taxonomy* rather than the auditability framework.

---

### The story in one paragraph

Android apps ship two privacy artefacts — a short structured Data Safety
label and a long unstructured privacy policy. When the two disagree, the
mismatch is rarely a clean contradiction; it is usually a *kind* of
mismatch with characteristic linguistic markers (a third-party SDK named
in the policy but no sharing field in the label, an "advertising ID"
referenced in policy text but no Device-IDs category, etc.). This paper
inducts a 7-type **Mismatch Taxonomy** from 1,441 annotator rationales,
quantifies its prevalence across 12 Google Play categories, validates it
against the inter-annotator-agreement signal, and shows that the taxonomy
predicts both *where* defects concentrate and *which* defects are most
ambiguous. The taxonomy yields a vocabulary that researchers, regulators
and tool builders currently lack.

### Why not just publish Draft 1 alone?

Draft 1 is a *framework + empirical-overview* paper. It introduces
auditability and quantifies the gap. Draft 2 is a *taxonomy + design
research* paper, deepening the qualitative side. Both can stand alone:
the corpora overlap but the contributions do not.

### Novelty over prior work

| Prior work | What it does | What it misses |
|---|---|---|
| PolicyLint (USENIX'19) | Detects internal policy contradictions automatically | No platform label; no human signal |
| PoliCheck (USENIX'20)  | Flow-to-policy entity-sensitive checks | Binary correct/incorrect; no taxonomy of *types* |
| Lalaine (USENIX'23) | iOS-label compliance at scale | iOS only; no human reviewer |
| Khandelwal (USENIX'24) | Google Data Safety measurement + dev study | Dev-side; no audit-reviewer side |
| Li (CHI'22) | Developer challenges creating labels | Producer side, not auditor side |
| **This paper** | **Reviewer-side rationale-grounded mismatch taxonomy with category-level prevalence and ambiguity scores** | — |

### Proposed contributions (four)

1. **The Mismatch Taxonomy** — 7 codes inducted from rationale text via
   Braun & Clarke (2006) reflexive thematic analysis with two coders and
   reliability reporting on a stratified sample of ~200 rationales.
2. **Per-category prevalence map** — a 12×7 matrix showing which
   mismatch types concentrate in which categories.
3. **Ambiguity score per mismatch type** — using the κ signal from
   doubly-annotated apps to estimate which codes split annotators.
4. **Design implications for evidence-grounded label UIs** — taxonomy-aware
   ambiguity indicators, per-type explanations, and category-conditional
   defaults.

### Empirical assets we can reuse from the existing corpus

- 1,506 audit judgments
- 1,441 rationale records
- 7 trained annotators × 12 categories
- ~240 apps with two annotators (κ ground truth)
- 3,576 parseable Data Safety records (for prevalence weighting)

### Methodological additions (beyond Draft 1)

1. **Reflexive thematic analysis** of a stratified sample (n≈200) following
   Braun & Clarke (2006); two coders + Cohen κ on codes.
2. **Mixed-method validation**: confirm taxonomy codes against the lexical
   indicators reported in Draft 1.
3. **Mismatch ambiguity score**: per code, the fraction of double-annotated
   pairs that disagreed when that code was present in either rationale.

### Section plan

1. Introduction (Draft 2 framing — taxonomy and vocabulary)
2. Related work
   - 2.1 Mismatch detection in mobile privacy (PolicyLint, PoliCheck,
     MAPS, Lalaine, Khandelwal'24)
   - 2.2 Vagueness and ambiguity in privacy text (Bhatia 2016,
     Wilson 2016)
   - 2.3 Thematic analysis in HCI (Braun & Clarke 2006)
3. Data and method
   - 3.1 DataGuard corpus (shared with Draft 1)
   - 3.2 Sampling for thematic analysis
   - 3.3 Coding protocol and reliability
4. The Mismatch Taxonomy (7 codes)
   - M1 Third-party flow shadowing
   - M2 Identifier-category misalignment
   - M3 Generic-hedge underspecification
   - M4 No-data overclaiming
   - M5 Location-grain mismatch
   - M6 Security-control / data-type confusion
   - M7 Boundary-of-responsibility mismatch
5. Quantitative prevalence
   - 5.1 Overall rates
   - 5.2 Per-category heat-map
   - 5.3 Ambiguity scores per code
6. Design implications
7. Discussion and limitations
8. Conclusion

### Key figures to build (TikZ)

- F1 **Taxonomy diagram** — 7 colour-coded ovals around the "label–policy
  mismatch" hub.
- F2 **12×7 heat-map** — prevalence of each code per category.
- F3 **Ambiguity-vs-prevalence scatter** — each code as a point.
- F4 **Mapping figure** — how each code drives a UI requirement.

### Status of this folder

This folder ships the **story + section plan + skeleton**. The full
manuscript is left as the next-step deliverable once the thematic
coding has been completed. See `skeleton.tex` for the structural shell.
