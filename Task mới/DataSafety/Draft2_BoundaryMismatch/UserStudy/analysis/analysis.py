"""
analysis.py — skeleton analysis for the BLE mixed-method evaluation.

This script implements the pre-registered analyses described in
analysis_plan.md. It runs end-to-end on the expected Qualtrics export
and prototype log. Until data is collected, the script runs against a
synthetic placeholder file that exercises every code path.

Usage:
    python analysis.py --vignette raw_vignette.csv \
                        --proto raw_prototype_log.csv \
                        --out results/

Inputs (expected schemas after pilot):
- raw_vignette.csv  (one row per participant, wide format)
    pid, condition (current|ble), seq (L1..L4),
    socialnova_mcq, socialnova_acc, socialnova_comp, socialnova_intent, socialnova_t3_5,
    chatbuzz_mcq,   chatbuzz_acc,   chatbuzz_comp,   chatbuzz_intent,   chatbuzz_t3_5,
    photopals_mcq,  photopals_acc,  photopals_comp,  photopals_intent,  photopals_t3_5,
    mapmate_mcq,    mapmate_acc,    mapmate_comp,    mapmate_intent,    mapmate_t3_5,
    iuipc, attn_check, rushed, age_band, gender, country, edu, it_bg, completion_sec
- raw_prototype_log.csv  (one row per click event from the prototype)
    pid, event (toggle_open|toggle_close|view_app), boundary, app, t_ms
"""

import argparse, os, json, math, hashlib
import numpy as np, pandas as pd
from scipy import stats

PRE_REG_HASH_TARGET = None   # set after OSF lock

# Filtered Maybe-rates from the published survey (Section 5 of the paper)
PUBLISHED_MAYBE = {
    "b1": 14.9, "b2": 13.8, "b3": 28.7, "b4": 19.5, "b5": 12.6,
    "b6": 14.9, "b7": 19.5, "b8": 19.5, "b9": 21.8,
}
APPS = ["socialnova", "chatbuzz", "photopals", "mapmate"]
DVS  = ["mcq", "acc", "comp", "intent"]


def load_vignette(path):
    df = pd.read_csv(path)
    return df


def apply_exclusions(df):
    """Pre-registered exclusions."""
    n0 = len(df)
    df = df[df["attn_check"] == True]
    df = df[df["completion_sec"] >= 240]
    df = df[df["rushed"] != "Yes, I rushed some"]
    # Straight-lining flag across the 12 Likerts
    likert_cols = [f"{a}_{d}" for a in APPS for d in ("acc","comp","intent")]
    df = df[df[likert_cols].std(axis=1) > 0.1]
    n1 = len(df)
    print(f"Exclusions: {n0} -> {n1} ({n0-n1} removed)")
    return df


def participant_means(df):
    out = pd.DataFrame()
    out["pid"] = df["pid"]
    out["condition"] = df["condition"]
    for dv in DVS:
        cols = [f"{a}_{dv}" for a in APPS]
        out[f"mean_{dv}"] = df[cols].mean(axis=1)
    return out


def welch_t(a, b, side="greater"):
    """Welch's t, one-sided greater by default. Returns d, ci, p."""
    t, p_two = stats.ttest_ind(a, b, equal_var=False)
    p = p_two / 2 if (side == "greater" and t > 0) else \
        (1 - p_two/2 if side == "greater" else p_two)
    # Cohen's d (Welch / pooled variant)
    s = math.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    d = (a.mean() - b.mean()) / s
    # Bootstrap 95% CI on d
    rng = np.random.default_rng(seed=42)
    boots = []
    for _ in range(10_000):
        ra = rng.choice(a.values, size=len(a), replace=True)
        rb = rng.choice(b.values, size=len(b), replace=True)
        sb = math.sqrt((ra.var(ddof=1) + rb.var(ddof=1)) / 2)
        boots.append((ra.mean() - rb.mean()) / sb)
    ci = (np.percentile(boots, 2.5), np.percentile(boots, 97.5))
    return d, ci, p


