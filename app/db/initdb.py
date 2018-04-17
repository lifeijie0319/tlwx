from model import Base
from sqlal import get_engine


engine = get_engine()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
