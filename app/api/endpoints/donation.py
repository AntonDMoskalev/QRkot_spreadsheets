from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.schemas.donation import (DonationCreate, DonationDB,
                                  DonationSuperUserDB)
from app.schemas.user import UserRead
from app.utils.invest import invested

router = APIRouter()


@router.get('/',
            response_model=list[DonationSuperUserDB],
            response_model_exclude_none=True,
            dependencies=[Depends(current_superuser)])
async def get_all_donations(session: AsyncSession = Depends(get_async_session)):
    """
    - Only for super users.
    - Gets a list of all donations.
    """
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get('/my', response_model=list[DonationDB])
async def get_user_donations(user: UserRead = Depends(current_user),
                             session: AsyncSession = Depends(get_async_session)):
    """
    Get a list of my donations.
    """
    all_my_donations = await donation_crud.get_multi(user_id=user.id,
                                                     session=session)
    return all_my_donations


@router.post('/',
             response_model=DonationDB,
             response_model_exclude_none=True)
async def create_donation(donation: DonationCreate,
                          user: UserRead = Depends(current_user),
                          session: AsyncSession = Depends(get_async_session)):
    """
    Make a donation.
    """
    new_donation = await donation_crud.create(donation, session, user)
    new_donation = await invested(obj_in=new_donation,
                                  model_db=CharityProject,
                                  session=session)
    new_donation = await donation_crud.save(new_donation, session)
    return new_donation