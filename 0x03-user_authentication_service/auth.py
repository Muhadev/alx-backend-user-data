#!/usr/bin/env python3
"""
auth module
"""
import bcrypt
from typing import Optional
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt.hashpw.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the password.

    Raises:
        ValueError: If the password is not provided or is empty.
    """
    if not password:
        raise ValueError("Password must be provided")

    # Generate salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


def _generate_uuid() -> str:
    """Generate a new UUID (Universally Unique Identifier).

    Returns:
        str: A string representation of a new UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password of the user.

        Returns:
            User: The User object created.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass  # Continue registration

        hashed_password = _hash_password(password)
        user = self._db.add_user(email, hashed_password)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user login credentials.

        Attempts to find a user by their email in the database.
        If found, checks if the provided password matches
        the stored hashed password.

        Args:
            email (str): The email of the user attempting to log in.
            password (str): The password provided during login.

        Returns:
            bool: True if login credentials are valid, False otherwise.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode('utf-8'),
                    user.hashed_password
                )
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """Create a session ID for the user based on email.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID generated for the user.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """Get user based on session ID.

        Args:
            session_id (str): The session ID to look up the user.

        Returns:
            Optional[User]: The corresponding User object
            if found, else None.
        """
        if session_id is None:
            return None

        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy user session by setting session ID to None.

        Args:
            user_id (int): The ID of the user whose session will be destroyed.
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token for the user
        with the provided email."""
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        reset_token = _generate_uuid()
        # Update user's reset_token in database
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token
