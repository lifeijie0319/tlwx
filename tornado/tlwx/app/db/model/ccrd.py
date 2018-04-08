from sqlalchemy import Column, String
from .base import Base


class CCRDOnlineApply(Base):
    __tablename__ = 'ccrd_online_apply'

    idno = Column(String(18), primary_key=True)
    name = Column(String(36), nullable=False)
    cel = Column(String(11), nullable=False)
