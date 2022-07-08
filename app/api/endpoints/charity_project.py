from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_id_exists,
                                check_charity_project_name_exists,
                                check_delete_project,
                                check_update_charity_project)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models.donation import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.utils.invest import invested


router = APIRouter()


@router.get('/',
            response_model_exclude_none=True,
            response_model=List[CharityProjectDB])
async def get_all_charity_projects(session: AsyncSession = Depends(get_async_session)):
    """Gets a list of all projects."""
    all_projects = await charity_project_crud.get_multi(session)

    return all_projects


@router.post('/',
             response_model=CharityProjectDB,
             response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)])
async def create_charity_project(charity_project: CharityProjectCreate,
                                 session: AsyncSession = Depends(get_async_session)):
    """
    * Only for super users.
    * Creates a charity project.
    """
    charity_project = await check_charity_project_name_exists(charity_project, session)
    new_charity_project = await charity_project_crud.create(charity_project, session)
    new_charity_project = await invested(obj_in=new_charity_project,
                                         model_db=Donation,
                                         session=session)
    new_charity_project = await charity_project_crud.save(new_charity_project,
                                                          session)
    return new_charity_project


@router.patch('/{charity_project_id}',
              response_model=CharityProjectDB,
              dependencies=[Depends(current_superuser)])
async def update_charity_project(charity_project_id: int,
                                 obj_in: CharityProjectUpdate,
                                 session: AsyncSession = Depends(get_async_session)):
    """
    - Only for super users.
    - A closed project cannot be edited,
    and it is also impossible to set the required amount
    less than the amount already invested.
    """
    charity_project = await check_charity_project_id_exists(charity_project_id,
                                                            session)
    obj_in = await check_charity_project_name_exists(obj_in,
                                                     session)
    charity_project = await check_update_charity_project(charity_project,
                                                         obj_in)
    charity_project = await charity_project_crud.update(charity_project,
                                                        obj_in,
                                                        session)
    charity_project = await charity_project_crud.save(charity_project,
                                                      session)
    return charity_project


@router.delete('/{charity_project_id}',
               response_model=CharityProjectDB,
               dependencies=[Depends(current_superuser)])
async def delete_charity_project(charity_project_id: int,
                                 session: AsyncSession = Depends(get_async_session)):
    """
    - Only for super users.
    - Deletes the project. You cannot delete a project in which funds have already been invested,
    it can only be closed.
    """
    charity_project = await check_charity_project_id_exists(charity_project_id,
                                                            session)
    charity_project = await check_delete_project(charity_project)
    charity_project = await charity_project_crud.remove(charity_project,
                                                        session)
    return charity_project
