from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class User(Base):
    __tablename__='user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    hashed_pasword = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)


class About(Base):
    __tablename__ = "about"

    id = Column(Integer, primary_key=True, index=True)
    header = Column(String(50), nullable=False)
    body = Column(String, nullable=False)
    time = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"))


class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=True)
    email = Column(String, nullable=False)
    subject = Column(String(50))
    message = Column(String)
    time = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"))

class Blog(Base):
    __tablename__="blog"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(30))
    first_name = Column(String, ForeignKey("user.first_name"))
    last_name = Column(String, ForeignKey("user.last_name"))
    body = Column(String(255))
    time_posted = Column(String)
    time_edited = Column(String, nullable=True)
    edited = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("user.id"))