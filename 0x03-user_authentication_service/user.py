#!/usr/bin/env python3
"""
Creates a SQLAlchemy model named User
for a database table named users
(using the mapping declaration of SQLAlchemy).
"""

from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """Creates table for users
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False)
    hash_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
