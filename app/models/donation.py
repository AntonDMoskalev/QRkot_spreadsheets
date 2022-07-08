from sqlalchemy import Column, Integer, Text, ForeignKey
from .base import BaseModel


class Donation(BaseModel):
    """Model for Donation."""
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)