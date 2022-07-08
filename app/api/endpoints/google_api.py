from aiogoogle import Aiogoogle
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_user
from app.crud.charity_project import charity_project_crud
from app.schemas.google_api import GoogleSpreadsheetsUrl
from app.services.google_api import (set_user_permissions, spreadsheets_create,
                                     spreadsheets_update_value)
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get('/', response_model=GoogleSpreadsheetsUrl,
                 dependencies=[Depends(current_user)])
async def get_all_closed_projects(wrapper_services: Aiogoogle = Depends(get_service),
                                  session: AsyncSession = Depends(get_async_session)):
    """
    Display all closed projects in the table.
    """
    projects_close = await charity_project_crud.get_projects_by_completion_rate(session)
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(spreadsheetid,
                                    projects_close,
                                    wrapper_services)
    return {'url': f'https://docs.google.com/spreadsheets/d/{spreadsheetid}'}