# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Location Recordings Retrieval Functions."""

from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from wwdtm.location.utility import LocationUtility
from wwdtm.validation import valid_int_id


class LocationRecordings:
    """Location recording information retrieval class.

    Contains methods used to retrieve recording information, including
    show flags.

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

        self.utility = LocationUtility(database_connection=self.database_connection)

    def retrieve_recordings_by_id(self, location_id: int) -> dict[str, Any]:
        """Retrieves location recording information.

        Location recording information includes the corresponding show
        dates and Best Of or Repeat show flags.

        :param location_id: Location ID
        :return: A dictionary containing location recording counts,
            dates and show flags
        """
        if not valid_int_id(location_id):
            return {}

        query = """
            SELECT (
            SELECT COUNT(lm.showid) FROM ww_showlocationmap lm
            JOIN ww_shows s ON s.showid = lm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL AND
            lm.locationid = %s ) AS regular_shows, (
            SELECT COUNT(lm.showid) FROM ww_showlocationmap lm
            JOIN ww_shows s ON s.showid = lm.showid
            WHERE lm.locationid = %s ) AS all_shows;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(
            query,
            (
                location_id,
                location_id,
            ),
        )
        result = cursor.fetchone()

        recording_counts = {
            "regular_shows": result["regular_shows"],
            "all_shows": result["all_shows"],
        }

        query = """
            SELECT lm.showid AS show_id, s.showdate AS date,
            s.bestof AS best_of, s.repeatshowid AS repeat_show_id
            FROM ww_showlocationmap lm
            JOIN ww_shows s ON s.showid = lm.showid
            WHERE lm.locationid = %s
            ORDER BY s.showdate ASC;
            """
        cursor.execute(query, (location_id,))
        results = cursor.fetchall()
        cursor.close()

        if results:
            recordings = []
            for recording in results:
                info = {
                    "show_id": recording["show_id"],
                    "date": recording["date"].isoformat(),
                    "best_of": bool(recording["best_of"]),
                    "repeat_show": bool(recording["repeat_show_id"]),
                }
                recordings.append(info)

            return {
                "count": recording_counts,
                "shows": recordings,
            }
        else:
            return {
                "count": recording_counts,
                "shows": [],
            }

    def retrieve_recordings_by_slug(self, location_slug: str) -> dict[str, Any]:
        """Retrieves location recording information.

        Location recording information includes the corresponding show
        dates and Best Of or Repeat show flags.

        :param location_slug: Location slug string
        :return: A dictionary containing location recording counts,
            dates and show flags
        """
        id_ = self.utility.convert_slug_to_id(location_slug)
        if not id_:
            return {}

        return self.retrieve_recordings_by_id(id_)
