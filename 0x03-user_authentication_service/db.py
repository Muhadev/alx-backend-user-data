#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            User: The first user that matches the filter criteria.

        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If invalid query arguments are provided.
        """
        session = self._session
        query = session.query(User)

        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError(f"Invalid field: {key}")
            query = query.filter(getattr(User, key) == value)

        user = query.first()
        if user is None:
            raise NoResultFound()
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes based on user_id

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments containing
            attribute-value pairs to update.

        Raises:
            ValueError: If an invalid argument that does not
            correspond to a user attribute is passed.
            NoResultFound: If no user is found with the given user_id.
        """
        session = self._session

        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise NoResultFound(f"No user found with id={user_id}")

        # Update user attributes based on kwargs
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise ValueError(f"Invalid argument: {key}")
            setattr(user, key, value)

        # Commit changes to the database
        session.commit()
