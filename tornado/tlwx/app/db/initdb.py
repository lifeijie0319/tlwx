from model import Base, CCRDOnlineApply
from sqlal import engine


#Base.metadata.drop_all(engine)
#Base.metadata.create_all(engine)
CCRDOnlineApply.__table__.drop(engine, checkfirst=True)
CCRDOnlineApply.__table__.create(engine, checkfirst=True)
