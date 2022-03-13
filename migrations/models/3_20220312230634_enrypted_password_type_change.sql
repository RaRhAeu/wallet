-- upgrade --
ALTER TABLE "password" ALTER COLUMN "encrypted_password" TYPE TEXT USING "encrypted_password"::TEXT;
-- downgrade --
ALTER TABLE "password" ALTER COLUMN "encrypted_password" TYPE VARCHAR(255) USING "encrypted_password"::VARCHAR(255);
