from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    """Basic scheme for all types of queries CharityProject."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(CharityProjectBase):
    """
    Scheme for editing the project,
    additional validation of fields checks for empty lines.
    """
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    @validator('name', 'full_amount')
    def value_cannot_be_none(cls, value):
        if not value or value is None:
            raise ValueError(
                'Значение не может быть равно null'
            )
        return value


class CharityProjectCreate(CharityProjectBase):
    """Scheme for creating a project."""
    pass


class CharityProjectDB(CharityProjectBase):
    """Scheme for returning objects from the database."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
