# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Guest Appearance Retrieval Functions."""

from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from wwdtm.guest.utility import GuestUtility
from wwdtm.validation import valid_int_id


class GuestAppearances:
    """Guest appearance information retrieval class.

    Contains methods used to retrieve Not My Job guest appearance
    information, scores and scoring exceptions.

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

        self.utility = GuestUtility(database_connection=self.database_connection)

    def retrieve_appearances_by_id(self, guest_id: int) -> dict[str, Any]:
        """Retrieves guest appearance information.

        :param guest_id: Guest ID
        :return: A dictionary containing guest appearances with
            corresponding show dates, Best Of or Repeat show flags,
            score and score exception flag
        """
        if not valid_int_id(guest_id):
            return {}

        query = """
            SELECT (
            SELECT COUNT(gm.showid) FROM ww_showguestmap gm
            JOIN ww_shows s ON s.showid = gm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL AND
            gm.guestid = %s ) AS regular_shows, (
            SELECT COUNT(gm.showid) FROM ww_showguestmap gm
            JOIN ww_shows s ON s.showid = gm.showid
            WHERE gm.guestid = %s ) AS all_shows;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(
            query,
            (
                guest_id,
                guest_id,
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
            SELECT gm.showid AS show_id, s.showdate AS date,
            s.bestof AS best_of, s.repeatshowid AS repeat_show_id,
            gm.guestscore AS score, gm.exception AS score_exception
            FROM ww_showguestmap gm
            JOIN ww_guests g ON g.guestid = gm.guestid
            JOIN ww_shows s ON s.showid = gm.showid
            WHERE gm.guestid = %s
            ORDER BY s.showdate ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (guest_id,))
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
                    "score": appearance["score"],
                    "score_exception": bool(appearance["score_exception"]),
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

    def retrieve_appearances_by_slug(self, guest_slug: str) -> dict[str, Any]:
        """Retrieves guest appearance information.

        :param guest_slug: Guest slug string
        :return: A dictionary containing guest appearances with
            corresponding show dates, Best Of or Repeat show flags,
            score and score exception flag
        """
        id_ = self.utility.convert_slug_to_id(guest_slug)
        if not id_:
            return {}

        return self.retrieve_appearances_by_id(id_)
