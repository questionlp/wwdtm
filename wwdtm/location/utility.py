# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Location Data Utility Functions."""

from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from slugify import slugify

from wwdtm.validation import valid_int_id


class LocationUtility:
    """Location information and utilities class.

    This class contains supporting functions used to check whether
    a location ID or slug string exists or to convert an ID to a slug
    string, or vice versa.

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

    def convert_id_to_slug(self, location_id: int) -> str | None:
        """Converts a location ID to the corresponding location slug string.

        :param location_id: Location ID
        :return: Location slug string if a corresponding value is found.
            Otherwise, ``None`` is returned
        """
        if not valid_int_id(location_id):
            return None

        query = """
            SELECT locationslug FROM ww_locations WHERE locationid = %s LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query, (location_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]

        return None

    def convert_slug_to_id(self, location_slug: str) -> int | None:
        """Converts a location slug string to the corresponding location ID.

        :param location_slug: Location slug string
        :return: Location ID if a corresponding value is found.
            Otherwise, ``None`` is returned
        """
        try:
            slug = location_slug.strip()
            if not slug:
                return None
        except ValueError:
            return None

        query = """
            SELECT locationid FROM ww_locations WHERE locationslug = %s LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query, (slug,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]

        return None

    def id_exists(self, location_id: int) -> bool:
        """Validates if a location ID exists.

        :param location_id: Location ID
        :return: ``True`` if the ID exists, otherwise ``False``
        """
        if not valid_int_id(location_id):
            return False

        query = """
            SELECT locationid FROM ww_locations WHERE locationid = %s LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query, (location_id,))
        result = cursor.fetchone()
        cursor.close()

        return bool(result)

    def slug_exists(self, location_slug: str) -> bool:
        """Validates if a location slug string exists.

        :param location_slug: Location slug string
        :return: ``True`` if the slug string exists, otherwise ``False``
        """
        try:
            slug = location_slug.strip()
            if not slug:
                return False
        except ValueError:
            return False

        query = """
            SELECT locationslug FROM ww_locations
            WHERE locationslug = %s
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query, (slug,))
        result = cursor.fetchone()
        cursor.close()

        return bool(result)

    @staticmethod
    def slugify_location(
        location_id: int = None,
        venue: str = None,
        city: str = None,
        state: str = None,
    ) -> str:
        """Generates a slug string using the location ID, venue, city and/or state.

        :param location_id: Location ID
        :param venue: Location venue name
        :param city: City where the location venue is located
        :param state: State where the location venue is located
        :return: Location slug string
        :raises: ValueError
        """
        if venue and city and state:
            return slugify(f"{venue} {city} {state}")
        elif venue and city and not state:
            return slugify(f"{venue} {city}")
        elif location_id and venue and (not city and not state):
            return slugify(f"{id}-{venue}")
        elif location_id and city and state and not venue:
            return slugify(f"{id} {city} {state}")
        elif location_id:
            return f"location-{location_id}"
        else:
            raise ValueError("Invalid location information provided")
