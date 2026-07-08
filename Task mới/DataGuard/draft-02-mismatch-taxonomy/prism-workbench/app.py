# PRISM Workbench MVP — Flask single-file backend.
# Tom tat: May chu Flask phuc vu ban Legacy va PRISM, ghi nhat ky vao SQLite.
#
# Run:  pip install -r requirements.txt && python app.py
# Open: http://localhost:5000/?build=legacy  or  http://localhost:5000/?build=prism
#
# The 7-code lexicon (M1..M7) is server-side; UI affordances D1..D8 consume the
# server-evaluated hits. No participant-identifying fields are logged; the
# participant_id is a server-assigned UUID stored only in a session cookie.

import json
import os
import re
import sqlite3
import time
import uuid
from pathlib import Path

from flask import (
    Flask,
    g,
    jsonify,
    redirect,
    request,
    send_from_directory,
    session,
    url_for,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
STATIC_DIR = ROOT / "static"
DATA_DIR = ROOT / "data"
DB_PATH = Path(os.environ.get("PRISM_DB_PATH", str(ROOT / "sessions.db")))
STIMULI_PATH = DATA_DIR / "stimuli.json"

# Verified ambiguity values from the paper (Sec.~5).
# M2 and M7 were not observed in the doubly-annotated subset.
AMBIGUITY = {
    "M1": 80.0,
    "M2": None,
    "M3": 60.0,
    "M4": 70.0,
    "M5": 66.7,
    "M6": 84.6,
    "M7": None,
}

app = Flask(
    __name__,
    static_folder=str(STATIC_DIR),
    static_url_path="/static",
)
app.secret_key = os.environ.get("PRISM_SECRET", "prism-workbench-dev-key")


# ---------------------------------------------------------------------------
# Lexicon — high-recall regex anchors for the 7 PRISM codes.
# Mirrors the canonical lexicon in Sec.~4 of the master plan.
# ---------------------------------------------------------------------------
LEXICON = {
    # M1 third-party flow shadowing
    "M1": [
        r"\bthird[- ]part(?:y|ies)\b",
        r"\bservice provider(?:s)?\b",
        r"\bshar(?:e|ed|es|ing) (?:with|to)\b",
        r"\baffiliate(?:s)?\b",
        r"\bvendor(?:s)?\b",
        r"\bsubsidiar(?:y|ies)\b",
        r"\b(?:advertising|ad) (?:network|partner)s?\b",
        r"\banalytics provider(?:s)?\b",
    ],
    # M2 identifier-category misalignment
    "M2": [
        r"\bdevice (?:id|identifier)s?\b",
        r"\badvertising (?:id|identifier)s?\b",
        r"\baaid\b|\bidfa\b|\bgaid\b|\bandroid id\b",
        r"\bmac address\b|\bimei\b",
        r"\bunique (?:device )?identifier(?:s)?\b",
        r"\bpersistent identifier(?:s)?\b",
    ],
    # M3 generic-hedge underspecification
    "M3": [
        r"\bmay\b",
        r"\bmight\b",
        r"\bsuch as\b",
        r"\bfor example\b",
        r"\bincluding but not limited to\b",
        r"\bcertain\b",
        r"\bsome\b",
        r"\bvarious\b",
        r"\bfrom time to time\b",
        r"\bas (?:necessary|needed|appropriate|required)\b",
    ],
    # M4 no-data overclaim
    "M4": [
        r"\bwe (?:do not|don't) (?:collect|share|sell)\b",
        r"\bno (?:personal )?(?:data|information) (?:is )?collect(?:ed)?\b",
        r"\bdoes not (?:collect|share|sell)\b",
        r"\bwithout (?:collecting|storing)\b",
    ],
    # M5 location-grain mismatch
    "M5": [
        r"\b(?:approximate|coarse|city[- ]?level|region[- ]?level) location\b",
        r"\b(?:precise|fine[- ]?grained|gps|exact) location\b",
        r"\bip[- ]?(?:address|derived) location\b",
        r"\bgeoloca(?:tion|ted)\b",
        r"\blatitude\b|\blongitude\b",
    ],
    # M6 security-control / data-type confusion
    "M6": [
        r"\bencrypt(?:ed|ion|s)?\b",
        r"\btls\b|\bssl\b|\bhttps\b",
        r"\bin transit\b|\bat rest\b",
        r"\bsecure (?:server|storage|transmission)\b",
        r"\bhash(?:ed|ing)?\b",
        r"\b(?:industry|reasonable) (?:standard )?security\b",
    ],
    # M7 boundary-of-responsibility mismatch
    "M7": [
        r"\bnot responsible for\b",
        r"\bgoverned by (?:their|the third[- ]party)\b",
        r"\bsubject to (?:their|the third[- ]party) privacy polic(?:y|ies)\b",
        r"\bwe (?:have )?(?:no|do not have) control\b",
        r"\bplease (?:refer to|review) (?:their|the third[- ]party)\b",
    ],
}

COMPILED = {
    code: [re.compile(p, re.IGNORECASE) for p in patterns]
    for code, patterns in LEXICON.items()
}


def lexicon_hits(text):
    """Return {code: [{'start': int, 'end': int, 'match': str}, ...]} for text."""
    out = {code: [] for code in LEXICON}
    if not text:
        return out
    for code, regs in COMPILED.items():
        for r in regs:
            for m in r.finditer(text):
                out[code].append(
                    {"start": m.start(), "end": m.end(), "match": m.group(0)}
                )
    return out


def code_set(hits):
    return {c for c, h in hits.items() if h}


# ---------------------------------------------------------------------------
# SQLite logging
# ---------------------------------------------------------------------------
SCHEMA = """
CREATE TABLE IF NOT EXISTS session_log (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    participant_id  TEXT NOT NULL,
    role_arm        TEXT,
    build           TEXT,
    app_id          INTEGER,
    event_type      TEXT NOT NULL,
    payload_json    TEXT,
    ts_ms           INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_session_participant
    ON session_log(participant_id);
"""


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(str(DB_PATH))
        g.db.row_factory = sqlite3.Row
        g.db.executescript(SCHEMA)
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def log_event(participant_id, role_arm, build, app_id, event_type, payload):
    db = get_db()
    db.execute(
        "INSERT INTO session_log "
        "(participant_id, role_arm, build, app_id, event_type, payload_json, ts_ms)"
        " VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            participant_id,
            role_arm,
            build,
            app_id,
            event_type,
            json.dumps(payload, ensure_ascii=False),
            int(time.time() * 1000),
        ),
    )
    db.commit()


