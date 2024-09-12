#!/usr/bin/env python3
"""
This module defines the User model for the SQLAlchemy ORM.
The User model represents the users table in the database.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    User model for representing a user record in the database.

    Attributes:
        id (int): The user's unique identifier, primary key.
        email (str): The user's email address, non-nullable.
        hashed_password (str): The hashed password of the user, non-nullable.
        session_id (str): The session ID associated with the user, nullable.
        reset_token (str): The reset token for password reset, nullable.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
