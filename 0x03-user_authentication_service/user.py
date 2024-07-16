#!/usr/bin/env python3
"""
User model module.
Defines the User model for a database table named users using SQLAlchemy.
"""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    """
    User model for the users table.

    Attributes:
        id (int): The integer primary key.
        email (str): A non-nullable string for the user's email.
        hashed_password (str): A non-nullable string for the hashed password.
        session_id (str): A nullable string for the session ID.
        reset_token (str): A nullable string for the reset token.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)


# SQLAlchemy setup (Example usage, not part of the User model)


if __name__ == "__main__":
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
