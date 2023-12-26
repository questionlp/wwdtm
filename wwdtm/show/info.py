# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2023 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
"""Wait Wait Don't Tell Me! Stats Supplemental Show Information
Retrieval Functions
"""
from functools import lru_cache
from typing import Any, Dict, List, Optional

from mysql.connector import connect
from slugify import slugify
from wwdtm.show.utility import ShowUtility
from wwdtm.location.location import LocationUtility
from wwdtm.validation import valid_int_id


class ShowInfo:
    """This class contains functions that retrieve show supplemental
    show information, including panelist, guest and Bluff the Listener
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

        self.utility = ShowUtility(database_connection=self.database_connection)
        self.loc_util = LocationUtility(database_connection=self.database_connection)
        self.panelists = self._retrieve_panelists()

    def _retrieve_panelists(self) -> Dict[int, Dict[str, str]]:
        """Returns a dictionary of panelist information.

        :return: Dictionary containing panelist ID as the key and
            panelist name and slug string as a dictionary as a value.
        """
        query = """
            SELECT panelistid, panelist, panelistslug
            FROM ww_panelists
            ORDER BY panelistid ASC;
        """
        cursor = self.database_connection.cursor(named_tuple=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        panelists = {}
        for row in results:
            panelists[row.panelistid] = {
                "name": row.panelist,
                "slug": row.panelistslug,
            }

        return panelists

    @lru_cache(typed=True)
    def retrieve_bluff_info_by_id(self, show_id: int) -> List[Dict[str, Any]]:
        """Returns a list of Bluff the Listener information for the
        requested show ID.

        :param show_id: Show ID
        :return: List containing each of the correct and chosen Bluff
            the Listener information.
        """
        if not valid_int_id(show_id):
            return {}

        query = """
            SELECT segment, chosenbluffpnlid AS chosen_id,
            correctbluffpnlid AS correct_id
            FROM ww_showbluffmap
            WHERE showid = %s;
            """
        cursor = self.database_connection.cursor(named_tuple=True)
        cursor.execute(query, (show_id,))
        result = cursor.fetchall()

        if not result:
            return []

        bluffs = []
        for row in result:
            if not row.chosen_id and not row.correct_id:
                bluffs.append(
                    {
                        "segment": row.segment,
                        "chosen_panelist": None,
                        "correct_panelist": None,
                    }
                )
            elif row.chosen_id and not row.correct_id:
                bluffs.append(
                    {
                        "segment": row.segment,
                        "chosen_panelist": {
                            "id": row.chosen_id,
                            "name": self.panelists[row.chosen_id]["name"],
                            "slug": self.panelists[row.chosen_id]["slug"]
                            if self.panelists[row.chosen_id]["slug"]
                            else slugify(self.panelists[row.chosen_id]["name"]),
                        },
                        "correct_panelist": None,
                    }
                )
            elif row.correct_id and not row.chosen_id:
                bluffs.append(
                    {
                        "segment": row.segment,
                        "chosen_panelist": None,
                        "correct_panelist": {
                            "id": row.correct_id,
                            "name": self.panelists[row.correct_id]["name"],
                            "slug": self.panelists[row.correct_id]["slug"]
                            if self.panelists[row.correct_id]["slug"]
                            else slugify(self.panelists[row.correct_id]["name"]),
                        },
                    }
                )
            else:
                bluffs.append(
                    {
                        "segment": row.segment,
                        "chosen_panelist": {
                            "id": row.chosen_id,
                            "name": self.panelists[row.chosen_id]["name"],
                            "slug": self.panelists[row.chosen_id]["slug"]
                            if self.panelists[row.chosen_id]["slug"]
                            else slugify(self.panelists[row.chosen_id]["name"]),
                        },
                        "correct_panelist": {
                            "id": row.correct_id,
                            "name": self.panelists[row.correct_id]["name"],
                            "slug": self.panelists[row.correct_id]["slug"]
                            if self.panelists[row.correct_id]["slug"]
                            else slugify(self.panelists[row.correct_id]["name"]),
                        },
                    }
                )

        return bluffs

    def retrieve_core_info_by_id(self, show_id: int) -> Dict[str, Any]:
        """Returns a dictionary with core information for the requested
        show ID.

        :param show_ids: List of show IDs
        :return: Dictionary containing host, scorekeeper, location,
            description and notes. If show core information could not be
            retrieved, an empty dictionary will be returned.
        """
        if not valid_int_id(show_id):
            return {}

        query = """
            SELECT s.showid AS show_id, s.showdate AS date,
            s.bestof AS best_of, s.repeatshowid AS repeat_show_id,
            l.locationid AS location_id, l.city, l.state,
            l.venue, l.locationslug AS location_slug, h.hostid AS host_id,
            h.host, h.hostslug AS host_slug, hm.guest as host_guest,
            sk.scorekeeperid AS scorekeeper_id, sk.scorekeeper,
            sk.scorekeeperslug AS scorekeeper_slug,
            skm.guest AS scorekeeper_guest,
            skm.description AS scorekeeper_description,
            sd.showdescription AS show_description,
            sn.shownotes AS show_notes
            FROM ww_shows s
            JOIN ww_showlocationmap lm ON lm.showid = s.showid
            JOIN ww_locations l ON l.locationid = lm.locationid
            JOIN ww_showhostmap hm ON hm.showid = s.showid
            JOIN ww_hosts h ON h.hostid = hm.hostid
            JOIN ww_showskmap skm ON skm.showid = s.showid
            JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
            JOIN ww_showdescriptions sd ON sd.showid = s.showid
            JOIN ww_shownotes sn ON sn.showid = s.showid
            WHERE s.showid = %s
            ORDER BY s.showdate ASC;
            """
        cursor = self.database_connection.cursor(named_tuple=True)
        cursor.execute(query, (show_id,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return {}

        location_info = {
            "id": result.location_id,
            "slug": result.location_slug,
            "city": result.city,
            "state": result.state,
            "venue": result.venue,
        }

        if not result.location_slug:
            location_info["slug"] = self.loc_util.slugify_location(
                location_id=result.location_id,
                venue=result.venue,
                city=result.city,
                state=result.state,
            )

        host_info = {
            "id": result.host_id,
            "name": result.host,
            "slug": result.host_slug if result.host_slug else slugify(result.host),
            "guest": bool(result.host_guest),
        }

        scorekeeper_info = {
            "id": result.scorekeeper_id,
            "name": result.scorekeeper,
            "slug": result.scorekeeper_slug
            if result.scorekeeper_slug
            else slugify(result.scorekeeper),
            "guest": bool(result.scorekeeper_guest),
            "description": result.scorekeeper_description
            if result.scorekeeper_description
            else None,
        }

        if result.show_description:
            description = str(result.show_description).strip()
        else:
            description = None

        if result.show_notes:
            notes = str(result.show_notes).strip()
        else:
            notes = None

        show_info = {
            "id": result.show_id,
            "date": result.date.isoformat(),
            "best_of": bool(result.best_of),
            "repeat_show": bool(result.repeat_show_id),
            "original_show_id": None,
            "original_show_date": None,
            "description": description,
            "notes": notes,
            "location": location_info,
            "host": host_info,
            "scorekeeper": scorekeeper_info,
        }

        repeat_show_id = result.repeat_show_id
        if repeat_show_id:
            original_date = self.utility.convert_id_to_date(repeat_show_id)
            show_info["original_show_id"] = repeat_show_id
            show_info["original_show_date"] = original_date
        else:
            show_info.pop("original_show_id", None)
            show_info.pop("original_show_date", None)

        return show_info

    @lru_cache(typed=True)
    def retrieve_guest_info_by_id(self, show_id: int) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing Not My Job
        guest information for the requested show ID.

        :param show_id: Show ID
        :return: Dictionary containing Not My Job guest information. If
            Not My Job information could not be retrieved, an empty list
            will be returned.
        """
        if not valid_int_id(show_id):
            return []

        query = """
            SELECT gm.guestid AS id, g.guest AS name,
            g.guestslug AS slug, gm.guestscore AS score,
            gm.exception AS score_exception
            FROM ww_showguestmap gm
            JOIN ww_guests g on g.guestid = gm.guestid
            JOIN ww_shows s on s.showid = gm.showid
            WHERE gm.showid = %s
            ORDER by gm.showguestmapid ASC;
            """
        cursor = self.database_connection.cursor(named_tuple=True)
        cursor.execute(query, (show_id,))
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        guests = []
        for guest in results:
            guests.append(
                {
                    "id": guest.id,
                    "name": guest.name,
                    "slug": guest.slug if guest.slug else slugify(guest.name),
                    "score": guest.score,
                    "score_exception": bool(guest.score_exception),
                }
            )

        return guests

    @lru_cache(typed=True)
    def retrieve_panelist_info_by_id(
        self, show_id: int, include_decimal_scores: bool = False
    ) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing panelist
        information for the requested show ID.

        :param show_id: Show ID
        :param include_decimal_scores: Flag set to include panelist
            decimal scores, if available
        :return: List of panelists with corresponding scores and
            ranking information. If panelist information could not be
            retrieved, an empty list will be returned.
        """
        if not valid_int_id(show_id):
            return []

        if include_decimal_scores:
            query = """
                SELECT pm.panelistid AS id, p.panelist AS name,
                p.panelistslug AS slug,
                pm.panelistlrndstart AS start,
                pm.panelistlrndstart_decimal AS start_decimal,
                pm.panelistlrndcorrect AS correct,
                pm.panelistlrndcorrect_decimal AS correct_decimal,
                pm.panelistscore AS score,
                pm.panelistscore_decimal AS score_decimal,
                pm.showpnlrank AS pnl_rank
                FROM ww_showpnlmap pm
                JOIN ww_panelists p on p.panelistid = pm.panelistid
                WHERE pm.showid = %s
                ORDER by pm.panelistscore DESC, pm.showpnlmapid ASC;
                """
        else:
            query = """
                SELECT pm.panelistid AS id, p.panelist AS name,
                p.panelistslug AS slug,
                pm.panelistlrndstart AS start,
                pm.panelistlrndcorrect AS correct,
                pm.panelistscore AS score, pm.showpnlrank AS pnl_rank
                FROM ww_showpnlmap pm
                JOIN ww_panelists p on p.panelistid = pm.panelistid
                WHERE pm.showid = %s
                ORDER by pm.panelistscore DESC, pm.showpnlmapid ASC;
                """

        cursor = self.database_connection.cursor(named_tuple=True)
        cursor.execute(query, (show_id,))
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        panelists = []
        for row in results:
            panelists.append(
                {
                    "id": row.id,
                    "name": row.name,
                    "slug": row.slug if row.slug else slugify(row.name),
                    "lightning_round_start": row.start,
                    "lightning_round_start_decimal": row.start_decimal
                    if "start_decimal" in row._fields
                    else None,
                    "lightning_round_correct": row.correct,
                    "lightning_round_correct_decimal": row.correct_decimal
                    if "correct_decimal" in row._fields
                    else None,
                    "score": row.score,
                    "score_decimal": row.score_decimal
                    if "score_decimal" in row._fields
                    else None,
                    "rank": row.pnl_rank if row.pnl_rank else None,
                }
            )

        return panelists
