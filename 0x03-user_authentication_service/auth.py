#!/usr/bin/env python3
"""
auth module
"""
import bcrypt
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

    def valid_login(self, email, password):
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
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf-8'),
                user.hashed_password
            )
        except NoResultFound:
            return False

        except Exception as e:
            # Handle any unexpected errors gracefully
            print(f"Error during login validation: {str(e)}")
            return False
