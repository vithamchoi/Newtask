# Vignette experiment — protocol

## Purpose
Measure whether the Boundary-Layer Explainer (BLE) renderer changes
boundary-case **comprehension**, perceived **label accuracy**, and
**installation intent** compared to the current Google Play Data Safety
section, in a between-subjects online study with crowd-recruited
participants.

## Design
- **Type:** Between-subjects vignette experiment (online).
- **IV:** Renderer (2 levels): \texttt{current} vs \texttt{ble}.
- **Within-subject factor:** App (4 levels, randomised order):
  SocialNova, ChatBuzz, PhotoPals, MapMate. Each app exposes a
  different sub-set of the nine boundary cases
  (see `materials/app_descriptions.md`).
- **Random assignment:** 50/50 to renderer at the participant level
  (see `randomization.md`).
- **Target N:** 100 valid responses per condition (200 total).
  After exclusions (attention check, completion-time floor) we expect
  $\geq 80$ per condition (see `sample_size.md`).

## Hypotheses
Pre-registered in `analysis/preregistration.md`. Briefly:
- **H1 (comprehension).** BLE participants score higher on a
  boundary-case comprehension quiz than current-label participants.
- **H2 (perceived accuracy).** BLE participants rate the label as
  more accurately describing the app's data practices.
- **H3 (installation intent shift).** BLE participants are more
  likely to revise their installation intent after viewing the
  label than current-label participants.
- **H4 (uncertainty signalling).** Within the BLE condition, drawer
  openings are higher for cases with higher Maybe-rates in the
  published survey ($b_3, b_9$).
- **H5 (no global install-intent effect).** Mean installation intent
  is **not** different between conditions; the effect is on
  *quality* of the decision (accuracy, comprehension), not on the
  intent itself. This is a null-effect hypothesis with directional
  pre-specification.

## Recruitment
- **Platform:** Prolific (preferred over MTurk for label-quality;
  Microworkers backup).
- **Inclusion:** Android user, English fluency, $\geq 18$ years,
  approval rating $\geq 95\%$, $\geq 50$ prior submissions.
- **Exclusions (post-hoc):** Fails an attention check, completes the
  study in $< 4$ minutes, fails the comprehension *pre*-test on the
  current-label baseline (to keep population comparable with the
  published survey), or selects the same Likert value on every
  judgment.
- **Compensation:** USD~\$3 for a median completion time of 15
  minutes; this matches Prolific's £9/hr norm.
- **Sample target:** see `sample_size.md`.

## Procedure (per participant)

1. **Consent** (see `consent.md`). Two checkboxes (information sheet
   read, agree to participate). No data is collected until both are
   ticked.
2. **Pre-task** (3 items, $\sim 60$ s). Self-reported Android
   familiarity (5-pt), prior Data Safety inspection (Yes/No/I don't
   recall), self-reported privacy concern (10-pt single item from
   IUIPC).
3. **Randomisation** into condition: \texttt{current} or \texttt{ble}.
   App order is randomised within participant (Latin square across
   the 4 apps to balance order).
4. **For each of the 4 apps** ($\sim 90$ s each):
   - View the label (rendered by the prototype in the assigned
     condition).
   - Comprehension item: a 4-option MCQ asking which boundary case
     produced the contested flag (see `instrument.md` §3).
   - Likert items: perceived accuracy (1--7), perceived
     comprehensiveness (1--7), installation intent (1--7).
   - One free-text item: ``In one sentence, what made you choose that
     intent?''
5. **Post-task** ($\sim 90$ s): attention check, two debrief items
   (saw drawer? / would want it?), demographics (age band, gender,
   country, education).
6. **Debrief** (always shown). Explains that the apps were
   fictional, that the Data Safety section the participant saw was
   based on real Google Play formatting, and that the BLE drawer is
   a research prototype.

## Measures
| Construct | Operationalisation | Scale |
|---|---|---|
| Comprehension | MCQ per app, 1 correct boundary case | 0/1 |
| Perceived accuracy | ``This label accurately describes what this app does with your data.'' | 1--7 |
| Perceived comprehensiveness | ``This label gives me enough information to decide.'' | 1--7 |
| Installation intent (per app) | ``How likely are you to install this app?'' | 1--7 |
| BLE engagement (B only) | Number of drawers opened, time spent open | count, ms |
| BLE toggle use (B only) | Counter-factual toggle opens | count |
| Pre-task privacy concern | Single IUIPC item | 1--10 |
| Attention | One trap item embedded in Likert grid | Pass/Fail |

## Quality controls
- **Attention check:** ``Please select 4 for this item to show
  you are paying attention.''
- **Completion-time floor:** $\geq 4$ min total.
- **Straight-lining flag:** Variance across the 12 Likert items
  (4 apps $\times$ 3 items) $> 0.1$.

## Analysis (high-level)
See `analysis/analysis_plan.md`. Primary tests are independent-samples
$t$ tests with Bonferroni correction across H1--H5, plus
mixed-effects models with participant as random intercept to use the
within-participant structure of the 4 apps. Effect sizes reported as
Cohen's $d$ with 95\% CIs.

## IRB
This protocol is an amendment to the original survey protocol filed
with the principal authors' institutional research ethics board. The
amendment adds the prototype and Likert items; no biometric or
identifying data is collected.

## Timeline
- Week 1: pilot ($N{=}10$); fix instrument bugs; calibrate timer.
- Week 2: full data collection (Prolific batches of 50).
- Week 3: cleaning + analysis + draft Section 7 of the manuscript.
