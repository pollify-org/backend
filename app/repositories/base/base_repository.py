from typing import Generic, Type, TypeVar, Sequence, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import QueryableAttribute, joinedload
from sqlalchemy import select
from app.functions.exceptions import not_found

T = TypeVar("T")

class BaseRepository(Generic[T]):
    @staticmethod
    async def get(model: Type[T], async_session: AsyncSession, id: UUID, relationships: list[QueryableAttribute] | None = None) -> T:
        stmt = select(model).where(model.id == id)
        if relationships:
            stmt = stmt.options(*[joinedload(r) for r in relationships])
        result = await async_session.scalar(stmt)
        if not result:
            raise not_found(msg=f"{model.__name__} not found")
        return result

    @staticmethod
    async def get_all(model: Type[T], async_session: AsyncSession) -> Sequence[T]:
        result = await async_session.execute(select(model))
        return result.scalars().all()

    @staticmethod
    async def save(model: Type[T], async_session: AsyncSession, entity: T, relationships: list[QueryableAttribute] | None = None) -> T:
        async_session.add(entity)
        await async_session.commit()
        if relationships:
            return await BaseRepository.get(model, async_session, entity.id, relationships)
        return entity

    @staticmethod
    async def delete(async_session: AsyncSession, entity: T):
        await async_session.delete(entity)
        await async_session.commit()

    @staticmethod
    async def update(async_session: AsyncSession, entity: T, **kwargs) -> T:
        for key, value in kwargs.items():
            setattr(entity, key, value)
        await async_session.commit()
        return entity

    @staticmethod
    async def find(model: Type[T], async_session: AsyncSession, raise_: bool = True, relationships: list[QueryableAttribute] | None = None, **kwargs) -> Optional[T]:
        stmt = select(model).filter_by(**kwargs)
        if relationships:
            stmt = stmt.options(*[joinedload(r) for r in relationships])
        result = await async_session.scalar(stmt)
        if not result and raise_:
            raise not_found(msg=f"{model.__name__} not found")
        return result

    @staticmethod
    async def get_by_id(model: Type[T], async_session: AsyncSession, user_id: UUID, relationships: list[QueryableAttribute] | None = None) -> T:
        return await BaseRepository.get(model, async_session, user_id, relationships)
