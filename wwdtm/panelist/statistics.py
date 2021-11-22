# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
"""Wait Wait Don't Tell Me! Stats Panelist Statistics Retrieval Functions
"""
from functools import lru_cache
from typing import Any, Dict, Optional

from mysql.connector import connect
import numpy
from wwdtm.panelist.scores import PanelistScores
from wwdtm.panelist.utility import PanelistUtility
from wwdtm.validation import valid_int_id


class PanelistStatistics:
    """This class contains functions used to retrieve data from a copy
    of the Wait Wait Stats database and calculate statistics for
    panelists.

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

        self.scores = PanelistScores(database_connection=self.database_connection)
        self.utility = PanelistUtility(database_connection=self.database_connection)

    @lru_cache(typed=True)
    def retrieve_bluffs_by_id(self, panelist_id: int) -> Dict[str, int]:
        """Returns a dictionary containing the number of chosen Bluffs
        and correct Bluffs for the requested panelist ID.

        :param panelist_id: Panelist ID
        :type panelist_id: int
        :return: Dictionary containing panelist Bluff counts. If
            panelist Bluff counts could not be returned, an empty
            dictionary will be returned.
        :rtype: Dict[str, int]
        """
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT ( "
                 "SELECT COUNT(blm.chosenbluffpnlid) FROM ww_showbluffmap blm "
                 "JOIN ww_shows s ON s.showid = blm.showid "
                 "WHERE s.repeatshowid IS NULL AND blm.chosenbluffpnlid = %s "
                 ") AS chosen, ( "
                 "SELECT COUNT(blm.correctbluffpnlid) FROM ww_showbluffmap blm "
                 "JOIN ww_shows s ON s.showid = blm.showid "
                 "WHERE s.repeatshowid IS NULL AND blm.correctbluffpnlid = %s "
                 ") AS correct;")
        cursor.execute(query, (panelist_id, panelist_id, ))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return {}

        bluffs = {
            "chosen": result["chosen"],
            "correct": result["correct"],
        }

        return bluffs

    @lru_cache(typed=True)
    def retrieve_bluffs_by_slug(self, panelist_slug: str) -> Dict[str, int]:
        """Returns a dictionary containing the number of chosen Bluffs
        and correct Bluffs for the requested panelist slug string.

        :param panelist_slug: Panelist slug string
        :type panelist_slug: str
        :return: Dictionary containing panelist Bluff counts. If
            panelist Bluff counts could not be returned, an empty
            dictionary will be returned.
        :rtype: Dict[str, int]
        """
        id_ = self.utility.convert_slug_to_id(panelist_slug)
        if not id_:
            return {}

        return self.retrieve_bluffs_by_id(id_)

    @lru_cache(typed=True)
    def retrieve_rank_info_by_id(self, panelist_id: int) -> Dict[str, int]:
        """Returns a dictionary with ranking information for the
        requested panelist ID.

        :param panelist_id: Panelist ID
        :type panelist_id: int
        :return: Dictionary containing panelist ranking information. If
            panelist ranking information could not be returned, an empty
            dictionary will be returned.
        :rtype: Dict[str, int]
        """
        if not valid_int_id(panelist_id):
            return {}

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT ( "
                 "SELECT COUNT(pm.showpnlrank) FROM ww_showpnlmap pm "
                 "JOIN ww_shows s ON s.showid = pm.showid "
                 "WHERE pm.panelistid = %s AND pm.showpnlrank = '1' AND "
                 "s.bestof = 0 and s.repeatshowid IS NULL) as '1', ( "
                 "SELECT COUNT(pm.showpnlrank) FROM ww_showpnlmap pm "
                 "JOIN ww_shows s ON s.showid = pm.showid "
                 "WHERE pm.panelistid = %s AND pm.showpnlrank = '1t' AND "
                 "s.bestof = 0 and s.repeatshowid IS NULL) as '1t', ( "
                 "SELECT COUNT(pm.showpnlrank) FROM ww_showpnlmap pm "
                 "JOIN ww_shows s ON s.showid = pm.showid "
                 "WHERE pm.panelistid = %s AND pm.showpnlrank = '2' AND "
                 "s.bestof = 0 and s.repeatshowid IS NULL) as '2', ( "
                 "SELECT COUNT(pm.showpnlrank) FROM ww_showpnlmap pm "
                 "JOIN ww_shows s ON s.showid = pm.showid "
                 "WHERE pm.panelistid = %s AND pm.showpnlrank = '2t' AND "
                 "s.bestof = 0 and s.repeatshowid IS NULL) as '2t', ( "
                 "SELECT COUNT(pm.showpnlrank) FROM ww_showpnlmap pm "
                 "JOIN ww_shows s ON s.showid = pm.showid "
                 "WHERE pm.panelistid = %s AND pm.showpnlrank = '3' AND "
                 "s.bestof = 0 and s.repeatshowid IS NULL "
                 ") as '3';")
        cursor.execute(query, (panelist_id, panelist_id, panelist_id,
                               panelist_id, panelist_id, ))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return {}

        rank_info = {
            "first": result["1"],
            "first_tied":  result["1t"],
            "second": result["2"],
            "second_tied": result["2t"],
            "third": result["3"],
        }

        return rank_info

    @lru_cache(typed=True)
    def retrieve_rank_info_by_slug(self, panelist_slug: str) -> Dict[str, int]:
        """Returns a dictionary with ranking information for the
        requested panelist slug string.

        :param panelist_slug: Panelist slug string
        :type panelist_slug: str
        :return: Dictionary containing panelist ranking information. If
            panelist ranking information could not be returned, an empty
            dictionary will be returned.
        :rtype: Dict[str, int]
        """
        id_ = self.utility.convert_slug_to_id(panelist_slug)
        if not id_:
            return {}

        return self.retrieve_rank_info_by_id(id_)

    @lru_cache(typed=True)
    def retrieve_statistics_by_id(self, panelist_id: int) -> Dict[str, Any]:
        """Returns a dictionary containing panelist statistics, ranking
        data, and scoring data for the requested panelist ID.

        :param panelist_id: Panelist ID
        :type panelist_id: int
        :return: Dictionary containing panelist statistics. If panelist
            statistics could not be returned, an empty dictionary will
            be returned.
        :rtype: Dict[str, Any]
        """
        if not valid_int_id(panelist_id):
            return {}

        score_data = self.scores.retrieve_scores_by_id(panelist_id)
        ranks = self.retrieve_rank_info_by_id(panelist_id)

        if not score_data or not ranks:
            return {}

        appearance_count = len(score_data)
        scoring = {
            "minimum": int(numpy.amin(score_data)),
            "maximum": int(numpy.amax(score_data)),
            "mean": round(numpy.mean(score_data), 4),
            "median": int(numpy.median(score_data)),
            "standard_deviation": round(numpy.std(score_data), 4),
            "total": int(numpy.sum(score_data)),
        }

        ranks_first = round(100 * (ranks["first"] / appearance_count), 4)
        ranks_first_tied = round(100 * (ranks["first_tied"] / appearance_count), 4)
        ranks_second = round(100 * (ranks["second"] / appearance_count), 4)
        ranks_second_tied = round(100 * (ranks["second_tied"] / appearance_count), 4)
        ranks_third = round(100 * (ranks["third"] / appearance_count), 4)

        ranks_percentage = {
            "first": ranks_first,
            "first_tied": ranks_first_tied,
            "second": ranks_second,
            "second_tied": ranks_second_tied,
            "third": ranks_third,
        }

        ranking = {
            "rank": ranks,
            "percentage": ranks_percentage,
        }

        statistics = {
            "scoring": scoring,
            "ranking": ranking,
        }

        return statistics

    @lru_cache(typed=True)
    def retrieve_statistics_by_slug(self, panelist_slug: str) -> Dict[str, Any]:
        """Returns a dictionary containing panelist statistics, ranking
        data, and scoring data for the requested panelist slug string.

        :param panelist_slug: Panelist slug string
        :type panelist_slug: str
        :return: Dictionary containing panelist statistics. If panelist
            statistics could not be returned, an empty dictionary will
            be returned.
        :rtype: Dict[str, Any]
        """
        id_ = self.utility.convert_slug_to_id(panelist_slug)
        if not id_:
            return {}

        return self.retrieve_statistics_by_id(id_)
