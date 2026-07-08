"""Flask backend for the DataGuard user study.

Endpoints (all JSON unless noted):
    GET  /                          static landing page
    POST /api/consent               create participant, return pid + sequence
    POST /api/demographics          submit demographics
    POST /api/tutorial              record tutorial pass/fail
    GET  /api/next_trial?pid=...    next trial payload (sequence-aware)
    POST /api/submit_trial          submit a trial response
    POST /api/submit_tlx            submit NASA-TLX for a condition block
    POST /api/submit_trust          submit TPA trust scale (after C2)
    POST /api/submit_feedback       submit formative expert feedback
    POST /api/finish                mark session complete
    GET  /api/export?token=...      admin: export full results as CSV bundle

Run:
    flask --app backend.app run --debug
"""

from __future__ import annotations
import datetime as dt
import json
import os
import random
import uuid
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from . import db, randomization, stimuli

STUDY_ROOT = Path(__file__).parent.parent

app = Flask(__name__, static_folder=str(STUDY_ROOT / "frontend"), static_url_path="/")
cors_origins = os.environ.get("DATAGUARD_CORS_ORIGINS", "*")
CORS(app, resources={r"/api/*": {"origins": cors_origins.split(",") if cors_origins != "*" else "*"}})

ADMIN_TOKEN = os.environ.get("DATAGUARD_ADMIN_TOKEN")
STUDY_MODE = os.environ.get("DATAGUARD_STUDY_MODE", "feedback").strip().lower()


def now_iso() -> str:
    return dt.datetime.utcnow().isoformat(timespec="seconds")


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/consent")
def consent():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/healthz")
def healthz():
    return jsonify({"ok": True, "mode": STUDY_MODE})


@app.route("/ETHICS_CONSENT.md")
def ethics_consent():
    return send_from_directory(STUDY_ROOT, "ETHICS_CONSENT.md", mimetype="text/markdown")


@app.route("/DEBRIEF.md")
def debrief():
    return send_from_directory(STUDY_ROOT, "DEBRIEF.md", mimetype="text/markdown")


# --------------- Consent & assignment ---------------

@app.post("/api/consent")
def api_consent():
    payload = request.get_json(force=True) or {}
    if not payload.get("agree"):
        return jsonify({"error": "consent required"}), 400
    pid = str(uuid.uuid4())
    # Assign condition order based on count of existing participants
    with db.get_conn() as c:
        n_existing = c.execute("SELECT COUNT(*) AS n FROM participants").fetchone()["n"]
    cond_order = randomization.assign_condition_order(n_existing)
    db.create_participant(pid, now_iso(), ",".join(cond_order))
    # Build trial sequence
    pools = stimuli.list_stimuli_by_stratum()
    rng = random.Random(pid)
    if STUDY_MODE == "controlled":
        seq = randomization.build_trial_sequence(pools, cond_order, rng)
        if not randomization.all_assignments_valid(seq):
            return jsonify({"error": "controlled study requires 24 loaded stimuli"}), 500
    else:
        seq = randomization.build_feedback_sequence(pools, cond_order, rng)
        if not seq:
            return jsonify({"error": "no stimuli loaded"}), 500
    # Insert trial stubs (open / submit timestamps filled later)
    for t in seq:
        db.insert_trial({
            "trial_id":   str(uuid.uuid4()),
            "pid":        pid,
            "condition":  t.condition,
            "app_id":     t.app_id,
            "stratum":    t.stratum,
            "trial_order": t.trial_order,
            "t_open":     "",
        })
    db.log_event(pid, "consent", {"condition_order": cond_order, "mode": STUDY_MODE})
    return jsonify({
        "pid": pid,
        "condition_order": cond_order,
        "n_trials": len(seq),
        "study_mode": STUDY_MODE,
    })


# --------------- Demographics & tutorial ---------------

@app.post("/api/demographics")
def api_demo():
    p = request.get_json(force=True) or {}
    pid = p.get("pid")
    if not pid:
        return jsonify({"error": "pid required"}), 400
    fields = {k: p.get(k) for k in (
        "age_band", "english_self", "android_use", "policy_read", "developer_exp"
    )}
    fields["developer_exp"] = int(bool(fields["developer_exp"]))
    db.update_demographics(pid, **fields)
    return jsonify({"ok": True})


@app.post("/api/tutorial")
def api_tutorial():
    p = request.get_json(force=True) or {}
    pid, passed = p.get("pid"), bool(p.get("passed"))
    if not pid:
        return jsonify({"error": "pid required"}), 400
    db.update_demographics(pid, tutorial_pass=int(passed))
    db.log_event(pid, "tutorial", {"passed": passed})
    return jsonify({"ok": True})


# --------------- Trial loop ---------------

@app.get("/api/next_trial")
def api_next_trial():
    pid = request.args.get("pid")
    if not pid:
        return jsonify({"error": "pid required"}), 400
    with db.get_conn() as c:
        row = c.execute(
            """SELECT trial_id, condition, app_id, stratum, trial_order
               FROM trials WHERE pid = ? AND t_submit IS NULL
               ORDER BY trial_order ASC LIMIT 1""",
            (pid,),
        ).fetchone()
    if not row:
        return jsonify({"done": True})
    payload = stimuli.stimulus_payload_for_condition(row["app_id"], row["condition"])
    db.update_trial(row["trial_id"], t_open=now_iso())
    with db.get_conn() as c:
        n_trials = c.execute("SELECT COUNT(*) AS n FROM trials WHERE pid = ?", (pid,)).fetchone()["n"]
    return jsonify({
        "trial_id":   row["trial_id"],
        "condition":  row["condition"],
        "stratum":    row["stratum"],
        "trial_order": row["trial_order"],
        "n_trials":   n_trials,
        "stimulus":   payload,
    })


