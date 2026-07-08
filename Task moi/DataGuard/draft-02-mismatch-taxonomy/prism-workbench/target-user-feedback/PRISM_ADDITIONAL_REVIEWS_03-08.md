# Additional PRISM Target-User and Expert Reviews

This file adds six further reviews for the PRISM mismatch taxonomy and
workbench. The reviewers are deliberately varied: legal/privacy counsel,
Android engineer, HCI researcher, junior auditor, regulator analyst, and
privacy NLP engineer.

## PRISM-LEGAL-03

**Role:** privacy/legal counsel  
**Experience:** 11 years advising digital-product teams on privacy notices  
**Feedback lens:** legal interpretability and developer remediation

### Eligibility

| Field | Response |
|---|---|
| Adult | yes |
| Privacy/compliance experience >2 years | yes |
| Comfortable reviewing English privacy policies | yes |
| Prior PRISM/DataGuard annotation | no |

### Ratings

| Dimension | Rating |
|---|---:|
| Taxonomy usefulness | 6/7 |
| Code clarity | 5/7 |
| Legal defensibility | 4/7 |
| Developer remediation value | 6/7 |
| Risk of over-interpretation | 5/7 |

### Code Feedback

M1 and M4 are most legally salient because they can be explained clearly to a
developer. M3 must be handled cautiously: legal drafting often uses "may" to
preserve future flexibility, and that is not automatically a mismatch. M7 is
important but should be tied to failure to disclose the underlying data flow,
not simply the presence of third-party-policy language.

### Affordance Feedback

| Affordance | Rating | Comment |
|---|---:|---|
| D1 recipient panel | 6 | Useful if it distinguishes processors, affiliates, ad networks, analytics vendors. |
| D2 identifier tooltip | 7 | Strong remediation value. |
| D3 hedge highlighter | 4 | Use as caution only. |
| D4 no-data prompt | 7 | High-value legal triage cue. |
| D5 location overlay | 5 | Useful with jurisdiction-specific examples. |
| D6 security/data tab | 4 | Needs careful explanation. |
| D7 responsibility chip | 6 | Useful when third-party policies are used to avoid disclosure. |
| D8 ambiguity badge | 5 | Helpful if not framed as non-compliance. |

### Final Comment

PRISM should output audit language such as "requires review" or "policy support
unclear", not "violation". The taxonomy is strongest when it helps reviewers
write precise remediation requests.

## PRISM-ANDROID-04

**Role:** Android engineering lead  
**Experience:** 8 years integrating SDKs, analytics, ads, crash reporting  
**Feedback lens:** developer practicality and SDK disclosure mapping

### Eligibility

| Field | Response |
|---|---|
| Adult | yes |
| Android app development experience | yes |
| Has filled Data Safety forms | yes |
| Prior PRISM/DataGuard annotation | no |

### Ratings

| Dimension | Rating |
|---|---:|
| Taxonomy usefulness | 6/7 |
| Code clarity | 5/7 |
| Developer remediation value | 7/7 |
| Risk of over-flagging | 4/7 |

### Code Feedback

M2 is the most developer-useful code. Many teams do not realise that
advertising ID, installation ID, Firebase installation ID, crash identifiers,
or device identifiers should be reflected in Data Safety. M1 is also useful,
but the UI should account for SDKs used only for app functionality or crash
reporting versus ad personalisation.

M6 is important because developers often think "encrypted in transit" is enough
to satisfy privacy disclosure expectations. The workbench should show that
security claims and data-category claims answer different questions.

### Affordance Feedback

D2 should include common SDK examples: AdMob, Firebase Analytics, Crashlytics,
AppsFlyer, Facebook SDK, Unity Ads. D1 should group third parties by purpose:
ads, analytics, crash reporting, payment, authentication, cloud hosting.

### Final Comment

I would use PRISM before submitting a Play Console update if it gave me a
developer checklist: "policy mentions X; check Data Safety field Y." That
would be more useful than an academic code label alone.

## PRISM-HCI-05

**Role:** HCI researcher in decision support and expert workflows  
**Experience:** 12 years  
**Feedback lens:** cognitive load, UI interpretability, and warning design

### Eligibility

| Field | Response |
|---|---|
| Adult | yes |
| HCI/privacy research experience | yes |
| Familiar with controlled user studies | yes |
| Prior PRISM/DataGuard annotation | no |

### Ratings

