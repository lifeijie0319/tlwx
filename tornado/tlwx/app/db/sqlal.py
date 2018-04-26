from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('ibm_db_sa://tonglian:qwe123@127.0.0.1:50000/wxdb', echo=True)
Session = sessionmaker(bind=engine)
