# Draft 1 — Beyond Notice: The Necessity Gap in Google Play Data Safety Disclosures

## Target venue
International Journal of Human-Computer Studies (Elsevier).

## Story (one paragraph)
App-store privacy labels assume that *visibility = decidability*: once a category and a purpose are listed, the user can decide. Our linked survey + task data (N=87, 310 social apps) show this assumption fails. Users *do* form a clear hierarchy of "personalness" for the 14 Data Safety categories, but that hierarchy barely predicts whether they think a *specific* app practice is *necessary*. The same person who calls Location "personal" rates Location collection by a navigation app as necessary; the same person who calls App-activity "not personal" still objects to its collection by a social game. We call this disconnect the **Necessity Gap** and argue it is the central HCI bottleneck in app-store transparency, more fundamental than label accuracy or salience.

## Novelty (three contributions IJHCS reviewers will recognise)
1. **First participant-linked evidence** that within the *same individual*, category-level personalness ratings do not transfer to app-level necessity judgments (rating-level n=2,323; participant-category n=1,080; cluster bootstrap CIs include zero in both directions).
2. **The Necessity Gap construct**, formally connecting Nissenbaum's *contextual integrity*, Solove's *consent dilemma*, and the GDPR's *proportionality* principle to a measurable HCI phenomenon — and operationalised as a tier-mismatch between (a) category recognition, (b) boundary comprehension, and (c) contextual necessity.
3. **Five empirically grounded design requirements** for the next generation of app-store labels — feature-level "why", processing-boundary "where", recipient "who", control "how", and an ambiguous-category flag — derived from where the gap is largest.

## Files
- `main.tex`            — IJHCS Elsevier-style manuscript (complete).
- `figures.tex`         — Colourful TikZ/pgfplots figures (used via `\input`).
- `references.bib`      — Verified bibliography.
- `compile.sh`          — pdflatex + bibtex build script.
