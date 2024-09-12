#!/usr/bin/env python3
"""
Auth module to handle user authentication and registration.
"""

from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
from typing import Optional


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt with a salt.

    Args:
        password (str): The password string to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """Initialize Auth instance with a database connection."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user with an email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The newly registered User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        # Check if user already exists
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # User does not exist, proceed with registration
            hashed_password = _hash_password(password)
            user = self._db.add_user(
                email=email,
                hashed_password=hashed_password
                )
            return user
        except InvalidRequestError as e:
            raise ValueError(f"Invalid query arguments passed: {e}")
