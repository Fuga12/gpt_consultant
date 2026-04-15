#!/bin/sh
set -e

if [ "${APP_PROFILE:-dev}" != "dummy" ] && [ -n "${APP_DATABASE__HOST:-}" ]; then
  export PGHOST="$APP_DATABASE__HOST"
  export PGPORT="${APP_DATABASE__PORT:-5432}"
  export PGUSER="$APP_DATABASE__USER"
  export PGPASSWORD="$APP_DATABASE__PASSWORD"
  export PGDATABASE="$APP_DATABASE__NAME"
  until pg_isready -q; do
    sleep 1
  done
  psql -v ON_ERROR_STOP=1 -f /srv/app/migrations/20260415120000_init_accounts_bots.sql
fi

exec uv run python -m app "$@"
