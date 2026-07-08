"""Effect sizes: bootstrap CI for between-condition deltas on accuracy,
workload, and time. Cohen's d for the within-subject contrasts.

Run after data collection:
    python analysis/effect_sizes.py \
        --trials data/processed/trials.csv \
        --tlx    data/processed/tlx.csv \
        --out    analysis/results/effect_sizes.json
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

AXES = ["acc_share_corr","acc_share_comp","acc_coll_corr","acc_coll_comp"]


def cohens_d_paired(x: np.ndarray, y: np.ndarray) -> float:
    diff = x - y
    return float(diff.mean() / diff.std(ddof=1)) if len(diff) > 1 else float("nan")


def bootstrap_paired(x: np.ndarray, y: np.ndarray, n_iter=2000, seed=20260615):
    rng = np.random.default_rng(seed)
    diff = x - y
    boots = np.array([rng.choice(diff, size=len(diff), replace=True).mean()
                      for _ in range(n_iter)])
    return float(boots.mean()), float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", required=True)
    ap.add_argument("--tlx",    required=True)
    ap.add_argument("--out",    default="analysis/results/effect_sizes.json")
    args = ap.parse_args()

    out_path = Path(args.out); out_path.parent.mkdir(parents=True, exist_ok=True)
    trials = pd.read_csv(args.trials)
    tlx = pd.read_csv(args.tlx)

    trials["acc_mean"] = trials[AXES].mean(axis=1)
    cell = trials.groupby(["pid","condition"], as_index=False)["acc_mean"].mean()
    pivot = cell.pivot(index="pid", columns="condition", values="acc_mean").dropna()

    results = {"accuracy": {}, "workload": {}}
    for a, b in [("C1","C0"), ("C2","C0"), ("C2","C1")]:
        if {a,b}.issubset(pivot.columns):
            mean, lo, hi = bootstrap_paired(pivot[a].values, pivot[b].values)
            d            = cohens_d_paired(pivot[a].values, pivot[b].values)
            results["accuracy"][f"{a}_minus_{b}"] = {
                "mean_delta": mean, "ci95_lo": lo, "ci95_hi": hi, "cohens_d": d
            }

    tcell = tlx.pivot(index="pid", columns="condition", values="tlx_global").dropna()
    for a, b in [("C1","C0"), ("C2","C0"), ("C2","C1")]:
        if {a,b}.issubset(tcell.columns):
            mean, lo, hi = bootstrap_paired(tcell[a].values, tcell[b].values)
            d            = cohens_d_paired(tcell[a].values, tcell[b].values)
            results["workload"][f"{a}_minus_{b}"] = {
                "mean_delta": mean, "ci95_lo": lo, "ci95_hi": hi, "cohens_d": d
            }

    out_path.write_text(json.dumps(results, indent=2))
    print(f"[effect_sizes] wrote {out_path}")


if __name__ == "__main__":
    main()
