from model import Base, User
from sqlal import engine


#Base.metadata.drop_all(engine)
#Base.metadata.create_all(engine)
User.__table__.drop(engine, checkfirst=True)
User.__table__.create(engine, checkfirst=True)
