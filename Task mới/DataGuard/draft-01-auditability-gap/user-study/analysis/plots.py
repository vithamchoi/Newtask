"""Result figures: accuracy by condition x stratum, workload by condition,
reliability diagrams. Saves PDF and PNG to analysis/results/figs/.

Run after data collection:
    python analysis/plots.py --trials data/processed/trials.csv \
                             --tlx    data/processed/tlx.csv
"""
from __future__ import annotations
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PALETTE = {"C0":"#5A5A5A", "C1":"#2763B2", "C2":"#844CA2"}
AXES = ["acc_share_corr","acc_share_comp","acc_coll_corr","acc_coll_comp"]


def plot_accuracy(trials: pd.DataFrame, out_dir: Path) -> None:
    trials["acc_mean"] = trials[AXES].mean(axis=1)
    cell = trials.groupby(["condition","stratum"], as_index=False)["acc_mean"].agg(["mean","sem"]).reset_index()
    fig, ax = plt.subplots(figsize=(6.5, 4))
    strata = ["S1","S2","S3"]
    width = 0.27
    x = np.arange(len(strata))
    for i, cond in enumerate(["C0","C1","C2"]):
        row = cell[cell.condition == cond].set_index("stratum").reindex(strata)
        ax.bar(x + (i-1)*width, row["mean"], width,
               yerr=row["sem"], color=PALETTE[cond], label=cond,
               error_kw={"capsize": 3, "lw": 0.8})
    ax.set_xticks(x); ax.set_xticklabels(["S1 high-conf","S2 high-disagree","S3 no-data"])
    ax.set_ylabel("Mean per-trial accuracy"); ax.set_ylim(0, 1)
    ax.legend(frameon=False); ax.set_title("Accuracy by condition x stratum")
    fig.tight_layout(); fig.savefig(out_dir / "accuracy_by_stratum.pdf")
    fig.savefig(out_dir / "accuracy_by_stratum.png", dpi=160)


def plot_workload(tlx: pd.DataFrame, out_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    cell = tlx.groupby("condition")["tlx_global"].agg(["mean","sem"]).reindex(["C0","C1","C2"])
    ax.bar(cell.index, cell["mean"], yerr=cell["sem"],
           color=[PALETTE[c] for c in cell.index], error_kw={"capsize":3,"lw":0.8})
    ax.set_ylabel("NASA-TLX global (0-100)"); ax.set_ylim(0, 100)
    ax.set_title("Workload by condition")
    fig.tight_layout(); fig.savefig(out_dir / "workload.pdf")
    fig.savefig(out_dir / "workload.png", dpi=160)


def plot_reliability(reliability_dir: Path, out_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot([0,1],[0,1], ls="--", color="grey", lw=1, label="perfect")
    for cond in ["C0","C1","C2"]:
        p = reliability_dir / f"reliability_{cond}.csv"
        if not p.exists() or p.stat().st_size == 0: continue
        try:
            df = pd.read_csv(p)
        except pd.errors.EmptyDataError:
            continue
        if df.empty: continue
        agg = df.groupby("bin").apply(
            lambda g: pd.Series({"conf": np.average(g.mean_conf, weights=g.n),
                                 "acc":  np.average(g.emp_acc,   weights=g.n)})
        )
        ax.plot(agg["conf"], agg["acc"], marker="o", color=PALETTE[cond], label=cond)
    ax.set_xlabel("Mean confidence (per bin)"); ax.set_ylabel("Empirical accuracy")
    ax.set_title("Reliability diagram"); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(out_dir / "reliability.pdf")
    fig.savefig(out_dir / "reliability.png", dpi=160)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", required=True)
    ap.add_argument("--tlx",    required=True)
    ap.add_argument("--out",    default="analysis/results/figs/")
    ap.add_argument("--reliability-dir", default="analysis/results/")
    args = ap.parse_args()

    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    trials = pd.read_csv(args.trials)
    tlx    = pd.read_csv(args.tlx)
    plot_accuracy(trials, out)
    plot_workload(tlx, out)
    plot_reliability(Path(args.reliability_dir), out)
    print(f"[plots] wrote figures to {out}")


if __name__ == "__main__":
    main()
