from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE = 'sqlite:///./Blog_Api.sqlite'


engine = create_engine(SQLALCHEMY_DATABASE, connect_args={"check_same_thread": False})

sessionlocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()