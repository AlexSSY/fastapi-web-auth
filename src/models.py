from sqlalchemy import Column, Integer, String

from .db import engine, Base, SessionLocal
from . import helpers


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)


def create_all_tables():
    Base.metadata.create_all(engine)


def seed():
    """
    Just create one user
    """
    with SessionLocal() as db:
        user = db.get(User, 1)
        if not user:
            email = 'admin@mail.com'
            password = 'admin'
            password_hash = helpers.hash_password(password)
            db.add(User(email=email, password_hash=password_hash))
            db.commit()
