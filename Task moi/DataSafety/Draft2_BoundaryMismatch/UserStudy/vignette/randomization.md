# Randomisation and counter-balancing

## Renderer (between-subjects)
Each participant is randomly assigned to one of:
- **A = current** — Google-Play-style Data Safety renderer
- **B = ble** — BLE-enhanced renderer

Assignment is via Qualtrics's built-in randomiser with **even
presentation** ensured (rather than independent Bernoulli) so the two
groups end up balanced even at small batch sizes.

Server-side mapping:
```
participant.condition = (participant_index % 2 == 0) ? "current" : "ble"
```

## App order (within-subject)
All four apps (SocialNova, ChatBuzz, PhotoPals, MapMate) are presented
to every participant. The order is randomised using a **Latin square**
of order 4:

| Sequence | App 1 | App 2 | App 3 | App 4 |
|---|---|---|---|---|
| L1 | SocialNova | ChatBuzz | PhotoPals | MapMate |
| L2 | ChatBuzz   | PhotoPals  | MapMate    | SocialNova |
| L3 | PhotoPals  | MapMate    | SocialNova | ChatBuzz |
| L4 | MapMate    | SocialNova | ChatBuzz   | PhotoPals |

Each participant is assigned one of the 4 sequences with equal
probability.

## MCQ option order (within-item)
Within each comprehension MCQ, the four options are shuffled per
participant per app. The correct answer's screen position is logged
to enable a post-hoc check for position-based response bias.

## Likert anchors
The 7-point Likert anchors are **always** in the same direction
(1 = negative, 7 = positive) for L3.2, L3.3, L3.4, and L5.2 to keep
within-participant interpretation stable. The IUIPC item (L2.3) is
1--10 to remain comparable with prior literature.

## Reproducibility
The randomisation seed for the published analysis will be the
Prolific batch ID concatenated with `2024-bcm-vignette` and hashed
with SHA-256. The hash is fixed prior to data collection.

## Stratification
We do **not** stratify on demographic variables at recruitment but
will report the realised demographic balance across conditions in
Section 7 of the paper.
