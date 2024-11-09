from app.database.dependencies import sessDep
from uuid import UUID
from app.models.user import User
from app.repositories.base.base_repository import BaseRepository

class UserRepository:
    """Repositório de usuários."""
    @staticmethod
    async def find(async_session: sessDep, raise_: bool = True, **kwargs) -> User | None:
        """Encontra um usuário."""
        return await BaseRepository.find(User, async_session, raise_=raise_, **kwargs)
    
    @staticmethod
    async def save(async_session: sessDep, user: User) -> User:
        """Salva um usuário."""
        return await BaseRepository.save(User, async_session, user)
    

    
    @staticmethod
    async def find_by_email(async_session: sessDep, email: str) -> User | None:
        """Encontra um usuário pelo email."""
        return await BaseRepository.find(User, async_session, raise_=False, email=email)
    
    @staticmethod
    async def get_user_with_relationships(async_session: sessDep, user_id: UUID) -> User:
        """Obtém um usuário com relacionamentos carregados."""
        return await BaseRepository.get(User, async_session, user_id, relationships=["organizations"])
