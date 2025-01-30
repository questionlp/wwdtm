# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Panelist Appearance Retrieval Functions."""

from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from wwdtm.panelist.utility import PanelistUtility
from wwdtm.validation import valid_int_id


class PanelistAppearances:
    """Panelist appearance information retrieval class.

    Contains methods used to retrieve panelist appearance information
    and statistics, scores and rankings.

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

    def retrieve_appearances_by_id(
        self, panelist_id: int, use_decimal_scores: bool = False
    ) -> dict[str, Any]:
        """Retrieves panelist appearance information.

        :param panelist_id: Panelist ID
        :param use_decimal_scores: A boolean to determine if decimal
            scores returned instead of integer scores
        :return: A dictionary containing appearance statistics, scoring
            and ranking details
        """
        if not valid_int_id(panelist_id):
            return {}

        query = """
            SELECT (
            SELECT COUNT(pm.showid) FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL AND
            pm.panelistid = %s ) AS regular_shows, (
            SELECT COUNT(pm.showid) FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistid = %s ) AS all_shows, (
            SELECT COUNT(pm.panelistid) FROM ww_showpnlmap pm
            JOIN ww_shows s ON pm.showid = s.showid
            WHERE pm.panelistid = %s AND s.bestof = 0 AND
            s.repeatshowid IS NULL
            AND pm.panelistscore IS NOT NULL )
            AS shows_with_scores;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(
            query,
            (
                panelist_id,
                panelist_id,
                panelist_id,
            ),
        )
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

        query = """
            SELECT MIN(s.showid) AS first_id, MIN(s.showdate) AS first,
            MAX(s.showid) AS most_recent_id, MAX(s.showdate) AS most_recent
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            AND pm.panelistid = %s
            ORDER BY s.showdate ASC;
            """
        cursor.execute(query, (panelist_id,))
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

        if use_decimal_scores:
            query = """
                SELECT pm.showid AS show_id, s.showdate AS date,
                s.bestof AS best_of, s.repeatshowid AS repeat_show_id,
                pm.panelistlrndstart AS start,
                pm.panelistlrndstart_decimal AS start_decimal,
                pm.panelistlrndcorrect AS correct,
                pm.panelistlrndcorrect_decimal AS correct_decimal,
                pm.panelistscore AS score,
                pm.panelistscore_decimal AS score_decimal,
                pm.showpnlrank AS pnl_rank FROM ww_showpnlmap pm
                JOIN ww_panelists p ON p.panelistid = pm.panelistid
                JOIN ww_shows s ON s.showid = pm.showid
                WHERE pm.panelistid = %s
                ORDER BY s.showdate ASC;
                """
        else:
            query = """
                SELECT pm.showid AS show_id, s.showdate AS date,
                s.bestof AS best_of, s.repeatshowid AS repeat_show_id,
                pm.panelistlrndstart AS start,
                pm.panelistlrndcorrect AS correct,
                pm.panelistscore AS score,
                pm.showpnlrank AS pnl_rank FROM ww_showpnlmap pm
                JOIN ww_panelists p ON p.panelistid = pm.panelistid
                JOIN ww_shows s ON s.showid = pm.showid
                WHERE pm.panelistid = %s
                ORDER BY s.showdate ASC;
                """

        cursor.execute(query, (panelist_id,))
        results = cursor.fetchall()
        cursor.close()

        if result:
            appearances = []
            for appearance in results:
                info = {
                    "show_id": appearance["show_id"],
                    "date": appearance["date"].isoformat(),
                    "best_of": bool(appearance["best_of"]),
                    "repeat_show": bool(appearance["repeat_show_id"]),
                    "lightning_round_start": appearance["start"],
                    "lightning_round_start_decimal": appearance.get(
                        "start_decimal", None
                    ),
                    "lightning_round_correct": appearance["correct"],
                    "lightning_round_correct_decimal": appearance.get(
                        "correct_decimal", None
                    ),
                    "score": appearance["score"],
                    "score_decimal": appearance.get("score_decimal", None),
                    "rank": appearance.get("pnl_rank", None),
                }
                appearances.append(info)

            appearance_info["count"] = appearance_counts
            appearance_info["shows"] = appearances
        else:
            appearance_info["count"] = appearance_counts
            appearance_info["shows"] = []

        return appearance_info

    def retrieve_appearances_by_slug(
        self, panelist_slug: str, use_decimal_scores: bool = False
    ) -> dict[str, Any]:
        """Retrieves panelist appearance information.

        :param panelist_slug: Panelist slug string
        :param use_decimal_scores: A boolean to determine if decimal
            scores returned instead of integer scores
        :return: A dictionary containing appearance statistics, scoring
            and ranking details
        """
        id_ = self.utility.convert_slug_to_id(panelist_slug)
        if not id_:
            return {}

        return self.retrieve_appearances_by_id(
            id_, use_decimal_scores=use_decimal_scores
        )

    def retrieve_yearly_appearances_by_id(self, panelist_id: int) -> dict[int, int]:
        """Retrieves panelist appearance counts grouped by year.

        :param panelist_id: Panelist ID
        :return: A dictionary containing years as keys and appearance
            counts for each year as values
        """
        if not valid_int_id(panelist_id):
            return {}

        query = """
            SELECT DISTINCT YEAR(s.showdate) AS year
            FROM ww_shows s
            ORDER BY YEAR(s.showdate) ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            return {}

        years = {}
        for row in results:
            years[row["year"]] = 0

        query = """
            SELECT YEAR(s.showdate) AS year,
            COUNT(p.panelist) AS count
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            WHERE pm.panelistid = %s AND s.bestof = 0
            AND s.repeatshowid IS NULL
            GROUP BY p.panelist, YEAR(s.showdate)
            ORDER BY p.panelist ASC, YEAR(s.showdate) ASC;
            """
        cursor.execute(query, (panelist_id,))
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        for row in results:
            years[row["year"]] = row["count"]

        return years

    def retrieve_yearly_appearances_by_slug(self, panelist_slug: str) -> dict[int, int]:
        """Retrieves panelist appearance counts grouped by year.

        :param panelist_slug: Panelist slug string
        :return: A dictionary containing years as keys and appearance
            counts for each year as values
        """
        id_ = self.utility.convert_slug_to_id(panelist_slug)
        if not id_:
            return {}

        return self.retrieve_yearly_appearances_by_id(id_)
