#!/usr/bin/env python3
"""
Authentication module for user management.
"""

from db import DB
import bcrypt
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Hash a password with bcrypt.

        Args:
            password (str): The password to hash.

        Returns:
            bytes: The hashed password.
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)

    def register_user(self, email: str, password: str):
        """Register a new user with the given email and password.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If the user already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            user = self._db.add_user(email, hashed_password.decode())
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the provided email and password are valid.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            bool: True if the login is valid, otherwise False.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode(),
                user.hashed_password.encode()
                )
        except (NoResultFound, AttributeError):
            return False
