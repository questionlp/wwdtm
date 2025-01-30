# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Host Data Utility Functions."""

from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from wwdtm.validation import valid_int_id


class HostUtility:
    """Host information and utilities class.

    Contains methods used to convert between host ID and slug strings,
    and to check if host IDs and slug strings exist.

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

    def convert_id_to_slug(self, host_id: int) -> str | None:
        """Converts a host ID to the corresponding host slug string.

        :param host_id: Host ID
        :return: Host slug string if a corresponding value is found.
            Otherwise, ``None`` is returned
        """
        if not valid_int_id(host_id):
            return None

        query = """
            SELECT hostslug FROM ww_hosts WHERE hostid = %s LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query, (host_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]

        return None

    def convert_slug_to_id(self, host_slug: str) -> int | None:
        """Converts a host slug string to the corresponding host ID.

        :param host_slug: Host slug string
        :return: Host ID as an integer if a corresponding value is
            found. Otherwise, ``None`` is returned
        """
        try:
            slug = host_slug.strip()
            if not slug:
                return None
        except ValueError:
            return None

        query = """
            SELECT hostid FROM ww_hosts WHERE hostslug = %s LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query, (slug,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]

        return None

    def id_exists(self, host_id: int) -> bool:
        """Validates if a host ID exists.

        :param host_id: Host ID
        :return: ``True`` if the ID exists, otherwise ``False``
        """
        if not valid_int_id(host_id):
            return False

        query = """
            SELECT hostid FROM ww_hosts WHERE hostid = %s LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query, (host_id,))
        result = cursor.fetchone()
        cursor.close()

        return bool(result)

    def slug_exists(self, host_slug: str) -> bool:
        """Validates if a host slug string exists.

        :param host_slug: Host slug string
        :return: ``True`` if the slug string exists, otherwise ``False``
        """
        try:
            slug = host_slug.strip()
            if not slug:
                return False
        except ValueError:
            return False

        query = """
            SELECT hostslug FROM ww_hosts WHERE hostslug = %s LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query, (slug,))
        result = cursor.fetchone()
        cursor.close()

        return bool(result)
