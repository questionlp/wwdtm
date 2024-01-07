# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Don't Tell Me! Stats Location Data Retrieval Functions."""
from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from wwdtm.location.recordings import LocationRecordings
from wwdtm.location.utility import LocationUtility
from wwdtm.validation import valid_int_id


class Location:
    """Location information retrieval class.

    Contains methods used to retrieve location IDs, venue names and
    locations, including city and state, and recording dates.

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

        self.recordings = LocationRecordings(
            database_connection=self.database_connection
        )
        self.utility = LocationUtility(database_connection=self.database_connection)

    def retrieve_all(self, sort_by_venue: bool = False) -> list[dict[str, int | str]]:
        """Retrieves location information for all locations.

        :param sort_by_venue: A boolean to determine if the returned
            list is sorted by venue first or by state and city first
        :return: A list of dictionaries containing location ID, venue
            name, city, state and slug string
        """
        query = """
            SELECT locationid AS id, city, state, venue,
            locationslug AS slug
            FROM ww_locations
            """

        if sort_by_venue:
            query = query + "ORDER BY venue ASC, city ASC, state ASC;"
        else:
            query = query + "ORDER BY state ASC, city ASC, venue ASC;"

        cursor = self.database_connection.cursor(named_tuple=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        locations = []
        for row in results:
            locations.append(
                {
                    "id": row.id,
                    "city": row.city,
                    "state": row.state,
                    "venue": row.venue,
                    "slug": row.slug
                    if row.slug
                    else self.utility.slugify_location(
                        location_id=row.id,
                        venue=row.venue,
                        city=row.city,
                        state=row.state,
                    ),
                }
            )

        return locations

    def retrieve_all_details(self, sort_by_venue: bool = False) -> list[dict[str, Any]]:
        """Retrieves location information and recordings for all locations.

        :param sort_by_venue: A boolean to determine if the returned
            list is sorted by venue first or by state and city first
        :return: A list of dictionaries containing location ID, venue
            name, city, state, slug string and a list of recordings
        """
        query = """
            SELECT locationid AS id, city, state, venue,
            locationslug AS slug
            FROM ww_locations
            """
        if sort_by_venue:
            query = query + "ORDER BY venue ASC, city ASC, state ASC;"
        else:
            query = query + "ORDER BY state ASC, city ASC, venue ASC;"

        cursor = self.database_connection.cursor(named_tuple=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        locations = []
        for row in results:
            locations.append(
                {
                    "id": row.id,
                    "city": row.city,
                    "state": row.state,
                    "venue": row.venue,
                    "slug": row.slug
                    if row.slug
                    else self.utility.slugify_location(
                        location_id=row.id,
                        venue=row.venue,
                        city=row.city,
                        state=row.state,
                    ),
                    "recordings": self.recordings.retrieve_recordings_by_id(row.id),
                }
            )

        return locations

    def retrieve_all_ids(self, sort_by_venue: bool = False) -> list[int]:
        """Retrieves all location IDs.

        :param sort_by_venue: A boolean to determine if the returned
            list is sorted by venue first or by state and city first
        :return: A list of location IDs as integers
        """
        query = "SELECT locationid FROM ww_locations "
        if sort_by_venue:
            query = query + "ORDER BY venue ASC, city ASC, state ASC;"
        else:
            query = query + "ORDER BY state ASC, city ASC, venue ASC;"

        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [v[0] for v in results]

    def retrieve_all_slugs(self, sort_by_venue: bool = False) -> list[str]:
        """Retrieves all location slug strings.

        :param sort_by_venue: A boolean to determine if the returned
            list is sorted by venue first or by state and city first
        :return: A list of location slug strings
        """
        query = "SELECT locationslug FROM ww_locations "
        if sort_by_venue:
            query = query + "ORDER BY venue ASC, city ASC, state ASC;"
        else:
            query = query + "ORDER BY state ASC, city ASC, venue ASC;"

        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [v[0] for v in results]

    def retrieve_by_id(self, location_id: int) -> dict[str, int | str]:
        """Retrieves location information.

        :param location_id: Location ID
        :return: A dictionary containing location ID, venue, city, state
            and slug string
        """
        if not valid_int_id(location_id):
            return {}

        query = """
            SELECT locationid AS id, city, state, venue,
            locationslug AS slug
            FROM ww_locations
            WHERE locationid = %s
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(named_tuple=True)
        cursor.execute(query, (location_id,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return {}

        return {
            "id": result.id,
            "city": result.city,
            "state": result.state,
            "venue": result.venue,
            "slug": result.slug
            if result.slug
            else self.utility.slugify_location(
                location_id=result.id,
                venue=result.venue,
                city=result.city,
                state=result.state,
            ),
        }

    def retrieve_by_slug(self, location_slug: str) -> dict[str, int | str]:
        """Retrieves location information.

        :param location_slug: Location slug string
        :return: A dictionary containing location ID, venue, city, state
            and slug string
        """
        try:
            slug = location_slug.strip()
            if not slug:
                return {}
        except AttributeError:
            return {}

        id_ = self.utility.convert_slug_to_id(slug)
        if not id_:
            return {}

        return self.retrieve_by_id(id_)

    def retrieve_details_by_id(self, location_id: int) -> dict[str, Any]:
        """Retrieves location information and recordings.

        :param location_id: Location ID
        :return: A dictionary containing location ID, venue name, city,
            state, slug string and a list of recordings
        """
        if not valid_int_id(location_id):
            return {}

        info = self.retrieve_by_id(location_id)
        if not info:
            return {}

        info["recordings"] = self.recordings.retrieve_recordings_by_id(location_id)

        return info

    def retrieve_details_by_slug(self, location_slug: str) -> dict[str, Any]:
        """Retrieves location information and recordings.

        :param location_slug: Location slug string
        :return: A dictionary containing location ID, venue name, city,
            state, slug string and a list of recordings
        """
        try:
            slug = location_slug.strip()
            if not slug:
                return {}
        except AttributeError:
            return {}

        id_ = self.utility.convert_slug_to_id(slug)
        if not id_:
            return {}

        return self.retrieve_details_by_id(id_)
