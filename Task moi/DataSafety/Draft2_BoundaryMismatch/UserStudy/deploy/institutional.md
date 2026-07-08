# Deploying to an institutional / RMIT web server

Some IRB protocols require the study to be hosted on a university
domain. The prototype is fully static so any web server (Apache,
nginx, Caddy, IIS, even shared hosting) will host it.

## Generic recipe

1. Ask RMIT IT for static web hosting space on a domain like
   `research.rmit.edu.au/~your-handle/bcm/`. The request usually
   takes 1–2 business days.
2. Upload the entire contents of `UserStudy/prototype/` to that
   space (FTP, SFTP, rsync, or the institution's web UI).
3. Confirm that `apps.json` and `mcq_bank.json` are served with the
   `application/json` MIME type. Most servers do this automatically;
   if not, ask IT for the right `.htaccess` line.
4. Set `BACKEND_URL` in `study.js` and re-upload that file.

## Apache `.htaccess` (if needed)

```
<FilesMatch "\.json$">
  Header set Content-Type "application/json"
</FilesMatch>
<FilesMatch "\.html$">
  Header set Cache-Control "no-cache"
</FilesMatch>
```

## nginx snippet

```
location ~* \.json$ {
  add_header Content-Type application/json;
}
location ~* \.html$ {
  add_header Cache-Control no-cache;
}
```

## Privacy / IRB notes

- The prototype only sends data to the Apps Script `BACKEND_URL` you
  configured. If your IRB requires data-residency (e.g. all data must
  stay in Australia), point `BACKEND_URL` at an institutional
  endpoint instead of Google Apps Script. The on-the-wire payload is
  the same JSON; only the destination changes.
- The prototype reads no third-party scripts. There is no Google
  Analytics, no advertising pixels, no fonts loaded from external
  CDNs. The HTML/CSS/JS are self-contained.

## Verifying the deploy

Open the public URL in an incognito window and walk through the same
sanity check listed in `deploy/README.md`.
