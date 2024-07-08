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
