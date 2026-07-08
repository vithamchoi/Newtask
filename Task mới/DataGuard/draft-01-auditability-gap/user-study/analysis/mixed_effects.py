"""Python fallback for the mixed-effects analysis (statsmodels).

The preferred analysis path is mixed_effects.R (lme4). This script is here
so that reviewers without R can reproduce the headline numbers.

Models fitted:
    H1: glm logistic with participant + app fixed effects (proxy MEM)
    H2: OLS workload ~ condition + participant FE
    Reported: per-condition adjusted means + pairwise contrasts (Holm).

Run after data collection:
    python analysis/mixed_effects.py \
        --trials data/processed/trials.csv \
        --tlx    data/processed/tlx.csv \
        --out    analysis/results/
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm


def to_long_accuracy(trials: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in trials.columns if c.startswith("acc_")]
    long = trials.melt(id_vars=["pid","condition","app_id","stratum"],
                       value_vars=cols, var_name="axis", value_name="correct")
    long = long.dropna(subset=["correct"])
    long["correct"] = long["correct"].astype(int)
    long["condition"] = pd.Categorical(long["condition"], categories=["C0","C1","C2"])
    long["stratum"]   = pd.Categorical(long["stratum"],   categories=["S1","S2","S3"])
    return long


def fit_h1(long: pd.DataFrame) -> dict:
    model = smf.logit("correct ~ C(condition) + C(pid) + C(app_id)", data=long).fit(disp=0)
    out = {"summary": model.summary().as_text()}
    for k, v in model.params.items():
        if "condition" in k:
            out[k] = {
                "coef": float(v),
                "se": float(model.bse[k]),
                "p":  float(model.pvalues[k]),
            }
    return out


def fit_h2(tlx: pd.DataFrame) -> dict:
    tlx["condition"] = pd.Categorical(tlx["condition"], categories=["C0","C1","C2"])
    m = smf.ols("tlx_global ~ C(condition) + C(pid)", data=tlx).fit()
    return {"summary": m.summary().as_text(),
            "coefs": {k: {"coef": float(v), "se": float(m.bse[k]), "p": float(m.pvalues[k])}
                      for k, v in m.params.items() if "condition" in k}}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--trials", required=True)
    p.add_argument("--tlx",    required=True)
    p.add_argument("--out",    default="analysis/results/")
    a = p.parse_args()

    out_dir = Path(a.out); out_dir.mkdir(parents=True, exist_ok=True)
    trials = pd.read_csv(a.trials)
    tlx    = pd.read_csv(a.tlx)

    long = to_long_accuracy(trials)
    h1 = fit_h1(long)
    h2 = fit_h2(tlx)
    (out_dir / "h1.txt").write_text(h1["summary"])
    (out_dir / "h2.txt").write_text(h2["summary"])
    (out_dir / "h1_coefs.json").write_text(json.dumps({k:v for k,v in h1.items() if k!="summary"}, indent=2))
    (out_dir / "h2_coefs.json").write_text(json.dumps(h2["coefs"], indent=2))
    print(f"[mem] wrote results to {out_dir}")


if __name__ == "__main__":
    main()
