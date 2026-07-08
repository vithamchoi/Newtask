# Quick start

Everything you need to launch the BLE evaluation, in one page.

## 0. What's in this folder

```
UserStudy/
├── README.md, QUICKSTART.md     ← you are here
├── prototype/                   ← interactive study (HTML/CSS/JS)
│   ├── study.html                  ← the single-page-app participants run
│   ├── index.html                  ← landing for moderators
│   ├── current.html, ble.html      ← condition-only previews for think-aloud
│   ├── style.css, study.js, app.js
│   └── apps.json, mcq_bank.json
├── backend/                     ← Google Apps Script + setup guide
├── deploy/                      ← GitHub Pages / Netlify / institutional guides
├── analysis/                    ← pre-registration, hypotheses, analysis.py
├── vignette/                    ← protocol, instrument, consent, randomisation
├── thinkaloud/                  ← protocol, tasks, probes, coding book
├── materials/                   ← app descriptions, recruitment, IRB letter
```

## 1. End-to-end timeline (you can hand this to your supervisor)

| Stage | Owner | Days |
|---|---|---|
| 1. Read `vignette/protocol.md` end-to-end | You | 0.5 |
| 2. Open `prototype/study.html` locally and run through `?pid=PILOT-001` | You | 0.5 |
| 3. Stand up backend (`backend/deploy_apps_script.md`) | You | 0.5 |
| 4. Deploy prototype (`deploy/github_pages.md` or `deploy/netlify.md`) | You | 0.5 |
| 5. File IRB amendment (`materials/irb_amendment_template.md`) | You + ethics office | 14–28 |
| 6. Lock OSF pre-registration (`analysis/osf_preregistration.md`) | You | 1 |
| 7. Pilot $N{=}10$ | You + Prolific | 3–5 |
| 8. Fix any pilot bugs | You | 1–2 |
| 9. Vignette main collection ($N{=}200$) | You + Prolific | 5–10 |
| 10. Think-aloud sessions (12–15) | You + Zoom | 5–8 |
| 11. Analysis (`analysis/analysis.py`) | You | 3 |
| 12. Write Section 7 of the manuscript | You | 5 |

Total: about 6–9 weeks once IRB is approved. The IRB wait is the
critical-path blocker; everything else can run in parallel.

## 2. Run the prototype locally right now

```bash
cd Draft2_BoundaryMismatch/UserStudy/prototype
python3 -m http.server 8080
# Open http://localhost:8080/study.html?pid=PILOT-001 in a browser.
```

You should advance through:
landing → consent → pre-task → 4 apps with MCQ+Likerts → attention
check → post-task → debrief with a downloadable JSON.

## 3. The four files you need to edit before launch

1. `prototype/study.js` — set `BACKEND_URL` to the Apps Script URL
   you deploy in step 3.
2. `analysis/osf_preregistration.md` — fill in author names,
   submission date, OSF link, lock hash.
3. `materials/irb_amendment_template.md` — fill in PI name, HREC
   number, dates, contact email.
4. `materials/recruitment_text.md` — fill in Prolific posting
   times, contact email for think-aloud scheduling.

## 4. The three URLs you'll need

After deploys:

| Purpose | Where |
|---|---|
| Participant study link | `https://YOUR-DOMAIN/study.html?pid={{PROLIFIC_PID}}` |
| Backend POST endpoint  | `https://script.google.com/macros/s/AKfycb…/exec` |
| OSF pre-registration   | `https://osf.io/…` (filled in after lock) |

Add the participant link to the Prolific posting; Prolific
automatically substitutes `{{PROLIFIC_PID}}` per participant.

## 5. Validation checklist before opening recruitment

- [ ] IRB amendment approved.
- [ ] OSF pre-registration locked and the hash recorded.
- [ ] Backend URL set in `study.js` and committed.
- [ ] At least one full pilot run completed end-to-end.
- [ ] Backend Sheet shows the pilot row with all expected columns.
- [ ] Attention check passes on the pilot run.
- [ ] BLE condition reaches the debrief with at least one drawer
       opened (otherwise revise the affordance per
       `vignette/sample_size.md` §Pilot).
- [ ] All 12 apps appear at least once across 12 simulated pids
       (the smoke test in section 6 of QUICKSTART confirms this).

## 6. Smoke-test the SPA without a browser

```bash
cd Draft2_BoundaryMismatch/UserStudy/prototype
node --check study.js  # syntax-only
node --check app.js
python3 -c "import json; print('apps:', len(json.load(open('apps.json'))))"
python3 -c "import json; print('mcq:',  len(json.load(open('mcq_bank.json'))))"
```

Expected output: every line passes; apps = 12; mcq = 10
(9 boundary cases + the metadata key).

## 7. After data lands

- Export the Google Sheet to CSV.
- Run `python analysis/analysis.py --vignette raw.csv --proto
  proto.csv --out results/`.
- Inspect `results/summary_table.csv` — one row per hypothesis with
  the pre-registered verdict.

## 8. If something blocks you

- **Backend POST fails** — `backend/deploy_apps_script.md`
  §Troubleshooting.
- **GitHub Pages 404** — `deploy/github_pages.md` §Troubleshooting.
- **Drawer not discovered in pilot** — revise the affordance per
  `vignette/sample_size.md` §Pilot.
- **IRB pushes back** — see `materials/irb_amendment_template.md`
  §4 risk mitigations; most common pushback is data-residency,
  resolvable by relocating the backend.

That's the whole pipeline. You can hand this file to a collaborator
and they can pick it up cold.
