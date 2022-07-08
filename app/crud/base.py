from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    """
    A base class for CRUD with a set of methods
    for interacting with the database.
    """

    def __init__(self, model):
        self.model = model

    async def get(self, session: AsyncSession, obj_id: int = None, name: str = None):
        """
        The method for getting a record from the database by ID or by Name,
        both arguments are optional (choose based on the task).
        Attention! you cannot use a method with 2 arguments at once.
        """
        if name:
            db_obj = await session.execute(select(self.model).where(self.model.name == name))
        elif obj_id:
            db_obj = await session.execute(select(self.model).where(self.model.id == obj_id))
        else:
            raise TypeError('Укажите один из аргументов: obj_id(int) или name(str)')
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession, user_id: str = None):
        """
        The method for getting all records from the database,
        additionally can be filtered by user ID (optional).
        """
        if user_id is not None:
            db_objs = await session.execute(select(self.model).where(self.model.user_id == user_id))
        else:
            db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(self, obj_in, session: AsyncSession, user: Optional[str] = None):
        """
        A method for creating a new record in the database,
        optionally specifying the user ID (check the possibility of the model used).
        """
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        return db_obj

    async def update(self, db_obj, obj_in, session: AsyncSession):
        """
        A method for partial updates in the database.
        """
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        return db_obj

    async def remove(self, db_obj, session: AsyncSession):
        """
        Method for deleting from the database.
        """
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def save(self, obj, session: AsyncSession):
        """
        Method for saving and closing the session.
        """
        await session.commit()
        await session.refresh(obj)
        return obj
