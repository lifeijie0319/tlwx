from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..config import DB2_DIALECT


engine = create_engine(DB2_DIALECT)
Session = sessionmaker(bind=engine)
