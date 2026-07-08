# DataGuard User Study

Source code and protocol for the controlled, within-subjects user study of
DataGuard described in *The Auditability Gap*, planned as Study 5 of the IJHCS
submission.

**Location.** This folder lives inside `drafts/draft-01-auditability-gap/`
so the controlled-study code sits next to the manuscript. References that
reach outside this folder (for example the retrospective corpus) use three
levels up — e.g. `../../../data-labels.xlsx` for the audit workbook used by
`stimuli/build_pool.py`.

## What this is

A reproducible web-based experiment that exposes each participant to three
privacy-label-audit conditions in counterbalanced order:

| Condition | Interface | Tests |
|-----------|-----------|-------|
| **C0** | Google Play Data Safety panel + raw privacy-policy text (baseline) | Manual audit with current public artefacts |
| **C1** | Side-by-side structured Data Safety + extracted Data Share / Data Collect sections | Information-architecture benefit |
| **C2** | C1 + highlighted candidate policy evidence + AI-suggested label + uncertainty flag | Evidence-grounded AI assistance benefit |

The unit task is to judge one app on four labels (sharing correctness, sharing
completeness, collection correctness, collection completeness) plus rationale.

Dependent variables captured per trial:
- **Accuracy** vs adjudicated gold standard (primary)
- **Task completion time**
- **Self-reported confidence** (per judgment; 0–100 slider)
- **NASA-TLX** workload (six dimensions, post-block)
- **Trust in AI** (TPA scale, post-block, C2 only)

Within-subject factor: condition (C0/C1/C2). App order and condition order
counterbalanced using a Latin-square design. Random effect: participant and
app.

## Repository layout

```
data-guard-user-study/
├── README.md
├── PROTOCOL.md              Full study protocol (IRB-ready)
├── PREREGISTRATION.md       Pre-registered hypotheses + analysis plan
├── CODEBOOK.md              Variable definitions
├── ETHICS_CONSENT.md        Informed-consent template
├── DEBRIEF.md               Post-study debrief script
├── requirements.txt         Python dependencies
├── backend/
│   ├── app.py               Flask server
│   ├── db.py                SQLite schema + accessors
│   ├── randomization.py     Latin-square + stratified app sampling
│   ├── stimuli.py           Stimulus loader
│   └── auth.py              Participant token auth
├── frontend/
│   ├── index.html           Consent + landing
│   ├── tutorial.html        Walkthrough
│   ├── trial.html           Main trial UI
│   ├── css/study.css
│   └── js/
│       ├── trial_engine.js
│       ├── conditions/
│       │   ├── c0_raw.js
│       │   ├── c1_structured.js
│       │   └── c2_evidence.js
│       └── instruments/
│           ├── nasa_tlx.js
│           ├── confidence.js
│           └── trust.js
├── stimuli/
│   ├── stimuli_pool.json    24 stimulus apps, 3 strata × 8
│   ├── gold_standard.json   Adjudicated labels
│   └── README.md            Stratification scheme
├── evidence_locator/
│   ├── locate.py            LLM-assisted evidence highlighting (C2)
│   └── prompts.yaml
├── analysis/
│   ├── power_analysis.py    Pre-study power calculation
│   ├── mixed_effects.py     Mixed-effects models (statsmodels)
│   ├── mixed_effects.R      Mixed-effects models (lme4) -- preferred
│   ├── calibration.py       Brier score + reliability diagrams
│   ├── effect_sizes.py      Bootstrap CIs for between-condition deltas
│   └── plots.py             Result figures
├── data/
│   ├── raw/                 Raw responses (gitignored)
│   ├── processed/           Cleaned per-trial data
│   └── README.md
└── tests/
    ├── test_randomization.py
    ├── test_stimuli.py
    └── test_responses.py
```

## Quick start

```bash
# 1. Set up
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Initialise DB and load stimuli
python -m backend.db --init
python -m backend.db --load stimuli/stimuli_pool.json

# 3. Run server
flask --app backend.app run --debug

# Server now listens on http://127.0.0.1:5000
# Browse to /consent to start a participant session.
```

## Expert-feedback deployment

The current checked-in stimulus pool contains a short three-app sample, so the
production default is `DATAGUARD_STUDY_MODE=feedback`. This mode is intended
for collecting formative expert feedback on the interface and materials. See
`DEPLOYMENT.md` for Docker and Render deployment instructions.

## Pre-study checklist

- [ ] IRB / ethics approval on file (see `PROTOCOL.md`, §Ethics).
- [ ] Gold standard adjudicated by two expert coders.
- [ ] Stimulus pool stratified across three strata (high-confidence, high-disagreement, no-data).
- [ ] Pilot run with ≥4 participants to debug.
- [ ] Power-calculation sign-off (see `analysis/power_analysis.py`).
- [ ] Preregistration on OSF (template in `PREREGISTRATION.md`).

## Sample size & power

Target: **N = 30 participants** × 24 stimulus apps × 3 conditions =
~2,160 trials (after counterbalancing). Mixed-effects logistic with
participant + app random intercepts; primary contrast C2 vs C0 on accuracy.
See `analysis/power_analysis.py` for the simulation-based power study.

## License

Apache-2.0 (code), CC-BY-4.0 (protocol and instruments).

## Citation

If you use this framework, please cite the parent paper:

> *The Auditability Gap: A Human-Centered Study of Privacy-Label
> Verification in the Google Play Data Safety Ecosystem.*
> Submitted to the International Journal of Human-Computer Studies.
