# Stimulus pool

The stimulus pool comprises 24 Android apps, stratified into three strata
of 8 apps each. The pool is built deterministically from the retrospective
DataGuard corpus.

## Strata

- **S1 — high-confidence** (8 apps). Apps where the gold-standard
  adjudication produced an unambiguous Supported or Contradicted verdict on
  every axis, and the original κ on this app exceeded 0.40. These serve as a
  ceiling for accuracy.
- **S2 — high-disagreement** (8 apps). Apps where the original DataGuard
  per-app κ was below 0 (worse than chance), with at least one Ambig gold
  label. These exercise the ambiguity-aware affordance of C2.
- **S3 — no-data** (8 apps). Apps whose Data Safety section declared neither
  sharing nor collection. The retrospective study showed these are the worst
  audit case (46.8–59.6% Incorrect); they exercise the evidence-first
  affordance of C2.

## Gold-standard construction

1. Two expert coders (PhD-level, trained on the four-state codebook
   Supported / Contradicted / Omitted / Insufficient) independently rate each
   of 24 apps on the four axes (sharing correctness, sharing completeness,
   collection correctness, collection completeness). Total: 192 axis-level
   verdicts.
2. Pre-consensus Cohen's κ is computed and reported per app and globally.
3. Disagreements are resolved in a recorded consensus meeting. The resolved
   verdict becomes the gold label.
4. Evidence spans are recorded as `evidence_share` and `evidence_collect`
   for use in condition C2.
5. The AI suggestion (label + uncertainty) for C2 is precomputed once via
   `evidence_locator/locate.py` and cached in `ai_suggestion`.

## Stratum balance per block

The randomizer (`backend/randomization.py`) assigns 8 apps per condition
block. To balance strata across blocks, the within-block stratum mix
rotates 3-3-2 / 3-2-3 / 2-3-3 across the three blocks of a session so that
every stratum gets exactly 8 trials per participant across the session.

## Files

- `stimuli_pool.json` — full pool with all per-app fields needed by the
  three conditions. Loaded into SQLite by `backend/db.py --load`.
- `gold_standard.json` — adjudicated gold labels (kept separate so the
  pool can be released without leaking gold to participants).

## Note on policy text

The `policy_text` in `stimuli_pool.json` is a frozen snapshot captured at
study build time. We pin a timestamp per app in the
`captured_at` field so reviewers can verify the artefact provenance.
