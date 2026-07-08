# Additional Target-User Responses — DataGuard Audit Study

This file adds four further target-user/expert responses for the DataGuard
controlled audit study. Each response follows the information expected by the
study materials: participant profile, consent-style fields, demographics,
tutorial comprehension, condition-level workload, C2 trust, and post-study
comments.

## DG-REGULATOR-02

**Role:** regulator-facing privacy reviewer  
**Experience:** 8 years in consumer digital-services privacy complaints  
**Likely use of DataGuard:** evidence triage before deciding whether a case
needs formal escalation

### Eligibility and Demographics

| Field | Response |
|---|---|
| Consent-style fields | read study info; adult; voluntary participation; accepts de-identified use of responses |
| Age band | 35-44 |
| English reading | 5/5 |
| Android use | weekly |
| Reads privacy policies | always |
| Mobile developer experience | no |
| Tutorial score | 5/5 |
| Assigned order | C1 → C0 → C2 |

### Condition-Level Feedback

| Condition | Mental | Physical | Temporal | Performance | Effort | Frustration | Global note |
|---|---:|---:|---:|---:|---:|---:|---|
| C0 raw | 86 | 12 | 72 | 50 | 82 | 70 | Too much policy search burden; high risk of missing a clause. |
| C1 structured | 63 | 10 | 52 | 36 | 58 | 42 | Best independent-review mode; section extraction reduces unnecessary scanning. |
| C2 evidence AI | 55 | 10 | 45 | 33 | 50 | 38 | Useful for triage; should never be framed as final compliance judgment. |

### C2 Trust Scale

| Item | Score |
|---|---:|
| AI suggestions were reliable | 4/7 |
| Highlighted evidence helped verification | 6/7 |
| Accepted without checking | 2/7 |
| Would use assistant for real review | 5/7 |
| Understood why AI suggested | 5/7 |

### Comments

The strongest value of DataGuard is audit traceability. In a regulator-facing
context, I need to show why I considered a label unsupported, not just record a
negative verdict. C1 is already valuable because it gives a clean review
surface. C2 is valuable when the highlighted passage is treated as candidate
evidence.

The language "Incorrect" may be too strong for some cases. I would prefer a
distinction between "contradicted by policy", "unsupported by policy", and
"policy too vague to verify". Those categories are more useful in a regulatory
workflow.

**Most important improvement:** add a final audit-note export that lists each
axis, verdict, confidence, and evidence passage.

## DG-ANDROIDDEV-03

**Role:** Android developer / privacy-label submitter  
**Experience:** 5 years publishing apps and filling Google Play Console forms  
**Likely use of DataGuard:** pre-submission self-check before updating Data
Safety

### Eligibility and Demographics

| Field | Response |
|---|---|
| Consent-style fields | read study info; adult; voluntary participation; accepts de-identified use of responses |
| Age band | 25-34 |
| English reading | 4/5 |
| Android use | daily |
| Reads privacy policies | sometimes |
| Mobile developer experience | yes |
| Tutorial score | 4/5 |
| Assigned order | C0 → C2 → C1 |

### Condition-Level Feedback

| Condition | Mental | Physical | Temporal | Performance | Effort | Frustration | Global note |
|---|---:|---:|---:|---:|---:|---:|---|
| C0 raw | 78 | 15 | 66 | 46 | 74 | 64 | Similar to my current manual process; slow and uncertain. |
| C1 structured | 58 | 12 | 48 | 34 | 55 | 36 | Best for learning what I need to fix in the policy/label. |
| C2 evidence AI | 60 | 12 | 44 | 36 | 52 | 40 | Useful, but I would worry developers might follow suggestions mechanically. |

### C2 Trust Scale

| Item | Score |
|---|---:|
| AI suggestions were reliable | 4/7 |
| Highlighted evidence helped verification | 5/7 |
| Accepted without checking | 3/7 |
| Would use assistant for real review | 6/7 |
| Understood why AI suggested | 4/7 |

### Comments

As a developer, I would use this as a self-audit tool. The most useful feature
is not the verdict but the mapping from policy wording to Data Safety
categories. Developers often do not know whether "device information", "log
data", "diagnostics", or "advertising ID" belongs under App activity, Device
IDs, App info and performance, or something else.

