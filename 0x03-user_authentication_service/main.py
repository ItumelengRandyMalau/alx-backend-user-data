#!/usr/bin/env python3
"""
Main file
"""
from user import User

print(User.__table__)

for column in User.__table__.columns:
    print("{}: {}".format(column, column.type))
