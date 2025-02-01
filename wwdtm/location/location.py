# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Location Data Retrieval Functions."""

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
            SELECT l.locationid AS id, l.city, l.state,
            pa.name AS state_name, l.venue, l.latitude, l.longitude,
            l.locationslug AS slug
            FROM ww_locations l
            LEFT JOIN ww_postal_abbreviations pa ON pa.postal_abbreviation = l.state
            """

        if sort_by_venue:
            query = query + "ORDER BY l.venue ASC, l.city ASC, pa.name ASC;"
        else:
            query = query + "ORDER BY pa.name ASC, l.city ASC, l.venue ASC;"

        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        locations = []
        for row in results:
            if not row["latitude"] and not row["longitude"]:
                coordinates = None
            else:
                coordinates = {
                    "latitude": row["latitude"] if row["latitude"] else None,
                    "longitude": row["longitude"] if row["longitude"] else None,
                }

            locations.append(
                {
                    "id": row["id"],
                    "city": row["city"],
                    "state": row["state"],
                    "state_name": row["state_name"],
                    "venue": row["venue"],
                    "coordinates": coordinates,
                    "slug": (
                        row["slug"]
                        if row["slug"]
                        else self.utility.slugify_location(
                            location_id=row["id"],
                            venue=row["venue"],
                            city=row["city"],
                            state=row["state"],
                        )
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
            SELECT l.locationid AS id, l.city, l.state,
            pa.name AS state_name, l.venue, l.latitude, l.longitude,
            l.locationslug AS slug
            FROM ww_locations l
            LEFT JOIN ww_postal_abbreviations pa ON pa.postal_abbreviation = l.state
            """
        if sort_by_venue:
            query = query + " ORDER BY l.venue ASC, l.city ASC, pa.name ASC;"
        else:
            query = query + " ORDER BY pa.name ASC, l.city ASC, l.venue ASC;"

        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        locations = []
        for row in results:
            if not row["latitude"] and not row["longitude"]:
                coordinates = None
            else:
                coordinates = {
                    "latitude": row["latitude"] if row["latitude"] else None,
                    "longitude": row["longitude"] if row["longitude"] else None,
                }

            locations.append(
                {
                    "id": row["id"],
                    "city": row["city"],
                    "state": row["state"],
                    "state_name": row["state_name"],
                    "venue": row["venue"],
                    "coordinates": coordinates,
                    "slug": (
                        row["slug"]
                        if row["slug"]
                        else self.utility.slugify_location(
                            location_id=row["id"],
                            venue=row["venue"],
                            city=row["city"],
                            state=row["state"],
                        )
                    ),
                    "recordings": self.recordings.retrieve_recordings_by_id(row["id"]),
                }
            )

        return locations

    def retrieve_all_ids(self, sort_by_venue: bool = False) -> list[int]:
        """Retrieves all location IDs.

        :param sort_by_venue: A boolean to determine if the returned
            list is sorted by venue first or by state and city first
        :return: A list of location IDs as integers
        """
        query = """
            SELECT l.locationid
            FROM ww_locations l
            LEFT JOIN ww_postal_abbreviations pa ON pa.postal_abbreviation = l.state
            """
        if sort_by_venue:
            query = query + " ORDER BY l.venue ASC, l.city ASC, pa.name ASC;"
        else:
            query = query + " ORDER BY pa.name ASC, l.city ASC, l.venue ASC;"

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
        query = """
            SELECT l.locationslug
            FROM ww_locations l
            LEFT JOIN ww_postal_abbreviations pa ON pa.postal_abbreviation = l.state
            """
        if sort_by_venue:
            query = query + " ORDER BY l.venue ASC, l.city ASC, pa.name ASC;"
        else:
            query = query + " ORDER BY pa.name ASC, l.city ASC, l.venue ASC;"

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
            SELECT l.locationid AS id, l.city, l.state,
            pa.name AS state_name, l.venue, l.latitude, l.longitude,
            l.locationslug AS slug
            FROM ww_locations l
            LEFT JOIN ww_postal_abbreviations pa ON pa.postal_abbreviation = l.state
            WHERE l.locationid = %s
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (location_id,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return {}

        if not result["latitude"] and not result["longitude"]:
            coordinates = None
        else:
            coordinates = {
                "latitude": result["latitude"] if result["latitude"] else None,
                "longitude": result["longitude"] if result["longitude"] else None,
            }

        return {
            "id": result["id"],
            "city": result["city"],
            "state": result["state"],
            "state_name": result["state_name"],
            "venue": result["venue"],
            "coordinates": coordinates,
            "slug": (
                result["slug"]
                if result["slug"]
                else self.utility.slugify_location(
                    location_id=result["id"],
                    venue=result["venue"],
                    city=result["city"],
                    state=result["state"],
                )
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

    def retrieve_postal_abbreviations(self) -> dict[str, dict[str, str]]:
        """Retrieves postal abbreviations, corresponding names and countries.

        :return: A dictionary containing postal abbreviation as keys
            and corresponding name and country as values.
        """
        query = """
            SELECT postal_abbreviation, name, country
            FROM ww_postal_abbreviations
            ORDER BY postal_abbreviation ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return None

        abbreviations = {}
        for row in results:
            abbreviations[row["postal_abbreviation"]] = {
                "name": row["name"],
                "country": row["country"],
            }

        return abbreviations

    def retrieve_postal_abbreviations_list(self) -> list[dict[str, str]]:
        """Retrieves postal abbreviations, corresponding name and countries as a list.

        :return: A list of dictionaries, each containing postal abbreviation,
            corresponding name and country.
        """
        _postal_abbreviations = self.retrieve_postal_abbreviations()

        if not _postal_abbreviations:
            return None

        abbreviations = []
        for abbreviation in _postal_abbreviations:
            abbreviations.append(
                {
                    "postal_abbreviation": abbreviation,
                    "name": _postal_abbreviations[abbreviation]["name"],
                    "country": _postal_abbreviations[abbreviation]["country"],
                }
            )

        return abbreviations

    def retrieve_postal_details_by_abbreviation(
        self,
        abbreviation: str,
    ) -> dict[str, str]:
        """Retrieves postal abbreviation information for a given abbreviation.

        :param abbreviation: Postal Abbreviation
        :return: A dictionary containing postal abbreviation,
            corresponding name, and country.
        """
        if not abbreviation:
            return None

        query = """
            SELECT postal_abbreviation, name, country
            FROM ww_postal_abbreviations
            WHERE postal_abbreviation = %s
            ORDER BY postal_abbreviation ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (abbreviation,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return None

        return {
            "postal_abbreviation": result["postal_abbreviation"],
            "name": result["name"],
            "country": result["country"],
        }

    def retrieve_random_id(self) -> int:
        """Retrieves an ID for a random location.

        :return: ID for a random location.
        """
        query = """
            SELECT locationid FROM ww_locations
            WHERE locationslug <> 'tbd'
            ORDER BY RAND()
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return None

        return result[0]

    def retrieve_random_slug(self) -> str:
        """Retrieves a slug string for a random location.

        :return: Slug string for a random location.
        """
        query = """
            SELECT locationslug FROM ww_locations
            WHERE locationslug <> 'tbd'
            ORDER BY RAND()
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return None

        return result[0]

    def retrieve_random(self) -> dict[str, int | str]:
        """Retrieves information for a random location.

        :return: A dictionary containing location ID, venue, city, state
            and slug string
        """
        _id = self.retrieve_random_id()

        if not _id:
            return None

        return self.retrieve_by_id(location_id=_id)

    def retrieve_random_details(self) -> dict[str, Any]:
        """Retrieves information and recordings for a random location.

        :return: A dictionary containing location ID, venue name, city,
            state, slug string and a list of recordings
        """
        _id = self.retrieve_random_id()

        if not _id:
            return None

        return self.retrieve_details_by_id(location_id=_id)
