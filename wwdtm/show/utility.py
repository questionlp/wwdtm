# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Show Data Utility Functions."""

import datetime
from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from wwdtm.validation import valid_int_id


class ShowUtility:
    """Show information and utility class.

    Contains methods to convert between show ID and date, and to check
    if show IDs and dates exist.

    :param connect_dict: A dictionary containing database connection
        settings as required by MySQL Connector/Python
    :param database_connection: MySQL database connection object
    """

    def __init__(
        self,
        connect_dict: dict[str, Any] = None,
        database_connection: MySQLConnection | PooledMySQLConnection = None,
    ):
        """Class initialization method."""
        if connect_dict:
            self.connect_dict = connect_dict
            self.database_connection = connect(**connect_dict)
        elif database_connection:
            if not database_connection.is_connected():
                database_connection.reconnect()

            self.database_connection = database_connection

    def convert_date_to_id(self, year: int, month: int, day: int) -> int | None:
        """Converts a show date to the corresponding show ID.

        :param year: Year portion of a show date
        :param month: Month portion of a show date
        :param day: Day portion of a show date
        :return: Show ID if a corresponding value is found. Otherwise,
            ``None`` is returned
        """
        try:
            show_date = datetime.datetime(year, month, day)
        except ValueError:
            return None

        query = """
            SELECT showid FROM ww_shows WHERE showdate = %s LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query, (show_date.isoformat(),))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]

        return None

    def convert_id_to_date(self, show_id: int) -> str | None:
        """Converts a show ID to the corresponding show date.

        :param show_id: Show ID
        :return: Show date if a corresponding value is found. Otherwise,
            ``None`` is returned
        """
        if not valid_int_id(show_id):
            return None

        query = """
            SELECT showdate FROM ww_shows WHERE showid = %s LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query, (show_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0].isoformat()

        return None

    def date_exists(self, year: int, month: int, day: int) -> bool:
        """Validates if a show date exists.

        :param year: Year portion of a show date
        :param month: Month portion of a show date
        :param day: Day portion of a show date
        :return: ``True`` if the show date exists, otherwise ``False``
        """
        try:
            show_date = datetime.datetime(year, month, day)
        except ValueError:
            return False

        query = """
            SELECT showid FROM ww_shows WHERE showdate = %s LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query, (show_date.isoformat(),))
        result = cursor.fetchone()
        cursor.close()

        return bool(result)

    def id_exists(self, show_id: int) -> bool:
        """Validates if a show ID exists.

        :param show_id: Show ID
        :return: ``True`` if the show ID exists, otherwise ``False``
        """
        if not valid_int_id(show_id):
            return False

        query = """
            SELECT showid FROM ww_shows WHERE showid = %s LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query, (show_id,))
        result = cursor.fetchone()
        cursor.close()

        return bool(result)
