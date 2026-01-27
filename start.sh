#!/usr/bin/env bash
set -euo pipefail

# Initialize sqlite database and directories
python - <<'PY'
from app import create_app
app = create_app()
with app.app_context():
    try:
        from app.db_setup import init_db
        init_db()
        print('DB initialized')
    except Exception as e:
        print('DB init failed:', e)
PY

# Exec gunicorn (replace process so signals are forwarded)
exec gunicorn --bind 0.0.0.0:8000 run:app --workers 3
