# Rationale-quality coding rubric
*Used by two blind raters to score each participant's free-text rationale 0–3 per applicable PRISM code.*

## Scoring scale (applied per code, per app, per rationale)

| Score | Definition |
|---|---|
| **0** | Rationale does not address the code at all, or addresses it incorrectly (e.g., names a recipient the policy does not mention). |
| **1** | Rationale mentions the code's surface trigger (e.g., names *third party*) but does not explain why it bears on the verdict. |
| **2** | Rationale identifies the code's surface trigger AND connects it to the relevant artefact mismatch (e.g., "policy names Crashlytics but Data Safety has no Shared row"). |
| **3** | Rationale identifies the code, connects it to the mismatch, AND specifies a corrective action or downstream interpretation (e.g., "label should add Crashlytics under Shared / Analytics purpose"). |

## Application rules

- **One score per applicable code per rationale.** A rationale that addresses three codes receives three scores.
- **Codes are applicable only if the gold-set marks the code as present on the stimulus.** Raters do not score codes that were not pre-identified by the expert consensus.
- **Raters work blind.** Raters do not see the participant's condition (Legacy / PRISM) and do not see the gold-set verdict during scoring.
- **Inter-rater agreement reported.** Cohen's κ on the four-point ordinal scale per code, reported in §8.1 of the paper.
- **Disagreements ≥2 points resolved by arbitration.** A third coder (PI) resolves any disagreement of two or more scale points.

## Worked examples per code

> *Rater note:* the examples are drawn from the rationale columns of `data-labels.xlsx`, lightly redacted. They are representative of the kinds of rationale you will see in the live study, not the participants' own rationales (which you will not see during calibration).

### M1 — Third-party flow shadowing

| Score | Example rationale |
|---|---|
| 0 | *"Looks correct."* |
| 1 | *"Policy says third parties."* |
| 2 | *"Policy lists Crashlytics and Firebase Analytics; Data Safety has no Shared row."* |
| 3 | *"Policy enumerates Crashlytics, Firebase, AdMob; Data Safety should add Shared rows for Analytics and Advertising or, at minimum, declare third-party sharing for App activity."* |

### M2 — Identifier-category misalignment

| Score | Example rationale |
|---|---|
| 0 | *"OK."* |
| 1 | *"Mentions advertising ID."* |
| 2 | *"Policy mentions AAID for ads; Data Safety has Device IDs but only for App functionality."* |
| 3 | *"AAID is used for ad targeting per the policy; the Device IDs row needs a second purpose (Advertising) or a separate sharing declaration."* |

### M3 — Generic-hedge underspecification

| Score | Example rationale |
|---|---|
| 0 | *"Cannot decide."* |
| 1 | *"Policy uses 'may collect'."* |
| 2 | *"Policy hedges with 'may collect including but not limited to'; the actual practice is unverifiable from the policy."* |
| 3 | *"Hedging makes the policy unfalsifiable; recommend label remain unchanged but flag the policy for revision toward specific enumeration."* |

### M4 — No-data overclaim

| Score | Example rationale |
|---|---|
| 0 | *"Says no data; trusted."* |
| 1 | *"Label says no data but policy says otherwise."* |
| 2 | *"Data Safety declares No data shared; policy describes Firebase Analytics. Direct contradiction."* |
| 3 | *"Data Safety declares No data shared; policy lists three analytics SDKs. Label should be replaced with explicit Shared rows for App activity (Analytics)."* |

### M5 — Location-grain mismatch

| Score | Example rationale |
|---|---|
| 0 | *"Location seems fine."* |
| 1 | *"Policy mentions location."* |
| 2 | *"Policy describes IP-derived approximate location; Data Safety has no Location row."* |
| 3 | *"IP-derived location is not representable in the binary grain; label should add Approximate location row, or note the IP-derived grain in the policy section if Approximate is too strong."* |

### M6 — Security/data-type confusion

| Score | Example rationale |
|---|---|
| 0 | *"Encryption looks good."* |
| 1 | *"Label says encrypted in transit."* |
| 2 | *"Data Safety claims encrypted in transit; policy does not mention encryption at all, so the claim cannot be corroborated."* |
| 3 | *"Encryption claim in the label is uncorroborated by the policy; recommend label remove the claim or policy add the corresponding security section."* |

### M7 — Boundary-of-responsibility mismatch

| Score | Example rationale |
|---|---|
| 0 | *"Policy refers to other sites."* |
| 1 | *"Policy disclaims linked sites."* |
| 2 | *"Policy explicitly disclaims responsibility for linked sites; the Data Safety table has no scope qualifier for this."* |
| 3 | *"Policy disclaimer means the label scope is ambiguous for the parts of the app that hand off to external services; the label should either narrow its scope explicitly or remove the disclaimer."* |

## Calibration protocol

Before live scoring begins:
1. Each rater independently scores a 20-rationale calibration set (4 rationales per code, drawn from the corpus).
2. Raters meet to compare scores; any difference of two or more points is discussed until consensus.
3. If post-calibration inter-rater κ on the calibration set is below 0.60, the rubric is revised before live scoring begins.

## Reporting

Per the pre-registration §3, the paper reports:
- Mean and 95% bootstrap CI of per-code reasoning-quality score, per condition.
- Inter-rater κ on the live-study scores, per code.
- Any arbitrations: count, code, condition, and the arbitration decision.
