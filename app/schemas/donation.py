from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    """Basic scheme for all types of queries Donation."""
    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(DonationBase):
    """Scheme for creating a donation."""
    pass


class DonationSuperUserDB(DonationBase):
    """
    Scheme for returning all donations
    from the database at the request of the superuser.
    """
    id: int
    create_date: datetime
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationDB(DonationBase):
    """
    The scheme for returning all user donations
    from the database.
    """
    id: int
    create_date: datetime

    class Config:
        orm_mode = True