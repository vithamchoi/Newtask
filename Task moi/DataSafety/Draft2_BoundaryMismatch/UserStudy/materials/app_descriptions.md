# Fictional app pool (12 apps; participants see a stratified random 4)

The prototype now ships with a **pool of 12 fictional apps**. Each
participant is shown a **random subset of 4 apps**, sampled
deterministically from their Prolific ID with a stratification rule
that guarantees at least one app from each of the three typology
families (Reversibility, Recipient, Consent). Sampling is implemented
in `prototype/app.js` via a hash-seeded PRNG so the assignment is
reproducible.

## Why a pool rather than 4 fixed apps?
- **Internal validity.** Idiosyncratic features of any single app
  (icon colour, tagline, fictional brand resonance) get averaged out
  across participants.
- **External validity.** Reviewers will see that the BLE pattern is
  not over-fitted to four hand-chosen vignettes.
- **Statistical power.** Variance attributable to "app" is now a
  random effect we can model out, which tightens the BLE-vs-current
  estimate.

## How sampling works
1. Each contested cell in `apps.json` is tagged with its typology
   family (Reversibility, Recipient, Consent, or Capability).
2. For participant `pid`, we hash `pid + "2024-bcm-bleeval"` with
   FNV-1a, seed Mulberry32, shuffle the pool, then greedily pick
   apps until each of the three families is covered at least once;
   we top up to $K{=}4$ at random.
3. The chosen subset is logged in the interaction log
   (`participant_assigned` event) so the analyst can reproduce it.

## Pool members (12 apps)

## SocialNova
- Type: short-video social.
- Boundary cases exercised: **$b_7$** (service provider) and
  **$b_9$** (anonymised transfer).
- Why this app: pairs two of the most contested cases (51.7\% and
  55.2\% accept in the filtered survey) so the participant sees the
  worst-case BLE drawer first.

## ChatBuzz
- Type: group messaging.
- Boundary case exercised: **$b_2$** (end-to-end encryption) and
  **$b_8$** (legal transfer for fraud).
- Why this app: $b_2$ is the *easiest* case (69.0\% accept). If the
  BLE drawer adds nothing here it adds nothing anywhere, so this is
  the BLE-pattern ceiling test.

## PhotoPals
- Type: shared photo albums.
- Boundary cases exercised: **$b_1$** (on-device only) on collection
  and **$b_5$** (user-initiated transfer) on sharing.
- Why this app: $b_1$ and $b_5$ are the affordance-positive cases
  (acceptance $\geq 58.6$\%), letting us measure whether BLE survives
  user agreement.

## MapMate
- Type: location-based social.
- Boundary cases exercised: **$b_3$** (off-device ephemeral) on
  collection, **$b_6$** (prominent consent) and **$b_9$** (anonymised)
  on sharing.
- Why this app: MapMate stacks three contested boundary cases at
  once, letting us measure drawer-set discoverability when the
  participant has to choose which to open.

## App design choices we did **not** make
- We did not use real branded apps (Facebook, Instagram, etc.) so
  participants' brand attitudes do not contaminate the renderer
  manipulation.
- We did not include any health, finance, or children's apps so the
  contextual norms (Nissenbaum 2004) remain within the social-app
  family used in the published survey.
- We did not include any app with a single boundary case so the
  drawer affordance is exercised at multiple levels of density in
  every participant's run.
