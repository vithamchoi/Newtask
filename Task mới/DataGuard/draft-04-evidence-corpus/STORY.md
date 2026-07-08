# Draft 4 — "The Evidence Corpus"
## A Public Resource of Human-Curated Privacy-Policy Evidence Pointers
## and the Linguistics of Why Auditors Doubt

**Target venue.** International Journal of Human-Computer Studies (Q1).

**Status.** Standalone. Uses only the existing DataGuard data — no new
experiments.

---

## The story in one paragraph

When a human auditor flags a Data Safety label as Incorrect, what
exactly are they pointing at in the policy? Until now there has been
**no public corpus** of human-curated, sentence-level evidence pointers
into privacy policies. The DataGuard corpus ships one for free: across
4,623 evidence excerpts from 1,506 audit judgments, annotators pasted
the policy fragment they considered relevant for each of four judgment
axes (sharing-correct, sharing-complete, collection-correct,
collection-complete). We characterise this corpus along three axes —
size and shape, linguistic feature distribution, and verdict
correlation — and show that **hedging language ("may", "include but
not limited to") is over-represented in evidence cited for Incorrect
verdicts (28.0%) compared with Correct verdicts (21.7%)**, while
third-party language is verdict-neutral (53–55% both directions). The
paper releases the evidence corpus as a reusable HCI resource and
maps each linguistic feature to a UI affordance.

## Why this is interesting/novel

| Existing resource | What it offers | What it misses |
|---|---|---|
| OPP-115 (Wilson 2016) | 115 policies × 23K fine-grained labels | No evidence-pointer schema |
| Polisis training data (Harkous 2018) | Classifier-level labels | No human-curated pointer |
| PolicyQA (Ahmad 2020) | QA over policies | No verdict-linked evidence |
| **DataGuard Evidence Corpus** | **4,623 evidence excerpts paired with audit verdict** | — |

This is the first dataset where each policy excerpt is paired with:
(i) the structured Data Safety claim it relates to,
(ii) a categorical audit verdict (Correct/Incorrect, Complete/Incomplete),
(iii) the annotator's free-text rationale, and (iv) annotator metadata.

## Headline empirical findings (existing data)

1. **Size and shape.**
   - 4,623 evidence excerpts total (4 evidence fields × 1,506 judgments
     − empties).
   - Mean length: 192–238 chars per excerpt.
   - Median: 146–186 chars (≈ one to two sentences).
   - The corpus is sentence-grained, not paragraph-grained.

2. **Coverage.**
   - 95.7% of audit judgments include at least one evidence or
     rationale field.
   - Evidence is more frequent for collection (86–90% of judgments) than
     sharing (68–82%).

3. **Verdict-discriminative linguistic features.**
   - **Hedging** ("may", "such as", "including but not limited to",
     "reserve the right"): 21.7% in Correct-share evidence vs **28.0%**
     in Incorrect-share evidence (+6.3 pp; suggests hedging makes
     auditors doubt).
   - **Third-party** mentions (SDK, partner, vendor, "service
     provider", named platforms): 53.1% Correct vs 55.4% Incorrect
     (+2.3 pp; near-neutral).
   - **Device identifiers** (advertising ID, IP, cookie, MAC): 6.9%
     Correct vs 8.0% Incorrect (+1.1 pp; weak signal).
   - **No-data claims** ("do not collect", "does not share"): 14.6%
     Correct vs 9.4% Incorrect (−5.2 pp; no-data language SUPPORTS the
     label being correct, not contradicts it).

4. **Two findings are counterintuitive.**
   - Third-party language is verdict-neutral — annotators see ads/SDK
     mentions and use them as evidence either way.
   - No-data language in the policy is associated with auditors
     marking the label \emph{Correct}, not Incorrect. The audit task is
     bilateral.

## Contributions (four)

1. **A new public corpus.** The DataGuard Evidence Corpus: 4,623
   sentence-level evidence excerpts, paired with a structured Data
   Safety claim, an audit verdict, an annotator rationale and
   annotator metadata.
2. **A linguistic feature analysis** showing which lexical families
   discriminate audit verdicts.
3. **A predictive baseline.** A simple linear classifier over four
   lexical features predicts share-correctness above chance — useful as
   a baseline for future LLM-assisted audit tools.
4. **Design implications.** Three UI affordances: a hedging
   highlighter, a third-party recipient panel, a no-data confirmation
   prompt.

## Why IJHCS

The Evidence Corpus is, in HCI terms, a record of the *citation
behaviour* of trained auditors. It is a primary HCI artefact: it
documents what trained reviewers consider sufficient evidence for a
judgment. The closest precedent is CLAUDETTE for
ToS~\citep{lippi2019claudette}; there is no comparable resource for
mobile privacy.

## Section plan

1. Introduction — the missing resource problem.
2. Related work — OPP-115, Polisis, CLAUDETTE, mobile-policy NLP.
3. The DataGuard Evidence Corpus — schema, provenance, summary stats.
4. Linguistic feature distribution.
5. Verdict-discriminative analysis.
6. A baseline predictive model from lexical features.
7. Design implications.
8. Limitations + release plan + conclusion.

## Figures (TikZ)

- F1 Corpus schema diagram (judgment node → 4 evidence pointers → policy)
- F2 Evidence-length distribution (boxplot, 4 fields)
- F3 Linguistic-marker prevalence (bar chart, 4 markers × 2 verdicts)
- F4 Marker-discrimination matrix (4×4 heatmap)
- F5 Feature-to-affordance ring

## What is NOT in the paper

- No new policy parsing. No new annotators. No user study.
- The corpus is from the existing audit workbook.

## Files in this folder

- `STORY.md` — this file
- `skeleton.tex` — compileable LaTeX shell
- shares `references.bib` via parent draft-01
