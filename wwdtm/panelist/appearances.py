# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
"""Wait Wait Don't Tell Me! Stats Panelist Appearance Retrieval Functions
"""
from functools import lru_cache
from typing import Any, Dict, Optional

from mysql.connector import connect
from wwdtm.panelist.utility import PanelistUtility


class PanelistAppearances:
    """This class contains functions that retrieve panelist appearance
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

        self.utility = PanelistUtility(database_connection=self.database_connection)

    @lru_cache(typed=True)
    def retrieve_appearances_by_id(self, panelist_id: int) -> Dict[str, Any]:
        """Returns a list of dictionary objects containing appearance
        information for the requested panelist ID.

        :param panelist_id: Panelist ID
        :type panelist_id: int
        :return:  Dictionary containing appearance counts and list of
            appearances for a panelist. If panelist appearances could
            not be retrieved, an empty dictionary is returned.
        :rtype: Dict[str, Any]
        """
        try:
            id_ = int(panelist_id)
        except ValueError:
            return {}

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT ( "
                 "SELECT COUNT(pm.showid) FROM ww_showpnlmap pm "
                 "JOIN ww_shows s ON s.showid = pm.showid "
                 "WHERE s.bestof = 0 AND s.repeatshowid IS NULL AND "
                 "pm.panelistid = %s ) AS regular_shows, ( "
                 "SELECT COUNT(pm.showid) FROM ww_showpnlmap pm "
                 "JOIN ww_shows s ON s.showid = pm.showid "
                 "WHERE pm.panelistid = %s ) AS all_shows, ( "
                 "SELECT COUNT(pm.panelistid) FROM ww_showpnlmap pm "
                 "JOIN ww_shows s ON pm.showid = s.showid "
                 "WHERE pm.panelistid = %s AND s.bestof = 0 AND "
                 "s.repeatshowid IS NULL "
                 "AND pm.panelistscore IS NOT NULL ) "
                 "AS shows_with_scores;")
        cursor.execute(query, (id_, id_, id_, ))
        result = cursor.fetchone()

        if result:
            appearance_counts = {
                "regular_shows": result["regular_shows"],
                "all_shows": result["all_shows"],
                "shows_with_scores": result["shows_with_scores"],
            }
        else:
            appearance_counts = {
                "regular_shows": 0,
                "all_shows": 0,
                "shows_with_scores": 0,
            }

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT MIN(s.showid) AS first_id, MIN(s.showdate) AS first, "
                 "MAX(s.showid) AS most_recent_id, MAX(s.showdate) AS most_recent "
                 "FROM ww_showpnlmap pm "
                 "JOIN ww_shows s ON s.showid = pm.showid "
                 "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
                 "AND pm.panelistid = %s "
                 "ORDER BY s.showdate ASC;")
        cursor.execute(query, (id_, ))
        result = cursor.fetchone()

        if result and result["first_id"]:
            first = {
                "show_id": result["first_id"],
                "show_date": result["first"].isoformat(),
            }

            most_recent = {
                "show_id": result["most_recent_id"],
                "show_date": result["most_recent"].isoformat(),
            }

            milestones = {
                "first": first,
                "most_recent": most_recent,
            }

            appearance_info = {
                "milestones": milestones,
            }
        else:
            appearance_info = {
                "milestones": None,
            }

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT pm.showid AS show_id, s.showdate AS date, "
                 "s.bestof AS best_of, s.repeatshowid, "
                 "pm.panelistlrndstart AS start, "
                 "pm.panelistlrndcorrect AS correct, "
                 "pm.panelistscore AS score, "
                 "pm.showpnlrank FROM ww_showpnlmap pm "
                 "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
                 "JOIN ww_shows s ON s.showid = pm.showid "
                 "WHERE pm.panelistid = %s "
                 "ORDER BY s.showdate ASC;")
        cursor.execute(query, (id_, ))
        results = cursor.fetchall()
        cursor.close()

        if result:
            appearances = []
            for appearance in results:
                rank = appearance["showpnlrank"]
                if not rank:
                    rank = None

                info = {
                    "show_id": appearance["show_id"],
                    "date": appearance["date"].isoformat(),
                    "best_of": bool(appearance["best_of"]),
                    "repeat_show": bool(appearance["repeatshowid"]),
                    "lightning_round_start": appearance["start"],
                    "lightning_round_correct": appearance["correct"],
                    "score": appearance["score"],
                    "rank": rank,
                }
                appearances.append(info)

            appearance_info["count"] = appearance_counts
            appearance_info["shows"] = appearances
        else:
            appearance_info["count"] = appearance_counts
            appearance_info["shows"] = []

        return appearance_info

    @lru_cache(typed=True)
    def retrieve_appearances_by_slug(self, panelist_slug: str) -> Dict[str, Any]:
        """Returns a list of dictionary objects containing appearance
        information for the requested panelist slug string.

        :param panelist_slug: Panelist slug string
        :type panelist_slug: str
        :return:  Dictionary containing appearance counts and list of
            appearances for a panelist. If panelist appearances could
            not be retrieved, an empty dictionary is returned.
        :rtype: Dict[str, Any]
        """
        id_ = self.utility.convert_slug_to_id(panelist_slug)
        if not id_:
            return {}

        return self.retrieve_appearances_by_id(id_)

    @lru_cache(typed=True)
    def retrieve_yearly_appearances_by_id(self, panelist_id: int) -> Dict[int, int]:
        """Returns a dictionary containing panelist appearances broken
        down by year, for the requested panelist ID.

        :param panelist_id: Panelist ID
        :type panelist_id: int
        :return: Dictionary containing scoring breakdown by year. If
            panelist appearances could not be retrieved, an empty
            dictionary is returned.
        :rtype: Dict[int, int]
        """
        years = {}
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT DISTINCT YEAR(s.showdate) AS year "
                 "FROM ww_shows s "
                 "ORDER BY YEAR(s.showdate) ASC;")
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            return {}

        for row in results:
            years[row["year"]] = 0

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT YEAR(s.showdate) AS year, "
                 "COUNT(p.panelist) AS count "
                 "FROM ww_showpnlmap pm "
                 "JOIN ww_shows s ON s.showid = pm.showid "
                 "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
                 "WHERE pm.panelistid = %s AND s.bestof = 0 "
                 "AND s.repeatshowid IS NULL "
                 "GROUP BY p.panelist, YEAR(s.showdate) "
                 "ORDER BY p.panelist ASC, YEAR(s.showdate) ASC;")
        cursor.execute(query, (panelist_id, ))
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        for row in results:
            years[row["year"]] = row["count"]

        return years

    @lru_cache(typed=True)
    def retrieve_yearly_appearances_by_slug(self, panelist_slug: str
                                            ) -> Dict[int, int]:
        """Returns a dictionary containing panelist appearances broken
        down by year, for the requested panelist slug string.

        :param panelist_slug: Panelist slug string
        :type panelist_slug: str
        :return: Dictionary containing scoring breakdown by year. If
            panelist appearances could not be retrieved, an empty
            dictionary is returned.
        :rtype: Dict[int, int]
        """
        id_ = self.utility.convert_slug_to_id(panelist_slug)
        if not id_:
            return {}

        return self.retrieve_yearly_appearances_by_id(id_)