def tost(a, b, sesoi=0.30, alpha=0.05):
    """Two one-sided tests for equivalence on Cohen's d."""
    s = math.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    d_obs = (a.mean() - b.mean()) / s
    se_d = math.sqrt(1/len(a) + 1/len(b))
    # one-sided p for lower and upper SESOI bounds
    p_low = 1 - stats.norm.cdf((d_obs + sesoi)/se_d)
    p_high = stats.norm.cdf((d_obs - sesoi)/se_d)
    # 90% CI on d
    z = stats.norm.ppf(1 - alpha)
    ci90 = (d_obs - z*se_d, d_obs + z*se_d)
    return d_obs, ci90, max(p_low, p_high)


def h1_h2_h3(df_per_participant):
    """Run H1, H2, H3 with Bonferroni correction."""
    results = []
    for dv, label in [("mcq","H1: comprehension"),
                       ("acc","H2: perceived accuracy"),
                       ("comp","H3: comprehensiveness")]:
        col = f"mean_{dv}"
        a = df_per_participant[df_per_participant.condition=="ble"][col]
        b = df_per_participant[df_per_participant.condition=="current"][col]
        d, ci, p = welch_t(a, b, side="greater")
        p_adj = min(1.0, p * 3)
        verdict = (
            "supported" if (p_adj < 0.0167 and d >= 0.30)
            else "refuted" if ci[1] < 0.20
            else "no decision"
        )
        results.append({"hypothesis": label, "d": round(d,3),
                        "ci_lo": round(ci[0],3), "ci_hi": round(ci[1],3),
                        "p": round(p,4), "p_adj": round(p_adj,4),
                        "verdict": verdict})
    return pd.DataFrame(results)


def h4(proto_df):
    """Per-case drawer-opening rate (BLE arm only) vs published Maybe."""
    bs = sorted(PUBLISHED_MAYBE.keys())
    counts = (proto_df[(proto_df.event == "toggle_open")]
              .groupby("boundary").pid.nunique())
    n_bleparticipants = proto_df[proto_df.event == "view_app"].pid.nunique()
    opening_rate = {b: counts.get(b, 0)/n_bleparticipants for b in bs}
    rates = [opening_rate[b]*100 for b in bs]
    maybes = [PUBLISHED_MAYBE[b]    for b in bs]
    rho, p = stats.spearmanr(rates, maybes)
    return pd.DataFrame([{"hypothesis":"H4: signal vs engagement",
                           "rho": round(rho,3), "p": round(p,4),
                           "verdict": "supported" if (rho>=0.5 and p<0.05)
                                       else "refuted" if rho<=0.1
                                       else "no decision"}])


def h5(df_per_participant):
    a = df_per_participant[df_per_participant.condition=="ble"]["mean_intent"]
    b = df_per_participant[df_per_participant.condition=="current"]["mean_intent"]
    d, ci, p = tost(a, b)
    verdict = ("equivalence supported" if p < 0.05 and ci[0] > -0.30 and ci[1] < 0.30
               else "directional effect" if (ci[0]>0 or ci[1]<0)
               else "no decision")
    return pd.DataFrame([{"hypothesis":"H5: equivalence on install intent",
                           "d": round(d,3),
                           "ci90_lo": round(ci[0],3), "ci90_hi": round(ci[1],3),
                           "p_tost": round(p,4),
                           "verdict": verdict}])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vignette", required=True)
    ap.add_argument("--proto", required=True)
    ap.add_argument("--out", default="results/")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    df = load_vignette(args.vignette)
    df = apply_exclusions(df)
    pp = participant_means(df)

    res_main = h1_h2_h3(pp)
    proto_df = pd.read_csv(args.proto)
    res_h4   = h4(proto_df[proto_df.pid.isin(pp[pp.condition=="ble"].pid)])
    res_h5   = h5(pp)

    summary = pd.concat([res_main, res_h4, res_h5], ignore_index=True)
    summary.to_csv(os.path.join(args.out, "summary_table.csv"), index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
