from model.ccrd import CCRDOnlineApply
from sqlal import get_engine


engine = get_engine()
#CCRDOnlineApply.__table__.create(bind=engine, checkfirst=True)
