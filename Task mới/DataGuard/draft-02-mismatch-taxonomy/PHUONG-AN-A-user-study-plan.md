# Phương án A — PRISM workbench user study plan (IJHCS submission)

**Goal.** Add a confirmatory HCI evaluation of the PRISM workbench so that Draft 2 has the user-evaluation contribution that IJHCS reviewers expect. Target a strong accept by closing the *"does the code-aware UI actually help an auditor?"* gap.

**Outcome we want to be able to state in the paper.**
> "In a within-subjects experiment with 24 trained reviewers (Arm A) and a between-subjects experiment with 30 data-protection practitioners (Arm B), the PRISM workbench produced a 15.4% (95% CI 9.1–21.6) reduction in median NASA-TLX cognitive load, a 12.8% reduction in task-completion time, and an inter-reviewer Cohen's κ improvement of 0.18 against the gold codebook, with no false-positive cost on category M4 cases."

(The exact numbers come out of the data; the *shape* of the claim is fixed by the protocol below.)

---

## 1. Timeline — 8 weeks end-to-end

| Week | Phase | Deliverable |
|---|---|---|
| 1 | MVP build, gold-set construction | Workbench MVP frozen; 40-app gold set finalized |
| 2 | Pilot ($n=4$), protocol freeze, ethics submission | OSF pre-registration locked; ethics approval letter |
| 3 | Arm A recruitment, schedule sessions | 24 reviewers booked into 90-min slots |
| 4–5 | Arm A data collection | 24 sessions logged; raw data + screen recordings |
| 6 | Arm B recruitment + data collection | 30 practitioners run async/remote |
| 7 | Analysis + statistical tests | Result tables, plots ready |
| 8 | Write Section 8 + revise Sections 1, 2, 7, 11 | Camera-ready Draft 2 |

---

## 2. What you need to build — the PRISM workbench MVP

The mockup in Figure 8 already specifies the interface; the MVP only needs the affordances *the experiment will actually compare*. Scope is intentionally minimal.

### 2.1 Two builds, share 80% of code
1. **Legacy build** — replicates the original DataGuard workbench from Draft 1: a side-by-side Data Safety + Policy view, four radio buttons (sharing-correct, sharing-complete, collection-correct, collection-complete), and a free-text rationale field. **No code affordances.**
2. **PRISM build** — same skeleton plus:
   - **D1** Third-party recipient panel (extract recipient names from policy via NER → render list with linked/unlinked status)
   - **D2** Identifier-to-category mapping tooltip on `Device or other IDs`
   - **D3** Hedge highlighter (amber underline on M3-lexicon matches)
   - **D4** No-data audit prompt (inline alert when label declares no-data + M1/M2 lexicon fires)
   - **D5** Location-grain overlay (chip showing detected grain: approximate / precise / IP-derived)
   - **D6** Security/Data tab (separate visual section)
   - **D7** Responsibility-scope chip (orange badge when M7-lexicon fires)
   - **D8** Cross-cutting ambiguity badge bar (shows codes ≥70% historical disagreement)

### 2.2 Tech stack (recommended)
- **Frontend**: React + TypeScript (you already have `data-guard-client/` skeleton)
- **Backend**: Flask or FastAPI, serves the 1,213 parseable policy-label pairs; logs every click + time event
- **Logging**: each session = 1 JSON file with `{participant_id, condition, app_id, click_stream[], verdict, rationale, NASA-TLX, completion_time_seconds}`
- **Lexicon engine**: ship the YAML lexicon from Section 3.4 as a server-side service; D1–D7 affordances consume its output

### 2.3 Effort estimate
- 1 senior frontend dev × 1 week = MVP frontend (both builds via feature flag)
- 0.5 senior backend dev × 1 week = logging + lexicon service
- 0.5 designer × 2 days = polishing affordance visual design

---

## 3. Stimuli — what apps participants audit

### 3.1 40-app stratified sample from the 1,213-app corpus
Stratify by *prevalence quadrant* (Figure 6 in paper):
| Quadrant | Description | # apps |
|---|---|---|
| Common & ambiguous | M1-dominant apps | 10 |
| Common & tractable | M3-dominant apps (hedge-heavy, no other codes) | 10 |
| Rare & ambiguous | M6-bearing apps | 10 |
| Rare & tractable | clean controls (no code fires) | 10 |

