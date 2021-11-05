# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is relased under the terms of the Apache License 2.0
"""Wait Wait Don't Tell Me! Stats Location Data Utility Functions
"""
from functools import lru_cache
from typing import Any, Dict, Optional

from mysql.connector import connect
from slugify import slugify

class LocationUtility:
    """This class contains supporting functions used to check whether
    or not a Location ID or slug string exists or to convert an ID to a
    slug string, or vice versa.

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


    @lru_cache(typed=True)
    def convert_id_to_slug(self, id: int) -> str:
        """Converts a location's ID to the matching location slug
        string value.

        :param id: Location ID
        :type id: int
        :return: Location slug string, if a match is found
        :rtype: str
        """
        try:
            id = int(id)
        except ValueError:
            return None

        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT locationslug FROM ww_locations "
                 "WHERE locationid = %s "
                 "LIMIT 1;")
        cursor.execute(query, (id, ))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]

        return None

    @lru_cache(typed=True)
    def convert_slug_to_id(self, slug: str) -> int:
        """Converts a location's slug string to the matching location
        ID value.

        :param slug: Location slug string
        :type slug: str
        :return: Location ID, if a match if found
        :rtype: int
        """
        try:
            slug = slug.strip()
            if not slug:
                return None
        except ValueError:
            return None

        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT locationid FROM ww_locations "
                 "WHERE locationslug = %s "
                 "LIMIT 1;")
        cursor.execute(query, (slug, ))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]

        return None

    @lru_cache(typed=True)
    def id_exists(self, id: int) -> bool:
        """Checks to see if a location ID exists.

        :param id: Location ID
        :type id: int
        :return: True or False, based on whether the location ID exists
        :rtype: bool
        """
        try:
            id = int(id)
        except ValueError:
            return False

        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT locationid FROM ww_locations "
                 "WHERE locationid = %s "
                 "LIMIT 1;")
        cursor.execute(query, (id, ))
        result = cursor.fetchone()
        cursor.close()

        return bool(result)

    @lru_cache(typed=True)
    def slug_exists(self, slug: str) -> bool:
        """Checks to see if a location slug string exists.

        :param slug: Location slug string
        :type slug: str
        :return: True or False, based on whether the location slug
            string exists
        :rtype: bool
        """
        try:
            slug = slug.strip()
            if not slug:
                return False
        except ValueError:
            return False

        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT locationslug FROM ww_locations "
                 "WHERE locationslug = %s "
                 "LIMIT 1;")
        cursor.execute(query, (slug, ))
        result = cursor.fetchone()
        cursor.close()

        return bool(result)

    def slugify_location(self,
                         id: int=None,
                         venue: str=None,
                         city: str=None,
                         state: str=None
                        ) -> str:
        """Generates a slug string based on the location's venue name,
        city, state and/or location ID.

        :param id: Location ID
        :type id: int
        :param venue: Location venue name
        :type venue: str
        :param city: City where the location venue is located
        :type city: str
        :param state: State where the location venue is located
        :type state: str
        :return: Location slug string
        :rtype: str
        :raises: ValueError
        """
        if venue and city and state:
            return slugify(f"{venue} {city} {state}")
        elif venue and city and not state:
            return slugify(f"{venue} {city}")
        elif id and venue and (not city and not state):
            return slugify(f"{id}-{venue}")
        elif id and city and state and not venue:
            return slugify(f"{id} {city} {state}")
        elif id:
            return f"location-{id}"
        else:
            raise ValueError("Invalid location information provided")
