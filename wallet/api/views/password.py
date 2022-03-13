from uuid import UUID

from fastapi import Depends, Response
from fastapi_jwt_auth import AuthJWT

from wallet.api.errors import APIError
from wallet.database.models import PasswordModel, UserModel
from wallet.serializers.password import BasePasswordInfo, PasswordInfo, CreatePassword
from wallet.utils.router import InferringRouter
from wallet.utils.security import generate_aes_key_from_hash, aes_encrypt, safe_compare

password_router = InferringRouter(prefix="/password", tags=["password"])


@password_router.get("")
async def list_user_passwords(auth: AuthJWT = Depends()) -> list[BasePasswordInfo]:
    """List user passwords"""
    auth.jwt_required()
    jwt = auth.get_raw_jwt()
    user_id = jwt["user_id"]
    password_list = await PasswordModel.filter(user_id=user_id)
    return [BasePasswordInfo.from_orm(p) for p in password_list]


@password_router.get("/{id}")
async def get_user_password(id: UUID, auth: AuthJWT = Depends()) -> PasswordInfo:
    """Get password value"""
    auth.jwt_required()
    jwt = auth.get_raw_jwt()
    user_id = jwt["user_id"]
    pwd = await PasswordModel.get_or_none(id=id).prefetch_related("user")
    if not pwd:
        raise APIError(status=404, detail="Password not found")
    if not safe_compare(user_id, pwd.user_id):
        raise APIError(status=403, detail="Forbidden")
    return PasswordInfo.from_orm(pwd)


@password_router.post("", status_code=201)
async def create_new_password(p: CreatePassword, auth: AuthJWT = Depends()) -> BasePasswordInfo:
    auth.jwt_required()
    jwt = auth.get_raw_jwt()
    user_id = jwt["user_id"]
    user = await UserModel.get_or_none(id=user_id).only("password_hash")
    if not user:
        raise APIError(status=404, detail="User does not exist")

    key = generate_aes_key_from_hash(user.password_hash)
    encrypted_password = aes_encrypt(key, p.password)
    password_obj = PasswordModel(user_id=user_id, **p.dict())
    password_obj.encrypted_password = encrypted_password
    await password_obj.save()

    return BasePasswordInfo.from_orm(password_obj)


@password_router.delete("/{id}", response_class=Response, status_code=204)
async def delete_password(id: UUID, auth: AuthJWT = Depends()):
    auth.jwt_required()
    jwt = auth.get_raw_jwt()
    user_id = jwt["user_id"]
    await PasswordModel.filter(id=id, user_id=user_id).delete()
