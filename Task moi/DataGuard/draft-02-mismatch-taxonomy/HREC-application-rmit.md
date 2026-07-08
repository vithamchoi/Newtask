# RMIT University Human Research Ethics Committee (HREC) — Application

**Project title.** PRISM: A code-aware audit workbench for Android privacy disclosures — user evaluation.
**Risk classification.** Low risk.
**Application type.** Standard online research with human participants; remote and/or supervised laboratory settings.
**Estimated submission date.** [CONFIRM WITH SUPERVISOR]
**Estimated decision turnaround.** 4–6 weeks for low-risk research (RMIT HREC service standard).

---

## 1. Project summary (≈300 words)

This study evaluates the usability and cognitive-load impact of PRISM, a research prototype workbench for auditing Android privacy disclosures. Android applications on Google Play publish two privacy artefacts — a structured Data Safety section and a free-text privacy policy — which auditors (researchers, regulators, journalists, security analysts) must reconcile by hand. PRISM is a research workbench, derived from an earlier corpus study, that surfaces a seven-code taxonomy of label–policy mismatches (M1–M7) and eight code-conditional interface affordances (D1–D8) to support that reconciliation. The present study compares PRISM against a legacy binary-verdict workbench in a within-subjects experiment ($n=24$ trained reviewers, Arm A) and tests a single affordance, the D8 ambiguity badge, in a between-subjects experiment ($n=30$ data-protection practitioners, Arm B).

Primary measures are NASA-TLX cognitive load (Hart 2006), task-completion time, inter-rater agreement against a gold codebook, and rationale-quality scores. No physiological, medical, biometric, or identifying personal data is collected. All participants are adults working in privacy / privacy-adjacent roles and engage with the workbench on a stratified sample of forty publicly available Android apps.

The result will inform the user-evaluation section of a manuscript planned for submission to the International Journal of Human-Computer Studies (IJHCS), addressing the current gap between privacy-disclosure measurement work and human-centred audit-tool design.

## 2. Aims

A1. Compare PRISM vs Legacy on three primary measures: NASA-TLX, task-completion time, and inter-rater κ against a gold set.
A2. Test the specific contribution of the D8 ambiguity badge to over-flagging behaviour in a practitioner cohort.
A3. Capture qualitative feedback on each of the eight code-conditional affordances (D1–D8) via a structured exit interview.

## 3. Design

Mixed-methods, pre-registered (OSF — see `PRE-REGISTRATION-osf.md`).
- **Arm A.** Within-subjects, two conditions (Legacy / PRISM), counterbalanced via Latin square, 20 apps per condition, ≈90-minute session.
- **Arm B.** Between-subjects, two conditions (PRISM-without-D8 / PRISM-with-D8), random assignment 15:15, ≈60-minute remote-async session.

Total participants: $n=54$ (24 Arm A + 30 Arm B). Pilot: $n=4$ in Week 2.

## 4. Participant recruitment

- **Arm A.** Recruited from the RMIT University privacy-research panel (existing institutional list), CS/SE PhD cohorts, and graduate-student listservs. Recruitment email reviewed in advance with the RMIT Researcher Recruitment Office.
- **Arm B.** Recruited from privacy-professional networks: IAPP membership listserv, AANIM Vietnam DPA professional list, OAIC privacy-professional list. All practitioners are working professionals.

No recruitment incentives offered before consent. Compensation (Section 11) is provided upon completion regardless of accuracy.

## 5. Inclusion and exclusion criteria

**Inclusion (Arm A — Trained reviewers).**
- 18 years or older.
- ≥2 years coursework or research experience in privacy, security, HCI, or related.
- OR ≥1 first-author or co-authored peer-reviewed privacy publication.
- Reading fluency in English (study language).

**Inclusion (Arm B — Practitioners).**
- 18 years or older.
- ≥2 years professional experience in privacy compliance, DPO function, or privacy auditing.
- Reading fluency in English.

**Exclusion (both arms).**
- Conflict of interest (e.g., current employee of Google Play platform team).
- Inability to complete a 60–90 minute audit task without accommodation.

## 6. Consent process

- Plain-language statement (PLS) provided 24 hours before the session.
- Consent form (English and Vietnamese versions in `user-study/consent_form_EN.md` / `consent_form_VI.md`) signed at session start; participant retains a digital copy.
- Verbal confirmation of voluntary participation at session start.
- Participant may withdraw at any point during the session without penalty; data collected before withdrawal is destroyed at participant's request.

## 7. Data collection procedures

1. Initial screening questionnaire (3 demographic items: role, years experience, prior privacy training; no identifying fields).
2. Consent.
3. Tutorial walkthrough (≈10 min).
4. Block 1: 20 apps audited in assigned condition.
5. NASA-TLX block 1.
6. Block 2: 20 apps audited in opposite condition (Arm A only).
7. NASA-TLX block 2 (Arm A only).
8. Exit interview (5 open-text questions).
9. Compensation processed.

