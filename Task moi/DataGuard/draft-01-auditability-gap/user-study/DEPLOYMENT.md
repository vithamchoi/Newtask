# Deployment

This app is a Flask + SQLite deployment for collecting formative expert
feedback on the DataGuard user-study interface.

## Current mode

The default production mode is:

```bash
DATAGUARD_STUDY_MODE=feedback
```

This mode uses every stimulus currently loaded in `stimuli/stimuli_pool.json`
once. It is suitable for expert review of the study materials and interface.
It is not the full controlled study.

For the full preregistered controlled study, first complete the 24-app
stimulus pool and gold standard, then set:

```bash
DATAGUARD_STUDY_MODE=controlled
```

## Required environment variables

```bash
DATAGUARD_DB=/data/study.db
DATAGUARD_ADMIN_TOKEN=<long random token>
DATAGUARD_STUDY_MODE=feedback
```

Optional:

```bash
DATAGUARD_CORS_ORIGINS=https://your-study-domain.example
WEB_CONCURRENCY=2
PORT=8080
```

## Docker

```bash
docker build -t dataguard-user-study .
docker run --rm -p 8080:8080 \
  -e DATAGUARD_ADMIN_TOKEN="$(openssl rand -hex 32)" \
  -v "$PWD/data/raw:/data" \
  dataguard-user-study
```

Open:

```text
http://localhost:8080/
```

## Render

Use `render.yaml` as a blueprint. The service needs a persistent disk mounted
at `/data` so `study.db` survives redeploys.

After deployment, add a custom domain in Render and point your DNS record to
the Render target.

## Export

Use the admin token set in production:

```bash
curl "https://your-study-domain.example/api/export?token=$DATAGUARD_ADMIN_TOKEN" \
  -o dataguard-study-export.json
```

The export contains participants, trials, TLX, trust, and expert feedback.
