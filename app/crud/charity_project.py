from app.models import CharityProject
from sqlalchemy import select, asc
from .base import CRUDBase
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import db


class CRUD_CharityProject(CRUDBase):
    """CRUD for CharityProject."""
    async def get_projects_by_completion_rate(self, session=AsyncSession):
        """
        Retrieves all closed projects
        from the database and sorts them by investment time.
        """
        query = await session.execute(
            select(CharityProject.name,
                   CharityProject.description,
                   (db.datetime_func(CharityProject.close_date) -
                    db.datetime_func(CharityProject.create_date)
                    ).label('collection_time')).where(
                        CharityProject.fully_invested).order_by(
                            asc('collection_time')))
        return query.all()


charity_project_crud = CRUD_CharityProject(CharityProject)