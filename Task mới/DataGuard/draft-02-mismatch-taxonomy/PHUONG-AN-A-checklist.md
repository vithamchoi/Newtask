# Phương án A — daily kanban

Open this every morning. Move items left → right as they complete.

---

## NOT STARTED

### Week 1 — MVP + ethics submission
- [ ] Hire / assign senior frontend dev for MVP polish (1 week × 1 FTE)
- [ ] RMIT HREC submission package final review (PI sign-off)
- [ ] Submit HREC application — Week 1, Day 1
- [ ] Confirm AUD$6,660 budget holder + project code
- [ ] Reserve RMIT secure-storage folder (R-Drive) for `sessions.db` and screen recordings
- [ ] Set up private GitHub repo for workbench; mirror to OSF as `pre-reg-v1` tag

### Week 2 — gold set + pilot
- [ ] Gold-set: 3 expert coders independently code 40 apps with M1–M7 (≈6 hrs each)
- [ ] Gold-set consensus meeting (≈2 hrs) → final `user-study/gold_40.csv`
- [ ] Inter-expert κ reported as a sanity check
- [ ] Run 4-participant pilot (2 reviewers + 2 practitioners)
- [ ] Submit OSF pre-registration with frozen workbench commit hash

### Week 3 — Arm A recruitment
- [ ] Recruitment email to RMIT privacy-research panel
- [ ] Recruitment email to CS/SE PhD cohorts
- [ ] Screening-questionnaire intake form goes live
- [ ] Confirm 24 booked Arm A participants + 4 standby
- [ ] Send PLS and consent form 24 hours before each session

### Weeks 4–5 — Arm A data collection
- [ ] Run 24 Arm-A sessions (90 min each, 6 per day × 4 days)
- [ ] Daily backup of `sessions.db` to RMIT secure storage
- [ ] After each session, mark comprehension-check pass/fail
- [ ] Compensation processed within 48 hrs

### Week 6 — Arm B
- [ ] Recruitment email to IAPP / AANIM Vietnam DPA listservs
- [ ] Confirm 30 booked Arm B participants + 5 standby
- [ ] Run 30 Arm-B sessions (60 min each, mostly remote async)
- [ ] Rationale-quality scoring kickoff: 2 raters calibrated on 20-rationale set

### Week 7 — analysis
- [ ] Confirmatory tests of H1–H5 per pre-registration
- [ ] Effect-size CIs via bootstrap (10,000 resamples)
- [ ] Per-quadrant exploratory breakdown
- [ ] Per-affordance click-stream log-regression
- [ ] Exit-interview thematic analysis (2 coders, ≈8 hrs each)

### Week 8 — paper finalisation
- [ ] Drop verified numbers into Section 8 placeholder
- [ ] Update abstract, conclusion, headlines with user-study results
- [ ] Re-run full `pdflatex + bibtex + pdflatex × 2` to confirm clean compile
- [ ] Cross-check that no number in the paper is unverified
- [ ] Final author review + IJHCS submission

---

## IN PROGRESS
*(empty — fill as items move from NOT STARTED)*

---

## DONE

### Pre-Week 1 — already shipped
- [x] PRISM workbench MVP code (Flask + vanilla JS) at `prism-workbench/`
- [x] Workbench smoke-tested end-to-end (session → next-app → submit-verdict)
- [x] `build_stimuli.py` runs and produces `data/stimuli.json` with 40 stratified apps
- [x] OSF pre-registration document (`PRE-REGISTRATION-osf.md`)
- [x] RMIT HREC application skeleton (`HREC-application-rmit.md`)
- [x] Tutorial scripts for Legacy and PRISM builds (`tutorial_legacy.md`, `tutorial_prism.md`)
- [x] Rationale-quality coding rubric (`rationale_quality_rubric.md`)
- [x] Master plan (`PHUONG-AN-A-user-study-plan.md`)
- [x] Section 8 placeholder added to `main.tex` (compiles clean)
- [x] Lazar 2017 & Simmons 2021 added to `references.bib`

---

## Blockers / decisions you still own

- **B1.** Budget approval for AUD$6,660. Confirm budget holder.
- **B2.** Decision on whether Arm B is fully remote-async or supervised remote. Affects compensation processing.
- **B3.** Decision on screen-recording for Arm A (opt-in vs default). Affects HREC consent-form wording.
- **B4.** Decision on whether Vietnamese-language session is offered (relevant if recruiting from local cohort).
- **B5.** Confirm three co-authors to serve as expert coders for the gold-set.

---

## Daily standup template (use during Weeks 3–8)

```
Date: YYYY-MM-DD
Yesterday:
  - …
Today:
  - …
Blockers:
  - …
Numbers so far:
  Arm A complete: X / 24
  Arm B complete: Y / 30
  Workbench bugs reported: Z
```
