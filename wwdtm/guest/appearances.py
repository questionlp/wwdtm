# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
"""Wait Wait Don't Tell Me! Stats Guest Appearance Retrieval Functions
"""
from functools import lru_cache
from typing import Any, Dict, Optional

from mysql.connector import connect
from wwdtm.guest.utility import GuestUtility
from wwdtm.validation import valid_int_id


class GuestAppearances:
    """This class contains functions that retrieve guest appearance
    information from a copy of the Wait Wait Stats database.

    :param connect_dict: Dictionary containing database connection
        settings as required by mysql.connector.connect
    :param database_connection: mysql.connector.connect database
        connection
    """

    def __init__(
        self,
        connect_dict: Optional[Dict[str, Any]] = None,
        database_connection: Optional[connect] = None,
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

    @lru_cache(typed=True)
    def retrieve_appearances_by_id(self, guest_id: int) -> Dict[str, Any]:
        """Returns a list of dictionary objects containing appearance
        information for the requested guest ID.

        :param guest_id: Guest ID
        :return: Dictionary containing appearance counts and list of
            appearances for a guest. If guest appearances could not be
            retrieved, an empty dictionary is returned.
        """
        if not valid_int_id(guest_id):
            return {}

        cursor = self.database_connection.cursor(named_tuple=True)
        query = (
            "SELECT ( "
            "SELECT COUNT(gm.showid) FROM ww_showguestmap gm "
            "JOIN ww_shows s ON s.showid = gm.showid "
            "WHERE s.bestof = 0 AND s.repeatshowid IS NULL AND "
            "gm.guestid = %s ) AS regular_shows, ( "
            "SELECT COUNT(gm.showid) FROM ww_showguestmap gm "
            "JOIN ww_shows s ON s.showid = gm.showid "
            "WHERE gm.guestid = %s ) AS all_shows;"
        )
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
                "regular_shows": result.regular_shows,
                "all_shows": result.all_shows,
            }
        else:
            appearance_counts = {
                "regular_shows": 0,
                "all_shows": 0,
            }

        cursor = self.database_connection.cursor(named_tuple=True)
        query = (
            "SELECT gm.showid AS show_id, s.showdate AS date, "
            "s.bestof AS best_of, s.repeatshowid AS repeat_show_id, "
            "gm.guestscore AS score, gm.exception AS score_exception "
            "FROM ww_showguestmap gm "
            "JOIN ww_guests g ON g.guestid = gm.guestid "
            "JOIN ww_shows s ON s.showid = gm.showid "
            "WHERE gm.guestid = %s "
            "ORDER BY s.showdate ASC;"
        )
        cursor.execute(query, (guest_id,))
        results = cursor.fetchall()
        cursor.close()

        if results:
            appearances = []
            for appearance in results:
                info = {
                    "show_id": appearance.show_id,
                    "date": appearance.date.isoformat(),
                    "best_of": bool(appearance.best_of),
                    "repeat_show": bool(appearance.repeat_show_id),
                    "score": appearance.score,
                    "score_exception": bool(appearance.score_exception),
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

    @lru_cache(typed=True)
    def retrieve_appearances_by_slug(self, guest_slug: str) -> Dict[str, Any]:
        """Returns a list of dictionary objects containing appearance
        information for the requested guest slug string.

        :param guest_slug: Guest slug string
        :return: Dictionary containing appearance counts and list of
            appearances for a guest. If guest appearances could not be
            retrieved, empty dictionary is returned.
        """
        id_ = self.utility.convert_slug_to_id(guest_slug)
        if not id_:
            return {}

        return self.retrieve_appearances_by_id(id_)
