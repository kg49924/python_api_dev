from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# General way to create database url.
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@ip-address/hostname/<database_name>'
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Kara_at_123@localhost/python_api_dev_prod_db"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind = engine)

Base = declarative_base() #defining base class.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
