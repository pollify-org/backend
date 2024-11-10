# app/api/v1/endpoints/user.py

from fastapi import APIRouter, BackgroundTasks, Security
from app.database.dependencies import sessDep

from app.api.v1.user import request_reset_password
from app.database.dependencies import sessDep
from app.commons.exceptions import conflict
from app.models.auth.functions import authorize
from app.models.auth.role import Role
from app.models.user import User
from app.models.user.dependencies import userDep
from app.services.user_service import UserService
from app.models.user.schemas import UserDetailOut, UserIn, UserOut

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Security(authorize, scopes=[Role.ADMIN])],
)


@router.post("/user", response_model=None, status_code=201)
async def create_user(
    *,
    async_session: sessDep,
    user_in: UserIn,
    send_email: bool = True,
    bt: BackgroundTasks
):
    return await UserService.create_user(async_session, user_in, send_email, bt)

@router.get("/user", response_model=None, status_code=200)
async def get_users(async_session: sessDep):
    return await UserService.get_users(async_session)

@router.get("/user/{id}", response_model=None, status_code=200)
async def get_user(id: str, async_session: sessDep):
    return UserService.get(async_session, id)

@router.delete("/user/{id}", status_code=204)
async def delete_user(async_session: sessDep, user_id: str):
    await UserService.delete_user(async_session, user_id)

@router.put("/user/{id}", response_model=None, status_code=200)
async def update_user(async_session: sessDep, user: userDep, user_in: UserIn):
    return await UserService.update_user(async_session, user, user_in)
 