#!/usr/bin/env python3
"""
Route module for the API
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """
    Manage API authentication methods
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        This method will later be used to check if a path
        requires authentication.
        Currently, it just returns False.
        """
        if path is None:
            return True
        if not excluded_paths or excluded_paths is None:
            return True
        # Ensure path has a trailing slash
        if path[-1] != '/':
            path += '/'
        for excluded_path in excluded_paths:
            if excluded_path.endswith('/'):
                if path == excluded_path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        This method returns the value of the header
        request Authorization
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        This method will later be used to get the current
        user from the request.
        Currently, it just returns None.
        """
        return None
