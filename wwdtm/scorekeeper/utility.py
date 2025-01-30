# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Scorekeeper Data Utility Functions."""

from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from wwdtm.validation import valid_int_id


class ScorekeeperUtility:
    """Scorekeeper information and utilities class.

    Contains methods used to convert between scorekeeper ID and slug
    strings, and to check if scorekeeper IDs and slug strings exist.

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

    def convert_id_to_slug(self, scorekeeper_id: int) -> str | None:
        """Converts a scorekeeper ID to the corresponding scorekeeper slug string.

        :param scorekeeper_id: Scorekeeper ID
        :return: Scorekeeper slug string if a corresponding value is
            found. Otherwise, ``None`` is returned
        """
        if not valid_int_id(scorekeeper_id):
            return None

        query = """
            SELECT scorekeeperslug FROM ww_scorekeepers
            WHERE scorekeeperid = %s
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query, (scorekeeper_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]

        return None

    def convert_slug_to_id(self, scorekeeper_slug: str) -> int | None:
        """Converts a scorekeeper slug string to the corresponding scorekeeper ID.

        :param scorekeeper_slug: Scorekeeper slug string
        :return: Scorekeeper ID as an integer if a corresponding value
            is found. Otherwise, ``None`` is returned
        """
        try:
            slug = scorekeeper_slug.strip()
            if not slug:
                return None
        except ValueError:
            return None

        query = """
            SELECT scorekeeperid FROM ww_scorekeepers
            WHERE scorekeeperslug = %s
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query, (slug,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]

        return None

    def id_exists(self, scorekeeper_id: int) -> bool:
        """Validates if a scorekeeper ID exists.

        :param scorekeeper_id: Scorekeeper ID
        :return: ``True`` if the ID exists, otherwise ``False``
        """
        if not valid_int_id(scorekeeper_id):
            return False

        query = """
            SELECT scorekeeperid FROM ww_scorekeepers
            WHERE scorekeeperid = %s
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query, (scorekeeper_id,))
        result = cursor.fetchone()
        cursor.close()

        return bool(result)

    def slug_exists(self, scorekeeper_slug: str) -> bool:
        """Validates if a scorekeeper slug string exists.

        :param scorekeeper_slug: Scorekeeper slug string
        :return: ``True`` if the slug string exists, otherwise ``False``
        """
        try:
            slug = scorekeeper_slug.strip()
            if not slug:
                return False
        except ValueError:
            return False

        query = """
            SELECT scorekeeperslug FROM ww_scorekeepers
            WHERE scorekeeperslug = %s
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query, (slug,))
        result = cursor.fetchone()
        cursor.close()

        return bool(result)
