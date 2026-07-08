"""
Build the 40-app PRISM stimuli pool from the corpus.

Tom tat: Tao kho 40 ung dung phan tang theo 4 goc cua ma tran (pha-bien x mo-ho)
nhu dinh nghia trong PHUONG-AN-A-user-study-plan.md S3.1.

Quadrants (10 apps each):
  Q1 = common  & ambiguous  -> M1-dominant (M1 fires AND not M3-only)
  Q2 = common  & tractable  -> M3-dominant (only M3 fires)
  Q3 = rare    & ambiguous  -> M6-bearing (M6 fires)
  Q4 = rare    & tractable  -> clean controls (no code fires)

The first 5 apps in the output are tagged `is_tutorial=True` (walkthrough only).

Run:  python build_stimuli.py
Outputs:  data/stimuli.json
"""
import ast
import json
import random
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT.parent.parent.parent / "data-labels.xlsx"
OUT = ROOT / "data" / "stimuli.json"

CAT_NAMES = {
    1: "Art & Design", 2: "Beauty", 3: "Books & Reference", 4: "Business",
    5: "Communication", 6: "Lifestyle", 7: "Personalization",
    8: "Photography", 9: "Productivity", 10: "Shopping",
    11: "Social", 12: "Tools",
}

LEXICON = {
    "M1": [r"\bthird[- ]part(?:y|ies)\b", r"\bservice provider(?:s)?\b",
           r"\bshar(?:e|ed|es|ing) (?:with|to)\b", r"\baffiliate(?:s)?\b",
           r"\b(?:advertising|ad) (?:network|partner)s?\b",
           r"\banalytics provider(?:s)?\b"],
    "M2": [r"\bdevice (?:id|identifier)s?\b",
           r"\badvertising (?:id|identifier)s?\b",
           r"\baaid\b|\bidfa\b|\bgaid\b|\bandroid id\b",
           r"\bunique (?:device )?identifier(?:s)?\b"],
    "M3": [r"\bmay\b", r"\bmight\b", r"\bsuch as\b",
           r"\bincluding but not limited to\b", r"\bcertain\b",
           r"\bvarious\b", r"\bfrom time to time\b"],
    "M4": [r"\bwe (?:do not|don't) (?:collect|share|sell)\b",
           r"\bno (?:personal )?(?:data|information) (?:is )?collect(?:ed)?\b",
           r"\bdoes not (?:collect|share|sell)\b"],
    "M5": [r"\b(?:approximate|coarse|city[- ]?level) location\b",
           r"\b(?:precise|fine[- ]?grained|gps|exact) location\b",
           r"\bip[- ]?(?:address|derived) location\b",
           r"\bgeoloca(?:tion|ted)\b"],
    "M6": [r"\bencrypt(?:ed|ion|s)?\b", r"\btls\b|\bssl\b|\bhttps\b",
           r"\bin transit\b|\bat rest\b",
           r"\b(?:industry|reasonable) (?:standard )?security\b"],
    "M7": [r"\bnot responsible for\b",
           r"\bgoverned by (?:their|the third[- ]party)\b",
           r"\bsubject to (?:their|the third[- ]party) privacy polic(?:y|ies)\b",
           r"\bwe (?:have )?(?:no|do not have) control\b"],
}
COMPILED = {c: [re.compile(p, re.IGNORECASE) for p in pats]
            for c, pats in LEXICON.items()}


def hits_for(text):
    s = {}
    for code, regs in COMPILED.items():
        s[code] = sum(len(r.findall(text or "")) for r in regs)
    return s


def parse_ds(s):
    try:
        d = ast.literal_eval(str(s))
        return d
    except Exception:
        return {"data_shared": [], "data_collected": []}


def excerpt(text, max_chars=2400):
    if not isinstance(text, str):
        return ""
    text = text.strip()
    if len(text) <= max_chars:
        return text
    cut = text[:max_chars]
    last_period = cut.rfind(". ")
    if last_period > max_chars * 0.6:
        return cut[: last_period + 1]
    return cut


