# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Panelist Statistics Retrieval Functions."""

from decimal import Decimal
from typing import Any

import numpy
from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from wwdtm.panelist.decimal_scores import PanelistDecimalScores
from wwdtm.panelist.scores import PanelistScores
from wwdtm.panelist.utility import PanelistUtility
from wwdtm.validation import valid_int_id


class PanelistStatistics:
    """Panelist statistics information retrieval and calculation class.

    Contains methods used to retrieve Bluff the Listener, ranking
    and scoring statistics.

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

        self.scores = PanelistScores(database_connection=self.database_connection)
        self.scores_decimal = PanelistDecimalScores(
            database_connection=self.database_connection
        )
        self.utility = PanelistUtility(database_connection=self.database_connection)

    def retrieve_bluffs_by_id(self, panelist_id: int) -> dict[str, int]:
        """Retrieve panelist Bluff the Listener statistics.

        :param panelist_id: Panelist ID
        :return: A dictionary containing number of times a panelist's
            Bluff the Listener story was chosen and number of times
            they had the correct story
        """
        query = """
            SELECT (
            SELECT COUNT(blm.chosenbluffpnlid) FROM ww_showbluffmap blm
            JOIN ww_shows s ON s.showid = blm.showid
            WHERE s.repeatshowid IS NULL AND blm.chosenbluffpnlid = %s
            ) AS chosen, (
            SELECT COUNT(blm.correctbluffpnlid) FROM ww_showbluffmap blm
            JOIN ww_shows s ON s.showid = blm.showid
            WHERE s.repeatshowid IS NULL AND blm.correctbluffpnlid = %s
            ) AS correct;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(
            query,
            (
                panelist_id,
                panelist_id,
            ),
        )
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return {}

        return {
            "chosen": result["chosen"],
            "correct": result["correct"],
        }

    def retrieve_bluffs_by_slug(self, panelist_slug: str) -> dict[str, int]:
        """Retrieve panelist Bluff the Listener statistics.

        :param panelist_slug: Panelist slug string
        :return: A dictionary containing number of times a panelist's
            Bluff the Listener story was chosen and number of times
            they had the correct story
        """
        id_ = self.utility.convert_slug_to_id(panelist_slug)
        if not id_:
            return {}

        return self.retrieve_bluffs_by_id(id_)

    def retrieve_rank_info_by_id(self, panelist_id: int) -> dict[str, int]:
        """Retrieves panelist ranking information.

        :param panelist_id: Panelist ID
        :return: A dictionary containing the number of times a panelist
            has finished in 1st, 1st tied, 2nd, 2nd tied and 3rd place
        """
        if not valid_int_id(panelist_id):
            return {}

        query = """
            SELECT (
            SELECT COUNT(pm.showpnlrank) FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistid = %s AND pm.showpnlrank = '1' AND
            s.bestof = 0 and s.repeatshowid IS NULL) as 'first', (
            SELECT COUNT(pm.showpnlrank) FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistid = %s AND pm.showpnlrank = '1t' AND
            s.bestof = 0 and s.repeatshowid IS NULL) as 'first_tied', (
            SELECT COUNT(pm.showpnlrank) FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistid = %s AND pm.showpnlrank = '2' AND
            s.bestof = 0 and s.repeatshowid IS NULL) as 'second', (
            SELECT COUNT(pm.showpnlrank) FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistid = %s AND pm.showpnlrank = '2t' AND
            s.bestof = 0 and s.repeatshowid IS NULL) as 'second_tied', (
            SELECT COUNT(pm.showpnlrank) FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistid = %s AND pm.showpnlrank = '3' AND
            s.bestof = 0 and s.repeatshowid IS NULL
            ) as 'third';
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(
            query,
            (
                panelist_id,
                panelist_id,
                panelist_id,
                panelist_id,
                panelist_id,
            ),
        )
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return {}

        return {
            "first": result["first"],
            "first_tied": result["first_tied"],
            "second": result["second"],
            "second_tied": result["second_tied"],
            "third": result["third"],
        }

    def retrieve_rank_info_by_slug(self, panelist_slug: str) -> dict[str, int]:
        """Retrieves panelist ranking information.

        :param panelist_slug: Panelist slug string
        :return: A dictionary containing the number of times a panelist
            has finished in 1st, 1st tied, 2nd, 2nd tied and 3rd place
        """
        id_ = self.utility.convert_slug_to_id(panelist_slug)
        if not id_:
            return {}

        return self.retrieve_rank_info_by_id(id_)

    def retrieve_statistics_by_id(
        self, panelist_id: int, include_decimal_scores: bool = False
    ) -> dict[str, Any]:
        """Retrieves and calculates panelist statistics.

        :param panelist_id: Panelist ID
        :param use_decimal_scores: A boolean to determine if decimal
            scores should be used and returned instead of integer scores
        :return: A dictionary containing panelist scoring and ranking
            statistics
        """
        if not valid_int_id(panelist_id):
            return {}

        score_data = self.scores.retrieve_scores_by_id(panelist_id)
        ranks = self.retrieve_rank_info_by_id(panelist_id)
        if not score_data or not ranks:
            return {}

        if include_decimal_scores:
            score_data_decimal = self.scores_decimal.retrieve_scores_by_id(panelist_id)
            if not score_data_decimal:
                return {}

        appearance_count = len(score_data)
        scoring = {
            "minimum": int(numpy.amin(score_data)),
            "maximum": int(numpy.amax(score_data)),
            "mean": round(numpy.mean(score_data), 5),
            "median": int(numpy.median(score_data)),
            "standard_deviation": round(numpy.std(score_data), 5),
            "total": int(numpy.sum(score_data)),
        }

        if include_decimal_scores:
            scoring_decimal = {
                "minimum": Decimal(numpy.amin(score_data_decimal)),
                "maximum": Decimal(numpy.amax(score_data_decimal)),
                "mean": round(Decimal(numpy.mean(score_data_decimal)), 5),
                "median": Decimal(numpy.median(score_data_decimal)),
                "standard_deviation": round(Decimal(numpy.std(score_data_decimal)), 5),
                "total": Decimal(numpy.sum(score_data_decimal)),
            }

        ranks_first = round(100 * (ranks["first"] / appearance_count), 5)
        ranks_first_tied = round(100 * (ranks["first_tied"] / appearance_count), 5)
        ranks_second = round(100 * (ranks["second"] / appearance_count), 5)
        ranks_second_tied = round(100 * (ranks["second_tied"] / appearance_count), 5)
        ranks_third = round(100 * (ranks["third"] / appearance_count), 5)

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

        if include_decimal_scores:
            return {
                "scoring": scoring,
                "scoring_decimal": scoring_decimal,
                "ranking": ranking,
            }
        else:
            return {
                "scoring": scoring,
                "ranking": ranking,
            }

    def retrieve_statistics_by_slug(
        self, panelist_slug: str, include_decimal_scores: bool = False
    ) -> dict[str, Any]:
        """Retrieves and calculates panelist statistics.

        :param panelist_slug: Panelist slug string
        :param use_decimal_scores: A boolean to determine if decimal
            scores should be used and returned instead of integer scores
        :return: A dictionary containing panelist scoring and ranking
            statistics
        """
        id_ = self.utility.convert_slug_to_id(panelist_slug)
        if not id_:
            return {}

        return self.retrieve_statistics_by_id(
            id_, include_decimal_scores=include_decimal_scores
        )