| Dimension | Rating |
|---|---:|
| Taxonomy usefulness | 5/7 |
| UI actionability | 6/7 |
| Cognitive-load risk | 5/7 |
| Study readiness | 4/7 |

### Code Feedback

Seven codes may be too many to show simultaneously. The taxonomy should be
visible progressively: first show high-level concern type, then allow the
reviewer to expand code details. M3, M6, and M7 are interpretive and should not
use the same visual severity as M2 or M4.

### Affordance Feedback

The D8 ambiguity badge is promising. It should reduce false confidence, but it
could also increase uncertainty and slow reviewers. Measure whether D8 changes
both accuracy and decision time. The UI should not create a "Christmas tree"
effect where every policy sentence is highlighted.

### Final Comment

PRISM is a good HCI contribution if the paper treats the workbench as decision
support under ambiguity. The claim should be: code-aware interfaces shape
reviewer attention and rationale quality.

## PRISM-JUNIOR-06

**Role:** junior privacy auditor / postgraduate student  
**Experience:** 1.5 years privacy/security coursework  
**Feedback lens:** learnability and codebook usability

### Eligibility

| Field | Response |
|---|---|
| Adult | yes |
| Reads technical English | yes |
| Prior privacy coursework | yes |
| Prior PRISM/DataGuard annotation | no |

### Ratings

| Dimension | Rating |
|---|---:|
| Taxonomy usefulness | 6/7 |
| Code clarity | 4/7 |
| Confidence using codebook | 4/7 |
| Need for examples | 7/7 |

### Code Feedback

M1, M2, and M4 are easiest. M3 is understandable but hard to decide because
many policies say "may". M6 and M7 are hardest; I would need examples and
practice questions.

### Affordance Feedback

D2 identifier mapping and D4 no-data prompt would help me most. D8 ambiguity
badge would also help because I would know when disagreement is expected.

### Final Comment

I would need a codebook with examples before using PRISM reliably. Please add
"applies" and "does not apply" examples for every code.

## PRISM-REGULATOR-07

**Role:** regulator analyst / complaint triage officer  
**Experience:** 6 years in digital-service complaint review  
**Feedback lens:** triage, prioritisation, and defensible audit notes

### Eligibility

| Field | Response |
|---|---|
| Adult | yes |
| Privacy complaint/audit experience | yes |
| Comfortable with English policies | yes |
| Prior PRISM/DataGuard annotation | no |

### Ratings

| Dimension | Rating |
|---|---:|
| Taxonomy usefulness | 6/7 |
| Triage value | 7/7 |
| Evidence quality support | 6/7 |
| Risk of false escalation | 4/7 |

### Code Feedback

M4 should receive the highest priority. No-data declarations are easy for users
to understand and potentially misleading if contradicted. M1 and M2 are the
next priority. M3 should never escalate alone.

### Affordance Feedback

The workbench should produce a triage summary:

1. high-priority review cues;
2. evidence excerpts;
3. affected Data Safety fields;
4. recommended next action.

### Final Comment

PRISM could help regulators triage complaints faster, but it must keep the
human reviewer in control. I would not accept an automated final classification.

## PRISM-NLP-08

**Role:** privacy NLP engineer  
**Experience:** 7 years building document-classification and retrieval tools  
**Feedback lens:** lexicon robustness, model training, and benchmark design

### Eligibility

| Field | Response |
|---|---|
| Adult | yes |
| NLP/document AI experience | yes |
| Privacy-policy modelling experience | yes |
| Prior PRISM/DataGuard annotation | no |

### Ratings

| Dimension | Rating |
|---|---:|
| Taxonomy usefulness | 5/7 |
| Lexicon operationalisability | 5/7 |
| Model training value | 6/7 |
| False-positive risk | 5/7 |

### Code Feedback

The taxonomy is model-friendly, but the lexicon should be treated as weak
supervision, not ground truth. M3 will overfire because modal language is very
common. M1 and M2 are better candidates for high-precision extraction if named
SDKs and identifier dictionaries are maintained.

### Affordance Feedback

For D1, named-entity extraction should identify recipients and purposes. For
D3, hedge highlighting should include surrounding context. For D8, ambiguity
should be learned from reviewer disagreement, not only from code presence.

### Final Comment

PRISM can become a useful benchmark if it releases code labels, evidence
snippets, lexicon hits, and human disagreement metadata. The UI should use
model output as ranking support, not a binary detector.

