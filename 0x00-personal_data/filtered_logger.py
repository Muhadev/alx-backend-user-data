#!/usr/bin/env python3
"""
filtered_logger module
"""

import logging
import re
from typing import List


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """
    Returns the log message obfuscated by replacing
    the values of specified fields with a redaction string.

    Arguments:
    fields -- a list of strings representing all fields to obfuscate
    redaction -- a string representing by what the field will be obfuscated
    message -- a string representing the log line
    separator -- a string representing by which character is
    separating all fields in the log line (message)
    """
    pattern = '|'.join([f'(?<={field}=)[^{separator}]+' for field in fields])
    return re.sub(pattern, redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.msg,
            self.SEPARATOR
        )
        return super(RedactingFormatter, self).format(record)
