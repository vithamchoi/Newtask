#!/bin/sh
set -eu

mkdir -p "$(dirname "${DATAGUARD_DB:-/data/study.db}")"

python -m backend.db --init
python -m backend.db --load stimuli/stimuli_pool.json

exec gunicorn \
  --bind "0.0.0.0:${PORT:-8080}" \
  --workers "${WEB_CONCURRENCY:-2}" \
  --timeout "${GUNICORN_TIMEOUT:-120}" \
  backend.app:app