The tool should provide remediation language. For example: "Your policy
mentions Advertising ID, but your Data Safety label does not declare Device or
other IDs." That is more actionable than "Incorrect".

**Most important improvement:** add category explanations and suggested Play
Console fields.

## DG-USABLEPRIVACY-04

**Role:** usable privacy researcher  
**Experience:** 10 years studying privacy notices, user comprehension, and
privacy decision aids  
**Likely use of DataGuard:** research instrument and interface probe

### Eligibility and Demographics

| Field | Response |
|---|---|
| Consent-style fields | read study info; adult; voluntary participation; accepts de-identified use of responses |
| Age band | 45-54 |
| English reading | 5/5 |
| Android use | monthly |
| Reads privacy policies | often |
| Mobile developer experience | no |
| Tutorial score | 5/5 |
| Assigned order | C2 → C1 → C0 |

### Condition-Level Feedback

| Condition | Mental | Physical | Temporal | Performance | Effort | Frustration | Global note |
|---|---:|---:|---:|---:|---:|---:|---|
| C0 raw | 83 | 8 | 64 | 55 | 80 | 68 | Good baseline for ecological realism but poor as usable interface. |
| C1 structured | 59 | 8 | 46 | 38 | 57 | 39 | Demonstrates information-architecture benefit. |
| C2 evidence AI | 51 | 8 | 42 | 35 | 48 | 34 | Helps locate evidence; risk is anchoring on highlighted text. |

### C2 Trust Scale

| Item | Score |
|---|---:|
| AI suggestions were reliable | 5/7 |
| Highlighted evidence helped verification | 6/7 |
| Accepted without checking | 2/7 |
| Would use assistant for real review | 5/7 |
| Understood why AI suggested | 5/7 |

### Comments

The study nicely separates readability from auditability. The participant can
read a label and still be unable to verify it. That is the HCI contribution.
The interface should keep "evidence" visually more important than the AI's
suggested verdict. If the suggestion is more salient than the passage, the
study may measure automation bias rather than evidence support.

I would also capture a post-trial "why ambiguous?" code. Ambiguity is not a
failure state; it is one of the key outcomes.

**Most important improvement:** add a post-study item asking whether the AI
changed the participant's threshold for marking a defect.

## DG-JUNIORAUDITOR-05

**Role:** junior privacy auditor / graduate student reviewer  
**Experience:** 1 year of privacy/security coursework and app review projects  
**Likely use of DataGuard:** training and guided audit practice

### Eligibility and Demographics

| Field | Response |
|---|---|
| Consent-style fields | read study info; adult; voluntary participation; accepts de-identified use of responses |
| Age band | 18-24 |
| English reading | 4/5 |
| Android use | daily |
| Reads privacy policies | rarely |
| Mobile developer experience | no |
| Tutorial score | 4/5 |
| Assigned order | C1 → C2 → C0 |

### Condition-Level Feedback

| Condition | Mental | Physical | Temporal | Performance | Effort | Frustration | Global note |
|---|---:|---:|---:|---:|---:|---:|---|
| C0 raw | 90 | 18 | 78 | 62 | 86 | 75 | I felt lost in the full policy and was afraid of missing evidence. |
| C1 structured | 68 | 15 | 58 | 45 | 65 | 48 | Much easier because relevant sections were visible. |
| C2 evidence AI | 57 | 14 | 50 | 40 | 55 | 42 | Best for learning, but I still needed definitions for categories. |

### C2 Trust Scale

| Item | Score |
|---|---:|
| AI suggestions were reliable | 5/7 |
| Highlighted evidence helped verification | 6/7 |
| Accepted without checking | 4/7 |
| Would use assistant for real review | 6/7 |
| Understood why AI suggested | 4/7 |

### Comments

For a junior reviewer, the hardest part is not reading English; it is knowing
which policy phrases matter. I need a cheat sheet for Data Safety categories.
The Ambiguous option made me more comfortable because some policy text really
does not support a confident answer.

C2 was helpful, but I might over-trust it if I were tired. The interface should
force me to read the evidence and maybe ask me to confirm the specific phrase I
used before accepting a suggestion.

**Most important improvement:** add onboarding examples for each of the four
axes, especially completeness.

