# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
"""Wait Wait Don't Tell Me! Stats Host Appearance Retrieval Functions
"""
from functools import lru_cache
from typing import Any, Dict, Optional

from mysql.connector import connect
from wwdtm.host.utility import HostUtility


class HostAppearances:
    """This class contains functions that retrieve host appearance
    information from a copy of the Wait Wait Stats database.

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

        self.utility = HostUtility(database_connection=self.database_connection)

    @lru_cache(typed=True)
    def retrieve_appearances_by_id(self, host_id: int) -> Dict[str, Any]:
        """Returns a list of dictionary objects containing appearance
        information for the requested host ID.

        :param host_id: Host ID
        :type host_id: int
        :return:  Dictionary containing appearance counts and list of
            appearances for a host. If host appearances could not be
            retrieved, an empty dictionary is returned.
        :rtype: Dict[str, Any]
        """
        try:
            id_ = int(host_id)
        except ValueError:
            return {}

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT ( "
                 "SELECT COUNT(hm.showid) FROM ww_showhostmap hm "
                 "JOIN ww_shows s ON s.showid = hm.showid "
                 "WHERE s.bestof = 0 AND s.repeatshowid IS NULL AND "
                 "hm.hostid = %s ) AS regular_shows, ( "
                 "SELECT COUNT(hm.showid) FROM ww_showhostmap hm "
                 "JOIN ww_shows s ON s.showid = hm.showid "
                 "WHERE hm.hostid = %s ) AS all_shows;")
        cursor.execute(query, (id_, id_, ))
        result = cursor.fetchone()

        if result:
            appearance_counts = {
                "regular_shows": result["regular_shows"],
                "all_shows": result["all_shows"],
            }
        else:
            appearance_counts = {
                "regular_shows": 0,
                "all_shows": 0,
            }

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT hm.showid AS show_id, s.showdate AS date, "
                 "s.bestof AS best_of, s.repeatshowid, "
                 "hm.guest FROM ww_showhostmap hm "
                 "JOIN ww_hosts h ON h.hostid = hm.hostid "
                 "JOIN ww_shows s ON s.showid = hm.showid "
                 "WHERE hm.hostid = %s "
                 "ORDER BY s.showdate ASC;")
        cursor.execute(query, (id_, ))
        results = cursor.fetchall()
        cursor.close()

        if results:
            appearances = []
            for appearance in results:
                info = {
                    "show_id": appearance["show_id"],
                    "date": appearance["date"].isoformat(),
                    "best_of": bool(appearance["best_of"]),
                    "repeat_show": bool(appearance["repeatshowid"]),
                    "guest": bool(appearance["guest"]),
                }
                appearances.append(info)

            appearance_info = {
                "count": appearance_counts,
                "shows": appearances,
            }
        else:
            appearance_info = {
                "count": appearance_counts,
                "shows": [],
            }

        return appearance_info

    @lru_cache(typed=True)
    def retrieve_appearances_by_slug(self, host_slug: str) -> Dict[str, Any]:
        """Returns a list of dictionary objects containing appearance
        information for the requested host ID.

        :param host_slug: Host slug string
        :type host_slug: str
        :return:  Dictionary containing appearance counts and list of
            appearances for a host. If host appearances could not be
            retrieved, an empty dictionary is returned.
        :rtype: Dict[str, Any]
        """
        id_ = self.utility.convert_slug_to_id(host_slug)
        if not id_:
            return {}

        return self.retrieve_appearances_by_id(id_)
