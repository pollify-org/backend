from fastapi import APIRouter, BackgroundTasks
from pydantic import EmailStr
from app.config import config
from app.database.dependencies import sessDep
from app.functions.emailer import send_email
from app.models.auth.dependencies import authLoadDep, resetLoadDep
from app.models.auth.role import Role
from app.models.auth.token import Token
from app.models.user import User
from app.models.user.schemas import PasswordsIn, UserDetailOut
from app.services.user_service import UserService
router = APIRouter(prefix="/user", tags=["User"])


@router.get("/me", response_model=UserDetailOut, status_code=200)
async def me(user: authLoadDep):
    return user


@router.get("/request-reset-password/{email}", status_code=200)
async def request_reset_password(
    async_session: sessDep, email: EmailStr, bt: BackgroundTasks
) -> dict:
    return await UserService.request_reset_password(async_session, email, bt)


@router.post("/reset-password", status_code=200, response_model=UserDetailOut)
async def reset_password(
    async_session: sessDep,
    passwords: PasswordsIn,
    user: resetLoadDep,
    token: str | None = None,  
):
    return await UserService.reset_password(async_session, passwords, user,token)
