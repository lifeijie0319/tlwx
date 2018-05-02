from sqlalchemy.ext.declarative import declarative_base

from ...config import DB2_SCHEMA


Base = declarative_base()
Base.metadata.schema = DB2_SCHEMA