# ---------------------------------------------------------------------------
# Stimuli loading
# ---------------------------------------------------------------------------
def load_stimuli():
    if not STIMULI_PATH.exists():
        return []
    return json.loads(STIMULI_PATH.read_text(encoding="utf-8"))


STIMULI = load_stimuli()


# ---------------------------------------------------------------------------
# Participant id assignment
# ---------------------------------------------------------------------------
def ensure_participant():
    if "pid" not in session:
        session["pid"] = uuid.uuid4().hex[:12]
        session["index"] = 0
        session["build"] = request.args.get("build", "legacy")
        session["role_arm"] = request.args.get("arm", "A")
    return session["pid"]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    ensure_participant()
    # Allow ?build=legacy or ?build=prism to override stored build.
    build = request.args.get("build")
    if build in {"legacy", "prism"}:
        session["build"] = build
    return send_from_directory(str(STATIC_DIR), "index.html")


@app.route("/tlx")
def tlx_page():
    ensure_participant()
    return send_from_directory(str(STATIC_DIR), "tlx.html")


@app.route("/exit")
def exit_page():
    ensure_participant()
    return send_from_directory(str(STATIC_DIR), "exit.html")


@app.route("/api/session")
def api_session():
    pid = ensure_participant()
    return jsonify(
        {
            "participant_id": pid,
            "build": session.get("build", "legacy"),
            "role_arm": session.get("role_arm", "A"),
            "index": session.get("index", 0),
            "total": len(STIMULI),
            "ambiguity": AMBIGUITY,
        }
    )


_THIRD_PARTY_NAMES = [
    "Crashlytics", "Firebase Analytics", "Firebase",
    "Google AdMob", "AdMob", "Google Analytics", "Facebook SDK",
    "Facebook", "Unity Ads", "MoPub", "AppsFlyer", "Branch", "Adjust",
    "Mixpanel", "Amplitude", "Segment", "Flurry", "OneSignal",
    "Sentry", "Bugsnag", "Stripe", "PayPal", "Twilio",
]


def _parse_data_safety(raw: str) -> list[dict]:
    """Convert the raw Data-Safety dict-like string into a list of rows."""
    if not raw:
        return []
    out = []
    # Try to interpret as a Python dict literal first.
    try:
        import ast
        d = ast.literal_eval(raw) if isinstance(raw, str) else raw
        if isinstance(d, dict):
            for kind, items in [("Shared", d.get("data_shared", [])),
                                ("Collected", d.get("data_collected", [])),
                                ("Security", d.get("security_practices", []))]:
                if not items:
                    if kind in ("Shared", "Collected"):
                        out.append({"row": kind, "value": "(none)"})
                    continue
                for it in items:
                    name = it.get("category", "?") if isinstance(it, dict) else str(it)
                    out.append({"row": kind, "value": name})
            return out
    except (ValueError, SyntaxError, TypeError):
        pass
    # Fallback: dump raw text as one row
    return [{"row": "Data Safety (raw)", "value": str(raw)[:400]}]


