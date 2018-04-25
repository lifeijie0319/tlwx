from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

from .base import Base


class WXMenu(Base):
    __tablename__ = 'WXMENU'

    id = Column(Integer, primary_key=True)
    name = Column(String(36), nullable=False)
    level = Column(Integer, nullable=False)
    type = Column(String(12))
    key = Column(String(36))
    url = Column(String(144))
    parent_id = Column(Integer, ForeignKey('WXMENU.id'))

    children = relationship('WXMenu', backref=backref('parent', remote_side=[id]))


class User(Base):
    __tablename__ = 'USER'

    id = Column(Integer, primary_key=True)
    openid = Column(String(36), nullable=False, unique=True)
    ccrdno = Column(String(20), nullable=False, unique=True)
    binded = Column(Boolean(), default=True)
