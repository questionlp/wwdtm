# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Panelist Decimal Scores Retrieval Functions."""

from decimal import Decimal
from math import floor
from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from wwdtm.panelist.utility import PanelistUtility
from wwdtm.validation import valid_int_id


class PanelistDecimalScores:
    """Panelist decimal score retrieval class.

    Contains methods used to retrieve panelist decimal scores and
    calculate scoring statistics.

    :param connect_dict: A dictionary containing database connection
        settings as required by MySQL Connector/Python
    :param database_connection: MySQL database connection object
    """

    def __init__(
        self,
        connect_dict: dict[str, Any] = None,
        database_connection: MySQLConnection | PooledMySQLConnection = None,
    ):
        """Class initialization method."""
        if connect_dict:
            self.connect_dict = connect_dict
            self.database_connection = connect(**connect_dict)
        elif database_connection:
            if not database_connection.is_connected():
                database_connection.reconnect()

            self.database_connection = database_connection

        self.utility = PanelistUtility(database_connection=self.database_connection)

    def retrieve_scores_by_id(self, panelist_id: int) -> list[Decimal]:
        """Retrieves a list of panelist decimal scores, sorted by show date.

        :param panelist_id: Panelist ID
        :return: A list containing panelist decimal scores
        """
        if not valid_int_id(panelist_id):
            return []

        scores = []
        cursor = self.database_connection.cursor(dictionary=True)
        query = """
            SELECT pm.panelistscore_decimal AS score
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE panelistid = %s
            AND s.bestof = 0 and s.repeatshowid IS NULL
            ORDER BY s.showdate ASC;
            """
        cursor.execute(query, (panelist_id,))
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return []

        for appearance in result:
            if appearance["score"]:
                scores.append(appearance["score"])

        return scores

    def retrieve_scores_by_slug(self, panelist_slug: str) -> list[Decimal]:
        """Retrieves a list of panelist decimal scores, sorted by show date.

        :param panelist_slug: Panelist slug string
        :return: A list containing panelist decimal scores
        """
        id_ = self.utility.convert_slug_to_id(panelist_slug)
        if not id_:
            return []

        return self.retrieve_scores_by_id(id_)

    def retrieve_scores_grouped_list_by_id(
        self, panelist_id: int
    ) -> dict[str, list[str | int]]:
        """Retrieves panelist grouped decimal scores.

        :param panelist_id: Panelist ID
        :return: A dictionary containing two lists, one containing
            decimal scores and one containing counts of those scores
        """
        if not valid_int_id(panelist_id):
            return {}

        cursor = self.database_connection.cursor(dictionary=True)
        query = """
            SELECT MIN(pm.panelistscore_decimal) AS min,
            MAX(pm.panelistscore_decimal) AS max
            FROM ww_showpnlmap pm
            LIMIT 1;
            """
        cursor.execute(query)
        result = cursor.fetchone()

        if not result:
            return {}

        min_score = result["min"]
        max_score = result["max"]

        scores = {}
        for score in range(floor(min_score), floor(max_score) + 1):
            score = Decimal(score)
            score_plus_half = Decimal(score) + Decimal("0.5")
            scores[f"{score.normalize():f}"] = 0
            scores[f"{score_plus_half.normalize():f}"] = 0

        query = """
            SELECT pm.panelistscore_decimal AS score,
            COUNT(pm.panelistscore_decimal) AS score_count
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistid = %s
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            AND pm.panelistscore_decimal IS NOT NULL
            GROUP BY pm.panelistscore_decimal
            ORDER BY pm.panelistscore_decimal ASC;
            """
        cursor.execute(query, (panelist_id,))
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        for row in results:
            scores[f"{Decimal(row['score']).normalize():f}"] = row["score_count"]

        return {
            "score": list(scores.keys()),
            "count": list(scores.values()),
        }

    def retrieve_scores_grouped_list_by_slug(
        self, panelist_slug: str
    ) -> dict[str, list[int]]:
        """Retrieves panelist grouped decimal scores.

        :param panelist_slug: Panelist slug string
        :return: A dictionary containing two lists, one containing
            decimal scores and one containing counts of those scores
        """
        id_ = self.utility.convert_slug_to_id(panelist_slug)
        if not id_:
            return {}

        return self.retrieve_scores_grouped_list_by_id(id_)

    def retrieve_scores_grouped_ordered_pair_by_id(
        self, panelist_id: int
    ) -> list[tuple[str, int]]:
        """Retrieves a list of panelist decimal scores and counts as a tuple.

        :param panelist_id: Panelist ID
        :return: A list of tuples containing decimal scores and score
            counts
        """
        if not valid_int_id(panelist_id):
            return []

        cursor = self.database_connection.cursor(dictionary=True)
        query = """
            SELECT MIN(pm.panelistscore_decimal) AS min,
            MAX(pm.panelistscore_decimal) AS max
            FROM ww_showpnlmap pm;
            """
        cursor.execute(query)
        result = cursor.fetchone()

        if not result:
            return []

        min_score = result["min"]
        max_score = result["max"]

        scores = {}
        for score in range(floor(min_score), floor(max_score) + 1):
            score = Decimal(score)
            score_plus_half = Decimal(score) + Decimal("0.5")
            scores[f"{score.normalize():f}"] = 0
            scores[f"{score_plus_half.normalize():f}"] = 0

        query = """
            SELECT pm.panelistscore_decimal AS score,
            COUNT(pm.panelistscore_decimal) AS score_count
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistid = %s
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            AND pm.panelistscore_decimal IS NOT NULL
            GROUP BY pm.panelistscore_decimal
            ORDER BY pm.panelistscore_decimal ASC;
            """
        cursor.execute(query, (panelist_id,))
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        for row in results:
            scores[f"{Decimal(row['score']).normalize():f}"] = row["score_count"]

        return list(scores.items())

    def retrieve_scores_grouped_ordered_pair_by_slug(
        self,
        panelist_slug: str,
    ) -> list[tuple[str, int]]:
        """Retrieves a list of panelist decimal scores and counts as a tuple.

        :param panelist_slug: Panelist slug string
        :return: A list of tuples containing decimal scores and score
            counts
        """
        id_ = self.utility.convert_slug_to_id(panelist_slug)
        if not id_:
            return []

        return self.retrieve_scores_grouped_ordered_pair_by_id(id_)

    def retrieve_scores_list_by_id(
        self,
        panelist_id: int,
    ) -> dict[str, list[str | Decimal]]:
        """Retrieves panelist appearances and decimal scores as paired lists.

        :param panelist_id: Panelist ID
        :return: A dictionary containing a list show dates and a list
            of decimal scores
        """
        if not valid_int_id(panelist_id):
            return {}

        cursor = self.database_connection.cursor(dictionary=True)
        query = """
            SELECT s.showdate AS date, pm.panelistscore_decimal AS score
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistid = %s
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            AND pm.panelistscore_decimal IS NOT NULL
            ORDER BY s.showdate ASC;
            """
        cursor.execute(query, (panelist_id,))
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        show_list = []
        score_list = []
        for shows in results:
            show_list.append(shows["date"].isoformat())
            score_list.append(shows["score"])

        return {
            "shows": show_list,
            "scores": score_list,
        }

    def retrieve_scores_list_by_slug(
        self,
        panelist_slug: str,
    ) -> dict[str, list[str | Decimal]]:
        """Retrieves panelist appearances and decimal scores as paired lists.

        :param panelist_slug: Panelist slug string
        :return: A dictionary containing a list show dates and a list
            of decimal scores
        """
        id_ = self.utility.convert_slug_to_id(panelist_slug)
        if not id_:
            return {}

        return self.retrieve_scores_list_by_id(id_)

    def retrieve_scores_ordered_pair_by_id(
        self, panelist_id: int
    ) -> list[tuple[str, Decimal]]:
        """Retrieves panelist appearances and decimal scores as a list of tuples.

        :param panelist_id: Panelist ID
        :return: A list of tuples containing show dates and decimal
            scores
        """
        if not valid_int_id(panelist_id):
            return []

        cursor = self.database_connection.cursor(dictionary=True)
        query = """
            SELECT s.showdate AS date, pm.panelistscore_decimal AS score
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistid = %s
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            AND pm.panelistscore_decimal IS NOT NULL
            ORDER BY s.showdate ASC;
            """
        cursor.execute(query, (panelist_id,))
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        scores = []
        for show in results:
            show_date = show["date"].isoformat()
            score = show["score"]
            scores.append((show_date, score))

        return scores

    def retrieve_scores_ordered_pair_by_slug(
        self,
        panelist_slug: str,
    ) -> list[tuple[str, Decimal]]:
        """Retrieves panelist appearances and decimal scores as a list of tuples.

        :param panelist_slug: Panelist slug string
        :return: A list of tuples containing show dates and decimal
            scores
        """
        id_ = self.utility.convert_slug_to_id(panelist_slug)
        if not id_:
            return []

        return self.retrieve_scores_ordered_pair_by_id(id_)
