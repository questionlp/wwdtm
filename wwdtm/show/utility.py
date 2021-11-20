# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
"""Wait Wait Don't Tell Me! Stats Show Data Utility Functions
"""
import datetime
from functools import lru_cache
from typing import Any, Dict, Optional

from mysql.connector import connect


class ShowUtility:
    """This class contains supporting functions used to check whether
    or not a show ID or show date exists or to convert between show ID,
    and show dates.

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
    def convert_date_to_id(self,
                           year: int,
                           month: int,
                           day: int) -> Optional[int]:
        """Converts a show date to the matching show ID value.

        :param year: Year portion of a show date
        :type year: int
        :param month: Month portion of a show date
        :type month: int
        :param day: Day portion of a show date
        :type day: int
        :return: Show ID, if a match is found
        :rtype: int
        """
        try:
            show_date = datetime.datetime(year, month, day)
        except ValueError:
            return None

        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT showid FROM ww_shows "
                 "WHERE showdate = %s "
                 "LIMIT 1;")
        cursor.execute(query, (show_date.isoformat(), ))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]

        return None

    @lru_cache(typed=True)
    def convert_id_to_date(self, id: int) -> Optional[str]:
        """Converts a show's ID to the matching show date.

        :param id: Show ID
        :type id: int
        :return: Show date, if a match is found
        :rtype: str
        """
        try:
            id = int(id)
        except ValueError:
            return None

        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT showdate FROM ww_shows "
                 "WHERE showid = %s "
                 "LIMIT 1;")
        cursor.execute(query, (id, ))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0].isoformat()

        return None

    @lru_cache(typed=True)
    def date_exists(self,
                    year: int,
                    month: int,
                    day: int) -> bool:
        """Checks to see if a show date exists.

        :param year: Year portion of a show date
        :type year: int
        :param month: Month portion of a show date
        :type month: int
        :param day: Day portion of a show date
        :type day: int
        :return: True or False, based on whether the show date exists
        :rtype: bool
        """
        try:
            show_date = datetime.datetime(year, month, day)
        except ValueError:
            return False

        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT showid FROM ww_shows "
                 "WHERE showdate = %s "
                 "LIMIT 1;")
        cursor.execute(query, (show_date.isoformat(), ))
        result = cursor.fetchone()
        cursor.close()

        return bool(result)

    @lru_cache(typed=True)
    def id_exists(self, id: int) -> bool:
        """Checks to see if a show ID exists.

        :param id: Show ID
        :type id: int
        :return: True or False, based on whether the show ID exists
        :rtype: bool
        """
        try:
            id = int(id)
        except ValueError:
            return False

        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT showid FROM ww_shows "
                 "WHERE showid = %s "
                 "LIMIT 1;")
        cursor.execute(query, (id, ))
        result = cursor.fetchone()
        cursor.close()

        return bool(result)
