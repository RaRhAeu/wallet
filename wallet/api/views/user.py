from uuid import UUID

from fastapi import Depends, Response
from fastapi_jwt_auth import AuthJWT
from tortoise.exceptions import IntegrityError
from tortoise.transactions import in_transaction

from wallet.api.errors import APIError
from wallet.database.models import UserModel, PasswordModel
from wallet.serializers.user import GetUser, CreateUser, UpdateUser
from wallet.utils.router import InferringRouter
from wallet.utils.security import generate_password_hash, aes_encrypt, generate_aes_key_from_hash, safe_compare, \
    verify_password, aes_decrypt

user_router = InferringRouter(prefix="/user", tags=["user"])


@user_router.get("/me")
async def get_current_user(auth: AuthJWT = Depends()) -> GetUser:
    auth.jwt_required()

    current_user = auth.get_jwt_subject()

    user_obj = await UserModel.get_by_email(current_user)

    return GetUser.from_orm(user_obj)


@user_router.patch("/me")
async def update_user_info(user: UpdateUser, auth: AuthJWT = Depends()):
    """change password"""
    auth.jwt_required()
    current_user = auth.get_jwt_subject()

    user_obj = await UserModel.get_by_email(current_user)
    if not user_obj:
        raise APIError(status=404, detail="User does not exist")
    pwd_hash = generate_password_hash(user.password)
    if verify_password(user_obj.password_hash, user.password): # if old password == new password
        raise APIError(status=422, detail="New password must be different from previous one")

    key = generate_aes_key_from_hash(pwd_hash)

    old_key = generate_aes_key_from_hash(user_obj.password_hash)
    user_obj.password_hash = pwd_hash
    async with in_transaction():
        passwords = await PasswordModel.filter(user_id=user_obj.id).select_for_update()
        for p in passwords:
            decrypted = aes_decrypt(old_key, p.encrypted_password)
            p.encrypted_password = aes_encrypt(key, decrypted)
            await p.save(update_fields=("encrypted_password", "updated"))
        await user_obj.save(update_fields=("password_hash", "updated"))


@user_router.delete("/{id}", response_class=Response, status_code=204)
async def delete_user(id: UUID, auth: AuthJWT = Depends()):
    auth.jwt_required()
    jwt = auth.get_raw_jwt()
    user_obj = await UserModel.get_or_none(id=id)
    if user_obj:
        # delete user only if user is current user or is admin
        if jwt["user_id"] != user_obj.id and not user_obj.is_superuser:
            raise APIError(status=403, detail="Forbidden")
        await user_obj.delete()


@user_router.post("", status_code=201)
async def register_user(user: CreateUser):
    try:
        user_obj = UserModel(**user.dict(exclude={"password"}))
        user_obj.password_hash = generate_password_hash(user.password)
        await user_obj.save()
    except IntegrityError:
        raise APIError(status=409, detail="User with this email already exists")
