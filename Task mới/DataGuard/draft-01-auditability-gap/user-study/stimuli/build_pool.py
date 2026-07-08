"""Build the 24-app stimulus pool from the retrospective DataGuard corpus.

Reads ../../data-labels.xlsx and ../../data-guard-experiment/output/* to
identify candidate apps in each stratum, then writes ``stimuli_pool.json``
with the schema documented in ../CODEBOOK.md.

Usage:
    python stimuli/build_pool.py --corpus ../../data-labels.xlsx \\
            --out stimuli/stimuli_pool.json --n-per-stratum 8

This script is intentionally idempotent: re-running with the same arguments
should produce the same pool, so the gold standard remains pinned.
"""
from __future__ import annotations
import argparse
import json
import random
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--corpus", required=True, help="path to data-labels.xlsx")
    p.add_argument("--out",    default="stimuli/stimuli_pool.json")
    p.add_argument("--n-per-stratum", type=int, default=8)
    p.add_argument("--seed",   type=int, default=20260615)
    args = p.parse_args()

    print(f"[build_pool] reading {args.corpus}")
    try:
        import pandas as pd
    except Exception:
        raise SystemExit("pandas required: pip install pandas openpyxl")

    df = pd.read_excel(args.corpus)
    rng = random.Random(args.seed)

    # ---------- Stratum predicates ----------
    # S1 high-confidence: per-app majority agreement on all four axes and
    #                     non-empty Data Safety on both sides
    # S2 high-disagreement: double-annotated apps where per-app kappa < 0
    # S3 no-data: Data Safety declares no sharing AND no collection

    # NB: the exact column names depend on the workbook; adapt as needed.
    def is_no_data(row):
        ds = str(row.get("data_safety_content", ""))
        return ("data_shared': []" in ds) and ("data_collected': []" in ds)

    s3_candidates = [r for _, r in df.iterrows() if is_no_data(r)]
    print(f"[build_pool] candidate S3 (no-data): {len(s3_candidates)}")

    # S1: pick rows where both label_1 == 'Correct' and 'Unknown' avoided
    s1_candidates = [r for _, r in df.iterrows()
                     if str(r.get("label_1","")) == "Correct" and not is_no_data(r)]
    print(f"[build_pool] candidate S1 (high-conf):    {len(s1_candidates)}")

    # S2: rows where label_2 == 'Unknown' (proxy for disagreement)
    s2_candidates = [r for _, r in df.iterrows()
                     if str(r.get("label_2","")).startswith("Unknown")]
    print(f"[build_pool] candidate S2 (high-disagree): {len(s2_candidates)}")

    def sample(cands, n, stratum):
        rng.shuffle(cands)
        out = []
        for i, row in enumerate(cands[:n]):
            out.append(row_to_stimulus(row, stratum, i+1))
        return out

    pool = sample(s1_candidates, args.n_per_stratum, "S1") \
         + sample(s2_candidates, args.n_per_stratum, "S2") \
         + sample(s3_candidates, args.n_per_stratum, "S3")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(pool, f, indent=2)
    print(f"[build_pool] wrote {len(pool)} stimuli to {args.out}")
    print("Next: have two expert coders adjudicate gold labels and fill")
    print("the gold + evidence_share + evidence_collect + ai_suggestion")
    print("fields. See stimuli/README.md for the gold-standard protocol.")


def row_to_stimulus(row, stratum, idx):
    """Convert a workbook row into a stimulus skeleton.

    The gold / evidence / AI-suggestion fields are left empty here -- they
    must be filled in by the expert-coder adjudication step. We refuse to
    fabricate them so the pool ships in a coder-ready state.
    """
    import ast
    try:
        ds = ast.literal_eval(str(row.get("data_safety_content","{}")))
    except Exception:
        ds = {}
    return {
        "app_id":     f"{stratum}-{idx:03d}",
        "app_name":   str(row.get("app_name", row.get("app_pkg",""))),
        "category":   str(row.get("category","")),
        "stratum":    stratum,
        "play_url":   "",
        "policy_url": "",
        "captured_at": "",
        "data_safety": ds,
        "policy_text": str(row.get("privacy_policy_content","")),
        "section_share":   "",   # to be filled by sectioner or coder
        "section_collect": "",
        "evidence_share":   [],  # filled at adjudication time
        "evidence_collect": [],
        "ai_suggestion": {},     # filled by evidence_locator/locate.py
        "gold": {                # filled by adjudication
            "share_corr": None, "share_comp": None,
            "coll_corr":  None, "coll_comp":  None
        },
        "kappa_pre_consensus": None
    }


if __name__ == "__main__":
    main()