@app.post("/api/submit_trial")
def api_submit_trial():
    p = request.get_json(force=True) or {}
    trial_id = p.get("trial_id")
    pid = p.get("pid")
    if not (trial_id and pid):
        return jsonify({"error": "trial_id + pid required"}), 400
    t_submit = now_iso()
    # Compute rt_ms server-side from t_open
    with db.get_conn() as c:
        r = c.execute("SELECT t_open FROM trials WHERE trial_id = ? AND pid = ?",
                      (trial_id, pid)).fetchone()
    if not r:
        return jsonify({"error": "trial not found"}), 404
    try:
        rt_ms = int(
            (dt.datetime.fromisoformat(t_submit) - dt.datetime.fromisoformat(r["t_open"]))
            .total_seconds() * 1000
        )
    except Exception:
        rt_ms = None
    fields = {
        "t_submit":      t_submit,
        "rt_ms":         rt_ms,
        "j_share_corr":  p.get("j_share_corr"),
        "j_share_comp":  p.get("j_share_comp"),
        "j_coll_corr":   p.get("j_coll_corr"),
        "j_coll_comp":   p.get("j_coll_comp"),
        "conf_share_corr": p.get("conf_share_corr"),
        "conf_share_comp": p.get("conf_share_comp"),
        "conf_coll_corr":  p.get("conf_coll_corr"),
        "conf_coll_comp":  p.get("conf_coll_comp"),
        "rationale":     (p.get("rationale") or "").strip(),
        "evidence_paste": (p.get("evidence_paste") or "").strip(),
        "ai_suggestion_accepted": _safe_int(p.get("ai_suggestion_accepted")),
        "ai_overridden_axes":     _safe_int(p.get("ai_overridden_axes")),
    }
    db.update_trial(trial_id, **fields)
    return jsonify({"ok": True, "rt_ms": rt_ms})


def _safe_int(v):
    if v is None: return None
    try: return int(v)
    except Exception: return None


# --------------- Instruments ---------------

@app.post("/api/submit_tlx")
def api_tlx():
    p = request.get_json(force=True) or {}
    pid = p.get("pid"); cond = p.get("condition")
    if not (pid and cond):
        return jsonify({"error": "pid + condition required"}), 400
    sub = {k: _safe_int(p.get(k)) for k in
           ("mental","physical","temporal","performance","effort","frustration")}
    scored = dict(sub)
    if scored.get("performance") is not None:
        scored["performance"] = 100 - scored["performance"]
    g = [v for v in scored.values() if v is not None]
    sub["tlx_global"] = round(sum(g)/len(g), 2) if g else None
    row = {"pid": pid, "condition": cond, **sub, "submitted_ts": now_iso()}
    db.insert_tlx(row)
    return jsonify({"ok": True, "tlx_global": row["tlx_global"]})


@app.post("/api/submit_trust")
def api_trust():
    p = request.get_json(force=True) or {}
    pid = p.get("pid")
    if not pid:
        return jsonify({"error": "pid required"}), 400
    items = {k: _safe_int(p.get(k)) for k in
             ("t1_reliable","t2_evidence","t3_overrely","t4_intent","t5_understand")}
    # t3 is reverse-scored
    vals = [items[k] if k != "t3_overrely" else (8 - items[k] if items[k] else None)
            for k in items]
    vals = [v for v in vals if v is not None]
    trust_global = round(sum(vals)/len(vals), 2) if vals else None
    row = {"pid": pid, **items, "trust_global": trust_global, "submitted_ts": now_iso()}
    db.insert_trust(row)
    return jsonify({"ok": True, "trust_global": trust_global})


@app.post("/api/submit_feedback")
def api_feedback():
    p = request.get_json(force=True) or {}
    pid = p.get("pid")
    if not pid:
        return jsonify({"error": "pid required"}), 400
    row = {
        "pid": pid,
        "role": (p.get("role") or "").strip(),
        "expertise": (p.get("expertise") or "").strip(),
        "usefulness": _safe_int(p.get("usefulness")),
        "preferred_condition": (p.get("preferred_condition") or "").strip(),
        "most_helpful": (p.get("most_helpful") or "").strip(),
        "most_confusing": (p.get("most_confusing") or "").strip(),
        "missing_feature": (p.get("missing_feature") or "").strip(),
        "concern": (p.get("concern") or "").strip(),
        "final_comment": (p.get("final_comment") or "").strip(),
        "submitted_ts": now_iso(),
    }
    db.insert_expert_feedback(row)
    db.log_event(pid, "expert_feedback", {"submitted": True})
    return jsonify({"ok": True})


@app.post("/api/finish")
def api_finish():
    p = request.get_json(force=True) or {}
    pid = p.get("pid")
    if not pid:
        return jsonify({"error": "pid required"}), 400
    db.update_demographics(pid, session_status="complete", finish_ts=now_iso())
    db.log_event(pid, "finish", {})
    return jsonify({"ok": True})


# --------------- Admin export ---------------

@app.get("/api/export")
def api_export():
    if not ADMIN_TOKEN or request.args.get("token") != ADMIN_TOKEN:
        return jsonify({"error": "unauthorised"}), 401
    with db.get_conn() as c:
        out = {
            "participants": [dict(r) for r in c.execute("SELECT * FROM participants")],
            "trials":       [dict(r) for r in c.execute("SELECT * FROM trials")],
            "tlx":          [dict(r) for r in c.execute("SELECT * FROM tlx")],
            "trust":        [dict(r) for r in c.execute("SELECT * FROM trust")],
            "expert_feedback": [dict(r) for r in c.execute("SELECT * FROM expert_feedback")],
        }
    return jsonify(out)


if __name__ == "__main__":
    db.init_db()
    app.run(debug=True)
