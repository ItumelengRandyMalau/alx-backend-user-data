#!/usr/bin/env python3
"""
This module contains a function to obfuscate specified fields in log messages.
"""
import re
import logging
from typing import List
import mysql.connector
import os


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """
    Returns the log message with specified fields obfuscated.

    Args:
        fields (List[str]): List of field names to obfuscate.
        redaction (str): String to replace the field values with.
        message (str): The log message to be processed.
        separator (str): Character that separates
        the fields in the log message.

    Returns:
        str: The log message with specified fields obfuscated.
    """
    pattern = '|'.join([f"{field}=[^{separator}]*" for field in fields])
    return re.sub(pattern,
                  lambda m: f"{m.group(0).split('=')[0]}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Redacts specified fields in the log message.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log record with specified fields redacted.
        """
        original_message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION,
                            original_message, self.SEPARATOR)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """
    Creates a logger named 'user_data'
    that logs up to INFO level and uses a
    RedactingFormatter to obfuscate PII fields.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a MySQL database connection using
    credentials from environment variables.

    Returns:
        mysql.connector.connection.MySQLConnection:
        Configured MySQL database connection.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


def main():
    """ Main function """
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    logger = get_logger()

    for row in rows:
        message = "; ".join([f"{key}={value}" for key,
                             value in row.items()]) + ";"
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
