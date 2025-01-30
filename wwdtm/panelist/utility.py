# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Panelist Data Utility Functions."""

from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from wwdtm.validation import valid_int_id


class PanelistUtility:
    """Panelist information and utilities class.

    Contains methods used to convert between panelist ID and slug
    strings, and to check if panelist IDs and slug strings exist.

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

    def convert_id_to_slug(self, panelist_id: int) -> str | None:
        """Converts a panelist ID to the corresponding panelist slug string.

        :param panelist_id: Panelist ID
        :return: Panelist slug string if a corresponding value is found.
            Otherwise, ``None`` is returned
        """
        if not valid_int_id(panelist_id):
            return None

        cursor = self.database_connection.cursor(dictionary=False)
        query = """
            SELECT panelistslug FROM ww_panelists WHERE panelistid = %s LIMIT 1;
            """
        cursor.execute(query, (panelist_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]

        return None

    def convert_slug_to_id(self, panelist_slug: str) -> int | None:
        """Converts a panelist slug string to the corresponding panelist ID.

        :param panelist_slug: Panelist slug string
        :return: Panelist ID if a corresponding value is found.
            Otherwise, ``None`` is returned
        """
        try:
            slug = panelist_slug.strip()
            if not slug:
                return None
        except ValueError:
            return None

        cursor = self.database_connection.cursor(dictionary=False)
        query = """
            SELECT panelistid FROM ww_panelists WHERE panelistslug = %s LIMIT 1;
            """
        cursor.execute(query, (slug,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]

        return None

    def id_exists(self, panelist_id: int) -> bool:
        """Validates if a panelist ID exists.

        :param panelist_id: Panelist ID
        :return: ``True`` if the ID exists, otherwise ``False``
        """
        if not valid_int_id(panelist_id):
            return False

        cursor = self.database_connection.cursor(dictionary=False)
        query = """
            SELECT panelistid FROM ww_panelists WHERE panelistid = %s LIMIT 1;
            """
        cursor.execute(query, (panelist_id,))
        result = cursor.fetchone()
        cursor.close()

        return bool(result)

    def slug_exists(self, panelist_slug: str) -> bool:
        """Validates if a panelist slug string exists.

        :param panelist_slug: Panelist slug string
        :return: ``True`` if the slug string exists, otherwise ``False``
        """
        try:
            slug = panelist_slug.strip()
            if not slug:
                return False
        except ValueError:
            return False

        cursor = self.database_connection.cursor(dictionary=False)
        query = """
            SELECT panelistslug FROM ww_panelists
            WHERE panelistslug = %s
            LIMIT 1;
            """
        cursor.execute(query, (slug,))
        result = cursor.fetchone()
        cursor.close()

        return bool(result)