def _extract_third_parties(text: str) -> list[dict]:
    if not text:
        return []
    lower = text.lower()
    seen = []
    for name in _THIRD_PARTY_NAMES:
        if name.lower() in lower:
            seen.append({"name": name, "linked": False})
    return seen


@app.route("/api/next-app")
def api_next_app():
    pid = ensure_participant()
    idx = session.get("index", 0)
    if idx >= len(STIMULI):
        return jsonify({"done": True})
    raw_stim = STIMULI[idx]
    pol = raw_stim.get("policy_excerpt", "")
    hits = lexicon_hits(pol)
    stim = {
        "app_id":         raw_stim.get("app_id"),
        "app_name":       raw_stim.get("name") or raw_stim.get("app_name"),
        "category":       raw_stim.get("category"),
        "quadrant":       raw_stim.get("quadrant"),
        "is_tutorial":    bool(raw_stim.get("is_tutorial")),
        "expected_codes": raw_stim.get("expected_codes", []),
        "policy_excerpt": pol,
        "data_safety":    _parse_data_safety(raw_stim.get("data_safety_raw", "")),
        "third_parties":  _extract_third_parties(pol),
        "lexicon_hits":   hits,
        "codes_fired":    sorted(code_set(hits)),
        "index":          idx,
        "build":          session.get("build", "legacy"),
    }
    log_event(pid, session.get("role_arm"), session.get("build"),
              stim["app_id"], "start_app", {"index": idx})
    return jsonify(stim)


@app.route("/api/submit-verdict", methods=["POST"])
def api_submit_verdict():
    pid = ensure_participant()
    data = request.get_json(force=True)
    log_event(
        pid,
        session.get("role_arm"),
        session.get("build"),
        data.get("app_id"),
        "submit_verdict",
        data,
    )
    session["index"] = session.get("index", 0) + 1
    next_index = session["index"]
    block_size = 20
    # After 20-app block, route to TLX.
    if next_index in (block_size, 2 * block_size):
        return jsonify({"next": "tlx", "index": next_index})
    if next_index >= len(STIMULI):
        return jsonify({"next": "exit", "index": next_index})
    return jsonify({"next": "app", "index": next_index})


@app.route("/api/click-panel", methods=["POST"])
def api_click_panel():
    pid = ensure_participant()
    data = request.get_json(force=True)
    log_event(pid, session.get("role_arm"), session.get("build"),
              data.get("app_id"), "click_panel", data)
    return jsonify({"ok": True})


@app.route("/api/lexicon-hits", methods=["POST"])
def api_lexicon_hits():
    """Ad-hoc lexicon endpoint (text in, hits out)."""
    data = request.get_json(force=True)
    text = data.get("text", "")
    hits = lexicon_hits(text)
    return jsonify(
        {"hits": hits, "codes_fired": sorted(code_set(hits)),
         "ambiguity": AMBIGUITY}
    )


@app.route("/api/tlx", methods=["POST"])
def api_tlx():
    pid = ensure_participant()
    data = request.get_json(force=True)
    log_event(pid, session.get("role_arm"), session.get("build"),
              None, "tlx_submit", data)
    return jsonify({"ok": True})


@app.route("/api/exit", methods=["POST"])
def api_exit():
    pid = ensure_participant()
    data = request.get_json(force=True)
    log_event(pid, session.get("role_arm"), session.get("build"),
              None, "exit_submit", data)
    return jsonify({"ok": True})


@app.route("/api/export.csv")
def api_export():
    """Researcher endpoint — full event log as CSV (no identifying fields)."""
    db = get_db()
    rows = db.execute(
        "SELECT participant_id, role_arm, build, app_id, event_type,"
        "       payload_json, ts_ms FROM session_log ORDER BY ts_ms ASC"
    ).fetchall()
    out = ["participant_id,role_arm,build,app_id,event_type,payload_json,ts_ms"]
    for r in rows:
        payload = (r["payload_json"] or "").replace("\n", " ").replace('"', '""')
        out.append(
            f'{r["participant_id"]},{r["role_arm"] or ""},{r["build"] or ""},'
            f'{r["app_id"] or ""},{r["event_type"]},"{payload}",{r["ts_ms"]}'
        )
    return "\n".join(out), 200, {"Content-Type": "text/csv; charset=utf-8"}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    DATA_DIR.mkdir(exist_ok=True)
    STATIC_DIR.mkdir(exist_ok=True)
    print(f"PRISM workbench running. Stimuli loaded: {len(STIMULI)}.")
    print("Open: http://localhost:5000/?build=legacy  or  ?build=prism")
    app.run(host="0.0.0.0", port=5000, debug=False)
