-- upgrade --
ALTER TABLE "user" ALTER COLUMN "password_hash" TYPE VARCHAR(255) USING "password_hash"::VARCHAR(255);
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "password_hash" TYPE TEXT USING "password_hash"::TEXT;