Use the per-app code matrix CSV (already released as supplementary material) to pick the apps.

### 3.2 Gold-standard codes per app
- Recruit 3 expert auditors (NOT participating in main study; ideally co-authors + 1 external privacy researcher)
- Each expert independently codes all 40 apps with all 7 PRISM codes
- Resolve disagreements via consensus meeting → final gold-set
- Report inter-expert Cohen's κ on the gold-set as a sanity check

### 3.3 Counterbalance design
- 2 conditions × 40 apps = each participant sees 20 apps in each condition
- Latin square across 24 participants (Arm A) so that every app-condition pair is covered
- Order randomized within each block

---

## 4. Participants

### 4.1 Arm A — within-subjects, $n = 24$ trained reviewers
- **Inclusion**: graduate student or junior researcher with ≥2 years of privacy / security coursework OR ≥1 prior privacy publication
- **Source**: institutional privacy-research panel, university SE/CS PhD lists, RMIT cohorts
- **Compensation**: 60 USD per 90-min session (above local minimum wage; clear in consent form)
- **Sample size justification**: per-condition $n=24$ gives ≥0.80 power to detect a NASA-TLX Cohen's $d \geq 0.6$ at $\alpha=0.05$ on a paired-t test

### 4.2 Arm B — between-subjects, $n = 30$ data-protection practitioners
- **Inclusion**: ≥2 years working in privacy compliance, DPO function, or privacy auditing
- **Source**: IAPP membership listserv, regulator-facing professional mailing list (CNIL ECCP listserv, OAIC privacy-professional list, AANIM Vietnam DPA list)
- **Compensation**: 100 USD per 60-min remote async session
- **Sample size justification**: 15+15 between-subjects gives ≥0.80 power for the badge-effect ($d \geq 0.8$) on triage false-positive rate

### 4.3 Ethics (RMIT HREC submission)
You'll need:
- Plain-language statement (PLS)
- Consent form (English + Vietnamese versions in `user-study/`)
- Data-management plan (anonymized, on RMIT secure storage, 7-year retention)
- Risk assessment (low risk — no identifiable data, no payment-for-positive-results)
- Recruitment script + screening questionnaire
- Submit via RMIT HREC online portal; typical turnaround 4–6 weeks for low-risk

---

## 5. Measures — what to record per participant

### 5.1 Primary measures (the ones the paper will headline)
| Measure | Per app | Per session | Captured by |
|---|---|---|---|
| Task-completion time (sec) | ✓ | ✓ | Server logs (timestamp-on-app-open → submit-verdict) |
| NASA-TLX (0–100 weighted) | | ✓ × 6 subscales | Post-session form |
| Verdict agreement κ vs gold | ✓ | aggregated | Computed from server logs + gold-set |
| Per-code reasoning quality (0–3) | ✓ | aggregated | Blind expert raters score rationales |

### 5.2 Secondary measures (used for robustness checks)
- Confidence per verdict (7-point Likert)
- Self-reported per-affordance helpfulness (D1–D8, 7-point Likert)
- Click-stream features (which UI panel time spent on)
- Free-text post-session questions: (i) describe one app that was hard, (ii) what would you change about the interface, (iii) would you use this tool again

### 5.3 What you need to set up NOW (week 0)
- [ ] NASA-TLX paper or digital form (Hart & Staveland 1988 free-use)
- [ ] Screen-recording with audio for verbal-protocol analysis (Lookback.io or open-source `obs-studio`)
- [ ] Server-side logging schema; sample JSON in Appendix B
- [ ] Rationale-scoring rubric with examples (define what 0/1/2/3 looks like per code)
- [ ] Two independent raters trained on the rubric; report inter-rater κ on a pilot subset

---

## 6. Procedure — what a Arm-A session looks like

(Adjust slightly for remote Arm B; details below.)

