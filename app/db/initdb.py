from model import Base, User, SignInRule, SignInRecord
from sqlal import get_engine


engine = get_engine()
#Base.metadata.create_all(engine)
User.__table__.drop(bind=engine, checkfirst=True)
SignInRule.__table__.drop(bind=engine, checkfirst=True)
SignInRecord.__table__.drop(bind=engine, checkfirst=True)
User.__table__.create(bind=engine, checkfirst=True)
SignInRule.__table__.create(bind=engine, checkfirst=True)
SignInRecord.__table__.create(bind=engine, checkfirst=True)
