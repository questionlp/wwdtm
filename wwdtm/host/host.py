# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Don't Tell Me! Stats Host Data Retrieval Functions."""
from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from slugify import slugify

from wwdtm.host.appearances import HostAppearances
from wwdtm.host.utility import HostUtility
from wwdtm.validation import valid_int_id


class Host:
    """Host information retrieval class.

    Contains methods used to retrieve host information, including IDs,
    names, slug strings and appearances.

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

        self.appearances = HostAppearances(database_connection=self.database_connection)
        self.utility = HostUtility(database_connection=self.database_connection)

    def retrieve_all(self) -> list[dict[str, int | str]]:
        """Retrieves host information for all hosts.

        :return: A list of dictionaries containing host ID, name, slug
            string and gender for each host
        """
        query = """
            SELECT hostid AS id, host AS name, hostslug AS slug,
            hostgender AS gender
            FROM ww_hosts
            ORDER BY host ASC;
            """
        cursor = self.database_connection.cursor(named_tuple=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        hosts = []
        for row in results:
            hosts.append(
                {
                    "id": row.id,
                    "name": row.name,
                    "slug": row.slug if row.slug else slugify(row.name),
                    "gender": row.gender,
                }
            )

        return hosts

    def retrieve_all_details(self) -> list[dict[str, Any]]:
        """Retrieves host information and appearances for all hosts.

        :return: A list of dictionaries containing host ID, name, slug
            string, gender and a list of appearances with show flags for
            each host
        """
        query = """
            SELECT hostid AS id, host AS name, hostslug AS slug,
            hostgender AS gender
            FROM ww_hosts
            ORDER BY host ASC;
            """
        cursor = self.database_connection.cursor(named_tuple=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        hosts = []
        for row in results:
            hosts.append(
                {
                    "id": row.id,
                    "name": row.name,
                    "slug": row.slug if row.slug else slugify(row.name),
                    "gender": row.gender,
                    "appearances": self.appearances.retrieve_appearances_by_id(row.id),
                }
            )

        return hosts

    def retrieve_all_ids(self) -> list[int]:
        """Retrieves all host IDs, sorted by host name.

        :return: A list of host IDs as integers
        """
        cursor = self.database_connection.cursor(dictionary=False)
        query = "SELECT hostid FROM ww_hosts ORDER BY host ASC;"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [v[0] for v in results]

    def retrieve_all_slugs(self) -> list[str]:
        """Retrieves all host slug strings, sorted by host name.

        :return: A list of host slug strings
        """
        query = """
            SELECT hostslug FROM ww_hosts ORDER BY host ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [v[0] for v in results]

    def retrieve_by_id(self, host_id: int) -> dict[str, Any]:
        """Retrieves host information.

        :param host_id: Host ID
        :return: A dictionary containing host ID, name, gender and slug string
        """
        if not valid_int_id(host_id):
            return {}

        query = """
            SELECT hostid AS id, host AS name, hostslug AS slug,
            hostgender AS gender
            FROM ww_hosts
            WHERE hostid = %s
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(named_tuple=True)
        cursor.execute(query, (host_id,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return {}

        return {
            "id": result.id,
            "name": result.name,
            "slug": result.slug if result.slug else slugify(result.name),
            "gender": result.gender,
        }

    def retrieve_by_slug(self, host_slug: str) -> dict[str, Any]:
        """Retrieves host information.

        :param host_slug: Host slug string
        :return: A dictionary containing host ID, name, gender and slug
            string
        """
        try:
            slug = host_slug.strip()
            if not slug:
                return {}
        except AttributeError:
            return {}

        id_ = self.utility.convert_slug_to_id(slug)
        if not id_:
            return {}

        return self.retrieve_by_id(id_)

    def retrieve_details_by_id(self, host_id: int) -> dict[str, Any]:
        """Retrieves host information and appearances.

        :param host_id: Host ID
        :return: A dictionary containing host ID, name, gender, slug
            string and a list of appearances with show flags
        """
        if not valid_int_id(host_id):
            return {}

        info = self.retrieve_by_id(host_id)
        if not info:
            return {}

        info["appearances"] = self.appearances.retrieve_appearances_by_id(host_id)

        return info

    def retrieve_details_by_slug(self, host_slug: str) -> dict[str, Any]:
        """Retrieves host information and appearances.

        :param host_slug: Host slug string
        :return: A dictionary containing host ID, name, slug string and
            a list of appearances with show flags
        """
        try:
            slug = host_slug.strip()
            if not slug:
                return {}
        except AttributeError:
            return {}

        id_ = self.utility.convert_slug_to_id(slug)
        if not id_:
            return {}

        return self.retrieve_details_by_id(id_)
