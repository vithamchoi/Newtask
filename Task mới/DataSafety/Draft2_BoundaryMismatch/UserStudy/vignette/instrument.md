# Vignette experiment — full survey instrument

Items in this order. Items prefixed `[Q]` are forced-choice; `[L]` are
7-point Likert; `[T]` are free-text; `[A]` are attention checks.

---

## §1 Consent
*(see `consent.md`)*

## §2 Pre-task

**Q2.1** How long have you used an Android phone?
- Less than 1 year
- 1–3 years
- 3–5 years
- More than 5 years
- I do not currently use an Android phone *(disqualify)*

**Q2.2** Before today, had you ever looked at the **Data Safety**
section of an app on Google Play?
- Yes, regularly
- Yes, occasionally
- I might have but I don't recall
- No, never
- I don't know what that is

**L2.3** On a scale of 1 to 10, how concerned are you about personal
data being collected from your phone?
*(1 = not at all concerned, 10 = extremely concerned)*

## §3 Per-app block

The participant sees this block four times, once per app, in a Latin-
square randomised order. The renderer (current vs BLE) is fixed across
all four apps within the participant.

For app $a \in \{$SocialNova, ChatBuzz, PhotoPals, MapMate$\}$:

**[label]** *The prototype renders the Data Safety section for app $a$ under the participant's assigned condition. Time-on-page is logged.*

**Q3.1** Which of the following best describes what this app does
with **{contested\_category}**?
- (correct) **{boundary-case description}**, in plain language drawn from the BLE pattern
- (distractor 1) **{plausible-other-boundary description}**
- (distractor 2) **{plausible-other-boundary description}**
- I cannot tell from this label

*(The MCQ is constructed so the correct answer is the boundary case
applied by the developer in `apps.json`. Distractors are taken from
adjacent boundary cases in the same family.)*

**L3.2** This label accurately describes what this app does with your
data.
*(1 = strongly disagree, 7 = strongly agree)*

**L3.3** This label gives me enough information to decide whether to
install this app.
*(1 = strongly disagree, 7 = strongly agree)*

**L3.4** How likely are you to install this app?
*(1 = definitely would not, 7 = definitely would)*

**T3.5** In one sentence, what made you choose that answer?

## §4 Attention

**A4.1** To show you are paying attention, please select **4** for
this item.

## §5 Post-task (BLE condition only)

**Q5.1** During the study, did you open any of the **Boundary-Layer
Explainer** drawers (the yellow boxes attached to some rows)?
- Yes, I opened several
- Yes, I opened one
- I noticed them but didn't open them
- I don't remember seeing them

**Q5.2** If a real privacy label looked like the one you just saw,
how useful would you find the BLE drawer?
*(1 = not at all useful, 7 = extremely useful)*

**T5.3** What would you change about the BLE drawer to make it more
useful?

## §6 Post-task (both conditions)

**Q6.1** Have you completed the four apps in good faith and read each
label before answering?
- Yes
- No, I rushed some
*(no penalty for honest answer; flagged in cleaning)*

**T6.2** Anything else you want to tell us about the label you just
saw?

## §7 Demographics

**Q7.1** Age band: 18–24 / 25–34 / 35–44 / 45–54 / 55–64 / 65+ / prefer
not to say.

**Q7.2** Gender: woman / man / non-binary / prefer to self-describe
[free text] / prefer not to say.

**Q7.3** Country of residence (free text, Prolific autofill).

**Q7.4** Highest completed education: high school / some college /
bachelor's / master's / doctoral / other.

**Q7.5** Do you work in computing, IT, or cybersecurity? Yes / No /
Prefer not to say.

## §8 Debrief screen

```
Thank you for completing the study.

The apps you just saw (SocialNova, ChatBuzz, PhotoPals, MapMate) are
fictional and were created for research purposes only. The Data
Safety section you saw was based on the real format used by Google
Play; the Boundary-Layer Explainer (BLE) is a research prototype that
does not yet exist in the real Play Store.

Your responses will be used as part of a study evaluating whether
this design helps users understand app privacy disclosures. No
personally identifiable information will be associated with your
responses in any publication.

If you have questions, please contact the research team via the
Prolific message system.
```

---

## Item-construction notes

- The MCQ (Q3.1) is **identical in both conditions** so the comparison
  is purely the renderer's effect on comprehension.
- L3.2 and L3.3 are derived from the perceived-accuracy items in
  Zhang et al. (2022).
- L3.4 is the standard purchase/install-intent item used widely in
  IJHCS-class studies.
- T3.5 is included to enable a light qualitative pass that
  triangulates with the think-aloud arm.

## Estimated time

~13–17 minutes total, with median around 15 minutes.
