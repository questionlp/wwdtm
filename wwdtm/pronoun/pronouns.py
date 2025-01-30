# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Pronouns Data Retrieval Functions."""

from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


class Pronouns:
    """Pronouns information retrieval class.

    Contains methods used to retrieve available pronouns.

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

    def retrieve_all(self) -> list[dict[int, str]]:
        """Retrieves all pronouns.

        :return: A list of dictionaries containing pronouns IDs and
            corresponding pronouns
        """
        query = """
            SELECT pronounsid, pronouns
            FROM ww_pronouns
            ORDER BY pronounsid ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        pronouns = []
        for row in results:
            pronouns.append(
                {
                    "id": row["pronounsid"],
                    "pronouns": row["pronouns"],
                }
            )

        return pronouns

    def retrieve_all_ids(self) -> list[int]:
        """Retrieves all pronouns IDs, sorted by ID.

        :return: A list of pronouns IDs as integers
        """
        cursor = self.database_connection.cursor(dictionary=False)
        query = """
            SELECT pronounsid
            FROM ww_pronouns
            ORDER BY pronounsid ASC;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [row[0] for row in results]

    def retrieve_all_as_dict(self) -> dict[int, str]:
        """Retrieves all pronouns as a dictionary.

        :return: A dictionary of pronouns IDs and pronoun strings,
            ordered by pronouns ID
        """
        query = """
            SELECT pronounsid, pronouns
            FROM ww_pronouns
            ORDER BY pronounsid ASC;
        """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        return {row["pronounsid"]: row["pronouns"] for row in results}

    def retrieve_all_pronouns(self) -> list[str]:
        """Retrieves all pronouns names.

        :return: A list of pronouns names, ordered by pronouns ID
        """
        query = """
            SELECT pronouns
            FROM ww_pronouns
            ORDER BY pronounsid ASC;
        """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [row[0] for row in results]

    def retrieve_by_id(self, pronouns_id: int) -> dict[int, str]:
        """Retrieves pronouns information.

        :param pronouns_id: Pronouns ID
        :return: A dictionary containing pronouns ID and corresponding
            pronouns
        """
        query = """
            SELECT pronounsid, pronouns
            FROM ww_pronouns
            WHERE pronounsid = %s
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (pronouns_id,))
        result = cursor.fetchone()

        if not result:
            return {}

        return {
            "id": result["pronounsid"],
            "pronouns": result["pronouns"],
        }
