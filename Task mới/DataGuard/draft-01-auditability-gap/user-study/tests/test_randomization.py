"""Tests for the Latin-square + stratified-block randomizer."""
import random
import pytest

from backend.randomization import (
    assign_condition_order, build_trial_sequence, all_assignments_valid,
    CONDITIONS,
)


def test_condition_order_covers_three_distinct():
    seen = set()
    for i in range(12):
        seen.add(assign_condition_order(i))
    # We expect at least all 3 cyclic rotations + their mirror
    assert len(seen) >= 3


def test_trial_sequence_24_trials():
    pools = {"S1": [f"s1-{i}" for i in range(8)],
             "S2": [f"s2-{i}" for i in range(8)],
             "S3": [f"s3-{i}" for i in range(8)]}
    rng = random.Random(42)
    seq = build_trial_sequence(pools, ("C0","C1","C2"), rng)
    assert all_assignments_valid(seq)
    # 24 unique apps
    apps = {t.app_id for t in seq}
    assert len(apps) == 24


def test_trial_sequence_balanced_strata_per_session():
    pools = {"S1": [f"s1-{i}" for i in range(8)],
             "S2": [f"s2-{i}" for i in range(8)],
             "S3": [f"s3-{i}" for i in range(8)]}
    rng = random.Random(0)
    seq = build_trial_sequence(pools, ("C0","C1","C2"), rng)
    counts = {"S1": 0, "S2": 0, "S3": 0}
    for t in seq:
        counts[t.stratum] += 1
    # 3+3+2, 3+2+3, 2+3+3 -> 8+8+8
    assert counts["S1"] == 8
    assert counts["S2"] == 8
    assert counts["S3"] == 8


def test_each_condition_has_8_trials():
    pools = {"S1": [f"s1-{i}" for i in range(8)],
             "S2": [f"s2-{i}" for i in range(8)],
             "S3": [f"s3-{i}" for i in range(8)]}
    seq = build_trial_sequence(pools, ("C1","C2","C0"), random.Random(7))
    from collections import Counter
    counts = Counter(t.condition for t in seq)
    for c in CONDITIONS:
        assert counts[c] == 8
