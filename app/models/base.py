import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


class BaseModel(Base):
    """
    The basic model (abstract) for a Charity project and Donation.
    """
    __abstract__ = True

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    close_date = Column(DateTime)

    def close(self):
        """
        The method for closing an investment or project,
        use when full_amount = invested_amount is reached.
        """
        self.invested_amount = self.full_amount
        self.fully_invested = True
        self.close_date = datetime.datetime.utcnow()