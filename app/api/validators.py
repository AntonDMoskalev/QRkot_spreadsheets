from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate
from http import HTTPStatus


async def check_charity_project_id_exists(charity_project_id: int,
                                          session: AsyncSession) -> CharityProject:
    """
    The validator checks the presence of an object in the database by ID.
    """
    charity_project = await charity_project_crud.get(obj_id=charity_project_id,
                                                     session=session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не на найден!')
    return charity_project


async def check_charity_project_name_exists(obj_in, session: AsyncSession):
    """
    The validator checks the presence of an object in the database by Name.
    """
    obj = obj_in.dict(exclude_unset=True)
    name = obj.get('name')
    if name:
        charity_project_name = await charity_project_crud.get(name=name,
                                                              session=session)
        if charity_project_name:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail='Проект с таким именем уже существует!')
    return obj_in


async def check_update_charity_project(charity_project: CharityProject,
                                       obj_in: CharityProjectUpdate) -> CharityProject:
    """
    The validator checks whether the project is closed for investment.
    """
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    return charity_project


async def check_delete_project(charity_project: CharityProject) -> CharityProject:
    """
    The validator checks whether the project can be deleted.
    """
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return charity_project
