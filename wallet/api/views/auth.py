from fastapi import Depends, Response
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from wallet.api.errors import APIError
from wallet.database.models import UserModel
from wallet.serializers.token import AccessToken, TokenPair
from wallet.serializers.user import User
from wallet.utils.router import InferringRouter

auth_router = InferringRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login")
async def login_user(user: User, auth: AuthJWT = Depends()) -> TokenPair:
    user_obj = await UserModel.get_by_email(user.email)
    if user_obj is None:
        raise APIError(status=404, detail="User does not exist")
    if not user_obj.verify_password(user.password):
        raise APIError(status=401, detail="Unauthorized")

    access_token = auth.create_access_token(subject=user_obj.email, user_claims={"user_id": str(user_obj.id)})
    refresh_token = auth.create_refresh_token(subject=user_obj.email)
    return TokenPair(access_token=access_token, refresh_token=refresh_token)


@auth_router.post("/jwt/refresh")
def refresh_access_token(auth: AuthJWT = Depends()) -> AccessToken:
    auth.jwt_refresh_token_required()
    current_user = auth.get_jwt_subject()
    new_access_token = auth.create_access_token(subject=current_user)

    return AccessToken(access_token=new_access_token)


@auth_router.get("/jwt/verify", response_class=Response)
async def verify_token(auth: AuthJWT = Depends()):
    auth.jwt_required()
    return JSONResponse(status_code=200, content={"detail": "Token verified"})
