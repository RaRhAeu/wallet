from pydantic import BaseSettings, Field, SecretStr


class Settings(BaseSettings):
    env: str = Field("DEV", env="ENV")
    DB_URL: str = Field(
        "postgres://postgres:postgres@localhost:5432/manager", env="DB_URL"
    )

    AES_IV: str = Field("m+UEIGKNOZyQin1pr8UVPg==", env="AES_IV")

    class Config:
        use_enum_values = True


class JWTSettings(BaseSettings):
    authjwt_secret_key: str = Field("TEST_KEY", env="JWT_SECRET")
    authjwt_algorithm: str = "HS256"
    # authjwt_access_token_expires: timedelta = Field(default=timedelta(hours=2))


settings = Settings()


TORTOISE_ORM = {
    "connections": {"default": settings.DB_URL},
    "apps": {
        "models": {
            "models": ["aerich.models", "wallet.database.models"],
            "default_connection": "default",
        },
    },
}
