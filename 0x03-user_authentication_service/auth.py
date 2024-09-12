#!/usr/bin/env python3

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
import bcrypt
import uuid
from typing import Optional


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Hashes a password with bcrypt."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
 