"""Stimulus loader and accessors."""

from __future__ import annotations
import json
from . import db


def list_stimuli_by_stratum() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {"S1": [], "S2": [], "S3": []}
    with db.get_conn() as c:
        rows = c.execute("SELECT app_id, stratum FROM stimuli").fetchall()
    for r in rows:
        if r["stratum"] in out:
            out[r["stratum"]].append(r["app_id"])
    return out


def fetch_stimulus(app_id: str) -> dict | None:
    with db.get_conn() as c:
        r = c.execute("SELECT * FROM stimuli WHERE app_id = ?", (app_id,)).fetchone()
    if r is None:
        return None
    d = dict(r)
    # decode JSON columns
    for k in ("data_safety_json", "evidence_share", "evidence_collect", "ai_suggestion_json"):
        if d.get(k):
            try:
                d[k] = json.loads(d[k])
            except Exception:
                pass
    return d


def stimulus_payload_for_condition(app_id: str, condition: str) -> dict:
    """Return only the fields the participant should see, gated by condition."""
    full = fetch_stimulus(app_id)
    if not full:
        raise KeyError(f"unknown app_id {app_id}")
    base = {
        "app_id":     full["app_id"],
        "app_name":   full["app_name"],
        "category":   full["category"],
        "play_url":   full["play_url"],
        "policy_url": full["policy_url"],
        "data_safety": full["data_safety_json"],
        "policy_text": full["policy_text"],
    }
    if condition == "C0":
        return base
    if condition == "C1":
        return {**base,
                "section_share": full["section_share"],
                "section_collect": full["section_collect"]}
    if condition == "C2":
        return {**base,
                "section_share": full["section_share"],
                "section_collect": full["section_collect"],
                "evidence_share":  full["evidence_share"],
                "evidence_collect": full["evidence_collect"],
                "ai_suggestion":  full["ai_suggestion_json"]}
    raise ValueError(f"unknown condition {condition}")
