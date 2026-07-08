# PRISM Combined Target-User Comments

This file synthesises the two target-user feedback packets in this folder:

- `PRISM-EXPERT-01`: usable privacy researcher / audit methodologist.
- `PRISM-PRACTITIONER-02`: data-protection practitioner.

## Shared Overall Reaction

Both target users found the seven-code taxonomy useful because it gives
reviewers a vocabulary beyond "Correct" and "Incorrect". The taxonomy is most
valuable when it helps reviewers explain *why* a Data Safety label and privacy
policy do not align.

The strongest perceived use cases are:

- audit triage;
- reviewer training;
- developer remediation notes;
- evidence-grounded interface cues;
- category-specific analysis of mismatch patterns.

The weakest or riskiest use case is automatic compliance judgment. Both users
warned that PRISM codes should be review cues rather than final decisions.

## Code-Level Comments

### M1 — Third-Party Flow Shadowing

This is one of the most valuable codes. Users expect it to catch cases where a
policy mentions AdMob, Firebase, analytics providers, advertising partners,
service providers, affiliates, or other third-party recipients while the Data
Safety label under-declares sharing.

Boundary issue: distinguish independent third-party recipients from processors
or service providers acting only on behalf of the developer.

### M2 — Identifier-Category Misalignment

Highly actionable. Users especially liked the mapping from advertising ID,
Android ID, unique device identifier, cookies, IP address, and similar policy
phrases to Data Safety categories.

Requested UI: a tooltip or glossary that explains which Google Data Safety
category each policy term maps to.

### M3 — Generic-Hedge Underspecification

Useful but risky. Users do not want every "may", "such as", or "including" to
be treated as a defect. M3 should be shown as an ambiguity cue.

Recommended wording: "scope unclear" or "policy language is non-committal",
not "mismatch detected".

### M4 — No-Data Overclaim

The most actionable code. Both users rated it as high priority. If the Data
Safety label says no collection or no sharing, policy mentions of identifiers,
analytics, crash logs, SDKs, cookies, advertising, or IP-derived location should
trigger review.

Recommended UI: interruptive but not accusatory prompt.

### M5 — Location-Grain Mismatch

Useful but needs examples. Users asked for a reference table showing precise,
approximate, city/region, IP-derived, and inferred location.

### M6 — Security-Control / Data-Type Confusion

Important for training but hard to apply. The risk is that ordinary security
practice language such as HTTPS, encryption, TLS, or "secure storage" gets
mistaken for a data-practice disclosure issue.

Recommended use: manual-review warning, not automated flag.

### M7 — Boundary-of-Responsibility Mismatch

Potentially useful when a policy pushes responsibility to third-party privacy
policies instead of clearly disclosing data flows. However, many policies
contain third-party disclaimers legitimately.

Recommended use: responsibility-scope cue that asks the reviewer to inspect
whether data flow itself is disclosed.

## Feedback on D1-D8 Affordances

| Affordance | User reaction |
|---|---|
| D1 Third-party recipient panel | Very strong. Should list named recipients and recipient roles. |
| D2 Identifier mapping tooltip | Very strong. Essential for junior reviewers and practitioners. |
| D3 Hedge highlighter | Useful only if subtle. Do not make it look like a defect. |
| D4 No-data audit prompt | Strongest prompt. Highest priority. |
| D5 Location-grain overlay | Useful with examples; otherwise confusing. |
| D6 Security/data tab | Needs training text and examples. |
| D7 Responsibility-scope chip | Useful as caution marker, not final verdict. |
| D8 Ambiguity badge | Useful for calibration; should say "historically disputed cue". |

## Most Important Requested Change

Add a severity/action matrix:

| Type | Codes | Suggested UI wording |
|---|---|---|
| Likely contradiction | M2, M4 | "High-priority review cue" |
| Likely omission | M1, M5 | "Possible under-disclosure" |
| Ambiguity/scope issue | M3, M7 | "Scope unclear; inspect evidence" |
| Training/manual-review issue | M6 | "Security/data distinction requires review" |

## Direct Quotes for Paper/Design Notes

> PRISM is most valuable as a structured explanation layer. I would use it to
> triage cases and write clearer remediation requests. I would not use it as a
> standalone compliance decision system.

> The taxonomy gives reviewers a practical vocabulary beyond Correct/Incorrect.
> It is strongest when framed as a review-cue taxonomy rather than an automated
> defect detector.

> M4 and M2 can be high-priority alerts. M3, M6, and M7 should be softer
> interpretive prompts.

