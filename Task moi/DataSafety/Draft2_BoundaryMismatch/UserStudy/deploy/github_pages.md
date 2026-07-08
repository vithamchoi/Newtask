# Deploying to GitHub Pages

Total time: about 10 minutes. Cost: free. Produces a public URL of
the form `https://YOUR-USERNAME.github.io/bcm-vignette/`.

## Prerequisites
- A GitHub account.
- Git installed locally **or** a GitHub Desktop client. (Either works;
  the steps below show command-line. If you prefer the desktop client,
  see the "GUI" section.)

## Steps (command line)

1. **Create a new GitHub repository.**
   - Go to <https://github.com/new>.
   - Name it `bcm-vignette` (or anything you like).
   - Visibility: Public (required for free GitHub Pages).
   - Do **not** add a README or .gitignore at this step.
   - Click **Create repository**.

2. **Initialise a local repo from the prototype folder.**

   From the project root (the one that contains `UserStudy/`), run:

   ```bash
   cd UserStudy/prototype
   git init
   git add .
   git commit -m "Initial commit: BCM vignette prototype v1.0.0"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/bcm-vignette.git
   git push -u origin main
   ```

3. **Turn on GitHub Pages.**
   - In the GitHub repo page, click **Settings** → **Pages** (left
     sidebar).
   - **Source:** Deploy from a branch.
   - **Branch:** `main`, folder `/(root)`.
   - Click **Save**.
   - Wait 30–60 seconds. A green banner appears with the URL:
     `https://YOUR-USERNAME.github.io/bcm-vignette/`.

4. **Set the backend URL in study.js.**

   You should have already deployed the Apps Script backend (see
   `../backend/deploy_apps_script.md`). Open `study.js`, set
   `BACKEND_URL`, commit, push:

   ```bash
   # Edit study.js, then:
   git add study.js
   git commit -m "Wire backend URL"
   git push
   ```

   GitHub Pages re-publishes within 1–2 minutes.

## Steps (GitHub Desktop)

1. Create the repo on github.com as above.
2. Open GitHub Desktop → **File** → **Add Local Repository** → point
   it at `UserStudy/prototype/`.
3. **Repository** → **Push Origin**.
4. In Settings → Pages on github.com, enable as above.

## Sanity check

Open `https://YOUR-USERNAME.github.io/bcm-vignette/index.html`.

You should see the landing page. Click through to `study.html?pid=DEMO-001`,
complete the flow, and confirm a row in your Google Sheet.

## Updates after launch

Any change to a file in `prototype/` is published by `git push`. GitHub
Pages re-builds within a minute. Bump `STUDY_VER` in `study.js` so the
analyst can tell which version a participant ran.

## Custom domain (optional)

If you want `bcm.your-research-group.org`:
- Add a `CNAME` file in the repo containing your domain.
- In Settings → Pages, fill in the custom domain.
- Add a CNAME DNS record at your registrar pointing to
  `YOUR-USERNAME.github.io`.
- Wait for DNS to propagate (15 min–24 h).

## Troubleshooting

- **404 on `study.html`** — Make sure you pushed everything in
  `prototype/`. `git status` should be clean.
- **POST to backend fails with CORS** — Apps Script web apps add the
  right headers by default. If you see CORS errors, re-deploy the
  Apps Script and use the *new* URL (the URL changes when you change
  the "execute as" setting).
- **Stale assets** — GitHub Pages aggressively caches. Append `?v=2`
  to JS/CSS URLs in `study.html` to force a reload.
