# EC-TOOLBUILDER-01 — Evidence Corpus Release Feedback

**Artifact status:** target-user feedback; authored expert feedback  
**Persona:** privacy NLP / HCI tool-builder  
**Likely use:** build evidence-location and reviewer-assistance tools for
mobile privacy-label audits.

## Overall Reaction

This corpus is highly useful because it contains what most privacy-policy
datasets lack: the sentence or passage a trained reviewer actually pointed to
when judging a structured platform-side claim. I would use it primarily to
build and evaluate evidence-location support, not to automate compliance
decisions.

The most valuable fields are:

- structured Data Safety claim;
- evidence excerpt;
- verdict axis;
- human verdict;
- annotator ID;
- rationale;
- app/category metadata.

The pairing between claim and excerpt is essential. A policy sentence alone is
not enough to infer whether a Data Safety label is correct or complete.

## Ratings

| Dimension | Rating | Comment |
|---|---:|---|
| Dataset usefulness | 5/5 | Strong resource for evidence-grounded audit tools. |
| Schema clarity | 4/5 | Good, but needs a strict data dictionary and examples. |
| Benchmark readiness | 3/5 | Needs official splits and baseline scripts in the release. |
| HCI relevance | 4/5 | Strong if framed as evidence-selection/citation behaviour. |
| Risk of misuse | 3/5 | Manageable if discouraged uses are explicit. |

## Intended Use I Would Actually Adopt

I would use the corpus for:

1. **Evidence sentence retrieval:** given policy text and Data Safety claim,
   rank candidate policy sentences.
2. **Top-K reviewer support:** show top 3-5 likely evidence sentences in an
   audit UI.
3. **Claim-conditioned verdict assistance:** only after the evidence is shown,
   estimate whether the claim is supported, contradicted, omitted, or unclear.
4. **Reviewer-behaviour analysis:** compare whether different reviewers cite
   shorter, broader, more hedged, or more third-party-heavy passages.

I would not use it to publicly rank apps as compliant or non-compliant.

## Required Release Additions

Before I could use the corpus in a paper or tool, I would need:

- `evidence_corpus.csv` with stable row IDs;
- `datasheet.md`;
- `schema.md` with each field, value range, and example row;
- `LICENSE.txt`;
- `CITATION.cff`;
- official benchmark splits;
- script to reproduce lexical marker features;
- script to reproduce top-K retrieval baseline;
- a small sample file safe to inspect in documentation.

## Official Splits Requested

Please provide at least three official splits:

1. **App-level split:** no app appears in both train and test.
2. **Annotator-aware split:** evaluate whether model performance depends on
   annotator style.
3. **Category-balanced split:** preserve Google Play category balance.

Without official splits, future results will be hard to compare.

## Benchmark Tasks I Recommend

| Task | Input | Output | Why useful |
|---|---|---|---|
| Evidence retrieval | policy + structured claim | ranked evidence sentences | Most directly useful for UI support |
| Evidence selection | top-K candidates | selected best candidate | Models auditor citation behaviour |
| Verdict prediction | claim + evidence | correct/incorrect or complete/incomplete | Useful but should be secondary |
| Uncertainty calibration | claim + evidence | calibrated confidence | Important before any UI suggestion |

## Comments on Findings

The linguistic findings are useful because they prevent naive automation:

- Hedging should not be treated as a direct contradiction. It is a doubt cue.
- Third-party language is not automatically negative. It can support either
  correct or incorrect verdicts depending on the label.
- No-data language can be supporting evidence, not just a contradiction cue.

This is exactly why a corpus like this matters: it shows that audit evidence is
bilateral and claim-conditioned.

## UI Implication Feedback

I support:

- hedging highlighter as subtle cue;
- no-data confirmation prompt;
- third-party recipient panel.

I would avoid:

- single top-1 authoritative highlight;
- automatic red "mismatch" badge from lexical cues;
- hidden verdict suggestions;
- confidence scores that are not empirically calibrated.

## Free-Text Review Comment

The paper should describe the corpus as a record of reviewer citation
behaviour. That is the HCI contribution. The machine-learning baselines are
useful, but they should be framed as floors for future evidence-locator tools,
not as the main result. I would trust the corpus more if it includes official
splits, a clear datasheet, and strong warnings against using it for app-level
compliance ranking.

