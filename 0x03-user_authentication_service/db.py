#!/usr/bin/env python3
"""
DB module to manage database operations.
"""

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User  # Import User model from user.py


class DB:
    """DB class to manage database operations.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance."""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database.

        Args:
            email (str): The user's email.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Finds a user by arbitrary keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments for filtering user records.

        Returns:
            User: The first user found that matches the given criteria.

        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If the query is improperly formed.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except InvalidRequestError:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user's attributes.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments for updating user attributes.

        Raises:
            ValueError: If an invalid attribute is provided.
            NoResultFound: If no user with the specified ID is found.
        """
        valid_attributes = {
            "email",
            "hashed_password",
            "session_id",
            "reset_token"
            }
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if key not in valid_attributes:
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)

        self._session.commit()
