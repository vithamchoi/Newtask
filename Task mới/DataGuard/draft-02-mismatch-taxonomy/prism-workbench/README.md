# PRISM workbench MVP

Tóm tắt: workbench cho user-study Phương án A (IJHCS Draft 2). Hai builds — *legacy* và *prism* — chạy cùng Flask backend, log mọi event vào SQLite, có NASA-TLX + exit-interview tích hợp sẵn.

## Setup (one-time)

```bash
pip install -r requirements.txt
python build_stimuli.py          # produces data/stimuli.json from data-labels.xlsx
```

`build_stimuli.py` stratifies the 1,213 parseable policy–label pairs into the four prevalence/ambiguity quadrants from §3.1 of the user-study plan and picks 10 apps from each quadrant. The first 5 apps in the output are flagged `is_tutorial=True`.

## Run

```bash
python app.py
# Open http://localhost:5000/?build=legacy
# Open http://localhost:5000/?build=prism
```

If the workbench is deployed on the RMIT secure server, the recommended invocation is:

```bash
PRISM_DB_PATH=/var/lib/prism/sessions.db \
PRISM_SECRET=<random-32-bytes>          \
PRISM_EXPORT_TOKEN=<random-32-bytes>    \
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Endpoints

| Path | Method | Purpose |
|---|---|---|
| `/?build=legacy\|prism` | GET | Audit task front-end |
| `/tlx` | GET | NASA-TLX form after each 20-app block |
| `/exit` | GET | Five-question exit interview |
| `/api/session` | GET | Returns the participant's UUID, build, role-arm, total |
| `/api/next-app` | GET | Next stimulus + lexicon hits + third-party recipients (PRISM only renders them) |
| `/api/submit-verdict` | POST | Records 4 radio verdicts + rationale + time-on-app |
| `/api/click-panel` | POST | Click-stream events (which D-affordance was used) |
| `/api/tlx` | POST | NASA-TLX 6-subscale scores per block |
| `/api/exit` | POST | Five exit-interview answers |
| `/api/export.csv?token=…` | GET | Researcher CSV export of all events (token-protected) |

## Data captured per session

All data is pseudonymous. `participant_id` is a server-assigned 12-char hex; no name, no email, no IP is recorded.

| Table | Columns |
|---|---|
| `session_log` | `participant_id, role_arm, build, app_id, event_type, payload_json, ts_ms` |

Event types: `start_app`, `submit_verdict`, `click_panel`, `tlx_submit`, `exit_submit`.

## D1–D8 affordances in the PRISM build

| Affordance | What it does | Code path |
|---|---|---|
| D1 Third-party recipient panel | Lists recipients extracted from policy with linked/unlinked markers | `_extract_third_parties` in `app.py` |
| D2 Identifier-to-category map | Tooltip on `Device or other IDs` row (added in `index.html` for prism build) | `index.html` |
| D3 Hedge highlighter | `<mark class="M3">` around M3-lexicon spans | server-side `lexicon_hits` |
| D4 No-data audit prompt | Red banner when M4 fires AND M1/M2 fires | `renderAlertM4` in `index.html` |
| D5 Location-grain overlay | Chip with detected grain on Location DS row | `index.html` (PRISM CSS) |
| D6 Security/Data tab | Security rows in their own `<fieldset>` | `renderSecurity` in `index.html` |
| D7 Responsibility-scope chip | Orange chip when M7 fires | `index.html` |
| D8 Ambiguity badge bar | Bottom bar with M6 / M1 / M4 / M5 / M3 ambiguity percentages from the paper; M2 & M7 shown as "not observed" | `renderBadgeBar` in `index.html` |

## File map

```
prism-workbench/
├── app.py                 # Flask backend, all endpoints, server-side lexicon
├── build_stimuli.py       # one-shot script that produces data/stimuli.json
├── requirements.txt       # Flask, pandas, openpyxl
├── README.md              # this file
├── data/
│   └── stimuli.json       # 40 stratified apps (10 per quadrant)
├── static/
│   ├── index.html         # legacy + prism builds (CSS toggled by ?build=)
│   ├── tlx.html           # NASA-TLX 6-subscale form
│   └── exit.html          # 5-question exit interview
└── sessions.db            # SQLite event log (created at first run)
```

## Privacy notice

The workbench logs:
- A pseudonymous UUID-style `participant_id`
- The build (`legacy` or `prism`) the participant was assigned
- Each app the participant audits, the verdict, and the rationale text
- NASA-TLX block scores and exit-interview answers
- Click events on the D1/D4/D6/D7/D8 affordances (for click-stream analysis)

The workbench does NOT log:
- Participant name, email, IP, user-agent
- Any identifying field

Data is retained on RMIT secure storage for 7 years per HREC policy and then permanently deleted.
