data "external_schema" "sqlalchemy" {
  program = [
    "uv",
    "run",
    "atlas-provider-sqlalchemy",
    "--path", "./app/migrations",
    "--dialect", "postgresql",
  ]
}

env "local" {
  src = data.external_schema.sqlalchemy.url
  # Ephemeral Postgres; major version aligned with docker-compose (postgres:18).
  dev = "docker://postgres/18/dev?search_path=public"
  migration {
    dir = "file://app/migrations"
  }
  format {
    migrate {
      diff = "{{ sql . \"  \" }}"
    }
  }
}

# Set ATLAS_DATABASE_URL (libpq postgres://..., not postgresql+asyncpg) before apply.
# Example: postgres://app:pass@localhost:5432/app_dev?sslmode=disable
env "apply" {
  url = getenv("ATLAS_DATABASE_URL")
  migration {
    dir = "file://app/migrations"
  }
}
