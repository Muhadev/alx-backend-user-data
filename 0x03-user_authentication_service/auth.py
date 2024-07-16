#!/usr/bin/env python3
"""
auth module
"""
import bcrypt


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
