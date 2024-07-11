#!/usr/bin/env python3
"""
SessionAuth module for the API
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """SessionAuth class for session-based authentication"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for a user_id

        Args:
            user_id (str): The user ID for which to create a session

        Returns:
            str: The session ID or None if user_id is None or not a string
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
