from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from tortoise.contrib.fastapi import register_tortoise

from wallet._version import __version__
from wallet.api.errors import APIError
from wallet.api.tags_metadata import tags_metadata
from wallet.api.views import auth_router, password_router, user_router
from wallet.settings import TORTOISE_ORM, JWTSettings

app = FastAPI(
    title="Password Wallet",
    description="Password management and storage API",
    version=__version__,
    openapi_tags=tags_metadata
)

register_tortoise(app=app, config=TORTOISE_ORM)


@AuthJWT.load_config
def get_config():
    return JWTSettings()


@app.route("/heatlthz")
async def health_endpoint():
    return JSONResponse({"health": "OK"})


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.exception_handler(APIError)
async def handle_detail_error(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.details.status, content=exc.details.dict(exclude={"headers"})
    )

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(password_router)
