# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Host Appearance Retrieval Functions."""

from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from wwdtm.host.utility import HostUtility
from wwdtm.validation import valid_int_id


class HostAppearances:
    """Host appearance information retrieval class.

    Contains methods used to retrieve host appearance information,
    including show flags.

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

        self.utility = HostUtility(database_connection=self.database_connection)

    def retrieve_appearances_by_id(self, host_id: int) -> dict[str, Any]:
        """Retrieves host appearance information.

        :param host_id: Host ID
        :return: A dictionary containing host appearances with
            corresponding show dates and Best Of or Repeat show flags
        """
        if not valid_int_id(host_id):
            return {}

        query = """
            SELECT (
            SELECT COUNT(hm.showid) FROM ww_showhostmap hm
            JOIN ww_shows s ON s.showid = hm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL AND
            hm.hostid = %s ) AS regular_shows, (
            SELECT COUNT(hm.showid) FROM ww_showhostmap hm
            JOIN ww_shows s ON s.showid = hm.showid
            WHERE hm.hostid = %s ) AS all_shows;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(
            query,
            (
                host_id,
                host_id,
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
            SELECT hm.showid AS show_id, s.showdate AS date,
            s.bestof AS best_of, s.repeatshowid AS repeat_show_id,
            hm.guest FROM ww_showhostmap hm
            JOIN ww_hosts h ON h.hostid = hm.hostid
            JOIN ww_shows s ON s.showid = hm.showid
            WHERE hm.hostid = %s
            ORDER BY s.showdate ASC;
            """
        cursor.execute(query, (host_id,))
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

    def retrieve_appearances_by_slug(self, host_slug: str) -> dict[str, Any]:
        """Retrieves host appearance information.

        :param host_slug: Host slug string
        :return: A dictionary containing host appearances with
            corresponding show dates and Best Of or Repeat show flags
        """
        id_ = self.utility.convert_slug_to_id(host_slug)
        if not id_:
            return {}

        return self.retrieve_appearances_by_id(id_)
