# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is relased under the terms of the Apache License 2.0
"""Wait Wait Don't Tell Me! Stats Panelist Scores Retrieval Functions
"""
from typing import Any, Dict, List, Optional, Tuple

from mysql.connector import connect
from wwdtm.panelist.utility import PanelistUtility

class PanelistScores:
    """This class contains functions used to retrieve panelist scores
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

        self.utility = PanelistUtility(database_connection=self.database_connection)

    def retrieve_scores_by_id(self, id: int) -> List[int]:
        """Returns a list of panelist scores for appearances for the
        requested panelist ID.

        :param id: Panelist ID
        :type id: int
        :return: List containing panelist scores
        :rtype: List[int]
        """
        scores = []
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT s.showdate, pm.panelistscore "
                 "FROM ww_showpnlmap pm "
                 "JOIN ww_shows s ON s.showid = pm.showid "
                 "WHERE panelistid = %s "
                 "AND s.bestof = 0 and s.repeatshowid IS NULL;")
        cursor.execute(query, (id, ))
        result = cursor.fetchall()
        cursor.close()

        for appearance in result:
            if appearance["panelistscore"]:
                scores.append(appearance["panelistscore"])

        return scores

    def retrieve_scores_by_slug(self, slug: str
                               ) -> List[int]:
        """Returns a list of panelist scores for appearances for the
        requested panelist slug string.

        :param slug: Panelist slug string
        :type slug: str
        :return: List containing panelist scores
        :rtype: List[int]
        """
        id = self.utility.convert_slug_to_id(slug)
        if not id:
            return None

        return self.retrieve_scores_by_id(id)

    def retrieve_scores_grouped_list_by_id(self, id: int
                                          ) -> Dict[str, List[int]]:
        """Returns a panelist's score grouping for the requested
        panelist ID.

        :param id: Panelist ID
        :type id: int
        :return: Dictionary containing two lists, one containing scores
            and one containing counts of those scores
        :rtype: Dict[str, List[int]]
        """
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT MIN(pm.panelistscore) AS min, "
                 "MAX(pm.panelistscore) AS max "
                 "FROM ww_showpnlmap pm "
                 "LIMIT 1;")
        cursor.execute(query)
        result = cursor.fetchone()

        if not result:
            return None

        min_score = result["min"]
        max_score = result["max"]

        scores = {}
        for score in range(min_score, max_score + 1):
            scores[score] = 0

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT pm.panelistscore AS score, "
                 "COUNT(pm.panelistscore) AS score_count "
                 "FROM ww_showpnlmap pm "
                 "JOIN ww_shows s ON s.showid = pm.showid "
                 "WHERE pm.panelistid = %s "
                 "AND s.bestof = 0 AND s.repeatshowid IS NULL "
                 "AND pm.panelistscore IS NOT NULL "
                 "GROUP BY pm.panelistscore "
                 "ORDER BY pm.panelistscore ASC;")
        cursor.execute(query, (id, ))
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return None

        for row in results:
            scores[row["score"]] = row["score_count"]

        scores_list = {
            "score": list(scores.keys()),
            "count": list(scores.values()),
        }

        return scores_list

    def retrieve_scores_grouped_list_by_slug(self, slug: str
                                            ) -> Dict[str, List[int]]:
        """Returns a panelist's score grouping for the requested
        panelist slug string.

        :param slug: Panelist slug string
        :type slug: str
        :return: Dictionary containing two lists, one containing scores
            and one containing counts of those scores
        :rtype: Dict[str, List[int]]
        """
        id = self.utility.convert_slug_to_id(slug)
        if not id:
            return None

        return self.retrieve_scores_grouped_list_by_id(id)

    def retrieve_scores_grouped_ordered_pair_by_id(self, id: int
                                                  ) -> List[Tuple[int, int]]:
        """Returns an list of tuples containing a score and the
        corresponding number of instances a panelist has scored that amount
        for the requested panelist ID.

        :param id: Panelist ID
        :type id: int
        :return: List of tuples containing scores and score counts
        :rtype: List[Tuple[int, int]]
        """
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT MIN(pm.panelistscore) AS min, "
                 "MAX(pm.panelistscore) AS max "
                 "FROM ww_showpnlmap pm;")
        cursor.execute(query)
        result = cursor.fetchone()

        if not result:
            return None

        min_score = result["min"]
        max_score = result["max"]

        scores = {}
        for score in range(min_score, max_score + 1):
            scores[score] = 0

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT pm.panelistscore AS score, "
                 "COUNT(pm.panelistscore) AS score_count "
                 "FROM ww_showpnlmap pm "
                 "JOIN ww_shows s ON s.showid = pm.showid "
                 "WHERE pm.panelistid = %s "
                 "AND s.bestof = 0 AND s.repeatshowid IS NULL "
                 "AND pm.panelistscore IS NOT NULL "
                 "GROUP BY pm.panelistscore "
                 "ORDER BY pm.panelistscore ASC;")
        cursor.execute(query, (id, ))
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return None

        for row in results:
            scores[row["score"]] = row["score_count"]

        return list(scores.items())

    def retrieve_scores_grouped_ordered_pair_by_slug(self, slug: str,
                                                    ) -> List[Tuple[int, int]]:
        """Returns an list of tuples containing a score and the
        corresponding number of instances a panelist has scored that amount
        for the requested panelist slug string.

        :param slug: Panelist slug string
        :type slug: str
        :return: List of tuples containing scores and score counts
        :rtype: List[Tuple[int, int]]
        """
        id = self.utility.convert_slug_to_id(slug)
        if not id:
            return None

        return self.retrieve_scores_grouped_ordered_pair_by_id(id)

    def retrieve_scores_list_by_id(self, id: int,
                                  ) -> Dict[str, Any]:
        """Returns a dictionary containing two lists, one with show
        dates and one with corresponding scores for the requested
        panelist ID.

        :param id: Panelist ID
        :type id: int
        :return: List of tuples containing show dates and scores
        :rtype: Dict[str, Any]
        """
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT s.showdate, pm.panelistscore "
                 "FROM ww_showpnlmap pm "
                 "JOIN ww_shows s ON s.showid = pm.showid "
                 "WHERE pm.panelistid = %s "
                 "AND s.bestof = 0 AND s.repeatshowid IS NULL "
                 "AND pm.panelistscore IS NOT NULL "
                 "ORDER BY s.showdate ASC;")
        cursor.execute(query, (id, ))
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return None

        show_list = []
        score_list = []
        for shows in results:
            show_list.append(shows["showdate"].isoformat())
            score_list.append(shows["panelistscore"])

        scores = {
            "shows": show_list,
            "scores": score_list,
        }

        return scores

    def retrieve_scores_list_by_slug(self, slug: str,
                                  ) -> Dict[str, Any]:
        """Returns a dictionary containing two lists, one with show
        dates and one with corresponding scores for the requested
        panelist slug string.

        :param slug: Panelist slug string
        :type slug: str
        :return: List of tuples containing show dates and scores
        :rtype: Dict[str, Any]
        """
        id = self.utility.convert_slug_to_id(slug)
        if not id:
            return None

        return self.retrieve_scores_list_by_id(id)

    def retrieve_scores_ordered_pair_by_id(self, id: int
                                          ) -> List[Tuple[str, int]]:
        """Returns an list of tuples containing a show date and the
        corresponding score for the requested panelist ID.

        :param id: Panelist ID
        :type id: int
        :return: List of tuples containing show dates and scores
        :rtype: List[Tuple[str, int]]
        """
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT s.showdate, pm.panelistscore "
                 "FROM ww_showpnlmap pm "
                 "JOIN ww_shows s ON s.showid = pm.showid "
                 "WHERE pm.panelistid = %s "
                 "AND s.bestof = 0 AND s.repeatshowid IS NULL "
                 "AND pm.panelistscore IS NOT NULL "
                 "ORDER BY s.showdate ASC;")
        cursor.execute(query, (id, ))
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return None

        scores = []
        for show in results:
            show_date = show["showdate"].isoformat()
            score = show["panelistscore"]
            scores.append((show_date, score))

        return scores

    def retrieve_scores_ordered_pair_by_slug(self, slug: str,
                                            ) -> List[Tuple[str, int]]:
        """Returns an list of tuples containing a show date and the
        corresponding score for the requested panelist slug string.

        :param slug: Panelist slug string
        :type slug: str
        :return: List of tuples containing show dates and scores
        :rtype: List[Tuple[str, int]]
        """
        id = self.utility.convert_slug_to_id(slug)
        if not id:
            return None

        return self.retrieve_scores_ordered_pair_by_id(id)
