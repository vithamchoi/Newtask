"""Postprocess raw SQLite responses into per-trial CSVs ready for analysis.

Joins trials with stimuli to compute axis-level accuracy vs gold,
NASA-TLX with participant info, etc.

Run after data collection:
    python analysis/postprocess.py \
        --db   data/raw/study.db \
        --out  data/processed/
"""
from __future__ import annotations
import argparse
import json
import sqlite3
from pathlib import Path

import pandas as pd

AXES = ("share_corr","share_comp","coll_corr","coll_comp")

# Gold-state -> categorical-verdict mapping
def verdict_for_axis(axis: str, gold: str) -> str | None:
    if not gold: return None
    if axis.endswith("corr"):
        if gold == "Supported":     return "Correct"
        if gold == "Contradicted":  return "Incorrect"
        if gold == "Insufficient":  return "Ambig"
        if gold == "Omitted":       return "Incorrect"   # treat omission as correctness fail
    else:  # completeness
        if gold == "Supported":     return "Complete"
        if gold == "Omitted":       return "Incomplete"
        if gold == "Contradicted":  return "Incomplete"
        if gold == "Insufficient":  return "Ambig"
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db",  required=True)
    ap.add_argument("--out", default="data/processed/")
    args = ap.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)

    con = sqlite3.connect(args.db)
    trials = pd.read_sql("SELECT * FROM trials", con)
    stim   = pd.read_sql("SELECT app_id, g_share_corr, g_share_comp, g_coll_corr, g_coll_comp FROM stimuli", con)
    parts  = pd.read_sql("SELECT * FROM participants", con)
    tlx    = pd.read_sql("SELECT * FROM tlx", con)
    trust  = pd.read_sql("SELECT * FROM trust", con)
    con.close()

    df = trials.merge(stim, how="left", on="app_id")
    for ax in AXES:
        df[f"acc_{ax}"] = df.apply(
            lambda r: 1 if r.get(f"j_{ax}") and r.get(f"j_{ax}") == verdict_for_axis(ax, r.get(f"g_{ax}"))
                       else (0 if r.get(f"j_{ax}") and r.get(f"g_{ax}") else None),
            axis=1
        )

    # Exclusions per PREREGISTRATION
    bad_pids = parts[(parts.tutorial_pass == 0) |
                     (parts.session_status == "withdrawn")].pid.tolist()
    df = df[~df.pid.isin(bad_pids)]
    # Median trial time < 8s -> exclude session
    med = df.groupby("pid").rt_ms.median()
    short = med[med < 8000].index.tolist()
    df = df[~df.pid.isin(short)]

    df.to_csv(out / "trials.csv", index=False)
    tlx[~tlx.pid.isin(bad_pids + short)].to_csv(out / "tlx.csv", index=False)
    trust[~trust.pid.isin(bad_pids + short)].to_csv(out / "trust.csv", index=False)
    parts.to_csv(out / "participants.csv", index=False)
    print(f"[postprocess] wrote {len(df)} included trials to {out / 'trials.csv'}")


if __name__ == "__main__":
    main()
