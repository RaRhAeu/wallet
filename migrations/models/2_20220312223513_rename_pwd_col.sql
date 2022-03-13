-- upgrade --
ALTER TABLE "password" RENAME COLUMN "password" TO "encrypted_password";
-- downgrade --
ALTER TABLE "password" RENAME COLUMN "encrypted_password" TO "password";