### 6.1 90-min protocol
1. **0–10 min**: consent, demographics, screening, NASA-TLX familiarisation
2. **10–20 min**: standardised tutorial on whichever workbench they get first (counterbalanced)
3. **20–55 min**: Block 1 — 20 apps in Condition X (Legacy or PRISM)
4. **55–60 min**: short break, NASA-TLX for block 1
5. **60–80 min**: Block 2 — 20 apps in Condition Y (the other)
6. **80–85 min**: NASA-TLX for block 2
7. **85–90 min**: exit interview (5 questions) + payment

### 6.2 Things to script verbatim
- Tutorial wording (must be identical across conditions except for the affordance-specific parts)
- Disagreement-handling instructions: tell participants the gold-set exists but is hidden, that there is no "correct" verdict the researchers are looking for
- Compensation messaging: paid regardless of accuracy

### 6.3 Pilot ($n=4$, Week 2) checklist
- 2 reviewers + 2 practitioners
- Run full protocol end-to-end
- Look for: (i) tutorial confusion, (ii) workbench bugs, (iii) average session length within ±10% of plan, (iv) NASA-TLX feasibility, (v) any stimulus that yielded 100% same-verdict across pilot (drop / replace)

---

## 7. Pre-registration template (OSF)

Submit on OSF Registry **before** Week 3 recruitment begins. Use the AsPredicted format.

**Hypotheses:**
- **H1** (primary): median per-app NASA-TLX is ≥15% lower in PRISM vs Legacy ($\alpha=0.05$, one-sided Wilcoxon signed-rank).
- **H2** (primary): inter-reviewer κ-vs-gold ≥0.10 higher in PRISM vs Legacy ($\alpha=0.05$, paired).
- **H3** (primary): completion time is non-inferior in PRISM vs Legacy (margin $\delta=10\%$).
- **H4** (secondary): D8 ambiguity badge reduces over-flagging of M1/M3 cases by ≥30% (between-subjects in Arm B).
- **H5** (secondary): per-code reasoning quality scores increase by ≥0.5 scale points on M1/M2/M6 in PRISM.

**Stopping rule:** fixed $n$ — no early stopping.

**Exclusion criteria:** participants who complete <80% of stimuli, who fail the comprehension-check item, or who submit a verdict in <5 seconds for >25% of stimuli (likely click-through).

**Analysis plan:** Wilcoxon signed-rank for paired comparisons (Arm A), Mann-Whitney U for between-subjects (Arm B), Bonferroni correction across H1–H3.

---

## 8. Analysis plan — concrete tables/plots to produce

### 8.1 New Section 8 tables (will replace current §7.5)
| Table | Content |
|---|---|
| Table 8.1 — Participants | Demographics: age, role, years experience, prior privacy training |
| Table 8.2 — Primary outcomes | NASA-TLX, completion time, κ-vs-gold per condition with 95% CI |
| Table 8.3 — Per-code reasoning quality | M1–M7 reasoning-quality scores per condition |
| Table 8.4 — D8 badge effect | False-positive rate of M1/M3 over-flagging with/without badge |

### 8.2 New Section 8 figures (TikZ-friendly)
- F8.1 — TLX subscale radar (Mental / Physical / Temporal / Performance / Effort / Frustration) per condition
- F8.2 — Per-app completion-time box-plot per condition (40 apps × 2 conditions)
- F8.3 — Rationale-quality histogram per code per condition

### 8.3 Reporting style
- Effect sizes with 95% bootstrap CIs (10,000 resamples)
- Pre-registered hypotheses tested first; exploratory analyses clearly labeled
- Negative results reported in same depth as positive

---

## 9. What additional information / data you must collect from now

The HCI evaluation does not need new audit data — you already have the corpus. What you DO need to gather is the user-study data and surrounding documentation:

### 9.1 Already in repo (re-use)
- ✓ `data-labels.xlsx` — corpus for stimuli
- ✓ Per-app code matrix — for stratification
- ✓ Lexicon YAML — for D1–D7 server-side service
- ✓ `user-study/consent_form_EN.md`, `consent_form_VI.md` — re-use & update

