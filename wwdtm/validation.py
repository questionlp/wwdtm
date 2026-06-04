# Copyright (c) 2018-2026 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Type validation module."""

from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from . import MINIMUM_DATABASE_VERSION, database_version


def check_database_version(
    connect_dict: dict[str, Any] = None,
    database_connection: MySQLConnection | PooledMySQLConnection = None,
) -> bool:
    """Checks current database version against minimum database version.

    :param connect_dict: A dictionary containing database connection
        settings as required by MySQL Connector/Python
    :param database_connection: MySQL database connection object
    :return: True or False, based on if the current database version
        meets the library's minimum database version
    """
    if not connect_dict and not database_connection:
        return False

    if connect_dict and not database_connection:
        database_connection = connect(**connect_dict)

    current_database_version = database_version(database_connection=database_connection)

    return (
        current_database_version
        and current_database_version >= MINIMUM_DATABASE_VERSION
    )


def valid_int_id(int_id: int) -> bool:
    """Validates an ID value as a signed 32-bit integer used in ID fields in MySQL tables.

    :param int_id: ID number to validate
    :return: True or False, based on if the integer falls inclusively
        between 0 and 2147483647
    """
    try:
        if not int_id:
            return False

        int_id_ = int(int_id)
    except ValueError:
        return False

    # Minimum value of a signed INT in MySQL/MariaDB is 0 and the
    # maximum value of signed INT type in MySQL/MariaDB is (2**31) - 1,
    # or 2147483647
    return 0 <= int_id_ <= (2**31 - 1)


def valid_rounding_digits(
    number_digits: int, min_digits: int = 0, max_digits: int = 20
) -> bool:
    """Validates number of rounding digits is within the min/max value.

    :param number_digits: Number of rounding digits to validate
    :param min_digits: Minimum number of rounding digits
    :param max_digits: Maximum number of rounding digits
    :return: True or False, based on if the number of rounding digits
        is within the min/max value and if it is an integer
    """
    if number_digits is None:
        return False

    if not isinstance(number_digits, int):
        return False

    return min_digits <= number_digits <= max_digits
