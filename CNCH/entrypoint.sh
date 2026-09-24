#!/bin/sh
set -e

# Fix ownership of bind-mounted volumes (runs as root before dropping privileges)
chown -R app:app /app/data /app/media

# Run migrations as app user
gosu app python manage.py migrate --noinput

# Start the server as app user
exec gosu app "$@"
