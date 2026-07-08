# DG-COMPLIANCE-01 — Target-User Comments

**Participant/expert type:** privacy and compliance analyst  
**Relevant experience:** 6 years reviewing mobile/web privacy disclosures  
**Data Safety familiarity:** moderate  
**Perspective:** likely user of a DataGuard-like audit interface

## Overall Assessment

DataGuard addresses a workflow I recognise: I need to compare a short,
developer-declared privacy label with a policy that may use different language,
different categories, and legal hedging. The value is not that the system tells
me whether an app is "bad"; the value is that it helps me build an evidence
trail for a judgment.

The study's concept of auditability is practical. In my normal work, a label is
not useful unless I can answer: "Where in the policy is this supported?" or
"Where does the policy contradict or omit this claim?" The interface conditions
map naturally to real workflows: raw review, structured review, and
evidence-assisted review.

## Ratings

| Question | Rating | Comment |
|---|---:|---|
| Is the task understandable? | 4/5 | Understandable after the tutorial; needs a stronger example for completeness. |
| Is auditability a useful concept? | 5/5 | Yes. It names the real review burden. |
| Would I use C0 raw review? | 2/5 | Only if forced; it is slow and easy to miss evidence. |
| Would I use C1 structured review? | 4/5 | Good for independent manual review. |
| Would I use C2 AI evidence support? | 4/5 | Useful as passage-finding support; should not auto-decide. |
| Do I trust the AI suggestion? | 3/5 | I trust highlighted evidence more than suggested verdicts. |

## Detailed Comments

### What worked

- Separating sharing correctness, sharing completeness, collection
  correctness, and collection completeness matches how I actually review
  disclosures.
- The Ambiguous option is necessary. Many policies are too vague for a clean
  binary answer.
- The strongest interface feature is the visible evidence passage. It lets me
  justify the decision later.
- C1 already reduces burden by separating Data Share and Data Collect sections.
- C2 is especially helpful on "no data" cases where the policy mentions AdMob,
  advertising identifiers, Firebase, analytics, crash logs, cookies, or
  IP-derived location.

### What was difficult

- Correctness vs completeness is still hard. I need more examples:
  - correct but incomplete;
  - incorrect but complete;
  - ambiguous because the policy is vague;
  - insufficient evidence because the policy does not mention the category.
- Some policy phrases do not map cleanly to Google categories. Examples:
  "usage information", "log data", "technical information", "device
  information", "diagnostic data", and "personal information".
- A single evidence text box is less ideal than selecting evidence spans
  directly in the policy panel.
- I would be cautious about using "defect" language if there is no adjudicated
  gold standard. I would call these reviewer-flagged audit concerns.

## Suggested User-Facing Wording Changes

Current framing I would avoid:

> The app's label is wrong.

Preferred framing:

> The policy text does not provide clear support for this Data Safety claim, or
> appears to describe a data practice missing from the label.

Current framing I would avoid:

> AI-suggested judgment.

Preferred framing:

> Candidate evidence located by the assistant; reviewer must inspect before
> deciding.

## Final Free-Text Comment

If this were a deployed review tool, I would want it to help me produce a
defensible audit note, not a one-click verdict. The main benefit is evidence
grounding. The system should surface relevant passages, show uncertainty, and
leave the final interpretation to the reviewer. I would also strongly recommend
a category glossary and direct text selection for evidence capture.

