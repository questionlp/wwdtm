# Copyright (c) 2018-2026 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats External Sites Data Retrieval Functions."""

from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


class ExternalSites:
    """External sites information retrieval class.

    Contains methods used to retrieve available external sites.

    :param connect_dict: A dictionary containing database connection
        settings as required by MySQL Connector/Python
    :param database_connection: MySQL database connection object

    .. version-added:: 3.4.4
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
        """Retrieves all external sites, sorted by site ID.

        :return: A list of dictionaries each containing external site
            ID, site name, slug string, social media network flag and
            icon name

        .. version-added:: 3.4.4
        """
        query = """
            SELECT siteid, site, siteslug, socialmedia, iconname
            FROM ww_externalsites
            ORDER BY siteid ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        sites = []
        for row in results:
            sites.append(
                {
                    "id": row["siteid"],
                    "site": row["site"],
                    "slug": row["siteslug"],
                    "social_media": bool(row["socialmedia"]),
                    "icon": row["iconname"],
                }
            )

        return sites

    def retrieve_all_ids(self) -> list[int]:
        """Retrieves all external site IDs, sorted by site ID.

        :return: A list of external site IDs

        .. version-added:: 3.4.4
        """
        cursor = self.database_connection.cursor(dictionary=False)
        query = """
            SELECT siteid
            FROM ww_externalsites
            ORDER BY siteid ASC;
            """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [row[0] for row in results]

    def retrieve_all_as_dict(self) -> dict[int, dict[str, str]]:
        """Retrieves all external sites as a dictionary, sorted by site ID.

        :return: A dictionary of external site IDs as keys, each
            containing site name, slug string, social network flag and
            icon name

        .. version-added:: 3.4.4
        """
        query = """
            SELECT siteid, site, siteslug, socialmedia, iconname
            FROM ww_externalsites
            ORDER BY siteid ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        sites = {}
        for row in results:
            sites[row["siteid"]] = {
                "site": row["site"],
                "slug": row["siteslug"],
                "social_media": bool(row["socialmedia"]),
                "icon": row["iconname"],
            }

        return sites

    def retrieve_all_site_names(self) -> list[str]:
        """Retrieves all external sites, ordered by site ID.

        :return: A list of external site names

        .. version-added:: 3.4.4
        """
        query = """
            SELECT site
            FROM ww_externalsites
            ORDER BY siteid ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [row[0] for row in results]

    def retrieve_all_site_slugs(self) -> list[str]:
        """Retrieves all external site slug strings, ordered by site ID.

        :return: A list of extern media site slug strings

        .. version-added:: 3.4.4
        """
        query = """
            SELECT siteslug
            FROM ww_externalsites
            ORDER BY siteid ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [row[0] for row in results]

    def retrieve_by_id(self, site_id: int) -> dict[int, str]:
        """Retrieves external site information by site ID.

        :param site_id: External site ID
        :return: A dictionary containing external site ID, site name,
            slug string, social media flag and icon name

        .. version-added:: 3.4.4
        """
        query = """
            SELECT siteid, site, siteslug, socialmedia, iconname
            FROM ww_externalsites
            WHERE siteid = %s
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (site_id,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return {}

        return {
            "id": result["siteid"],
            "site": result["site"],
            "slug": result["siteslug"],
            "social_media": bool(result["socialmedia"]),
            "icon": result["iconname"],
        }

    def retrieve_by_slug(self, site_slug: str) -> dict[int, str]:
        """Retrieves external site information by site slug string.

        :param site_id: External site slug string
        :return: A dictionary containing external site ID, site name,
            slug string, social media flag and icon name

        .. version-added:: 3.4.4
        """
        query = """
            SELECT siteid, site, siteslug, socialmedia, iconname
            FROM ww_externalsites
            WHERE siteslug = %s
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (site_slug,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return {}

        return {
            "id": result["siteid"],
            "site": result["site"],
            "slug": result["siteslug"],
            "social_media": bool(result["socialmedia"]),
            "icon": result["iconname"],
        }
