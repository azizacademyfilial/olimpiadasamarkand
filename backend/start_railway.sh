#!/usr/bin/env bash
set -euo pipefail

if [ -d ".venv" ]; then
  . .venv/bin/activate
fi

python manage.py migrate --noinput
python manage.py seed_demo
python manage.py collectstatic --noinput
gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}
