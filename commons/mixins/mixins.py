from sqlalchemy import Column, Boolean, DateTime, func, Integer, String

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False, nullable=False)

    async def delete(self, session: AsyncSession):
        self.is_deleted = True
        session.add(self)
        await session.commit()

    @classmethod
    async def get_all_deleted(cls, session: AsyncSession):
        """
        Optener los registros eliminados
        """
        result = await session.execute(select(cls).where(cls.is_deleted == True))
        return result.scalars().all()
    
    @classmethod
    async def get_all(cls, session: AsyncSession):
        """
        Optener los registros no eliminados
        """
        result = await session.execute(select(cls).where(cls.is_deleted == False))
        return result.scalars().all()

class TimestampMixin:
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

