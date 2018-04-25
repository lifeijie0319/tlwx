from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('ibm_db_sa://py3:qwe123@localhost:50000/wxbank', echo=True)
Session = sessionmaker(bind=engine)
