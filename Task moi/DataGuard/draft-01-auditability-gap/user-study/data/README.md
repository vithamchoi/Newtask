# `data/` — collected responses

## Layout

- `raw/study.db` — SQLite file holding all live responses (gitignored).
- `processed/` — cleaned per-trial / per-block CSVs produced by
  `analysis/postprocess.py`. The CSV schema is documented in
  `../CODEBOOK.md`.

## Releasing data

After the manuscript is accepted:

1. Run `python analysis/postprocess.py --db raw/study.db --out processed/`.
2. Manually inspect free-text fields in `trials.csv` (`rationale`,
   `evidence_paste`) for accidental identifiers and redact.
3. Hash participant IDs with a one-way function to break any link to
   server logs.
4. Bundle `processed/*.csv`, the gold standard, the codebook, and the
   analysis scripts.
5. Deposit on OSF or Zenodo with the parent-paper DOI.

## Provenance

Every release should include `processed/PROVENANCE.md` recording: the
git commit hash of the user-study repo, the SQLite file SHA-256, and the
date of the postprocessing run.
