# Deploying to Netlify

Fastest option: drag-and-drop your `prototype/` folder into the
Netlify dashboard and you have a live URL in under 60 seconds.

## Drag-and-drop (fastest)

1. Sign in at <https://app.netlify.com>.
2. On the dashboard, locate the **"Sites"** drop zone (or click
   **Add new site → Deploy manually**).
3. Drag the entire `UserStudy/prototype/` folder onto the drop zone.
4. Netlify uploads, builds (no build step is needed; it just hosts
   the static files), and assigns a random URL such as
   `https://lyrical-otter-7c2e.netlify.app`.
5. Copy the URL. Update `BACKEND_URL` in `study.js` if needed, then
   re-drag the folder to re-publish.

## Git-based deploy (recommended for production)

1. Push `prototype/` to a GitHub or GitLab repo (see
   `github_pages.md` for steps 1–2).
2. In Netlify dashboard, **Add new site → Import an existing
   project**.
3. Pick GitHub, authorise, select your repo, branch `main`.
4. **Build command:** leave empty.
5. **Publish directory:** `.` (or `prototype` if the prototype is in
   a subfolder of the repo).
6. Click **Deploy site**.

Every `git push` from now on triggers a redeploy automatically.

## Custom domain

Site settings → Domain management → Add custom domain. Netlify
provisions a free Let's Encrypt TLS certificate.

## netlify.toml (optional)

If you want to pin headers or redirect rules, add this file at the
repo root:

```toml
[[headers]]
  for = "/*"
  [headers.values]
    Cache-Control = "public, max-age=300"

[[redirects]]
  from = "/study"
  to   = "/study.html"
  status = 200
```

This caches assets for 5 min (so updates appear quickly during
piloting) and lets participants visit `/study?pid=…` without the
`.html` suffix.

## Troubleshooting

- **404 on `study.html`** — Confirm `Publish directory` is the
  folder that contains `study.html`.
- **POST to backend fails** — Open the browser network tab; the
  response should be 200 from the Apps Script URL. If you see CORS,
  re-deploy the Apps Script as above.
- **localStorage doesn't persist** — Some incognito browsers
  disable storage; ask pilot participants to use a normal window.
