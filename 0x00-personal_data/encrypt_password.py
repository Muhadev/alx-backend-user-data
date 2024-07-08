#!/usr/bin/env python3
"""
Encrypt password module
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt and returns the
    salted, hashed password as a byte string.

    Arguments:
    password -- the password to hash
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates that the provided password matches the hashed password.

    Arguments:
    hashed_password -- the hashed password to check against
    password -- the password to validate
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
