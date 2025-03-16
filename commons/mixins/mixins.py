from sqlalchemy import Column, Boolean, DateTime, func, Integer, String

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False, nullable=False)

    async def delete(self, session: AsyncSession, cascade=False):
        self.is_deleted = True
        session.add(self)

        stmt = select(type(self)).filter_by(id=self.id)
        stmt = stmt.options(*[selectinload(getattr(type(self), rel.key)) for rel in self.__mapper__.relationships])

        result = await session.execute(stmt)
        obj_with_relations = result.scalars().first()

        if not obj_with_relations:
            await session.rollback()
            return
    
        for rel in self.__mapper__.relationships:
            if "delete" in rel.cascade or "delete-orphan" in rel.cascade:
                try:
                    related_objects = getattr(obj_with_relations, rel.key)
                except Exception as e:
                    print(e) 
                
                    
                if related_objects is None:
                    continue
                
                if isinstance(related_objects, list):  
                    for obj in related_objects:
                        await obj.delete(session, cascade=True)
                        
                else: 
                    await related_objects.delete(session, cascade=True)
                    
        if not cascade:
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

