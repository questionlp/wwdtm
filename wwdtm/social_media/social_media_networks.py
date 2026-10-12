# Copyright (c) 2018-2026 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Social Media Networks Data Retrieval Functions."""

from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


class SocialMediaNetworks:
    """Social media networks information retrieval class.

    Contains methods used to retrieve available social media networks.

        :param connect_dict: A dictionary containing database connection
            settings as required by MySQL Connector/Python
        :param database_connection: MySQL database connection object
    """

    def __init__(
        self,
        connect_dict: dict[str, Any] = None,
        database_connection: MySQLConnection | PooledMySQLConnection = None,
    ):
        if connect_dict:
            self.connect_dict = connect_dict
            self.database_connection = connect(**connect_dict)
        elif database_connection:
            if not database_connection.is_connected():
                database_connection.reconnect()

            self.database_connection = database_connection

    def retrieve_all(self) -> list[dict[int, str]]:
        """Retrieves all social media networks.

        :return: A list of dictionaries containing social media network
            IDs, names and slug strings
        """
        query = """
            SELECT networkid, network, networkslug
            FROM ww_socialmedianetworks
            ORDER BY networkid ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        networks = []
        for row in results:
            networks.append(
                {
                    "id": row["networkid"],
                    "network": row["network"],
                    "slug": row["networkslug"],
                }
            )

        return networks

    def retrieve_all_ids(self) -> list[int]:
        """Retrieves all social media network IDs, sorted by ID.

        :return: A list of social media network IDs as integers
        """
        cursor = self.database_connection.cursor(dictionary=False)
        query = """
            SELECT networkid
            FROM ww_socialmedianetworks
            ORDER BY networkid ASC;
            """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [row[0] for row in results]

    def retrieve_all_as_dict(self) -> dict[int, dict[str, str]]:
        """Retrieves all social media networks as a dictionary.

        :return: A dictionary of social media network IDs as keys each
            containing network name and slug key/values, ordered by
            social media network ID
        """
        query = """
            SELECT networkid, network, networkslug
            FROM ww_socialmedianetworks
            ORDER BY networkid ASC;
        """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        networks = {}
        for row in results:
            networks[row["networkid"]] = {
                "network": row["network"],
                "slug": row["networkslug"],
            }

        return networks

    def retrieve_all_network_names(self) -> list[str]:
        """Retrieves all social media network names.

        :return: A list of social media network names, ordered by
            social media network ID
        """
        query = """
            SELECT network
            FROM ww_socialmedianetworks
            ORDER BY networkid ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [row[0] for row in results]

    def retrieve_all_network_slugs(self) -> list[str]:
        """Retrieves all social media network slug strings.

        :return: A list of social media network slug strings,
            ordered by social media network ID
        """
        query = """
            SELECT networkslug
            FROM ww_socialmedianetworks
            ORDER BY networkid ASC;
        """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [row[0] for row in results]

    def retrieve_by_id(self, network_id: int) -> dict[int, str]:
        """Retrieves social media network information by ID.

        :param network_id: Social media network ID
        :return: A dictionary containing social media network ID,
            network name and slug strings
        """
        query = """
            SELECT networkid, network, networkslug
            FROM ww_socialmedianetworks
            WHERE networkid = %s
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (network_id,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return {}

        return {
            "id": result["networkid"],
            "network": result["network"],
            "slug": result["networkslug"],
        }

    def retrieve_by_slug(self, network_slug: str) -> dict[int, str]:
        """Retrieves social media network information by slug string.

        :param network_slug: Social media network slug string
        :return: A dictionary containing social media network ID,
            network name and slug strings
        """
        query = """
            SELECT networkid, network, networkslug
            FROM ww_socialmedianetworks
            WHERE networkslug = %s
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (network_slug,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return {}

        return {
            "id": result["networkid"],
            "network": result["network"],
            "slug": result["networkslug"],
        }
