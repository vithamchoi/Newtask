# Think-aloud study — moderator protocol

## Purpose
Capture, in fine detail, **how** users encounter and reason about the
BLE drawers when they look at an app's Data Safety section. The
vignette experiment will tell us *whether* BLE moves the needle on
comprehension and intent; the think-aloud will tell us *why* it does
or does not, and which parts of the drawer text fail or surprise.

## Format
- **Mode:** Remote video session (Zoom / Meet), screen-share required.
- **Duration:** 30–45 minutes per participant.
- **Recording:** Audio + screen, with explicit verbal consent at the
  top of each session. No webcam needed.
- **Target N:** 12–15 participants, recruited until thematic
  saturation (the standard rule of thumb for think-aloud usability
  studies is $N{=}5$ for major issues, $N{=}10$ for moderate, and
  $N{=}15$ for thorough coverage).
- **Compensation:** USD~\$25 e-gift card.

## Recruitment
- Posted through the same Prolific account as the vignette but
  filtered to **English fluency, current Android user, no prior
  participation in the vignette arm.** This prevents cross-arm
  contamination.
- Demographic balance: target 50/50 gender; range across age bands.

## Setup checklist (moderator)
- [ ] Recording started (audio + screen).
- [ ] Consent confirmed verbally on tape.
- [ ] Prototype URL pre-loaded in a shared browser tab.
- [ ] Notes document open in moderator's other monitor.
- [ ] 5-min hard buffer at start in case of share-setup issues.

## Phases (timing approximate)

### 1. Warm-up (3 min)
> "Thanks for joining. Before we start I want to remind you that
> we're testing the design, not you. There's no right or wrong
> answer — please say whatever comes to mind. If anything is
> confusing, please describe what's confusing in your own words.
> Are you ready to share your screen?"

Ask one warm-up question to verify the participant can speak fluently
while looking at a screen:
> "Could you show me how you usually install an app on your phone, and
> say what you look at before tapping Install?"

### 2. Calibration with current condition (5 min)
> "I'm going to load a privacy label for a fictional app. Please
> look at it the way you would normally look at one, and tell me
> what you're noticing as you go."

Open `prototype/current.html?app=socialnova`. Let the participant
explore. Take notes (don't intervene). After they've read it once,
prompt:
> "Suppose you were deciding whether to install SocialNova. Would
> you install it? What would make you change your mind?"

This is the **baseline** — the participant's reading of a current Data
Safety section. Move on once you have a clear baseline narrative.

### 3. Main think-aloud with BLE condition (15 min, 3 apps)
Open `prototype/ble.html?app=chatbuzz`, then PhotoPals, then MapMate
in counter-balanced order across participants (see `tasks.md`).

For each app, ask the participant to think aloud as they read. Use
the probes in `probes.md` **only when prompted by their reading**.
Specifically, probe:
- The first time they encounter a drawer ("what do you think this
  is?", "what is it telling you?")
- The first time they open the counter-factual toggle ("what does
  that change? does it surprise you?")
- The first time they skip a drawer ("what made you skip past
  that?")

Note times of all drawer opens / closes / toggle opens.

### 4. Comparative probe (5 min)
After the third BLE app, switch back to one of the current-condition
apps the participant has not seen (e.g., MapMate):
> "Here is the same kind of label as the first one, without the
> yellow boxes. Compared to what you just looked at, what does this
> one tell you, and what does it not?"

This is the **counter-factual elicitation**. The point is to surface
what was added by BLE, in the participant's own words.

### 5. Debrief and Likert (5 min)
- 4 single-item Likerts (clarity, helpfulness, trust, would-want).
- Two open-ended questions:
  - "What would you cut from the BLE drawer?"
  - "What would you add?"
- Thank-you and gift-card delivery instructions.

## Things to **not** do (moderator hygiene)
- Do **not** explain what a boundary case is. Let the participant
  arrive at (or fail to arrive at) the concept on their own.
- Do **not** read drawer text aloud for them. We want their reading,
  not yours.
- Do **not** suggest the drawer's intended interpretation. Probe
  open-endedly.

## Outputs per session
- Audio + screen recording (stored on encrypted institutional drive).
- Moderator notes (one document per participant, structured by
  phase).
- Time-coded list of drawer opens/closes (from the prototype log
  in `localStorage` plus moderator timer).
- Likert scores (4 items per participant).
