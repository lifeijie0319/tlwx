from sqlalchemy import Column, ForeignKey, Integer, String
from .base import Base


class CCRDOnlineApply(Base):
    __tablename__ = 'CCRD_ONLINE_APPLY'

    id = Column(Integer, primary_key=True)
    openid = Column(String(36), nullable=False)
    name = Column(String(36), nullable=False)
    idno = Column(String(18), nullable=False)
    id_type = Column(String(1), ForeignKey('CREDENTIAL_TYPE.code'), default='I')
    cellphone = Column(String(11), nullable=False)


class CredentialType(Base):
    __tablename__ = 'CREDENTIAL_TYPE'

    code = Column(String(1), nullable=False, primary_key=True)
    name = Column(String(36), nullable=False)