def main():
    if not CORPUS.exists():
        print(f"ERROR: corpus not found at {CORPUS}", file=sys.stderr)
        sys.exit(2)
    print(f"Loading corpus from {CORPUS}...")
    app = pd.read_excel(CORPUS, sheet_name="App")
    lab = pd.read_excel(CORPUS, sheet_name="Label")
    label_ids = set(lab["app_id"].unique())
    app = app[app["app_id"].isin(label_ids)]
    app = app[app["privacy_policy_content"].astype(str).str.strip().str.len() > 60]
    app["category"] = app["category_id"].map(CAT_NAMES)
    print(f"Parseable policy-label pairs: {len(app)}")

    # Compute lexicon hits for every app.
    records = []
    for _, row in app.iterrows():
        policy = str(row["privacy_policy_content"])
        h = hits_for(policy)
        fired = {c for c, n in h.items() if n > 0}
        records.append({
            "app_id": int(row["app_id"]),
            "package": str(row["app_pkg"]),
            "name": str(row["app_name"])[:60],
            "category": row["category"],
            "policy_excerpt": excerpt(policy),
            "data_safety_raw": str(row["data_safety_content"]),
            "lexicon_count": h,
            "codes_fired": sorted(fired),
        })

    df = pd.DataFrame(records)

    def classify(row):
        fired = set(row["codes_fired"])
        if not fired:
            return "Q4_clean"
        if "M6" in fired:
            return "Q3_rare_ambig"
        if fired == {"M3"}:
            return "Q2_common_tractable"
        if "M1" in fired:
            return "Q1_common_ambig"
        return "Q2_common_tractable"

    df["quadrant"] = df.apply(classify, axis=1)
    print("Quadrant pool sizes:")
    print(df["quadrant"].value_counts())

    rng = random.Random(20260617)
    picked = []
    for q, label in [("Q1_common_ambig", "common & ambiguous"),
                     ("Q2_common_tractable", "common & tractable"),
                     ("Q3_rare_ambig", "rare & ambiguous"),
                     ("Q4_clean", "rare & tractable")]:
        pool = df[df["quadrant"] == q].to_dict(orient="records")
        rng.shuffle(pool)
        # Prefer category spread.
        seen_cats = set()
        chosen = []
        for r in pool:
            if r["category"] in seen_cats and len(chosen) < 10:
                continue
            chosen.append(r)
            seen_cats.add(r["category"])
            if len(chosen) == 10:
                break
        # If we didn't reach 10 via category-spread, top up from remaining pool.
        if len(chosen) < 10:
            for r in pool:
                if r not in chosen:
                    chosen.append(r)
                if len(chosen) == 10:
                    break
        for r in chosen:
            r["quadrant"] = q
            r["quadrant_label"] = label
        picked.extend(chosen)
        print(f"  {q}: picked {len(chosen)}")

    # Mark first 5 worst examples (highest total hit count) as tutorial.
    by_hits = sorted(
        picked,
        key=lambda r: -sum(r["lexicon_count"].values()),
    )
    tutorial_ids = {r["app_id"] for r in by_hits[:5]}
    for r in picked:
        r["is_tutorial"] = r["app_id"] in tutorial_ids

    # Drop the lexicon_count blob from the final JSON; the server recomputes it.
    out = []
    for r in picked:
        out.append({
            "app_id": r["app_id"],
            "package": r["package"],
            "name": r["name"],
            "category": r["category"],
            "quadrant": r["quadrant"],
            "quadrant_label": r["quadrant_label"],
            "is_tutorial": r["is_tutorial"],
            "data_safety_raw": r["data_safety_raw"],
            "policy_excerpt": r["policy_excerpt"],
            "expected_codes": r["codes_fired"],
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(out)} stimuli to {OUT}")
    print(f"Tutorial apps: {sorted(tutorial_ids)}")


if __name__ == "__main__":
    main()
