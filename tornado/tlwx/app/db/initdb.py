from model import Base, CredentialType
from sqlal import engine


#Base.metadata.drop_all(engine)
#Base.metadata.create_all(engine)
CredentialType.__table__.drop(engine, checkfirst=True)
CredentialType.__table__.create(engine, checkfirst=True)
