from typing import Any, Type

from tortoise import Model, fields
from tortoise.models import MODEL

from wallet.utils.security import verify_password, generate_aes_key_from_hash, aes_decrypt


class UserModel(Model):
    id = fields.UUIDField(pk=True)
    email = fields.CharField(255, unique=True, index=True)
    password_hash = fields.CharField(255)
    use_hmac = fields.BooleanField()
    is_superuser = fields.BooleanField(default=False)

    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)

    passwords: fields.ReverseRelation["PasswordModel"]

    @classmethod
    async def get_by_email(cls, email: str):
        return await cls.get_or_none(email=email)

    def verify_password(self, password) -> bool:
        return verify_password(password, self.password_hash)

    class Meta:
        table = "user"


class PasswordModel(Model):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.UserModel", on_delete=fields.CASCADE, related_name="passwords")

    login = fields.CharField(255)
    encrypted_password = fields.TextField()

    url = fields.TextField(null=True)
    description = fields.TextField(null=True)

    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)

    @property
    def password(self) -> str:
        user_password = self.user.password_hash
        key = generate_aes_key_from_hash(user_password)
        password = aes_decrypt(key, self.encrypted_password)
        return password

    class Meta:
        table = "password"