### 9.2 NEW data you must collect, in order
1. **Stimuli gold-set** (40 apps × 7 codes × 3 expert coders + consensus) → `user-study/gold_40.csv`
2. **Participant screening responses** (Arm A: 24 + standby; Arm B: 30 + standby) → `user-study/screening_responses.csv`
3. **Per-session log files** (one JSON per participant) → `user-study/responses/A_<pid>.json` and `B_<pid>.json`
4. **NASA-TLX score sheets** (one per block per participant) → `user-study/tlx/A_<pid>_<block>.json`
5. **Rationale-quality scores** (two raters × all rationales) → `user-study/rationale_scores.csv`
6. **Exit-interview transcripts** (audio + transcribed) → `user-study/exit/A_<pid>.txt`
7. **Screen recordings** (one per Arm-A session) → encrypted RMIT secure storage; not in repo

### 9.3 NEW documents to produce
- Pre-registration on OSF (template in §7 above)
- RMIT HREC application (estimate 20 hours to prepare)
- Tutorial scripts (Legacy + PRISM versions, ~3 pages each, verbatim)
- Rationale-quality coding rubric with calibration examples (~5 pages)
- Statistical-analysis pre-registered script (Python notebook, version controlled)

### 9.4 NEW infrastructure
- Workbench MVP deployed at private URL (RMIT IT can host)
- Logging server with TLS + Postgres backend
- Backup snapshots after each session
- Pseudonymised participant IDs (no name, no email; only role-tag + sequential ID)

---

## 10. Risks and mitigations

| Risk | Probability | Mitigation |
|---|---|---|
| Ethics approval delayed | High | Submit Week 1 in parallel with MVP build |
| Recruitment shortfall (Arm B practitioners) | Medium | Have 5+ standby names lined up; consider remote-only and global timezone slots |
| Workbench bugs at scale | Medium | Mandatory load-test before Week 3; fall-back: paper-based audit for unrecoverable bugs |
| Effect sizes smaller than planned | Medium | Pre-register non-inferiority margin so the paper is publishable even if H1 is borderline |
| Gold-set disagreement | Medium | Consensus meeting + report expert κ; drop apps with ≤2/3 agreement |

---

## 11. What I need from you to start

Please confirm or clarify:

1. **Budget envelope** — can you secure approx. $24×60 + 30×100 = 1{,}440 + 3{,}000 = $$4{,}440$ in participant compensation, plus dev-time for the MVP build?
2. **Engineering capacity** — do you have access to a senior frontend dev (or do we need to recruit / hire one)?
3. **Ethics turnaround** — does RMIT HREC typically take 4–6 weeks for low-risk studies, or longer? This is the critical-path constraint.
4. **Recruitment access** — do you have institutional contacts to recruit 30 data-protection practitioners (Arm B)? If not, we need a fallback (e.g., practitioner-Twitter ads, Prolific filter).
5. **Co-author availability** — for the expert gold-set (Section 3.2), can you and 1–2 co-authors commit ~6 hours each to code 40 apps with the 7 codes?

Once you confirm these I can:
- Draft the OSF pre-registration document (~3 pages)
- Draft the RMIT HREC application (~10 pages incl. PLS, consent, data-management plan)
- Draft the tutorial scripts (~6 pages, both conditions)
- Write the placeholder Section 8 in `main.tex` so the paper will compile end-to-end and you can drop in results during Weeks 7–8

---

## 12. After Phương án A finishes — what the IJHCS submission looks like

Updated Draft 2 will gain a full **Section 8: User evaluation** (~6 pages):
- §8.1 Method (participants, stimuli, procedure)
- §8.2 Results (4 tables, 3 figures, all pre-registered hypotheses tested)
- §8.3 Qualitative analysis (exit-interview themes, post-session quotes)
- §8.4 Discussion of effect-size patterns
- §8.5 Threats to validity

Total length will be ~40 pages, well within IJHCS's typical range (35–45 pages for research articles). Bibliography grows from 52 to ~58 with HCI-evaluation references (Lazar's *Research Methods in HCI*, NASA-TLX original, Wickens for cognitive-load theory).

With Section 8 in place, the paper will hit **all** standard IJHCS contribution criteria: corpus, taxonomy, statistical model, designed interactive system, AND measured user-evaluation effects.
