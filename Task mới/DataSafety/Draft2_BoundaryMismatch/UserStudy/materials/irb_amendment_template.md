# IRB amendment — letter template

> **How to use this file.** Replace every `[bracketed]` field below
> with the relevant value, paste the result into your institution's
> ethics-amendment form, and attach (a) the participant consent text
> (`vignette/consent.md`), (b) the full survey instrument
> (`vignette/instrument.md`), (c) the moderator protocol
> (`thinkaloud/protocol.md`), and (d) this pre-registration
> (`analysis/osf_preregistration.md`).

---

**To:** [Institutional Research Ethics Committee / HREC]
**From:** [Principal Investigator name + email]
**Date:** [submission date]
**Re:** Amendment to study [ORIGINAL HREC NUMBER] — *Understanding
Android privacy disclosures* — adding a comparative evaluation of a
prototype label renderer.

## 1. Background

The originally approved study (HREC #[NUMBER], approved [DATE])
collected survey responses from 87 Android users on Microworkers
about Google Play's Data Safety section. The protocol covered
demographic items, judgments of category personalness and purpose
acceptance, judgments of nine policy "boundary cases", and
app-instance necessity ratings across a corpus of 310 fictional and
real social apps.

The present amendment proposes to **add a comparative evaluation of
a prototype label renderer**, the *Boundary-Layer Explainer* (BLE),
designed on the basis of those original survey findings. The
amendment introduces a new data-collection arm; **no participant
from the original study will be re-contacted**.

## 2. What is being added

### 2.1 Arm A — online vignette experiment (between-subjects)
- **Participants:** approximately 200 Prolific workers (target
  $\geq 80$ valid per condition after pre-registered exclusions).
- **Eligibility:** current Android user; English fluency; $\geq 18$
  years; Prolific approval rating $\geq 95\%$; $\geq 50$ prior
  submissions.
- **Compensation:** USD~\$3 for a median completion time of 15
  minutes.
- **Manipulation:** random assignment to one of two label
  renderers — `current` (mimics Google Play Data Safety) or `ble`
  (adds a small explainer drawer per contested cell with a
  one-line rule clause, community-acceptance signal, and a
  counter-factual toggle).
- **Measures:** boundary-case comprehension MCQ, three 7-point
  Likerts (perceived accuracy, perceived comprehensiveness,
  installation intent), one free-text rationale per app,
  drawer-engagement events, demographic items.

### 2.2 Arm B — think-aloud sessions (qualitative)
- **Participants:** 12--15 Prolific workers (separately recruited,
  excluded from Arm A).
- **Format:** 30--45 minute remote video sessions (Zoom). Audio
  and screen recorded with verbal consent at session start.
- **Compensation:** USD~\$25 gift card.
- **Procedure:** participants share their screen and walk through
  the same prototype, narrating their thoughts. The moderator
  follows a structured probe list and avoids leading questions.

### 2.3 Apps
Both arms use a pool of **12 fictional apps**. Each participant
sees a randomly sampled subset of 4, stratified to cover the three
typology families (Reversibility / Recipient / Consent). No real
app brands are referenced. App developers, taglines, and icons are
fictional.

### 2.4 Pre-registration
A pre-registration following the OSF Standard template will be
locked on the Open Science Framework before recruitment opens.
The locked form, the analysis pipeline, the consent text, and the
moderator protocol will be released publicly with the resulting
publication.

## 3. Why this amendment is low-risk

- **No biometric or device data is collected.** The prototype reads
  no permissions, requests no system access, and loads no
  third-party scripts. The HTML/CSS/JS are self-contained.
- **No clinical, vulnerable, or minor population is involved.**
  Recruitment is restricted to consenting adults.
- **The fictional apps do not show distressing, political, sexual,
  or otherwise sensitive content.** Privacy reasoning is the only
  domain.
- **Participants may withdraw at any moment** without penalty. The
  consent screen states this explicitly and the platform allows
  free withdrawal of payment-eligibility.
- **Data residency** is governed by the deployment choice for the
  backend (see `backend/deploy_apps_script.md`). If the
  institution requires Australian residency, the backend will be
  hosted on the institutional infrastructure rather than Google
  Apps Script. The on-the-wire payload is identical.

## 4. Risks and mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| Participant misreads "fictional app" cue and believes they are inspecting a real app's privacy practices | low | Explicit fictional-app statement on consent and debrief screens; familiar Data Safety formatting only, not familiar brands. |
| Drawer text raises concerns about the participant's own real apps | low | Debrief script offers the privacy-resource link of the participant's choice of regulator (ACMA, ICO, FTC). |
| Crowd-work attention loss | medium | Attention check; completion-time floor; honest self-report item; analysis-pre-registered exclusions. |
| Re-identification via free-text | very low | Free text fields are short ($\leq 1$ sentence) and explicitly framed as design feedback. The consent screen states that any text the participant types will appear in the de-identified release. |

## 5. Data management plan

- **Collection.** Responses POSTed from the prototype to a
  research-controlled Google Sheet (or institutional equivalent).
  Each row contains Prolific ID, condition, per-app responses,
  demographic fields, interaction events.
- **Storage.** Sheet shared with the named investigators only;
  exported weekly to an institutional secure drive.
- **Retention.** 5 years post-publication, consistent with the
  institution's research-data policy.
- **De-identification.** Prolific ID is removed before public
  release; only an opaque participant code remains. Free-text
  responses are released verbatim per the consent statement;
  identifying tokens (proper names, locations) are not solicited
  by any item.
- **Public release.** De-identified per-participant table, the
  analysis notebook, and the coded think-aloud transcripts
  (with participant-approved redactions) will be released as
  supplementary material at publication time.

## 6. Materials attached

- (a) Consent form for Arm A (online vignette).
- (b) Consent script for Arm B (think-aloud sessions).
- (c) Full survey instrument.
- (d) Moderator protocol and probe list for Arm B.
- (e) Pre-registration (OSF Standard form).
- (f) Recruitment text for both arms.

## 7. Requested decision

We request approval of this amendment under expedited review on the
grounds that (i) the participant population is the same low-risk
adult crowd-work population covered by the original protocol,
(ii) no biometric, device, or sensitive data is collected, and
(iii) the only material additions are the prototype renderer and a
small set of survey/Likert items already common in IJHCS-class
HCI studies.

If you require any modification, we will respond within 5 working
days.

Sincerely,
[PI name and title]
[Institution]
[Contact email]