Server-side logging captures: pseudonymous `participant_id` (UUID), assigned build, app id audited, four-radio verdict, rationale text, time-on-app (milliseconds), NASA-TLX subscale scores, exit-interview answers, and click events on D-affordances. No name, email, IP, or user-agent is recorded.

Screen recordings (Arm A only, with explicit consent) are captured locally and uploaded to RMIT secure storage at session end; they are reviewed only for exit-interview annotation and deleted after rationale-quality scoring is complete.

## 8. Data management plan

- **Storage.** Workbench server logs stored on RMIT secure storage (RMIT Cloud / R-Drive equivalent) with TLS in transit and encryption at rest.
- **Retention.** 7 years per RMIT HREC policy, then permanently destroyed.
- **Access.** Restricted to listed researchers via RMIT SSO; access log retained.
- **Pseudonymisation.** `participant_id` is a server-assigned UUID. The mapping from `participant_id` to the participant's email (used only for compensation processing) is held in a separate access-restricted spreadsheet and destroyed at study close.
- **Publication.** Aggregated results published; the per-participant data is released under CC-BY-4.0 after manual scrubbing of any inadvertent identifying spans in free-text rationales.
- **Pre-registration.** OSF deposit at `https://osf.io/[PROJECT-ID]/` linked from the paper.

## 9. Privacy and confidentiality

No identifying personal data is collected through the workbench. Recruitment emails and consent forms collect name + email; these fields are stored in a separate access-restricted spreadsheet linked to `participant_id` for compensation only. The link is destroyed within 30 days of study close. The published data release contains no identifying fields.

## 10. Risk assessment

Risk classification: **Low.** No physical, psychological, social, legal, or financial risk beyond ordinary daily life.

Risks identified and mitigated:

| Risk | Likelihood | Severity | Mitigation |
|---|---|---|---|
| Mild boredom / fatigue during 90-min Arm-A session | Moderate | Low | Mandatory short break between blocks; participant may pause/withdraw at any time |
| Anxiety from being measured against gold-set | Low | Low | Tutorial explicitly states verdict is not evaluated; compensation independent of accuracy |
| Identifiable rationale text (rare) | Low | Low | Manual scrub by lead researcher before publication; CC-BY-4.0 release post-scrub |
| Cyber risk if workbench server compromised | Low | Low | Workbench logs no identifying fields; pseudonym only; TLS in transit; RMIT IT-managed encryption at rest |

No risk to vulnerable groups; participants are working adults exclusively.

## 11. Compensation

- Arm A: AUD$90 per 90-min session (≈AUD$60/hr, above local minimum wage). Paid by RMIT-managed gift card or direct deposit at session end.
- Arm B: AUD$150 per 60-min session.
- Compensation is paid in full regardless of completion accuracy; partial completion is paid pro-rata.
- Compensation total: ($24 × 90$) + ($30 × 150$) = AUD$2{,}160 + 4{,}500 = AUD$6{,}660$. [CONFIRM BUDGET HOLDER]

## 12. Withdrawal procedures

Participants may withdraw at any time during the session by closing the browser tab. Data collected up to that point is anonymised and may be retained for partial analysis unless the participant explicitly requests destruction. A withdrawal mailbox (`[CONTACT EMAIL]`) is available post-session for delayed withdrawal requests; data is destroyed within 14 days of such a request.

## 13. Researcher qualifications

[CONFIRM WITH SUPERVISOR — list each researcher's role and qualifications]
- Principal Investigator: [NAME], [TITLE], RMIT School of Computing Technologies.
- Co-investigators: [LIST].
- All researchers hold current Working with Children Checks and Police Checks as required by RMIT policy.

## 14. Drop-in: Plain-language statement (PLS)

> Reuse `user-study/consent_form_EN.md` as the PLS body; add a one-paragraph header that states (i) the purpose of the study, (ii) why the participant has been invited, (iii) what participation involves, (iv) compensation, and (v) the participant's right to withdraw.

## 15. Drop-in: Consent form

> Reuse `user-study/consent_form_EN.md` and `consent_form_VI.md` verbatim. Add a separate checkbox for screen-recording consent (Arm A only, optional).

---

**Items still requiring confirmation before submission**

- [ ] Principal Investigator and co-investigator names + RMIT IDs
- [ ] Budget holder for AUD$6,660 compensation
- [ ] RMIT secure-storage path (R-Drive folder ID)
- [ ] OSF project ID once registered
- [ ] Privacy impact assessment if RMIT IT requires one for hosted workbench
- [ ] Approval to recruit via the IAPP listserv (third-party data subjects)
