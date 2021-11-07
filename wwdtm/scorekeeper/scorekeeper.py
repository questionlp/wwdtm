# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is relased under the terms of the Apache License 2.0
"""Wait Wait Don't Tell Me! Stats Scorekeeper Data Retrieval Functions
"""
from functools import lru_cache
from typing import Any, Dict, List, Optional

from mysql.connector import connect
from slugify import slugify
from wwdtm.scorekeeper.appearances import ScorekeeperAppearances
from wwdtm.scorekeeper.utility import ScorekeeperUtility

class Scorekeeper:
    """This class contains functions used to retrieve scorekeeper data
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

        self.appearances = ScorekeeperAppearances(database_connection=self.database_connection)
        self.utility = ScorekeeperUtility(database_connection=self.database_connection)

    def retrieve_all(self) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing scorekeeper
        ID, name and slug string for all scorekeepers.

        :return: List of all scorekeepers and their corresponding
            information. If scorekeeper information could not be
            retrieved, an empty list will be returned.
        :rtype: List[Dict[str, Any]]
        """
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT scorekeeperid AS id, scorekeeper, "
                 "scorekeeperslug AS slug, scorekeepergender AS gender "
                 "FROM ww_scorekeepers "
                 "WHERE scorekeeperslug != 'tbd' "
                 "ORDER BY scorekeeper ASC;")
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        scorekeepers = []
        for row in results:
            scorekeeper = {
                "id": row["id"],
                "name": row["scorekeeper"],
                "slug": row["slug"] if row["slug"] else slugify(row["scorekeeper"]),
                "gender": row["gender"],
            }

            scorekeepers.append(scorekeeper)

        return scorekeepers

    def retrieve_all_details(self) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing scorekeeper
        ID, name, slug string and appearance information for all
        scorekeepers.

        :return: List of all scorekeepers and their corresponding
            information and appearances. If scorekeeper information
            could not be retrieved, an empty list will be returned.
        :rtype: List[Dict[str, Any]]
        """
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT scorekeeperid AS id, scorekeeper, "
                 "scorekeeperslug AS slug, scorekeepergender AS gender "
                 "FROM ww_scorekeepers "
                 "WHERE scorekeeperslug != 'tbd' "
                 "ORDER BY scorekeeper ASC;")
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        scorekeepers = []
        for row in results:
            appearance = self.appearances.retrieve_appearances_by_id(row["id"])
            scorekeeper = {
                "id": row["id"],
                "name": row["scorekeeper"],
                "slug": row["slug"] if row["slug"] else slugify(row["scorekeeper"]),
                "gender": row["gender"],
                "appearances": appearance,
            }

            scorekeepers.append(scorekeeper)

        return scorekeepers

    def retrieve_all_ids(self) -> List[int]:
        """Returns a list of all scorekeeper IDs from the database,
        sorted by scorekeeper name.

        :return: List of all scorekeeper IDs. If scorekeeper IDs could
            not be retrieved, an empty list would be returned.
        :rtype: List[int]
        """
        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT scorekeeperid FROM ww_scorekeepers "
                 "WHERE scorekeeperslug != 'tbd' "
                 "ORDER BY scorekeeper ASC;")
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return []

        ids = []
        for row in result:
            ids.append(row[0])

        return ids

    def retrieve_all_slugs(self) -> List[str]:
        """Returns a list of all scorekeeper slug strings from the
        database, sorted by scorekeeper name.

        :return: List of all scorekeeper slug strings. If scorekeeper
            slug strings could not be retrieved, an empty list will be
            returned.
        :rtype: List[str]
        """
        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT scorekeeperslug FROM ww_scorekeepers "
                 "WHERE scorekeeperslug != 'tbd' "
                 "ORDER BY scorekeeper ASC;")
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
    def retrieve_by_id(self, id: int) -> Dict[str, Any]:
        """Returns a dictionary object containing scorekeeper ID, name
        and slug string for the requested scorekeeper ID.

        :param id: Scorekeeper ID
        :type id: int
        :return: Dictionary containing scorekeeper information. If
            scorekeeper information could not be retrieved, an empty
            dictionary will be returned.
        :rtype: Dict[str, Any]
        """
        try:
            id = int(id)
        except ValueError:
            return {}

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT scorekeeperid AS id, scorekeeper, "
                 "scorekeeperslug AS slug, scorekeepergender AS gender "
                 "FROM ww_scorekeepers "
                 "WHERE scorekeeperid = %s "
                 "LIMIT 1;")
        cursor.execute(query, (id, ))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return {}

        info = {
            "id": result["id"],
            "name": result["scorekeeper"],
            "slug": result["slug"] if result["slug"] else slugify(result["scorekeeper"]),
            "gender": result["gender"],
        }

        return info

    @lru_cache(typed=True)
    def retrieve_by_slug(self, slug: str) -> Dict[str, Any]:
        """Returns a dictionary object containing scorekeeper ID, name
        and slug string for the requested scorekeeper slug string.

        :param slug: Scorekeeper slug string
        :type slug: str
        :return: Dictionary containing scorekeeper information. If
            scorekeeper information could not be retrieved, an empty
            dictionary will be returned.
        :rtype: Dict[str, Any]
        """
        try:
            slug = slug.strip()
            if not slug:
                return {}
        except AttributeError:
            return {}

        id = self.utility.convert_slug_to_id(slug)
        if not id:
            return {}

        return self.retrieve_by_id(id)

    @lru_cache(typed=True)
    def retrieve_details_by_id(self, id: int) -> Dict[str, Any]:
        """Returns a dictionary object containing scorekeeper ID, name,
        slug string and appearance information for the requested
        scorekeeper ID.

        :param id: Scorekeeper ID
        :type id: int
        :return: Dictionary containing scorekeeper information and
            their appearances. If scorekeeper information could not be
            retrieved, an empty dictionary will be returned.
        :rtype: Dict[str, Any]
        """
        try:
            id = int(id)
        except ValueError:
            return {}

        info = self.retrieve_by_id(id)
        if not info:
            return {}

        info["appearances"] = self.appearances.retrieve_appearances_by_id(id)

        return info

    @lru_cache(typed=True)
    def retrieve_details_by_slug(self, slug: str) -> Dict[str, Any]:
        """Returns a dictionary object containing scorekeeper ID, name,
        slug string and appearance information for the requested
        scorekeeper slug string.

        :param slug: Scorekeeper slug string
        :type slug: str
        :return: Dictionary containing scorekeeper information and
            their appearances. If scorekeeper information could not be
            retrieved, an empty dictionary will be returned.
        :rtype: Dict[str, Any]
        """
        try:
            slug = slug.strip()
            if not slug:
                return {}
        except AttributeError:
            return {}

        id = self.utility.convert_slug_to_id(slug)
        if not id:
            return {}

        return self.retrieve_details_by_id(id)
