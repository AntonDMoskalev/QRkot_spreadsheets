from sqlalchemy import Column, String, Text
from .base import BaseModel


class CharityProject(BaseModel):
    """Model for Charity Project."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)