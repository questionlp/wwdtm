# Copyright (c) 2018-2023 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Don't Tell Me! Stats Location Data Retrieval Functions."""
from typing import Any, Dict, List, Optional

from mysql.connector import connect

from wwdtm.location.recordings import LocationRecordings
from wwdtm.location.utility import LocationUtility
from wwdtm.validation import valid_int_id


class Location:
    """Location Information Class.

    This class contains functions used to retrieve location data
    from a copy of the Wait Wait Stats database.

    :param connect_dict: Dictionary containing database connection
        settings as required by mysql.connector.connect
    :param database_connection: mysql.connector.connect database
        connection
    """

    def __init__(
        self,
        connect_dict: Optional[Dict[str, Any]] = None,
        database_connection: Optional[connect] = None,
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

    def retrieve_all(self, sort_by_venue: bool = False) -> List[Dict[str, Any]]:
        """Returns a list of dictionaries containing information for all locations.

        Returned information includes: location ID, city, state, venue and slug string.

        :param sort_by_venue: Sets whether to sort by venue first, or
            by state and city first
        :return: List of all locations and their corresponding
            information. If locations could not be retrieved, an empty
            list is returned.
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

    def retrieve_all_details(self, sort_by_venue: bool = False) -> List[Dict[str, Any]]:
        """Returns a list of dictionaries containing detailed information for all locations.

        Returned information includes: location ID, city, state, venue, slug string and recordings.

        :param sort_by_venue: Sets whether to sort by venue first, or
            by state and city first
        :return: List of all locations and their corresponding
            information and recordings. If locations could not be
            retrieved, an empty list is returned.
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

    def retrieve_all_ids(self, sort_by_venue: bool = False) -> List[int]:
        """Returns a list of all locations IDs.

        :param sort_by_venue: Sets whether to sort by venue first, or
            by state and city first
        :return: List of all location IDs. If location IDs could not be
            retrieved, an empty list is returned.
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

    def retrieve_all_slugs(self, sort_by_venue: bool = False) -> List[str]:
        """Returns a list of all location slug strings.

        :param sort_by_venue: Sets whether to sort by venue first, or
            by state and city first
        :return: List of all location slug strings. If location slug
            strings could not be retrieved, an empty list is returned.
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

    def retrieve_by_id(self, location_id: int) -> Dict[str, Any]:
        """Returns a dictionary containing location information.

        Returned information includes: location ID, venue, city, state and slug string.

        :param location_id: Location ID
        :return: Dictionary containing location information. If
            location information could not be retrieved, an empty
            dictionary is returned.
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

    def retrieve_by_slug(self, location_slug: str) -> Dict[str, Any]:
        """Returns a dictionary containing location information.

        Returned information includes: location ID, venue, city, state and slug string.

        :param location_slug: Location slug string
        :return: Dictionary containing location information. If
            location information could not be retrieved, an empty
            dictionary is returned.
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

    def retrieve_details_by_id(self, location_id: int) -> Dict[str, Any]:
        """Returns a dictionary containing detailed location information.

        Returned information includes: location ID, venue, city, state, slug string and recordings.

        :param location_id: Location ID
        :return: Dictionary containing location information and their
            recordings. If location information could not be retrieved,
            an empty dictionary is returned.
        """
        if not valid_int_id(location_id):
            return {}

        info = self.retrieve_by_id(location_id)
        if not info:
            return {}

        info["recordings"] = self.recordings.retrieve_recordings_by_id(location_id)

        return info

    def retrieve_details_by_slug(self, location_slug: str) -> Dict[str, Any]:
        """Returns a dictionary containing detailed location information.

        Returned information includes: location ID, venue, city, state, slug string and recordings.

        :param location_slug: Location slug string
        :return: Dictionary containing location information and their
            recordings. If location information could not be retrieved,
            an empty dictionary is returned.
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
