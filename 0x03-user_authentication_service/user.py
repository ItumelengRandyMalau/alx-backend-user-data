#!/usr/bin/env python3
"""
Creates a SQLAlchemy model named User
for a database table named users
(using the mapping declaration of SQLAlchemy).
"""

from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import registry

# Step 1: Define the registry
mapper_registry = registry()

# Step 2: Define the metadata
metadata = MetaData()

# Step 3: Define the users table with columns
users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),  # Primary key (id) column
    Column('email', String(250), nullable=False),  # Non-nullable email column
    Column('hashed_password', String(250), nullable=False),  # Non-nullable password
    Column('session_id', String(250), nullable=True),  # Nullable session_id column
    Column('reset_token', String(250), nullable=True)  # Nullable reset_token column
)


# Step 4: Define the User class
class User:
    def __init__(self, email, hashed_password, reset_token=None,
                 session_id=None):
        """
        Initialize the User instance with the given parameters.

        Args:
            email (str): User's email
            hashed_password (str): User's hashed password
            session_id (str, optional): Session ID, can be None.
            reset_token (str, optional): Reset token, can be None.
        """
        self.email = email
        self.hashed_password = hashed_password
        self.session_id = session_id
        self.reset_token = reset_token

    def __repr__(self):
        """Provides a string representation of the User instance."""
        return (f"<User(id={self.id}, email='{self.email}')>")


# Step 5: Map the User class to the users table using registry
mapper_registry.map_imperatively(User, users_table)
