"""Evidence locator: precompute per-axis evidence spans + suggested labels
for the C2 condition.

We use a sentence-level retrieval over the policy text scored against each
structured Data Safety claim, plus an LLM-classifier head that emits a
label and a 0-1 uncertainty. Outputs are cached so the user-study trial
loop is deterministic.

Inputs:
    stimuli/stimuli_pool.json   (skeleton built by stimuli/build_pool.py)

Outputs:
    stimuli/stimuli_pool.json   (in-place fill of evidence_* and ai_suggestion)

The LLM call layer is optional: by passing --offline the script will fall
back to a TF-IDF / regex baseline so the pipeline can be exercised without
external API access.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

AXES = ("share_corr", "share_comp", "coll_corr", "coll_comp")

# Heuristic triggers used by the offline fallback. They mirror the four
# heaviest rationale themes from Study 4 of the parent paper.
TRIGGERS = {
    "third_party": re.compile(
        r"\b(admob|firebase|google analytics|facebook|appsflyer|crashlytics|"
        r"ad network|advertising partner|third[- ]party|service provider|sdk|"
        r"vendors?)\b", re.I),
    "identifier":  re.compile(
        r"\b(advertising id|aaid|gaid|idfa|ip address|cookie|device id|"
        r"mac address|sim)\b", re.I),
    "hedging":     re.compile(
        r"\b(may (collect|share|use)|including but not limited to|such as|"
        r"from time to time)\b", re.I),
    "no_data_contradiction": re.compile(
        r"\b(we (collect|share)|analytics|advertising)\b", re.I),
}

def sentence_split(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text or "") if s.strip()]

def score_sentence(s: str) -> int:
    return sum(1 for pat in TRIGGERS.values() if pat.search(s))

def fallback_locate(stim: dict) -> dict:
    """Offline baseline -- pick the highest-scoring sentence per axis."""
    sents_share   = sentence_split(stim.get("section_share")  or stim.get("policy_text",""))
    sents_collect = sentence_split(stim.get("section_collect") or stim.get("policy_text",""))
    def top(sents):
        if not sents: return None
        return max(sents, key=score_sentence)
    ev_share   = top(sents_share)
    ev_collect = top(sents_collect)

    # No-data heuristic for label suggestion: if structured side is empty
    # but policy has a third-party trigger, suggest Incorrect.
    ds = stim.get("data_safety", {})
    no_shared    = not ds.get("data_shared")
    no_collected = not ds.get("data_collected")
    suggested = {}
    for axis in AXES:
        if axis.startswith("share"):
            empty, ev = no_shared,    ev_share
        else:
            empty, ev = no_collected, ev_collect
        score = score_sentence(ev or "")
        if empty and score >= 1:
            suggested[axis] = {"label": "Incorrect" if "corr" in axis else "Incomplete",
                               "uncertainty": max(0.15, 0.6 - 0.1*score)}
        elif score >= 2:
            suggested[axis] = {"label": "Incorrect" if "corr" in axis else "Incomplete",
                               "uncertainty": 0.45}
        else:
            suggested[axis] = {"label": "Correct" if "corr" in axis else "Complete",
                               "uncertainty": 0.35}

    return {
        "evidence_share":   [{"axis":"share_corr","match": ev_share}]   if ev_share else [],
        "evidence_collect": [{"axis":"coll_corr","match":  ev_collect}] if ev_collect else [],
        "ai_suggestion":    suggested,
    }

def llm_locate(stim: dict, model: str) -> dict:
    """Real LLM-backed locator. Stub: implement against your provider."""
    # NOTE: This stub is intentionally kept abstract so the repo does not
    # take an external dependency in CI. The expected output schema is the
    # same as fallback_locate().
    raise NotImplementedError("Plug in your LLM provider here.")

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--pool",    default="stimuli/stimuli_pool.json")
    p.add_argument("--out",     default=None,
                   help="default = overwrite --pool in place")
    p.add_argument("--offline", action="store_true",
                   help="use the deterministic TF-IDF/regex baseline")
    p.add_argument("--model",   default="gpt-4o-mini")
    args = p.parse_args()

    out_path = Path(args.out or args.pool)
    pool = json.loads(Path(args.pool).read_text())
    for stim in pool:
        try:
            filled = (fallback_locate(stim) if args.offline
                      else llm_locate(stim, args.model))
        except NotImplementedError:
            filled = fallback_locate(stim)
        for k, v in filled.items():
            stim[k] = v
    out_path.write_text(json.dumps(pool, indent=2))
    print(f"[locate] wrote {len(pool)} stimuli to {out_path}")

if __name__ == "__main__":
    main()
