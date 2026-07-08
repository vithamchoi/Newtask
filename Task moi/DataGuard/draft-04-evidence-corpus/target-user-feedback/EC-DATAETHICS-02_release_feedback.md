# EC-DATAETHICS-02 — Data Ethics and Release Feedback

**Artifact status:** target-user feedback; authored expert feedback  
**Persona:** data ethics / research governance reviewer  
**Likely use:** assess whether public release is responsible and whether the
manuscript handles risk, consent, and reuse clearly.

## Overall Reaction

The Evidence Corpus appears scientifically valuable, but its release needs
careful governance because it connects app identities, policy text, human audit
verdicts, and reviewer behaviour. Even if the source policies are public, the
compiled dataset creates a new reputational and interpretive artifact.

The release is acceptable in principle if the paper clearly separates:

- reviewer-flagged audit evidence from legally adjudicated non-compliance;
- citation behaviour from final compliance judgment;
- intended research/tool-building use from adversarial app ranking.

## Ratings

| Dimension | Rating | Comment |
|---|---:|---|
| Scientific value | 5/5 | Strong resource, likely reusable. |
| Re-identification risk for annotators | 3/5 | Manageable with pseudonymisation and aggregation. |
| Reputational risk for developers | 4/5 | Needs explicit handling. |
| Release readiness | 3/5 | Requires datasheet, redaction policy, and discouraged uses. |
| Ethical clarity in manuscript | 3.5/5 | Good direction, but should be more explicit. |

## Required Ethical Safeguards

Before release, I would expect:

1. **Annotator pseudonymisation:** stable IDs are acceptable, but no age,
   course, institution, or role combination that could identify a reviewer.
2. **Developer/app risk statement:** the corpus is for research and tool
   evaluation, not for public shaming or regulatory enforcement.
3. **Redaction pass:** remove developer emails, phone numbers, accidental
   personal contact details, and non-policy personal information.
4. **Context preservation:** do not release isolated excerpts without enough
   claim/context fields to avoid misinterpretation.
5. **Discouraged-use section:** explicitly prohibit or discourage app ranking,
   developer targeting, and compliance blacklists.
6. **Versioning and takedown process:** define what happens if a developer or
   annotator asks for correction/removal.

## Corpus Card Fields I Want Added

- Collection period.
- Source of policies and labels.
- Whether app names/package IDs are released.
- Whether original URLs are released.
- Whether policies may have changed since capture.
- Who annotated the evidence.
- Whether annotators consented to data release.
- Known skews by category and annotator.
- Intended users.
- Discouraged users/use cases.
- Maintenance contact.
- Version history.

## Main Risk

The biggest risk is that external users treat a human audit verdict as a legal
finding. The paper should repeatedly state that these are trained-reviewer
judgments under a research protocol, not regulatory determinations.

## Recommended Manuscript Wording

Use:

> reviewer-cited evidence associated with an audit verdict

Avoid:

> proof that the app violates privacy rules

Use:

> candidate evidence for evidence-grounded audit tooling

Avoid:

> ground truth compliance labels

## Free-Text Review Comment

I support release if the corpus is framed as an HCI/research artifact rather
than a compliance blacklist. The paper should include a release-governance
subsection with concrete redaction, versioning, and discouraged-use policies.
The dataset should preserve enough structured context to prevent excerpt
misuse, but should avoid exposing unnecessary annotator or developer contact
information.

