# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
"""Wait Wait Don't Tell Me! Stats Scorekeeper Data Utility Functions
"""
from functools import lru_cache
from typing import Any, Dict, Optional

from mysql.connector import connect


class ScorekeeperUtility:
    """This class contains supporting functions used to check whether
    or not a scorekeeper ID or slug string exists or to convert an ID
    to a slug string, or vice versa.

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
    def convert_id_to_slug(self, scorekeeper_id: int) -> Optional[str]:
        """Converts a scorekeeper's ID to the matching scorekeeper slug
        string value.

        :param scorekeeper_id: Scorekeeper ID
        :type scorekeeper_id: int
        :return: Scorekeeper slug string, if a match is found
        :rtype: str
        """
        try:
            id_ = int(scorekeeper_id)
        except ValueError:
            return None

        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT scorekeeperslug FROM ww_scorekeepers "
                 "WHERE scorekeeperid = %s "
                 "LIMIT 1;")
        cursor.execute(query, (id_, ))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]

        return None

    @lru_cache(typed=True)
    def convert_slug_to_id(self, scorekeeper_slug: str) -> Optional[int]:
        """Converts a scorekeeper's slug string to the matching
        scorekeeper ID value.

        :param scorekeeper_slug: Scorekeeper slug string
        :type scorekeeper_slug: str
        :return: Scorekeeper ID, if a match is found
        :rtype: int
        """
        try:
            slug = scorekeeper_slug.strip()
            if not slug:
                return None
        except ValueError:
            return None

        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT scorekeeperid FROM ww_scorekeepers "
                 "WHERE scorekeeperslug = %s "
                 "LIMIT 1;")
        cursor.execute(query, (slug, ))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]

        return None

    @lru_cache(typed=True)
    def id_exists(self, scorekeeper_id: int) -> bool:
        """Checks to see if a scorekeeper ID exists.

        :param scorekeeper_id: Scorekeeper ID
        :type scorekeeper_id: int
        :return: True or False, based on whether the scorekeeper ID
            exists
        :rtype: bool
        """
        try:
            id_ = int(scorekeeper_id)
        except ValueError:
            return False

        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT scorekeeperid FROM ww_scorekeepers "
                 "WHERE scorekeeperid = %s "
                 "LIMIT 1;")
        cursor.execute(query, (id_, ))
        result = cursor.fetchone()
        cursor.close()

        return bool(result)

    @lru_cache(typed=True)
    def slug_exists(self, scorekeeper_slug: str) -> bool:
        """Checks to see if a scorekeeper slug string exists.

        :param scorekeeper_slug: Scorekeeper slug string
        :type scorekeeper_slug: str
        :return: True or False, based on whether the scorekeeper slug
            string exists
        :rtype: bool
        """
        try:
            slug = scorekeeper_slug.strip()
            if not slug:
                return False
        except ValueError:
            return False

        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT scorekeeperslug FROM ww_scorekeepers "
                 "WHERE scorekeeperslug = %s "
                 "LIMIT 1;")
        cursor.execute(query, (slug, ))
        result = cursor.fetchone()
        cursor.close()

        return bool(result)
