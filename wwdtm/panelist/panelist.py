# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is relased under the terms of the Apache License 2.0
"""Wait Wait Don't Tell Me! Stats Panelist Data Retrieval Functions
"""
from functools import lru_cache
from typing import Any, Dict, List, Optional

from mysql.connector import connect
from slugify import slugify
from wwdtm.panelist.appearances import PanelistAppearances
from wwdtm.panelist.statistics import PanelistStatistics
from wwdtm.panelist.utility import PanelistUtility

class Panelist:
    """This class contains functions used to retrieve panelist data
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

        self.appearances = PanelistAppearances(database_connection=self.database_connection)
        self.statistics = PanelistStatistics(database_connection=self.database_connection)
        self.utility = PanelistUtility(database_connection=self.database_connection)

    def retrieve_all(self) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing panelist ID,
        name and slug string for all panelists.

        :return: List of all panelists and their corresponding
            information
        :rtype: List[Dict[str, Any]]
        """
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT panelistid AS id, panelist, panelistslug AS slug, "
                 "panelistgender AS gender "
                 "FROM ww_panelists "
                 "WHERE panelistslug != 'multiple' "
                 "ORDER BY panelist ASC;")
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return None

        panelists = []
        for row in results:
            panelist = {
                "id": row["id"],
                "name": row["panelist"],
                "slug": row["slug"] if row["slug"] else slugify(row["panelist"]),
                "gender": row["gender"],
            }

            panelists.append(panelist)

        return panelists

    def retrieve_all_details(self) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing panelist ID,
        name, slug string and appearance information for all panelists.

        :return: List of all panelists and their corresponding
            information and appearances
        :rtype: List[Dict[str, Any]]
        """
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT panelistid AS id, panelist, panelistslug AS slug, "
                 "panelistgender AS gender "
                 "FROM ww_panelists "
                 "WHERE panelistslug != 'multiple' "
                 "ORDER BY panelist ASC;")
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return None

        panelists = []
        for row in results:
            id = row["id"]
            panelist = {
                "id": id,
                "name": row["panelist"],
                "slug": row["slug"] if row["slug"] else slugify(row["panelist"]),
                "gender": row["gender"],
                "statistics": self.statistics.retrieve_statistics_by_id(id),
                "bluff": self.statistics.retrieve_bluffs_by_id(id),
                "appearances": self.appearances.retrieve_appearances_by_id(id),
            }

            panelists.append(panelist)

        return panelists

    def retrieve_all_ids(self) -> List[int]:
        """Returns a list of all panelist IDs from the database, sorted
        by panelist name.

        :return: List of all panelist IDs
        :rtype: List[int]
        """
        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT panelistid FROM ww_panelists "
                 "WHERE panelistslug != 'multiple' "
                 "ORDER BY panelist ASC;")
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
        """Returns a list of all panelist slug strings from the
        database, sorted by panelist name.

        :return: List of all panelist slug strings
        :rtype: List[str]
        """
        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT panelistslug FROM ww_panelists "
                 "WHERE panelistslug != 'multiple' "
                 "ORDER BY panelist ASC;")
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return None

        ids = []
        for row in result:
            ids.append(row[0])

        return ids

    @lru_cache(typed=True)
    def retrieve_by_id(self, id: int) -> Dict[str, Any]:
        """Returns a dictionary object containing panelist ID, name and
        slug string for the requested panelist ID.

        :param id: Panelist ID
        :type id: int
        :return: Dictionary containing panelist information
        :rtype: Dict[str, Any]
        """
        try:
            id = int(id)
        except ValueError:
            return None

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT panelistid AS id, panelist, panelistslug AS slug, "
                 "panelistgender AS gender "
                 "FROM ww_panelists "
                 "WHERE panelistid = %s "
                 "LIMIT 1;")
        cursor.execute(query, (id, ))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return None

        info = {
            "id": result["id"],
            "name": result["panelist"],
            "slug": result["slug"] if result["slug"] else slugify(result["panelist"]),
            "gender": result["gender"],
        }

        return info

    @lru_cache(typed=True)
    def retrieve_by_slug(self, slug: str) -> Dict[str, Any]:
        """Returns a dictionary object containing panelist ID, name and
        slug string for the requested panelist slug string.

        :param slug: Panelist slug string
        :type slug: str
        :return: Dictionary containing panelist information
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

    @lru_cache(typed=True)
    def retrieve_details_by_id(self, id: int) -> Dict[str, Any]:
        """Returns a dictionary object containing panelist ID, name, slug
        string and appearance information for the requested panelist ID.

        :param id: Panelist ID
        :type id: int
        :return: Dictionary containing panelist information and their
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

        info["statistics"] = self.statistics.retrieve_statistics_by_id(id)
        info["bluffs"] = self.statistics.retrieve_bluffs_by_id(id)
        info["appearances"] = self.appearances.retrieve_appearances_by_id(id)

        return info

    @lru_cache(typed=True)
    def retrieve_details_by_slug(self, slug: str) -> Dict[str, Any]:
        """Returns a dictionary object containing panelist ID, name, slug
        string and appearance information for the requested Panelist slug
        string.

        :param slug: Panelist slug string
        :type slug: str
        :return: Dictionary containing panelist information and their
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
