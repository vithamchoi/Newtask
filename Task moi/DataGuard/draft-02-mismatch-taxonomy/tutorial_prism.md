# Tutorial script — PRISM build
*Estimated time: 10–12 minutes. Read verbatim. Italics = experimenter action.*

---

## Opening (≈1 min)

> "Thank you for joining today. You'll see two versions of an audit workbench, presented in a counterbalanced order. The current version is *PRISM* — it adds eight code-conditional interface affordances on top of the baseline audit task. The next 10 minutes will walk you through what each affordance does. After the walkthrough you'll start Block 1: 20 apps. There'll be a short break and a questionnaire, then Block 2 with the other version. OK?"

*Wait for verbal acknowledgement.*

---

## Same baseline task as Legacy (≈1.5 min)

> "Just like the baseline, your task is to compare the Data Safety section on the left against the privacy-policy excerpt on the right, and give four binary verdicts: sharing correctness, sharing completeness, collection correctness, collection completeness. Then a one- or two-sentence rationale. Compensation does not depend on accuracy."

*If participant already saw the Legacy tutorial, skip the baseline-task section and say "you remember the four verdicts from before, right?".*

---

## The eight PRISM affordances (≈5 min)

Walk through each affordance once with the first tutorial app on screen. Use the script below; pause for questions after each.

### D1 — Third-party recipient panel (≈45 s)
> "Below the Data Safety table on the left, you see a panel labelled *D1 — Third-party recipients*. It lists every named recipient the workbench extracted from the policy and flags whether the corresponding row in the Data Safety table mentions it. *Unlinked* means the policy names a recipient that the label does not declare a sharing row for."

`[SCREENSHOT-PRISM-D1]`

### D2 — Identifier-to-category map (≈30 s)
> "If the Data Safety table includes the row *Device or other IDs*, hover over it. A tooltip lists which specific identifiers the policy mentions — advertising ID, IP, Android ID, cookies — and marks each as covered or uncovered by the label."

`[SCREENSHOT-PRISM-D2]`

### D3 — Hedge highlighter (≈30 s)
> "On the right side, the policy text is rendered with hedging language highlighted in amber. Phrases like 'may collect', 'such as', 'including but not limited to' all light up. The intent is to draw your eye to spans where the policy is hedging rather than committing to a specific practice."

`[SCREENSHOT-PRISM-D3]`

### D4 — No-data audit prompt (≈30 s)
> "When the Data Safety table says 'no data shared' and the policy mentions third-party recipients or persistent identifiers, you'll see a red banner at the top of the left pane. The banner does not tell you the verdict — it just flags that the configuration is worth examining."

`[SCREENSHOT-PRISM-D4]`

### D5 — Location-grain overlay (≈30 s)
> "If the policy describes location collection, you'll see a small green chip next to the Data Safety location row indicating the grain: *approximate*, *precise*, or *IP-derived*. The Data Safety taxonomy only has two grains, so an 'IP-derived' chip means the policy describes something the label cannot express directly."

`[SCREENSHOT-PRISM-D5]`

### D6 — Security / data tab (≈30 s)
> "Security practices are visually grouped in their own dashed-border box under the Data Safety table. The intent is to keep security claims like 'encrypted in transit' visually separate from data-type claims like 'Device IDs collected', because the two are sometimes confused."

`[SCREENSHOT-PRISM-D6]`

### D7 — Responsibility-scope chip (≈30 s)
> "If the policy contains a clause like 'we are not responsible for the practices of linked sites', you'll see a gold chip near the Data Safety block flagging it. The label does not have a scope qualifier, so this chip marks where the policy explicitly narrows the responsibility boundary."

`[SCREENSHOT-PRISM-D7]`

### D8 — Ambiguity badge bar (≈45 s)
> "At the very bottom of the screen there is a badge bar. The badges show the percentage of past doubly-annotated pairs where two trained reviewers disagreed about the verdict when that code was present. For example, M6 shows 84.6%. The intent is to tell you, *while* you are deciding, which codes have historically been hard to agree on. It does not change your verdict; it just asks you to record your reasoning more carefully. Codes shown as 'not observed' means we did not have enough doubly-annotated pairs in the original corpus to estimate the ambiguity."

`[SCREENSHOT-PRISM-D8]`

---

## Same data-collection contract (≈0.5 min)

> "Just like the Legacy version, the first five apps are tutorial — the verdict radios are disabled. From the sixth app onward, your verdicts and rationales are recorded. Take as much time as you want; no time pressure. Compensation is independent of accuracy."

---

## Comprehension check (≈0.5 min)

After the first tutorial app loads:

> "Quick check: which one of the eight affordances draws your attention to potentially over-claimed 'no-data' labels?"

Expected answer: D4 (the red banner).

If the answer is wrong or hesitant, walk through D4 again. Mark the comprehension check `PASSED` or `FAILED` on the experimenter form.

---

## Block flow (≈0.5 min)

> "After 20 apps you'll be redirected to a NASA-TLX questionnaire. Six sliders, no right answers. Then a short break. Then the second version and another 20 apps and another NASA-TLX. Then a 5-question exit interview. Done. Any questions?"

*Wait for any questions. Resolve. Hand the participant the laptop and step away.*

`[SCREENSHOT-PRISM-FULL]` — the full PRISM workbench in audit mode.
`[SCREENSHOT-EXIT]` — the exit-interview form.
