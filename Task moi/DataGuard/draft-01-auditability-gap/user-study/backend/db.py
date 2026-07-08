"""SQLite schema and accessors for the DataGuard user-study backend.

Tables:
    participants   one row per consented session
    trials         one row per (participant, app, condition) judgment
    tlx            one row per (participant, condition) NASA-TLX submission
    trust          one row per participant (after C2 only)
    expert_feedback one row per participant with formative study feedback
    stimuli        loaded stimulus pool with gold-standard labels
    audit_log      append-only event log for protocol-deviation auditing
"""

from __future__ import annotations
import argparse
import json
import os
import sqlite3
import uuid
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(os.environ.get("DATAGUARD_DB", "data/raw/study.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS participants (
    pid                TEXT PRIMARY KEY,
    consent_ts         TEXT NOT NULL,
    age_band           TEXT,
    english_self       INTEGER,
    android_use        TEXT,
    policy_read        TEXT,
    developer_exp      INTEGER,
    tutorial_pass      INTEGER DEFAULT 0,
    condition_order    TEXT,            -- comma-separated, e.g. "C0,C1,C2"
    session_status     TEXT DEFAULT 'started',
    excluded_reason    TEXT,
    finish_ts          TEXT
);

CREATE TABLE IF NOT EXISTS trials (
    trial_id           TEXT PRIMARY KEY,
    pid                TEXT NOT NULL,
    condition          TEXT NOT NULL,    -- C0 / C1 / C2
    app_id             TEXT NOT NULL,
    stratum            TEXT NOT NULL,    -- S1 / S2 / S3
    trial_order        INTEGER NOT NULL,
    t_open             TEXT NOT NULL,
    t_submit           TEXT,
    rt_ms              INTEGER,
    j_share_corr       TEXT,
    j_share_comp       TEXT,
    j_coll_corr        TEXT,
    j_coll_comp        TEXT,
    conf_share_corr    INTEGER,
    conf_share_comp    INTEGER,
    conf_coll_corr     INTEGER,
    conf_coll_comp     INTEGER,
    rationale          TEXT,
    evidence_paste     TEXT,
    ai_suggestion_accepted INTEGER,
    ai_overridden_axes INTEGER,
    FOREIGN KEY (pid) REFERENCES participants(pid)
);

CREATE TABLE IF NOT EXISTS tlx (
    pid          TEXT NOT NULL,
    condition    TEXT NOT NULL,
    mental       INTEGER,
    physical     INTEGER,
    temporal     INTEGER,
    performance  INTEGER,
    effort       INTEGER,
    frustration  INTEGER,
    tlx_global   REAL,
    submitted_ts TEXT,
    PRIMARY KEY (pid, condition),
    FOREIGN KEY (pid) REFERENCES participants(pid)
);

CREATE TABLE IF NOT EXISTS trust (
    pid          TEXT PRIMARY KEY,
    t1_reliable  INTEGER,
    t2_evidence  INTEGER,
    t3_overrely  INTEGER,
    t4_intent    INTEGER,
    t5_understand INTEGER,
    trust_global REAL,
    submitted_ts TEXT,
    FOREIGN KEY (pid) REFERENCES participants(pid)
);

CREATE TABLE IF NOT EXISTS expert_feedback (
    pid             TEXT PRIMARY KEY,
    role            TEXT,
    expertise       TEXT,
    usefulness      INTEGER,
    preferred_condition TEXT,
    most_helpful    TEXT,
    most_confusing  TEXT,
    missing_feature TEXT,
    concern         TEXT,
    final_comment   TEXT,
    submitted_ts    TEXT,
    FOREIGN KEY (pid) REFERENCES participants(pid)
);

CREATE TABLE IF NOT EXISTS stimuli (
    app_id         TEXT PRIMARY KEY,
    app_name       TEXT,
    category       TEXT,
    stratum        TEXT NOT NULL,
    play_url       TEXT,
    policy_url     TEXT,
    data_safety_json TEXT,          -- structured Data Safety
    policy_text    TEXT,            -- full policy
    section_share  TEXT,            -- extracted Data Share
    section_collect TEXT,           -- extracted Data Collect
    evidence_share TEXT,            -- evidence span(s) for C2 (JSON list)
    evidence_collect TEXT,
    ai_suggestion_json TEXT,        -- suggested verdicts + uncertainty for C2
    g_share_corr   TEXT,            -- gold (Supported/Contradicted/Omitted/Insufficient)
    g_share_comp   TEXT,
    g_coll_corr    TEXT,
    g_coll_comp    TEXT,
    kappa_pre_consensus REAL
);

CREATE TABLE IF NOT EXISTS audit_log (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    ts           TEXT NOT NULL,
    pid          TEXT,
    event_type   TEXT NOT NULL,
    payload      TEXT
);

CREATE INDEX IF NOT EXISTS idx_trials_pid ON trials(pid);
CREATE INDEX IF NOT EXISTS idx_trials_condition ON trials(condition);
CREATE INDEX IF NOT EXISTS idx_stimuli_stratum ON stimuli(stratum);
"""


def init_db(path: "Path | None" = None) -> None:
    # Resolve lazily so any override of DB_PATH after import wins.
    p = Path(path) if path is not None else DB_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(p) as conn:
        conn.executescript(SCHEMA)
        conn.commit()
    print(f"[db] initialised {p}")


@contextmanager
def get_conn(path: "Path | None" = None):
    # Resolve lazily on every call so the active DB_PATH wins.
    p = Path(path) if path is not None else DB_PATH
    conn = sqlite3.connect(p)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 5000")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ---------- Accessors ----------

def create_participant(pid: str, consent_ts: str, condition_order: str) -> None:
    with get_conn() as c:
        c.execute(
            "INSERT INTO participants (pid, consent_ts, condition_order) VALUES (?, ?, ?)",
            (pid, consent_ts, condition_order),
        )


def update_demographics(pid: str, **fields) -> None:
    keys = ", ".join(f"{k} = ?" for k in fields)
    vals = list(fields.values()) + [pid]
    with get_conn() as c:
        c.execute(f"UPDATE participants SET {keys} WHERE pid = ?", vals)


def insert_trial(row: dict) -> None:
    cols = ", ".join(row.keys())
    placeholders = ", ".join("?" for _ in row)
    with get_conn() as c:
        c.execute(f"INSERT INTO trials ({cols}) VALUES ({placeholders})", tuple(row.values()))


def update_trial(trial_id: str, **fields) -> None:
    keys = ", ".join(f"{k} = ?" for k in fields)
    vals = list(fields.values()) + [trial_id]
    with get_conn() as c:
        c.execute(f"UPDATE trials SET {keys} WHERE trial_id = ?", vals)


def insert_tlx(row: dict) -> None:
    cols = ", ".join(row.keys())
    placeholders = ", ".join("?" for _ in row)
    with get_conn() as c:
        c.execute(f"INSERT OR REPLACE INTO tlx ({cols}) VALUES ({placeholders})", tuple(row.values()))


def insert_trust(row: dict) -> None:
    cols = ", ".join(row.keys())
    placeholders = ", ".join("?" for _ in row)
    with get_conn() as c:
        c.execute(f"INSERT OR REPLACE INTO trust ({cols}) VALUES ({placeholders})", tuple(row.values()))


def insert_expert_feedback(row: dict) -> None:
    cols = ", ".join(row.keys())
    placeholders = ", ".join("?" for _ in row)
    with get_conn() as c:
        c.execute(
            f"INSERT OR REPLACE INTO expert_feedback ({cols}) VALUES ({placeholders})",
            tuple(row.values()),
        )


def load_stimulus_pool(json_path: Path) -> int:
    with open(json_path) as f:
        pool = json.load(f)
    n = 0
    with get_conn() as c:
        for app in pool:
            c.execute(
                """INSERT OR REPLACE INTO stimuli (
                    app_id, app_name, category, stratum,
                    play_url, policy_url,
                    data_safety_json, policy_text,
                    section_share, section_collect,
                    evidence_share, evidence_collect,
                    ai_suggestion_json,
                    g_share_corr, g_share_comp, g_coll_corr, g_coll_comp,
                    kappa_pre_consensus
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    app["app_id"], app.get("app_name"), app.get("category"),
                    app["stratum"], app.get("play_url"), app.get("policy_url"),
                    json.dumps(app.get("data_safety", {})),
                    app.get("policy_text", ""),
                    app.get("section_share", ""), app.get("section_collect", ""),
                    json.dumps(app.get("evidence_share", [])),
                    json.dumps(app.get("evidence_collect", [])),
                    json.dumps(app.get("ai_suggestion", {})),
                    app.get("gold", {}).get("share_corr"),
                    app.get("gold", {}).get("share_comp"),
                    app.get("gold", {}).get("coll_corr"),
                    app.get("gold", {}).get("coll_comp"),
                    app.get("kappa_pre_consensus"),
                ),
            )
            n += 1
    print(f"[db] loaded {n} stimulus apps")
    return n


def log_event(pid: str | None, event_type: str, payload: dict | None = None) -> None:
    import datetime as dt
    with get_conn() as c:
        c.execute(
            "INSERT INTO audit_log (ts, pid, event_type, payload) VALUES (?, ?, ?, ?)",
            (dt.datetime.utcnow().isoformat(timespec="seconds"), pid, event_type, json.dumps(payload or {})),
        )


# ---------- CLI ----------

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--init", action="store_true")
    p.add_argument("--load", metavar="PATH", help="Load stimulus pool JSON")
    args = p.parse_args()
    if args.init:
        init_db()
    if args.load:
        load_stimulus_pool(Path(args.load))


if __name__ == "__main__":
    main()
