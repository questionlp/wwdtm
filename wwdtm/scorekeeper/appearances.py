# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Scorekeeper Appearance Retrieval Functions."""

from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from wwdtm.scorekeeper.utility import ScorekeeperUtility
from wwdtm.validation import valid_int_id


class ScorekeeperAppearances:
    """Scorekeeper appearance information retrieval class.

    Contains methods used to retrieve scorekeeper appearance
    information, including show flags.

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

        self.utility = ScorekeeperUtility(database_connection=self.database_connection)

    def retrieve_appearances_by_id(self, scorekeeper_id: int) -> dict[str, Any]:
        """Retrieves scorekeeper appearance information.

        :param scorekeeper_id: Scorekeeper ID
        :return: A dictionary containing scorekeeper appearances with
            corresponding show dates and Best Of or Repeat show flags
        """
        if not valid_int_id(scorekeeper_id):
            return {}

        query = """
            SELECT (
            SELECT COUNT(skm.showid) FROM ww_showskmap skm
            JOIN ww_shows s ON s.showid = skm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL AND
            skm.scorekeeperid = %s ) AS regular_shows, (
            SELECT COUNT(skm.showid) FROM ww_showskmap skm
            JOIN ww_shows s ON s.showid = skm.showid
            WHERE skm.scorekeeperid = %s ) AS all_shows;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(
            query,
            (
                scorekeeper_id,
                scorekeeper_id,
            ),
        )
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

        query = """
            SELECT skm.showid AS show_id, s.showdate AS date,
            s.bestof AS best_of, s.repeatshowid AS repeat_show_id,
            skm.guest, skm.description
            FROM ww_showskmap skm
            JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
            JOIN ww_shows s ON s.showid = skm.showid
            WHERE sk.scorekeeperid = %s
            ORDER BY s.showdate ASC;
            """
        cursor.execute(query, (scorekeeper_id,))
        results = cursor.fetchall()
        cursor.close()

        if results:
            appearances = []
            for appearance in results:
                info = {
                    "show_id": appearance["show_id"],
                    "date": appearance["date"].isoformat(),
                    "best_of": bool(appearance["best_of"]),
                    "repeat_show": bool(appearance["repeat_show_id"]),
                    "guest": bool(appearance["guest"]),
                    "description": appearance["description"],
                }
                appearances.append(info)

            return {
                "count": appearance_counts,
                "shows": appearances,
            }

        else:
            return {
                "count": appearance_counts,
                "shows": [],
            }

    def retrieve_appearances_by_slug(self, scorekeeper_slug: str) -> dict[str, Any]:
        """Retrieves scorekeeper appearance information.

        :param scorekeeper_slug: Scorekeeper slug string
        :return: A dictionary containing scorekeeper appearances with
            corresponding show dates and Best Of or Repeat show flags
        """
        id_ = self.utility.convert_slug_to_id(scorekeeper_slug)
        if not id_:
            return {}

        return self.retrieve_appearances_by_id(id_)
