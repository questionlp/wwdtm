# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2023 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
"""Wait Wait Don't Tell Me! Stats Supplemental Show Information
Retrieval Functions for Multiple Shows
"""
from typing import Any, Dict, List, Optional

from mysql.connector import connect
from slugify import slugify
from wwdtm.show.utility import ShowUtility
from wwdtm.location.location import LocationUtility
from wwdtm.validation import valid_int_id


class ShowInfoMultiple:
    """This class contains functions that retrieve show supplemental
    show information, including panelist, guest and Bluff the Listener
    information for multiple shows from a copy of the Wait Wait Stats
    database

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

    def retrieve_bluff_info_all(self) -> Dict[int, List[Dict[str, Any]]]:
        """Returns a dictionary of Bluff the Listener information for
        all shows.

        :return: Dictionary containing each of the correct and chosen
            Bluff the Listener information.
        """

        query = """
            SELECT blm.showid, blm.segment, blm.chosenbluffpnlid AS chosen_id,
            blm.correctbluffpnlid AS correct_id
            FROM ww_showbluffmap blm
            JOIN ww_shows s on s.showid = blm.showid
            ORDER BY s.showid ASC, blm.segment ASC;
            """
        cursor = self.database_connection.cursor(named_tuple=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        bluff_info = {}
        for row in results:
            if row.showid not in bluff_info:
                bluff_info[row.showid] = []

            if not row.chosen_id and not row.correct_id:
                bluff_info[row.showid].append(
                    {
                        "segment": row.segment,
                        "chosen_panelist": None,
                        "correct_panelist": None,
                    }
                )
            elif row.chosen_id and not row.correct_id:
                bluff_info[row.showid].append(
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
                bluff_info[row.showid].append(
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
                bluff_info[row.showid].append(
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

        return bluff_info

    def retrieve_bluff_info_by_ids(
        self, show_ids: List[int]
    ) -> Dict[int, List[Dict[str, Any]]]:
        """Returns a dictionary containing Bluff the Listener information
        for the requested show IDs.

        :param show_ids: List of show IDs
        :return: Dictionary containing correct and chosen Bluff the
            Listener information.
        """
        for show_id in show_ids:
            if not valid_int_id(show_id):
                return {}

        query = """
            SELECT showid, segment, chosenbluffpnlid AS chosen_id,
            correctbluffpnlid AS correct_id
            FROM ww_showbluffmap
            WHERE showid IN ({ids})
            ORDER BY showid ASC, segment ASC;""".format(ids=", ".join(str(v) for v in show_ids))
        cursor = self.database_connection.cursor(named_tuple=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        bluff_info = {}
        for row in results:
            if row.showid not in bluff_info:
                bluff_info[row.showid] = []

            if not row.chosen_id and not row.correct_id:
                bluff_info[row.showid].append(
                    {
                        "segment": row.segment,
                        "chosen_panelist": None,
                        "correct_panelist": None,
                    }
                )
            elif row.chosen_id and not row.correct_id:
                bluff_info[row.showid].append(
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
                bluff_info[row.showid].append(
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
                bluff_info[row.showid].append(
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

        return bluff_info

    def retrieve_core_info_all(self) -> Dict[int, Dict[str, Any]]:
        """Returns a dictionary with core information for all shows.

        :return: Dictionary containing host, scorekeeper, location,
            description and notes. If show core information could not be
            retrieved, an empty dictionary will be returned.
        """
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
            ORDER BY s.showdate ASC;
            """
        cursor = self.database_connection.cursor(named_tuple=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        shows = {}
        for show in results:
            location_info = {
                "id": show.location_id,
                "slug": show.location_slug,
                "city": show.city,
                "state": show.state,
                "venue": show.venue,
            }

            if not show.location_slug:
                location_info["slug"] = self.loc_util.slugify_location(
                    location_id=show.location_id,
                    venue=show.venue,
                    city=show.city,
                    state=show.state,
                )

            host_info = {
                "id": show.host_id,
                "name": show.host,
                "slug": show.host_slug if show.host_slug else slugify(show.host),
                "guest": bool(show.host_guest),
            }

            scorekeeper_info = {
                "id": show.scorekeeper_id,
                "name": show.scorekeeper,
                "slug": show.scorekeeper_slug
                if show.scorekeeper_slug
                else slugify(show.scorekeeper),
                "guest": bool(show.scorekeeper_guest),
                "description": show.scorekeeper_description
                if show.scorekeeper_description
                else None,
            }

            if show.show_description:
                description = str(show.show_description).strip()
            else:
                description = None

            if show.show_notes:
                notes = str(show.show_notes).strip()
            else:
                notes = None

            show_info = {
                "id": show.show_id,
                "date": show.date.isoformat(),
                "best_of": bool(show.best_of),
                "repeat_show": bool(show.repeat_show_id),
                "original_show_id": None,
                "original_show_date": None,
                "description": description,
                "notes": notes,
                "location": location_info,
                "host": host_info,
                "scorekeeper": scorekeeper_info,
            }

            repeat_show_id = show.repeat_show_id
            if repeat_show_id:
                original_date = self.utility.convert_id_to_date(repeat_show_id)
                show_info["original_show_id"] = repeat_show_id
                show_info["original_show_date"] = original_date
            else:
                show_info.pop("original_show_id", None)
                show_info.pop("original_show_date", None)

            shows[show.show_id] = show_info

        return shows

    def retrieve_core_info_by_ids(
        self, show_ids: List[int]
    ) -> Dict[int, Dict[str, Any]]:
        """Returns a dictionary with core information for the requested
        show IDs.

        :param show_ids: List of show IDs
        :return: Dictionary containing host, scorekeeper, location,
            description and notes. If show core information could not be
            retrieved, an empty dictionary will be returned.
        """
        for show_id in show_ids:
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
            WHERE s.showid IN ({ids})
            ORDER BY s.showdate ASC;""".format(ids=", ".join(str(v) for v in show_ids))
        cursor = self.database_connection.cursor(named_tuple=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        shows = {}
        for show in results:
            location_info = {
                "id": show.location_id,
                "slug": show.location_slug,
                "city": show.city,
                "state": show.state,
                "venue": show.venue,
            }

            if not show.location_slug:
                location_info["slug"] = self.loc_util.slugify_location(
                    location_id=show.location_id,
                    venue=show.venue,
                    city=show.city,
                    state=show.state,
                )

            host_info = {
                "id": show.host_id,
                "name": show.host,
                "slug": show.host_slug if show.host_slug else slugify(show.host),
                "guest": bool(show.host_guest),
            }

            scorekeeper_info = {
                "id": show.scorekeeper_id,
                "name": show.scorekeeper,
                "slug": show.scorekeeper_slug
                if show.scorekeeper_slug
                else slugify(show.scorekeeper),
                "guest": bool(show.scorekeeper_guest),
                "description": show.scorekeeper_description
                if show.scorekeeper_description
                else None,
            }

            if show.show_description:
                description = str(show.show_description).strip()
            else:
                description = None

            if show.show_notes:
                notes = str(show.show_notes).strip()
            else:
                notes = None

            show_info = {
                "id": show.show_id,
                "date": show.date.isoformat(),
                "best_of": bool(show.best_of),
                "repeat_show": bool(show.repeat_show_id),
                "original_show_id": None,
                "original_show_date": None,
                "description": description,
                "notes": notes,
                "location": location_info,
                "host": host_info,
                "scorekeeper": scorekeeper_info,
            }

            repeat_show_id = show.repeat_show_id
            if repeat_show_id:
                original_date = self.utility.convert_id_to_date(repeat_show_id)
                show_info["original_show_id"] = repeat_show_id
                show_info["original_show_date"] = original_date
            else:
                show_info.pop("original_show_id", None)
                show_info.pop("original_show_date", None)

            shows[show.show_id] = show_info

        return shows

    def retrieve_guest_info_all(self) -> Dict[int, List[Dict[str, Any]]]:
        """Returns a list of dictionary objects containing Not My Job
        guest information for all shows.

        :return: Dictionary containing Not My Job guest information. If
            Not My Job information could not be retrieved, an empty list
            will be returned.
        """
        query = """
            SELECT s.showid AS show_id, gm.guestid AS guest_id,
            g.guest AS name, g.guestslug AS slug,
            gm.guestscore AS score, gm.exception AS score_exception
            FROM ww_showguestmap gm
            JOIN ww_guests g ON g.guestid = gm.guestid
            JOIN ww_shows s ON s.showid = gm.showid
            ORDER BY s.showdate ASC, gm.showguestmapid ASC;
            """
        cursor = self.database_connection.cursor(named_tuple=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        shows = {}
        for guest in results:
            if guest.show_id not in shows:
                shows[guest.show_id] = []

            shows[guest.show_id].append(
                {
                    "id": guest.guest_id,
                    "name": guest.name,
                    "slug": guest.slug if guest.slug else slugify(guest.name),
                    "score": guest.score,
                    "score_exception": bool(guest.score_exception),
                }
            )

        return shows

    def retrieve_guest_info_by_ids(
        self, show_ids: List[int]
    ) -> Dict[int, List[Dict[str, Any]]]:
        """Returns a list of dictionary objects containing Not My Job
        guest information for the requested show IDs.

        :param show_ids: List of show IDs
        :return: Dictionary containing Not My Job guest information. If
            Not My Job information could not be retrieved, an empty list
            will be returned.
        """
        for show_id in show_ids:
            if not valid_int_id(show_id):
                return {}

        query = """
            SELECT s.showid AS show_id, gm.guestid AS guest_id,
            g.guest AS name, g.guestslug AS slug,
            gm.guestscore AS score, gm.exception AS score_exception
            FROM ww_showguestmap gm
            JOIN ww_guests g ON g.guestid = gm.guestid
            JOIN ww_shows s ON s.showid = gm.showid
            WHERE gm.showid IN ({ids})
            ORDER BY s.showdate ASC,
            gm.showguestmapid ASC;""".format(ids=", ".join(str(v) for v in show_ids))
        cursor = self.database_connection.cursor(named_tuple=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        shows = {}
        for guest in results:
            if guest.show_id not in shows:
                shows[guest.show_id] = []

            shows[guest.show_id].append(
                {
                    "id": guest.guest_id,
                    "name": guest.name,
                    "slug": guest.slug if guest.slug else slugify(guest.name),
                    "score": guest.score,
                    "score_exception": bool(guest.score_exception),
                }
            )

        return shows

    def retrieve_panelist_info_all(
        self, include_decimal_scores: bool = False
    ) -> Dict[int, List[Dict[str, Any]]]:
        """Returns a list of dictionary objects containing panelist
        information for all shows.

        :param include_decimal_scores: Flag set to include panelist
            decimal scores, if available
        :return: List of panelists with corresponding scores and
            ranking information. If panelist information could not be
            retrieved, an empty list will be returned.
        """
        if include_decimal_scores:
            query = """
                SELECT s.showid AS show_id, pm.panelistid AS panelist_id,
                p.panelist AS name, p.panelistslug AS slug,
                pm.panelistlrndstart AS start,
                pm.panelistlrndstart AS start_decimal,
                pm.panelistlrndcorrect AS correct,
                pm.panelistlrndcorrect AS correct_decimal,
                pm.panelistscore AS score,
                pm.panelistscore_decimal AS score_decimal,
                pm.showpnlrank AS pnl_rank
                FROM ww_showpnlmap pm
                JOIN ww_panelists p ON p.panelistid = pm.panelistid
                JOIN ww_shows s ON s.showid = pm.showid
                ORDER by s.showdate ASC, pm.panelistscore DESC,
                pm.showpnlmapid ASC;
                """
        else:
            query = """
                SELECT s.showid AS show_id, pm.panelistid AS panelist_id,
                p.panelist AS name, p.panelistslug AS slug,
                pm.panelistlrndstart AS start,
                pm.panelistlrndcorrect AS correct,
                pm.panelistscore AS score,
                pm.showpnlrank AS pnl_rank
                FROM ww_showpnlmap pm
                JOIN ww_panelists p ON p.panelistid = pm.panelistid
                JOIN ww_shows s ON s.showid = pm.showid
                ORDER by s.showdate ASC, pm.panelistscore DESC,
                pm.showpnlmapid ASC;
                """
        cursor = self.database_connection.cursor(named_tuple=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        panelists = {}
        for panelist in results:
            if panelist.show_id not in panelists:
                panelists[panelist.show_id] = []

            panelists[panelist.show_id].append(
                {
                    "id": panelist.panelist_id,
                    "name": panelist.name,
                    "slug": panelist.slug if panelist.slug else slugify(panelist.name),
                    "lightning_round_start": panelist.start,
                    "lightning_round_start_decimal": panelist.start_decimal
                    if "start_decimal" in panelist._fields
                    else None,
                    "lightning_round_correct": panelist.correct,
                    "lightning_round_correct_decimal": panelist.correct_decimal
                    if "correct_decimal" in panelist._fields
                    else None,
                    "score": panelist.score,
                    "score_decimal": panelist.score_decimal
                    if "score_decimal" in panelist._fields
                    else None,
                    "rank": panelist.pnl_rank if panelist.pnl_rank else None,
                }
            )

        return panelists

    def retrieve_panelist_info_by_ids(
        self, show_ids: List[int], include_decimal_scores: bool = False
    ) -> Dict[int, List[Dict[str, Any]]]:
        """Returns a list of dictionary objects containing panelist
        information for the requested show IDs.

        :param show_ids: List of show IDs
        :param include_decimal_scores: Flag set to include panelist
            decimal scores, if available
        :return: List of panelists with corresponding scores and
            ranking information. If panelist information could not be
            retrieved, an empty list will be returned.
        """
        for show_id in show_ids:
            if not valid_int_id(show_id):
                return {}

        if include_decimal_scores:
            query = """
                SELECT s.showid AS show_id, pm.panelistid AS panelist_id,
                p.panelist AS name, p.panelistslug AS slug,
                pm.panelistlrndstart AS start,
                pm.panelistlrndstart AS start_decimal,
                pm.panelistlrndcorrect AS correct,
                pm.panelistlrndcorrect AS correct_decimal,
                pm.panelistscore AS score,
                pm.panelistscore_decimal AS score_decimal,
                pm.showpnlrank AS pnl_rank
                FROM ww_showpnlmap pm
                JOIN ww_panelists p ON p.panelistid = pm.panelistid
                JOIN ww_shows s ON s.showid = pm.showid
                WHERE pm.showid IN ({ids})
                ORDER by s.showdate ASC, pm.panelistscore DESC,
                pm.showpnlmapid ASC;""".format(ids=", ".join(str(v) for v in show_ids))
        else:
            query = """
                SELECT s.showid AS show_id, pm.panelistid AS panelist_id,
                p.panelist AS name, p.panelistslug AS slug,
                pm.panelistlrndstart AS start,
                pm.panelistlrndcorrect AS correct,
                pm.panelistscore AS score, pm.showpnlrank AS pnl_rank
                FROM ww_showpnlmap pm
                JOIN ww_panelists p ON p.panelistid = pm.panelistid
                JOIN ww_shows s ON s.showid = pm.showid
                WHERE pm.showid IN ({ids})
                ORDER by s.showdate ASC, pm.panelistscore DESC,
                pm.showpnlmapid ASC;""".format(ids=", ".join(str(v) for v in show_ids))

        cursor = self.database_connection.cursor(named_tuple=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        panelists = {}
        for panelist in results:
            if panelist.show_id not in panelists:
                panelists[panelist.show_id] = []

            panelists[panelist.show_id].append(
                {
                    "id": panelist.panelist_id,
                    "name": panelist.name,
                    "slug": panelist.slug if panelist.slug else slugify(panelist.name),
                    "lightning_round_start": panelist.start if panelist.start else None,
                    "lightning_round_start_decimal": panelist.start_decimal
                    if "start_decimal" in panelist._fields
                    else None,
                    "lightning_round_correct": panelist.correct
                    if panelist.correct
                    else None,
                    "lightning_round_correct_decimal": panelist.correct_decimal
                    if "correct_decimal" in panelist._fields
                    else None,
                    "score": panelist.score,
                    "score_decimal": panelist.score_decimal
                    if "score_decimal" in panelist._fields
                    else None,
                    "rank": panelist.pnl_rank if panelist.pnl_rank else None,
                }
            )

        return panelists
