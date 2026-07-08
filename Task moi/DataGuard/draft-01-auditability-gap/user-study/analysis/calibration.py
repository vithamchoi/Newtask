"""Confidence calibration: Brier score + reliability diagram per condition.

Run after data collection:
    python analysis/calibration.py \
        --trials data/processed/trials.csv \
        --out    analysis/results/
"""
from __future__ import annotations
import argparse
from pathlib import Path

import numpy as np
import pandas as pd


AXES = ["share_corr", "share_comp", "coll_corr", "coll_comp"]


def brier_per_trial(row) -> float:
    losses = []
    for ax in AXES:
        c = row.get(f"conf_{ax}")
        a = row.get(f"acc_{ax}")
        if pd.isna(c) or pd.isna(a):
            continue
        p = float(c) / 100.0
        losses.append((p - float(a)) ** 2)
    return float(np.mean(losses)) if losses else np.nan


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--trials", required=True)
    p.add_argument("--out",    default="analysis/results/")
    p.add_argument("--bootstrap", type=int, default=1000)
    args = p.parse_args()

    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.trials)
    df["brier"] = df.apply(brier_per_trial, axis=1)

    # Per-(participant, condition) cell mean
    cell = (df.groupby(["pid","condition"], as_index=False)["brier"]
              .mean().rename(columns={"brier":"brier_cell"}))

    # Per-condition summary
    summary = (cell.groupby("condition")["brier_cell"]
                   .agg(["mean","std","count"]).reset_index())
    summary.to_csv(out / "brier_summary.csv", index=False)

    # Paired bootstrap for Delta(C2 - C0)
    rng = np.random.default_rng(20260615)
    pivot = cell.pivot(index="pid", columns="condition", values="brier_cell").dropna()
    if {"C0","C2"}.issubset(pivot.columns):
        deltas = pivot["C2"] - pivot["C0"]
        boots = []
        for _ in range(args.bootstrap):
            sample = rng.choice(deltas.values, size=len(deltas), replace=True)
            boots.append(sample.mean())
        lo, hi = np.percentile(boots, [2.5, 97.5])
        with open(out / "brier_delta_C2_C0.txt", "w") as f:
            f.write(f"Delta(C2 - C0): mean = {np.mean(boots):.4f}\n")
            f.write(f"95% bootstrap CI: [{lo:.4f}, {hi:.4f}]\n")

    # Reliability diagram (10 bins) per condition
    rel_cols = ["axis","bin","bin_lo","bin_hi","n","mean_conf","emp_acc"]
    for cond, g in df.groupby("condition"):
        rows = []
        for ax in AXES:
            confs = g[f"conf_{ax}"].dropna().values / 100.0
            accs  = g[f"acc_{ax}"].dropna().values
            n = min(len(confs), len(accs))
            confs, accs = confs[:n], accs[:n]
            bins = np.linspace(0, 1, 11)
            bin_ids = np.digitize(confs, bins) - 1
            for b in range(10):
                mask = bin_ids == b
                if mask.sum() == 0: continue
                rows.append({
                    "axis": ax, "bin": b,
                    "bin_lo": float(bins[b]), "bin_hi": float(bins[b+1]),
                    "n": int(mask.sum()),
                    "mean_conf": float(confs[mask].mean()),
                    "emp_acc":   float(accs[mask].mean()),
                })
        # Always write a header so downstream tools can read the file
        pd.DataFrame(rows, columns=rel_cols).to_csv(
            out / f"reliability_{cond}.csv", index=False)
    print(f"[calibration] wrote results to {out}")


if __name__ == "__main__":
    main()
