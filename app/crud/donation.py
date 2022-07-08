from app.models import Donation
from .base import CRUDBase


class CRUD_Donation(CRUDBase):
    """CRUD for Donation."""
    pass


donation_crud = CRUD_Donation(Donation)