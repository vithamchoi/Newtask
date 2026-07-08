# Think-aloud — task scenarios

## Task framing
Across the session, each participant performs **one calibration task**
in the current condition and **three main tasks** in the BLE
condition. After the third BLE task, a **comparative re-look** at one
current-condition app is added. Each task is built around an
installation decision.

## Calibration task (current condition)

**App:** SocialNova
**Wording:**
> "Suppose you're scrolling Google Play looking for a new social app
> and you find SocialNova. Take a look at the privacy section the
> way you normally would, and tell me what you'd do."

**Why this app:** SocialNova carries two contested cells (Device IDs
shared via $b_7$; App activity shared via $b_9$) which gives the
participant a baseline reading of the binary flag interpretation.

## Main task A (BLE)

**App:** ChatBuzz
**Wording:**
> "Same scenario. You're looking for a messaging app. ChatBuzz says
> it uses end-to-end encryption. Take a look at the privacy
> section."

**What we look for:** Whether the participant opens the $b_2$
(end-to-end encryption) drawer. ChatBuzz is the high-acceptance
baseline; if the drawer adds value here it adds value everywhere.

## Main task B (BLE)

**App:** PhotoPals
**Wording:**
> "Now a photo-sharing app. PhotoPals says your photos stay on your
> phone. Take a look."

**What we look for:** The $b_1$ (on-device only) drawer is the
Capability tier. We expect dissenting participants to surface the
*capability-not-intent* argument from the published survey.

## Main task C (BLE)

**App:** MapMate
**Wording:**
> "Now a location app. MapMate uses your location for navigation and
> for personalisation. Take a look."

**What we look for:** MapMate is the **hardest** of the four apps:
it carries $b_3$ (off-device ephemeral) on collection and $b_6$
(prominent consent) plus $b_9$ (anonymised) on sharing. If a
participant opens all three drawers and toggles at least one, this
is strong qualitative evidence that the drawer set is discoverable
even when stacked.

## Comparative re-look (current condition)

**App:** Switch to one current-condition app the participant has not
seen.
**Wording:**
> "Here's the same kind of privacy section we started with — no
> yellow boxes. Compared to the one you just looked at, what does
> this one tell you, and what does it not?"

**What we look for:** Participants spontaneously naming things the
BLE added (e.g., "I don't know which third party gets it", "there's
no number telling me how many people accept this").

## App-order counter-balancing across 12 participants

| P# | Main A | Main B | Main C | Re-look |
|----|--------|--------|--------|---------|
| 1  | ChatBuzz | PhotoPals | MapMate   | SocialNova |
| 2  | PhotoPals | MapMate   | ChatBuzz  | SocialNova |
| 3  | MapMate   | ChatBuzz  | PhotoPals | SocialNova |
| 4  | ChatBuzz | MapMate   | PhotoPals | SocialNova |
| 5  | PhotoPals | ChatBuzz  | MapMate   | SocialNova |
| 6  | MapMate   | PhotoPals | ChatBuzz  | SocialNova |
| 7  | ChatBuzz | PhotoPals | MapMate   | SocialNova |
| 8  | PhotoPals | MapMate   | ChatBuzz  | SocialNova |
| 9  | MapMate   | ChatBuzz  | PhotoPals | SocialNova |
| 10 | ChatBuzz | MapMate   | PhotoPals | SocialNova |
| 11 | PhotoPals | ChatBuzz  | MapMate   | SocialNova |
| 12 | MapMate   | PhotoPals | ChatBuzz  | SocialNova |

(Calibration always SocialNova; comparative re-look always switches
the renderer condition for the calibration app so the participant
sees the "before/after" on the same app.)
