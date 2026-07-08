"""Smoke tests for the Flask API end-to-end."""
import json
import tempfile
import os
from pathlib import Path

import pytest


@pytest.fixture
def app(tmp_path, monkeypatch):
    # Use a temporary SQLite file so tests don't touch real data
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATAGUARD_DB", str(db_path))
    # Force reimport so the module picks up the env var
    import importlib
    from backend import db as db_module
    importlib.reload(db_module)
    db_module.DB_PATH = db_path
    db_module.init_db(db_path)

    # Insert one stimulus per stratum
    for i, s in enumerate(["S1","S2","S3"]):
        for j in range(8):
            db_module.load_stimulus_pool  # noqa: just to silence unused
            with db_module.get_conn() as c:
                c.execute("""INSERT INTO stimuli (app_id,stratum,policy_text)
                             VALUES (?,?,?)""",
                          (f"{s}-{j:03d}", s, f"policy {s} {j}"))

    from backend import app as app_module
    importlib.reload(app_module)
    app_module.db.DB_PATH = db_path
    yield app_module.app


def test_consent_creates_participant(app):
    client = app.test_client()
    r = client.post("/api/consent", json={"agree": True})
    assert r.status_code == 200
    data = r.get_json()
    assert "pid" in data
    assert data["n_trials"] == 24


def test_consent_refused_without_agree(app):
    client = app.test_client()
    r = client.post("/api/consent", json={"agree": False})
    assert r.status_code == 400
