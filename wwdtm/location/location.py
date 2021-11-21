# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
"""Wait Wait Don't Tell Me! Stats Location Data Retrieval Functions
"""
from functools import lru_cache
from typing import Any, Dict, List, Optional

from mysql.connector import connect
from wwdtm.location.recordings import LocationRecordings
from wwdtm.location.utility import LocationUtility
from wwdtm.validation import valid_int_id


class Location:
    """This class contains functions used to retrieve location data
    from a copy of the Wait Wait Stats database.

    :param connect_dict: Dictionary containing database connection
        settings as required by mysql.connector.connect
    :type connect_dict: Dict[str, Any], optional
    :param database_connection: mysql.connector.connect database
        connection
    :type database_connection: mysql.connector.connect, optional
    """

    def __init__(self,
                 connect_dict: Optional[Dict[str, Any]] = None,
                 database_connection: Optional[connect] = None):
        """Class initialization method.
        """
        if connect_dict:
            self.connect_dict = connect_dict
            self.database_connection = connect(**connect_dict)
        elif database_connection:
            if not database_connection.is_connected():
                database_connection.reconnect()

            self.database_connection = database_connection

        self.recordings = LocationRecordings(database_connection=self.database_connection)
        self.utility = LocationUtility(database_connection=self.database_connection)

    def retrieve_all(self, sort_by_venue: bool = False) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing location ID,
        city, state, venue and slug string for all locations.

        :param sort_by_venue: Sets whether to sort by venue first, or
            by state and city first
        :type sort_by_venue: bool
        :return: List of all locations and their corresponding
            information. If locations could not be retrieved, an empty
            list is returned.
        :rtype: List[Dict[str, Any]]
        """
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT locationid AS id, city, state, venue, "
                 "locationslug AS slug "
                 "FROM ww_locations "
                 "WHERE locationslug != 'tbd' ")
        if sort_by_venue:
            query = query + "ORDER BY venue ASC, city ASC, state ASC;"
        else:
            query = query + "ORDER BY state ASC, city ASC, venue ASC;"

        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        locations = []
        for row in results:
            slug = self.utility.slugify_location(location_id=row["id"],
                                                 venue=row["venue"],
                                                 city=row["city"],
                                                 state=row["state"])
            location = {
                "id": row["id"],
                "city": row["city"],
                "state": row["state"],
                "venue": row["venue"],
                "slug": row["slug"] if row["slug"] else slug,
            }

            locations.append(location)

        return locations

    def retrieve_all_details(self, sort_by_venue: bool = False
                             ) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing location ID,
        city, state, venue, slug string and recording information for
        all locations.

        :param sort_by_venue: Sets whether to sort by venue first, or
            by state and city first
        :type sort_by_venue: bool
        :return: List of all locations and their corresponding
            information and recordings. If locations could not be
            retrieved, an empty list is returned.
        :rtype: List[Dict[str, Any]]
        """
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT locationid AS id, city, state, venue, "
                 "locationslug AS slug "
                 "FROM ww_locations "
                 "WHERE locationslug != 'tbd' ")
        if sort_by_venue:
            query = query + "ORDER BY venue ASC, city ASC, state ASC;"
        else:
            query = query + "ORDER BY state ASC, city ASC, venue ASC;"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        locations = []
        for row in results:
            slug = self.utility.slugify_location(location_id=row["id"],
                                                 venue=row["venue"],
                                                 city=row["city"],
                                                 state=row["state"])
            recordings = self.recordings.retrieve_recordings_by_id(row["id"])
            location = {
                "id": row["id"],
                "city": row["city"],
                "state": row["state"],
                "venue": row["venue"],
                "slug": row["slug"] if row["slug"] else slug,
                "recordings": recordings,
            }

            locations.append(location)

        return locations

    def retrieve_all_ids(self, sort_by_venue: bool = False) -> List[int]:
        """Returns a list of all locations IDs from the database.

        :param sort_by_venue: Sets whether to sort by venue first, or
            by state and city first
        :type sort_by_venue: bool
        :return: List of all location IDs. If location IDs could not be
            retrieved, an empty list is returned.
        :rtype: List[int]
        """
        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT locationid FROM ww_locations "
                 "WHERE locationslug != 'tbd' ")
        if sort_by_venue:
            query = query + "ORDER BY venue ASC, city ASC, state ASC;"
        else:
            query = query + "ORDER BY state ASC, city ASC, venue ASC;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return []

        ids = []
        for row in result:
            ids.append(row[0])

        return ids

    def retrieve_all_slugs(self, sort_by_venue: bool = False) -> List[str]:
        """Returns a list of all location slug strings from the
        database.

        :param sort_by_venue: Sets whether to sort by venue first, or
            by state and city first
        :type sort_by_venue: bool
        :return: List of all location slug strings. If location slug
            strings could not be retrieved, an empty list is returned.
        :rtype: List[str]
        """
        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT locationslug FROM ww_locations "
                 "WHERE locationslug != 'tbd' ")
        if sort_by_venue:
            query = query + "ORDER BY venue ASC, city ASC, state ASC;"
        else:
            query = query + "ORDER BY state ASC, city ASC, venue ASC;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return []

        ids = []
        for row in result:
            ids.append(row[0])

        return ids

    @lru_cache(typed=True)
    def retrieve_by_id(self, location_id: int) -> Dict[str, Any]:
        """Returns a dictionary object containing location ID, venue,
        city, state and slug string for the requested location ID.

        :param location_id: Location ID
        :type location_id: int
        :return: Dictionary containing location information. If
            location information could not be retrieved, an empty
            dictionary is returned.
        :rtype: Dict[str, Any]
        """
        if not valid_int_id(location_id):
            return {}

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT locationid AS id, city, state, venue, "
                 "locationslug AS slug "
                 "FROM ww_locations "
                 "WHERE locationid = %s "
                 "LIMIT 1;")
        cursor.execute(query, (location_id, ))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return {}

        slug = self.utility.slugify_location(location_id=result["id"],
                                             venue=result["venue"],
                                             city=result["city"],
                                             state=result["state"])
        location = {
            "id": result["id"],
            "city": result["city"],
            "state": result["state"],
            "venue": result["venue"],
            "slug": result["slug"] if result["slug"] else slug,
        }

        return location

    @lru_cache(typed=True)
    def retrieve_by_slug(self, location_slug: str) -> Dict[str, Any]:
        """Returns a dictionary object containing location ID, venue,
        city, state and slug string for the requested location ID.

        :param location_slug: Location slug string
        :type location_slug: str
        :return: Dictionary containing location information. If
            location information could not be retrieved, an empty
            dictionary is returned.
        :rtype: Dict[str, Any]
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

    @lru_cache(typed=True)
    def retrieve_details_by_id(self, location_id: int) -> Dict[str, Any]:
        """Returns a dictionary object containing location ID, venue,
        city, state, slug string and a list of recordings for the
        requested location ID.

        :param location_id: Location ID
        :type location_id: int
        :return: Dictionary containing location information and their
            recordings. If location information could not be retrieved,
            an empty dictionary is returned.
        :rtype: Dict[str, Any]
        """
        if not valid_int_id(location_id):
            return {}

        info = self.retrieve_by_id(location_id)
        if not info:
            return {}

        info["recordings"] = self.recordings.retrieve_recordings_by_id(location_id)

        return info

    @lru_cache(typed=True)
    def retrieve_details_by_slug(self, location_slug: str) -> Dict[str, Any]:
        """Returns a dictionary object containing location ID, venue,
        city, state, slug string and a list of recordings for the
        requested location slug string.

        :param location_slug: Location slug string
        :type location_slug: str
        :return: Dictionary containing location information and their
            recordings. If location information could not be retrieved,
            an empty dictionary is returned.
        :rtype: Dict[str, Any]
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
