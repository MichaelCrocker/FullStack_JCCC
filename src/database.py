import os

from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

url_object = URL.create(
    "mysql+mysqlconnector",
    username="u560819325_pim_root",
    password="Shared@2024PIM",
    host="srv772.hstgr.io",
    database="u560819325_PIM"
)
engine = create_engine(url_object, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()