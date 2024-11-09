from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import BackgroundTasks
from app.repositories.user_repository import UserRepository
from app.models.user.schemas import UserIn, PasswordsIn
from app.functions.exceptions import conflict
from app.models.auth.token import Token
from app.models.auth.role import Role
from app.config import config
from app.functions.emailer import send_email
from app.models.user import User

class UserService:

    @staticmethod
    async def find(async_session: AsyncSession, raise_: bool = True, **kwargs) -> User | None:
        return await UserRepository.find(async_session, raise_=raise_, **kwargs)
        
    @staticmethod
    async def create_user(async_session: AsyncSession, user_in: UserIn, send_email: bool, bt: BackgroundTasks) -> User:
        # Verifica se o usuário já existe pelo email
        if await UserRepository.find_by_email(async_session, email=user_in.email):
            raise conflict(msg="User already exists")

        user = User(**user_in.model_dump())
        user = await UserRepository.save(async_session, user)
        
        # Envia email de reset de senha, se necessário
        if send_email:
            await UserService.request_reset_password(async_session, user.email, bt)
        
        return user

    @staticmethod
    async def save(async_session: AsyncSession, user: User) -> User:
        return await UserRepository.save(async_session, user)
    

    @staticmethod
    async def get_users(async_session: AsyncSession) -> list[User]:
        return await UserRepository.get_all(async_session)

    @staticmethod
    async def delete_user(async_session: AsyncSession, user_id: str):
        user = await UserRepository.get_by_id(async_session, user_id)
        if(user is None):
            raise conflict(msg="User not found")

        await UserRepository.delete(async_session, user)
        return {"message": "User deleted"}

    @staticmethod
    async def update_user(async_session: AsyncSession, user: User, user_in: UserIn) -> User:
        update_data = user_in.model_dump(exclude_unset=True)
        return await UserRepository.update(async_session, user, update_data)

    @staticmethod
    async def get(async_session: AsyncSession, user_id: str) -> User:
        return await UserRepository.get_by_id(async_session, user_id)
    
    @staticmethod
    async def get_user_by_email(async_session: AsyncSession, email: str) -> User:
        return await UserRepository.find_by_email(async_session, email=email)
    
    @staticmethod
    async def get_user_by_id(async_session: AsyncSession, user_id: str) -> User:
        return await UserRepository.get_by_id(async_session, user_id)
    

    @staticmethod
    async def request_reset_password(async_session: AsyncSession, email: str, bt: BackgroundTasks) -> dict:
        user = await UserRepository.find_by_email(async_session, email=email)
        if not user:
            return {"message": "Email sent"}

        token = Token.create_token(user.id, config.RESET_PASSWORD_EXPIRATION)
        bt.add_task(send_email, user.email, "Recuperação de senha", f"Seu token de recuperação de senha é: {token}")

        return {"message": "Email sent"}
    
    @staticmethod
    async def reset_password(async_session: AsyncSession, passwords: PasswordsIn, user: User, token: str | None = None) -> User:
        
        if token:
            Token.validate_token(token, user.id)
        
        user.password = passwords.password
        return await UserRepository.save(async_session, user)