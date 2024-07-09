#!/usr/bin/env python3
"""
Route module for the API
"""
from flask import request
from typing import List, TypeVar


class Auth():
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        This method will later be used to check if a path
        requires authentication.
        Currently, it just returns False.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        This method will later be used to get the Authorization
        header from the request.
        Currently, it just returns None.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        This method will later be used to get the current
        user from the request.
        Currently, it just returns None.
        """
        return None
