    #!/bin/sh
    set -e

    echo "Starting entrypoint script..."

    # generate SECRET_KEY if not set
    if [ -z "$DJANGO_SECRET_KEY" ]; then
      echo "DJANGO_SECRET_KEY not found. Generating..."
      export DJANGO_SECRET_KEY=$(python - <<'PY'
import secrets, sys
print(secrets.token_urlsafe(50))
PY
)
    fi

    # ensure env file present - render provides DATABASE_URL
    echo "DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}" > .env
    echo "DEBUG=${DEBUG:-False}" >> .env

    # Run migrations and collectstatic
    echo "Running migrations..."
    python manage.py migrate --noinput

    echo "Collecting static files..."
    python manage.py collectstatic --noinput

    echo "Starting Gunicorn..."
    exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers ${WEB_CONCURRENCY:-2}
