# Deploying the Apps Script backend

Goal: stand up a free, zero-server-cost endpoint that captures every
participant submission into a Google Sheet you control. The full
runtime is Google's; you don't need to manage anything.

## One-time setup

1. Sign in to the Google account that will own the data.
2. Open **Google Drive** → **New** → **Google Sheets**. Name the
   spreadsheet **"BCM Vignette Responses"**.
3. Inside the new spreadsheet, click **Extensions** → **Apps Script**.
   A code editor opens.
4. Delete the placeholder `function myFunction() { … }` and paste the
   full contents of `google_apps_script.gs` (in this folder).
5. Click **Save** (disk icon). Give the project a name (e.g. "BCM
   Vignette Backend").
6. Click **Deploy** → **New deployment**.
   - **Select type:** Web app.
   - **Description:** "BCM vignette v1.0".
   - **Execute as:** *Me (your-email@gmail.com)*.
   - **Who has access:** *Anyone*.
   - Click **Deploy**.
7. Google will ask for access permissions. Approve.
8. Copy the **Web app URL** that appears. It looks like
   `https://script.google.com/macros/s/AKfycb…/exec`.
9. Open `prototype/study.js`. Find the line:
   ```js
   const BACKEND_URL = ""; // ← set after deploying backend/...
   ```
   and paste the URL between the quotes.

## Verifying

- Open the URL itself in a browser. You should see the plain text
  "OK — BCM vignette backend is alive".
- Open `prototype/study.html?pid=PILOT-001` and complete the study.
- Open the spreadsheet. You should see one new row.

## Schema

Each submission appends one row with the columns documented at the
top of `google_apps_script.gs`. The free-text fields and the per-app
JSON are stored as JSON strings — the analysis pipeline unpacks them
into long-format CSV during cleaning.

## Quotas

Apps Script web apps have these limits relevant to us:
- **Triggers per user:** unlimited for `doPost`.
- **Execution time:** 6 minutes per call (we use < 1 s).
- **URL fetches:** not used by `doPost`.
- **Sheets append rate:** ~ 500 rows/sec (more than enough).

For a study of 200 participants, total throughput is trivially within
free-tier limits.

## Privacy notes

- The sheet contains the Prolific ID (`pid`) plus all response data
  but no identifying personal data beyond what the participant
  voluntarily typed in the optional demographic fields.
- The "Anyone" access setting on the web app only permits POSTs to
  the endpoint; it does **not** make the spreadsheet public. The
  spreadsheet's sharing settings remain at "Only you can view"
  unless you explicitly change them.
- For an additional layer, add a shared-secret check at the top of
  `doPost`:
  ```js
  if (body._auth !== "YOUR-SECRET-TOKEN") {
    return ContentService.createTextOutput(JSON.stringify({ ok: false, error: "auth" }))
      .setMimeType(ContentService.MimeType.JSON);
  }
  ```
  and add `_auth: "YOUR-SECRET-TOKEN"` to the JSON sent from
  `study.js`. This prevents drive-by POSTs from inflating your data.

## Rollback

If you need to redeploy (e.g. after a schema change), open Apps
Script → **Deploy** → **Manage deployments** → pencil icon → **New
version**. The URL stays the same; only the code is updated.
