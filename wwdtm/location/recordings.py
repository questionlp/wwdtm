# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is relased under the terms of the Apache License 2.0
"""Wait Wait Don't Tell Me! Stats Location Recordings Retrieval Functions
"""
from functools import lru_cache
from typing import Any, Dict, Optional

from mysql.connector import connect
from wwdtm.location.utility import LocationUtility

class LocationRecordings:
    """This class contains functions that retrieve location recordings
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

        self.utility = LocationUtility(database_connection=self.database_connection)

    @lru_cache(maxsize=256, typed=True)
    def retrieve_recordings_by_id(self, id: int) -> Dict[str, Any]:
        """Returns a list of dictionary objects containing recording
        information for the requested location ID.

        :param id: Location ID
        :type id: int
        :return: Dictionary containing recording counts and a list of
            appearances for a location
        :rtype: Dict[str, Any]
        """
        try:
            id = int(id)
        except ValueError:
            return None

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT ( "
                 "SELECT COUNT(lm.showid) FROM ww_showlocationmap lm "
                 "JOIN ww_shows s ON s.showid = lm.showid "
                 "WHERE s.bestof = 0 AND s.repeatshowid IS NULL AND "
                 "lm.locationid = %s ) AS regular_shows, ( "
                 "SELECT COUNT(lm.showid) FROM ww_showlocationmap lm "
                 "JOIN ww_shows s ON s.showid = lm.showid "
                 "WHERE lm.locationid = %s ) AS all_shows;")
        cursor.execute(query, (id, id ,))
        result = cursor.fetchone()

        recording_counts = {
            "regular_shows": result["regular_shows"],
            "all_shows": result["all_shows"],
        }

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT lm.showid AS show_id, s.showdate AS date, "
                 "s.bestof AS best_of, s.repeatshowid "
                 "FROM ww_showlocationmap lm "
                 "JOIN ww_shows s ON s.showid = lm.showid "
                 "WHERE lm.locationid = %s "
                 "ORDER BY s.showdate ASC;")
        cursor.execute(query, (id, ))
        results = cursor.fetchall()
        cursor.close()

        if results:
            recordings = []
            for recording in results:
                info = {
                    "show_id": recording["show_id"],
                    "date": recording["date"].isoformat(),
                    "best_of": bool(recording["best_of"]),
                    "repeat_show": bool(recording["repeatshowid"]),
                }
                recordings.append(info)

            recording_info = {
                "count": recording_counts,
                "shows": recordings,
            }
        else:
            recording_info = {
                "count": recording_counts,
                "shows": [],
            }

        return recording_info

    def retrieve_recordings_by_slug(self, slug: str) -> Dict[str, Any]:
        """Returns a list of dictionary objects containing recording
        information for the requested location slug string.

        :param slug: Location slug string
        :type slug: str
        :return: Dictionary containing recording counts and a list of
            appearances for a location
        :rtype: Dict[str, Any]
        """
        id = self.utility.convert_slug_to_id(slug)
        if not id:
            return None

        return self.retrieve_recordings_by_id(id)
