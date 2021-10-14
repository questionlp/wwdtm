# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is relased under the terms of the Apache License 2.0
"""Wait Wait Don't Tell Me! Stats Guest Data Retrieval Functions
"""
from functools import lru_cache
from typing import Any, Dict, List, Optional

from mysql.connector import connect
from slugify import slugify
from wwdtm.guest.appearances import GuestAppearances
from wwdtm.guest.utility import GuestUtility

class Guest:
    """This class contains functions used to retrieve guest data from a
    copy of the Wait Wait Stats database.

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

        self.appearances = GuestAppearances(database_connection=self.database_connection)
        self.utility = GuestUtility(database_connection=self.database_connection)

    def retrieve_all(self) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing guest ID,
        name and slug string for all guests.

        :return: List of all guests and their corresponding
            information
        :rtype: List[Dict[str, Any]]
        """
        self.database_connection.is_connected
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT guestid AS id, guest, guestslug AS slug "
                 "FROM ww_guests "
                 "WHERE guestslug != 'none' "
                 "ORDER BY guest ASC;")
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return None

        guests = []
        for row in results:
            guest = {
                "id": row["id"],
                "name": row["guest"],
                "slug": row["slug"] if row["slug"] else slugify(row["guest"]),
            }

            guests.append(guest)

        return guests

    def retrieve_all_details(self) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing guest ID,
        name, slug string and appearance information for all guests.

        :return: List of all guests and their corresponding
            information and appearances
        :rtype: List[Dict[str, Any]]
        """
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT guestid AS id, guest, guestslug AS slug "
                 "FROM ww_guests "
                 "WHERE guestslug != 'none' "
                 "ORDER BY guest ASC;")
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return None

        guests = []
        for row in results:
            appearances = self.appearances.retrieve_appearances_by_id(row["id"])
            guest = {
                "id": row["id"],
                "name": row["guest"],
                "slug": row["slug"] if row["slug"] else slugify(row["guest"]),
                "appearances": appearances,
            }

            guests.append(guest)

        return guests

    def retrieve_all_ids(self) -> List[int]:
        """Returns a list of all guest IDs from the database, sorted by
        guest name.

        :return: List of all guest IDs
        :rtype: List[int]
        """
        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT guestid FROM ww_guests "
                 "WHERE guestslug != 'none' "
                 "ORDER BY guest ASC;")
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return None

        ids = []
        for row in result:
            ids.append(row[0])

        return ids

    def retrieve_all_slugs(self) -> List[str]:
        """Returns a list of all guest slug strings from the database,
        sorted by guest name.

        :return: List of all guest slug strings
        :rtype: List[str]
        """
        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT guestslug FROM ww_guests "
                 "WHERE guestslug != 'none' "
                 "ORDER BY guest ASC;")
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return None

        ids = []
        for row in result:
            ids.append(row[0])

        return ids

    @lru_cache(maxsize=256, typed=True)
    def retrieve_by_id(self, id: int) -> Dict[str, Any]:
        """Returns a dictionary object containing guest ID, name and
        slug string for the requested guest ID.

        :param id: Guest ID
        :type id: int
        :return: Dictionary containing guest information
        :rtype: Dict[str, Any]
        """
        try:
            id = int(id)
        except ValueError:
            return None

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT guestid AS id, guest, guestslug AS slug "
                 "FROM ww_guests "
                 "WHERE guestid = %s "
                 "LIMIT 1;")
        cursor.execute(query, (id, ))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return None

        info = {
            "id": result["id"],
            "name": result["guest"],
            "slug": result["slug"] if result["slug"] else slugify(result["guest"]),
        }

        return info

    @lru_cache(maxsize=256, typed=True)
    def retrieve_by_slug(self, slug: str) -> Dict[str, Any]:
        """Returns a dictionary object containing guest ID, name and
        slug string for the requested guest slug string.

        :param slug: Guest slug string
        :type slug: str
        :return: Dictionary containing guest information
        :rtype: Dict[str, Any]
        """
        try:
            slug = slug.strip()
            if not slug:
                return False
        except AttributeError:
            return False

        id = self.utility.convert_slug_to_id(slug)
        if not id:
            return None

        return self.retrieve_by_id(id)

    @lru_cache(maxsize=256, typed=True)
    def retrieve_details_by_id(self, id: int) -> Dict[str, Any]:
        """Returns a dictionary object containing guest ID, name, slug
        string and appearance information for the requested Guest ID.

        :param id: Guest ID
        :type id: int
        :return: Dictionary containing guest information and their
            appearances
        :rtype: Dict[str, Any]
        """
        try:
            id = int(id)
        except ValueError:
            return None

        info = self.retrieve_by_id(id)
        if not info:
            return None

        info["appearances"] = self.appearances.retrieve_appearances_by_id(id)

        return info

    @lru_cache(maxsize=256, typed=True)
    def retrieve_details_by_slug(self, slug: str) -> Dict[str, Any]:
        """Returns a dictionary object containing guest ID, name, slug
        string and appearance information for the requested Guest slug
        string.

        :param slug: Guest slug string
        :type slug: str
        :return: Dictionary containing guest information and their
            appearances
        :rtype: Dict[str, Any]
        """
        try:
            slug = slug.strip()
            if not slug:
                return False
        except AttributeError:
            return False

        id = self.utility.convert_slug_to_id(slug)
        if not id:
            return None

        return self.retrieve_details_by_id(id)
