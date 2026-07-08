/**
 * google_apps_script.gs
 *
 * Backend for the BLE vignette experiment. Receives one POST per
 * participant containing the full STATE object from study.js and
 * writes it as a row to a Google Sheet.
 *
 * Setup (one-time):
 *   1. Open Google Drive -> New -> Google Sheets. Name it
 *      "BCM Vignette Responses".
 *   2. Inside that Sheet, Extensions -> Apps Script. Replace the
 *      default Code.gs with the contents of this file. Save.
 *   3. Deploy -> New deployment -> type "Web app".
 *      - Execute as: Me (your Google account)
 *      - Who has access: Anyone
 *      - Click Deploy. Copy the resulting URL.
 *   4. Paste the URL into BACKEND_URL in prototype/study.js.
 *   5. Test by running the study with ?pid=PILOT-001 and confirming
 *      a row appears in the Sheet.
 *
 * Schema (one column per field):
 *   ts_iso, pid, study_id, study_ver, condition, last_phase,
 *   started_at, submitted_at, completion_code, attention_pass,
 *   apps_assigned, per_app_json, posttask_json, pretask_json,
 *   events_json, user_agent
 */

function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents);
    const sheet = SpreadsheetApp.getActive().getSheetByName("responses")
                 || createSheet_();

    const row = [
      new Date().toISOString(),
      body.meta && body.meta.pid ? body.meta.pid : "",
      body.meta && body.meta.study_id ? body.meta.study_id : "",
      body.meta && body.meta.study_ver ? body.meta.study_ver : "",
      body.condition || "",
      body.meta && body.meta.last_phase ? body.meta.last_phase : "",
      body.meta && body.meta.started_at ? new Date(body.meta.started_at).toISOString() : "",
      new Date().toISOString(),
      body.completion_code || "",
      body.attention && body.attention.pass ? "pass" : "fail",
      (body.apps || []).map(function (a) { return a.id; }).join(","),
      JSON.stringify(body.per_app || {}),
      JSON.stringify(body.posttask || {}),
      JSON.stringify(body.pretask || {}),
      JSON.stringify(body.events || []),
      body.meta && body.meta.user_agent ? body.meta.user_agent : ""
    ];
    sheet.appendRow(row);

    return ContentService
      .createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  // Health check — open the URL in a browser to see "OK".
  return ContentService
    .createTextOutput("OK — BCM vignette backend is alive")
    .setMimeType(ContentService.MimeType.TEXT);
}

function createSheet_() {
  const ss = SpreadsheetApp.getActive();
  const sh = ss.insertSheet("responses");
  sh.appendRow([
    "ts_iso", "pid", "study_id", "study_ver", "condition", "last_phase",
    "started_at", "submitted_at", "completion_code", "attention_pass",
    "apps_assigned", "per_app_json", "posttask_json", "pretask_json",
    "events_json", "user_agent"
  ]);
  sh.getRange(1, 1, 1, 16).setFontWeight("bold");
  sh.setFrozenRows(1);
  return sh;
}
