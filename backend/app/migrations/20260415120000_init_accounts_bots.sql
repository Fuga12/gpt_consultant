-- Create "accounts" table
CREATE TABLE IF NOT EXISTS "public"."accounts" (
  "id" uuid NOT NULL,
  "name" character varying(255) NOT NULL,
  "created_at" timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY ("id")
);

-- Create "bots" table
CREATE TABLE IF NOT EXISTS "public"."bots" (
  "id" uuid NOT NULL,
  "account_id" uuid NOT NULL,
  "platform" character varying(32) NOT NULL,
  "is_active" boolean NOT NULL,
  "persona_name" character varying(255) NOT NULL,
  "system_prompt" text NOT NULL,
  "credentials" jsonb NOT NULL,
  "escalation_config" jsonb NULL,
  "created_at" timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY ("id"),
  CONSTRAINT "bots_account_id_fkey" FOREIGN KEY ("account_id") REFERENCES "public"."accounts" ("id") ON UPDATE NO ACTION ON DELETE CASCADE
);
