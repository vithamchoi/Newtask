"""Tests for the stimulus loader: gating by condition."""
import json
import tempfile
import unittest.mock as mock

import pytest

from backend import db, stimuli


SAMPLE = {
    "app_id": "T-001", "app_name": "Test", "category": "Tools", "stratum": "S1",
    "play_url": "x", "policy_url": "y",
    "data_safety_json": {"data_shared":[], "data_collected":[], "security_practices":[]},
    "policy_text": "policy body",
    "section_share": "share body",
    "section_collect": "collect body",
    "evidence_share":  [{"axis":"share_corr","match":"share body"}],
    "evidence_collect": [{"axis":"coll_corr","match":"collect body"}],
    "ai_suggestion_json": {"share_corr":{"label":"Correct","uncertainty":0.2}},
    "g_share_corr": "Supported", "g_share_comp": "Supported",
    "g_coll_corr": "Supported",  "g_coll_comp": "Supported",
    "kappa_pre_consensus": 0.7,
}


def test_c0_payload_only_data_safety_and_policy(monkeypatch):
    monkeypatch.setattr(stimuli, "fetch_stimulus", lambda _id: SAMPLE)
    out = stimuli.stimulus_payload_for_condition("T-001", "C0")
    assert "data_safety" in out and "policy_text" in out
    assert "section_share" not in out
    assert "evidence_share" not in out
    assert "ai_suggestion" not in out


def test_c1_payload_adds_sections(monkeypatch):
    monkeypatch.setattr(stimuli, "fetch_stimulus", lambda _id: SAMPLE)
    out = stimuli.stimulus_payload_for_condition("T-001", "C1")
    assert "section_share" in out and "section_collect" in out
    assert "evidence_share" not in out
    assert "ai_suggestion" not in out


def test_c2_payload_includes_evidence_and_ai(monkeypatch):
    monkeypatch.setattr(stimuli, "fetch_stimulus", lambda _id: SAMPLE)
    out = stimuli.stimulus_payload_for_condition("T-001", "C2")
    assert "evidence_share" in out
    assert "ai_suggestion"  in out


def test_unknown_condition_raises(monkeypatch):
    monkeypatch.setattr(stimuli, "fetch_stimulus", lambda _id: SAMPLE)
    with pytest.raises(ValueError):
        stimuli.stimulus_payload_for_condition("T-001", "C9")
