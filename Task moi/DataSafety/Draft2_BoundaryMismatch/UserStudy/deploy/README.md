# Deploying the prototype

The prototype is **static**: HTML, CSS, JSON, and JavaScript only. No
build step, no server-side code. Any static host will work. Three
common options:

| Option | Cost | Time to set up | Pros |
|---|---|---|---|
| **GitHub Pages** | Free | 10 min | Versioned, easy rollback, public URL |
| **Netlify** | Free | 5 min | Drag-and-drop, instant URL, free TLS |
| **Institutional web server** | Depends | 1–2 hours | Stays inside university domain (may be required by IRB) |

Step-by-step guides:

- `github_pages.md`
- `netlify.md`
- `institutional.md`

The backend (Google Apps Script) is described separately in
`../backend/deploy_apps_script.md`.

## Files that need to be hosted

The entire contents of `prototype/`:

```
prototype/
├── index.html
├── study.html       ← main participant flow
├── current.html     ← condition-A preview (think-aloud)
├── ble.html         ← condition-B preview (think-aloud)
├── style.css
├── app.js
├── study.js
├── apps.json
└── mcq_bank.json
```

Nothing in `analysis/`, `vignette/`, `thinkaloud/`, `materials/`, or
`backend/` is served to participants. Those are private research
materials.

## Sanity-check after deploy

After deploying, open the hosted URL and:

1. Visit `…/index.html` — should show the landing page.
2. Click "Run study (pid=DEMO-001)" — should advance through consent
   → pre-task → 4 apps → attention → post-task → debrief.
3. Open `…/study.html?pid=PILOT-001` directly — the same flow should
   start without going through the landing page.
4. Confirm the network tab shows a POST to your Apps Script URL on
   debrief (only if `BACKEND_URL` was set in `study.js`).
5. Confirm a row appears in the Google Sheet.

If any of those fails, see the troubleshooting section of the
relevant deploy guide.
