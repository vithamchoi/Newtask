# UserStudy — Mixed-method evaluation of the Boundary-Layer Explainer

This folder contains everything you need to launch a mixed-method
evaluation of the BLE renderer that will become Section 7 of the
*Boundary-Case Mismatch* manuscript. Two arms:

1. **Vignette experiment** (between-subjects, online, $N{=}200$).
2. **Think-aloud study** (in-lab, 12--15 participants).

> 👉  **First time here?** Open `QUICKSTART.md` for a one-page summary
> with a step-by-step timeline.

## Folder structure

```
UserStudy/
├── README.md, QUICKSTART.md
├── prototype/                       ← interactive study artifact
│   ├── index.html                      moderator/landing page
│   ├── study.html                      single-page-app participant runner
│   ├── current.html, ble.html          condition-only preview (think-aloud)
│   ├── style.css                       shared stylesheet
│   ├── app.js                          preview renderer
│   ├── study.js                        full SPA controller
│   ├── apps.json                       pool of 12 fictional apps
│   └── mcq_bank.json                   9 per-boundary-case MCQ templates
├── backend/                         ← server-less data capture
│   ├── google_apps_script.gs           Apps Script (paste into your sheet)
│   ├── deploy_apps_script.md           setup walkthrough
│   └── data_schema.json                per-row schema
├── deploy/                          ← hosting guides
│   ├── README.md                       hosting options overview
│   ├── github_pages.md                 GitHub Pages walk-through
│   ├── netlify.md                      Netlify walk-through
│   ├── netlify.toml                    optional Netlify config
│   └── institutional.md                Apache / nginx / RMIT IT
├── vignette/                        ← online experiment
│   ├── protocol.md                     design, hypotheses, procedure
│   ├── instrument.md                   full survey items
│   ├── consent.md                      consent form
│   ├── randomization.md                assignment + counter-balancing
│   └── sample_size.md                  power analysis
├── thinkaloud/                      ← in-lab arm
│   ├── protocol.md                     moderator protocol
│   ├── tasks.md                        task scenarios
│   ├── probes.md                       probe library
│   └── coding_book.md                  4-axis × 17-code scheme
├── analysis/                        ← pre-registered analyses
│   ├── preregistration.md              internal pre-reg
│   ├── osf_preregistration.md          OSF Standard Form version
│   ├── hypotheses.md                   verdict logic per hypothesis
│   ├── analysis_plan.md                runnable pipeline spec
│   ├── analysis.py                     end-to-end analysis script
│   └── requirements.txt                pinned dependencies
└── materials/                       ← shared
    ├── app_descriptions.md             pool composition rationale
    ├── recruitment_text.md             Prolific posting + scheduling email
    └── irb_amendment_template.md       letter template for the ethics committee
```

## What's been done for you

- ✅ Interactive prototype, runs end-to-end without any external service.
- ✅ 12-app pool with deterministic stratified sampling.
- ✅ 9-question MCQ bank, one per boundary case.
- ✅ Backend template (Google Apps Script → Sheet).
- ✅ Three deploy guides (GitHub Pages, Netlify, institutional).
- ✅ Full vignette protocol, instrument, consent, randomisation, power.
- ✅ Full think-aloud protocol, tasks, probes, coding book.
- ✅ Pre-registration (internal + OSF Standard form).
- ✅ Hypotheses with explicit *supported / refuted / no decision* rules.
- ✅ Analysis pipeline (Welch t / TOST / Spearman / verdict table).
- ✅ IRB amendment letter template.

## What's still on you

- ⬜ Fill in the bracketed placeholders in
  `materials/irb_amendment_template.md`, `analysis/osf_preregistration.md`,
  `materials/recruitment_text.md`.
- ⬜ Deploy the backend (`backend/deploy_apps_script.md`).
- ⬜ Deploy the prototype (`deploy/README.md`).
- ⬜ Set `BACKEND_URL` in `prototype/study.js`.
- ⬜ Submit the IRB amendment.
- ⬜ Lock the OSF pre-registration before the pilot.
- ⬜ Pilot $N{=}10$ → fix bugs → main collection.

## Smoke test

```bash
cd prototype
node --check study.js && node --check app.js
python3 -c "import json; print(len(json.load(open('apps.json'))), 'apps')"
python3 -c "import json; print(len(json.load(open('mcq_bank.json'))), 'mcq keys')"
```

Expected: every command succeeds; apps = 12; mcq = 10
(9 boundary cases + the metadata key).

## Pre-registration

`analysis/preregistration.md` is the internal version;
`analysis/osf_preregistration.md` is the OSF Standard form ready to
paste into <https://osf.io/registries/> when you lock.

## Pipeline at a glance

```
       ┌─────────────────┐         ┌──────────────────────────┐
       │   Prolific      │ pid ──▶ │   prototype/study.html   │
       │  recruitment    │         │  (your hosted URL)       │
       └─────────────────┘         └────────┬─────────────────┘
                                            │ POST(JSON)
                                            ▼
                                ┌────────────────────────┐
                                │ Google Apps Script     │
                                │   doPost handler       │
                                └────────┬───────────────┘
                                         │ appendRow
                                         ▼
                                ┌────────────────────────┐
                                │  Google Sheet (CSV)    │
                                └────────┬───────────────┘
                                         │ export
                                         ▼
                                ┌────────────────────────┐
                                │  analysis/analysis.py  │
                                └────────┬───────────────┘
                                         │
                                         ▼
                                ┌────────────────────────┐
                                │  results/summary.csv   │
                                │  (verdict per H1..H5)  │
                                └────────────────────────┘
```
