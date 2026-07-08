# Codebook

Variable definitions for the DataGuard user-study data files.

## participants.csv

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| `pid` | string | UUID4 | Random participant ID |
| `consent_ts` | datetime | ISO8601 | Consent timestamp |
| `age_band` | enum | 18-24 / 25-34 / 35-44 / 45-54 / 55+ | Self-reported |
| `english_self` | int | 1-5 | College reading self-rating |
| `android_use` | enum | daily / weekly / monthly / rarely / never | Frequency |
| `policy_read` | enum | always / sometimes / rarely / never | Self-reported |
| `developer_exp` | bool | true/false | Has worked in app dev/relations |
| `tutorial_pass` | bool | true/false | Passed comprehension check |
| `condition_order` | string | e.g. "C0,C1,C2" | Latin-square assignment |
| `session_status` | enum | started / complete / withdrawn / excluded | End state |
| `excluded_reason` | string | free text | If excluded |

## trials.csv

| Variable | Type | Description |
|----------|------|-------------|
| `trial_id` | string | UUID4 |
| `pid` | string | Participant ID |
| `condition` | enum {C0, C1, C2} | Condition assigned to this trial |
| `app_id` | string | Stimulus app identifier |
| `stratum` | enum {S1, S2, S3} | Stimulus stratum (S1 high-conf, S2 high-disagree, S3 no-data) |
| `trial_order` | int | 1–24 trial position within session |
| `t_open` | datetime | When trial loaded |
| `t_submit` | datetime | When trial submitted |
| `rt_ms` | int | t_submit − t_open in ms |
| `j_share_corr` | enum {Correct, Incorrect, Ambig, blank} | Sharing correctness verdict |
| `j_share_comp` | enum {Complete, Incomplete, Ambig, blank} | Sharing completeness verdict |
| `j_coll_corr` | enum {Correct, Incorrect, Ambig, blank} | Collection correctness verdict |
| `j_coll_comp` | enum {Complete, Incomplete, Ambig, blank} | Collection completeness verdict |
| `conf_share_corr` | int 0–100 | Self-reported confidence (slider) |
| `conf_share_comp` | int 0–100 | |
| `conf_coll_corr` | int 0–100 | |
| `conf_coll_comp` | int 0–100 | |
| `rationale` | text | Free-text reasoning |
| `evidence_paste` | text | Verbatim policy passage used |
| `ai_suggestion_accepted` | bool / null | C2 only: did the participant accept the AI's suggestion as-is on any axis? |
| `ai_overridden_axes` | int 0–4 / null | C2 only: number of axes where participant changed the AI suggestion |

## gold.csv

| Variable | Type | Description |
|----------|------|-------------|
| `app_id` | string | Stimulus identifier |
| `g_share_corr` | enum {Supported, Contradicted, Omitted, Insufficient} | Adjudicated gold for sharing correctness |
| `g_share_comp` | enum {...} | Same for completeness |
| `g_coll_corr` | enum {...} | |
| `g_coll_comp` | enum {...} | |
| `coder_a` | string | Coder ID, axis A |
| `coder_b` | string | Coder ID, axis B |
| `kappa_pre_consensus` | float | Pre-consensus κ on this app |

## tlx.csv

NASA-TLX captured per condition-block (3 rows per participant).

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| `pid` | string | UUID4 | |
| `condition` | enum {C0, C1, C2} | | |
| `mental` | int | 0–100 | Mental demand |
| `physical` | int | 0–100 | Physical demand |
| `temporal` | int | 0–100 | Temporal demand |
| `performance` | int | 0–100 | Self-rated performance (reverse-scored) |
| `effort` | int | 0–100 | Effort |
| `frustration` | int | 0–100 | Frustration |
| `tlx_global` | float | 0–100 | Unweighted mean |

## trust.csv

TPA-derived trust scale, captured after the C2 block only.

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| `pid` | string | UUID4 | |
| `t1_reliable` | int | 1–7 | "The AI suggestions were reliable." |
| `t2_evidence` | int | 1–7 | "The highlighted evidence helped me verify the suggested label." |
| `t3_overrely` | int | 1–7 (reverse) | "I sometimes accepted the AI suggestion without checking." |
| `t4_intent` | int | 1–7 | "I would use this AI assistant for real privacy reviews." |
| `t5_understand` | int | 1–7 | "I understood why the AI made its suggestions." |
| `trust_global` | float | 1–7 | Mean (t3 reverse-scored) |

## Derived per-trial measures (in processed data only)

| Variable | Type | Description |
|----------|------|-------------|
| `acc_share_corr` | int 0/1 | Trial-axis correctness vs gold (Supported→Correct, Contradicted→Incorrect, etc.) |
| `acc_share_comp` | int 0/1 | |
| `acc_coll_corr` | int 0/1 | |
| `acc_coll_comp` | int 0/1 | |
| `acc_total` | int 0–4 | Per-trial sum of axis correctness |
| `brier_share_corr` | float 0–1 | (confidence/100 − accuracy)² |
| `brier_total` | float 0–1 | Mean Brier across four axes |
| `rt_log` | float | log(rt_ms) |
