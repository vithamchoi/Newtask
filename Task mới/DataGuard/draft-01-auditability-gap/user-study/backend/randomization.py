"""Counterbalancing and stimulus sampling.

We use a 3x3 Latin square for condition order and a stratified random sample
of 8 stimulus apps per stratum (S1 / S2 / S3). The condition slot a stimulus
falls into is rotated through the Latin square so that across participants
each (app, condition) cell is filled approximately equally.
"""

from __future__ import annotations
import random
from dataclasses import dataclass
from typing import List

CONDITIONS = ("C0", "C1", "C2")

# Three Latin squares of order 3 cover all six row orderings (full set).
LATIN_SQUARES = [
    [("C0","C1","C2"), ("C1","C2","C0"), ("C2","C0","C1")],
    [("C0","C2","C1"), ("C2","C1","C0"), ("C1","C0","C2")],
]


def assign_condition_order(participant_index: int) -> tuple[str, str, str]:
    """Return the (block1, block2, block3) condition order for this participant."""
    square = LATIN_SQUARES[participant_index // 3 % len(LATIN_SQUARES)]
    return square[participant_index % 3]


@dataclass
class Trial:
    app_id: str
    stratum: str
    condition: str
    trial_order: int


def build_trial_sequence(
    stimuli_by_stratum: dict[str, list[str]],
    condition_order: tuple[str, str, str],
    rng: random.Random,
    apps_per_stratum_per_block: int = 3,    # 3 strata x 3 = 9 ... use 8 (see below)
) -> list[Trial]:
    """Construct the 24-trial sequence.

    8 apps per block x 3 blocks = 24 trials. Within each block we balance
    strata as evenly as possible (3 S1, 3 S2, 2 S3 rotating). Apps assigned
    to a block are not re-shown in another block (within-participant).
    """
    # Pull copies so we can mutate
    pools = {k: rng.sample(v, len(v)) for k, v in stimuli_by_stratum.items()}
    trials: list[Trial] = []
    order = 1
    # We want 8 apps per block. Use a 3/3/2 stratum mix per block;
    # rotate the "extra" each block so S3 also gets 3 in one of the blocks.
    block_mixes = [(3,3,2), (3,2,3), (2,3,3)]
    for block_idx, cond in enumerate(condition_order):
        n_s1, n_s2, n_s3 = block_mixes[block_idx]
        block_apps: list[tuple[str, str]] = []
        for stratum, n in (("S1", n_s1), ("S2", n_s2), ("S3", n_s3)):
            for _ in range(n):
                if not pools[stratum]:
                    raise RuntimeError(f"stratum {stratum} pool exhausted")
                block_apps.append((pools[stratum].pop(), stratum))
        rng.shuffle(block_apps)
        for app_id, stratum in block_apps:
            trials.append(Trial(app_id=app_id, stratum=stratum, condition=cond, trial_order=order))
            order += 1
    return trials


def build_feedback_sequence(
    stimuli_by_stratum: dict[str, list[str]],
    condition_order: tuple[str, str, str],
    rng: random.Random,
) -> list[Trial]:
    """Construct a short sequence for expert-feedback deployments.

    The controlled study requires 24 adjudicated stimuli. While the pool is
    still being built, this mode exposes each available stimulus once and
    rotates conditions through the Latin-square order. It is suitable for
    collecting formative expert feedback, not inferential analysis.
    """
    candidates: list[tuple[str, str]] = []
    for stratum in sorted(stimuli_by_stratum):
        for app_id in stimuli_by_stratum[stratum]:
            candidates.append((app_id, stratum))
    rng.shuffle(candidates)

    trials: list[Trial] = []
    for idx, (app_id, stratum) in enumerate(candidates):
        trials.append(Trial(
            app_id=app_id,
            stratum=stratum,
            condition=condition_order[idx % len(condition_order)],
            trial_order=idx + 1,
        ))
    return trials


def all_assignments_valid(seq: list[Trial]) -> bool:
    """Sanity: 24 unique apps; 3 conditions x 8 trials each."""
    if len(seq) != 24: return False
    if len({t.app_id for t in seq}) != 24: return False
    from collections import Counter
    cond_count = Counter(t.condition for t in seq)
    return all(cond_count[c] == 8 for c in CONDITIONS)
