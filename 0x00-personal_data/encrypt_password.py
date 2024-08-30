#!/usr/bin/env python3
"""
Module for password encryption and validation using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt with a randomly generated salt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The salted, hashed password.
    """
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the generated salt
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates that the provided password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The password to validate.

    Returns:
        bool: True if the password matches the
        hashed password, False otherwise.
    """
    # Check if the provided password matches the hashed password
    return bcrypt.checkpw(password.encode(), hashed_password)
