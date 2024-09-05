#!/usr/bin/env python3
"""
Auth class
"""

from flask import request
from typing import List, TypeVar

# Define a type variable for user type
User = TypeVar('User')


class Auth:
    """
    Manages API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required

        Args:
            path (str): The path to check
            excluded_paths (List[str]): A list of
            paths that do not require authentication

        Returns:
            bool: True if authentication is required, False otherwise
        """
        if path is None:
            return True

        if not excluded_paths:
            return True

        # Ensure path and excluded_paths are slash tolerant
        path = path.rstrip('/') + '/'

        for excluded_path in excluded_paths:
            if excluded_path.rstrip('/') + '/' == path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request

        Args:
            request (flask.Request, optional): The Flask
            request object. Defaults to None.

        Returns:
            str: The authorization header value, or None if not present
        """
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> User:
        """
        Retrieves the current user from the request

        Args:
            request (flask.Request, optional): The Flask
            request object. Defaults to None.

        Returns:
            User: None, indicating no user is retrieved
        """
        return None