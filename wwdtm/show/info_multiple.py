# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
# pylint: disable=C0209
"""Wait Wait Stats Show Detailed Information Retrieval Functions for Multiple Shows."""

from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from slugify import slugify

from wwdtm.location.location import LocationUtility
from wwdtm.show.utility import ShowUtility
from wwdtm.validation import valid_int_id


class ShowInfoMultiple:
    """Multiple show information retrieval class.

    Contains methods used to retrieve panelist, guest and Bluff the
    Listener information for multiple shows.

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

        self.utility = ShowUtility(database_connection=self.database_connection)
        self.loc_util = LocationUtility(database_connection=self.database_connection)
        self.panelists = self._retrieve_panelists()

    def _retrieve_panelists(self) -> dict[int, dict[str, str]]:
        """Retrieves panelist basic information.

        :return: A dictionary with panelist ID as the key and a
            dictionary with name and slug string as the value
        """
        query = """
            SELECT panelistid, panelist, panelistslug
            FROM ww_panelists
            ORDER BY panelistid ASC;
        """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        panelists = {}
        for row in results:
            panelists[row["panelistid"]] = {
                "name": row["panelist"],
                "slug": row["panelistslug"],
            }

        return panelists

    def retrieve_bluff_info_all(self) -> dict[int, list[dict[str, Any]]]:
        """Retrieves Bluff the Listener information for all shows.

        :return: A dictionary containing Bluff the Listener segment ID
            and information about the chosen Bluff panelist and correct
            Bluff panelist.
        """
        query = """
            SELECT blm.showid, blm.segment, blm.chosenbluffpnlid AS chosen_id,
            blm.correctbluffpnlid AS correct_id
            FROM ww_showbluffmap blm
            JOIN ww_shows s on s.showid = blm.showid
            ORDER BY s.showid ASC, blm.segment ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        bluff_info = {}
        for row in results:
            if row["showid"] not in bluff_info:
                bluff_info[row["showid"]] = []

            if not row["chosen_id"] and not row["correct_id"]:
                bluff_info[row["showid"]].append(
                    {
                        "segment": row["segment"],
                        "chosen_panelist": None,
                        "correct_panelist": None,
                    }
                )
            elif row["chosen_id"] and not row["correct_id"]:
                bluff_info[row["showid"]].append(
                    {
                        "segment": row["segment"],
                        "chosen_panelist": {
                            "id": row["chosen_id"],
                            "name": self.panelists[row["chosen_id"]]["name"],
                            "slug": (
                                self.panelists[row["chosen_id"]]["slug"]
                                if self.panelists[row["chosen_id"]]["slug"]
                                else slugify(self.panelists[row["chosen_id"]]["name"])
                            ),
                        },
                        "correct_panelist": None,
                    }
                )
            elif row["correct_id"] and not row["chosen_id"]:
                bluff_info[row["showid"]].append(
                    {
                        "segment": row["segment"],
                        "chosen_panelist": None,
                        "correct_panelist": {
                            "id": row["correct_id"],
                            "name": self.panelists[row["correct_id"]]["name"],
                            "slug": (
                                self.panelists[row["correct_id"]]["slug"]
                                if self.panelists[row["correct_id"]]["slug"]
                                else slugify(self.panelists[row["correct_id"]]["name"])
                            ),
                        },
                    }
                )
            else:
                bluff_info[row["showid"]].append(
                    {
                        "segment": row["segment"],
                        "chosen_panelist": {
                            "id": row["chosen_id"],
                            "name": self.panelists[row["chosen_id"]]["name"],
                            "slug": (
                                self.panelists[row["chosen_id"]]["slug"]
                                if self.panelists[row["chosen_id"]]["slug"]
                                else slugify(self.panelists[row["chosen_id"]]["name"])
                            ),
                        },
                        "correct_panelist": {
                            "id": row["correct_id"],
                            "name": self.panelists[row["correct_id"]]["name"],
                            "slug": (
                                self.panelists[row["correct_id"]]["slug"]
                                if self.panelists[row["correct_id"]]["slug"]
                                else slugify(self.panelists[row["correct_id"]]["name"])
                            ),
                        },
                    }
                )

        return bluff_info

    def retrieve_bluff_info_by_ids(
        self, show_ids: list[int]
    ) -> dict[int, list[dict[str, Any]]]:
        """Retrieves Bluff the Listener information for a list of shows.

        :param show_id: A list of show IDs
        :return: A dictionary containing Bluff the Listener segment ID
            and information about the chosen Bluff panelist and correct
            Bluff panelist.
        """
        for show_id in show_ids:
            if not valid_int_id(show_id):
                return {}

        query = """
            SELECT showid, segment, chosenbluffpnlid AS chosen_id,
            correctbluffpnlid AS correct_id
            FROM ww_showbluffmap
            WHERE showid IN ({ids})
            ORDER BY showid ASC, segment ASC;""".format(
            ids=", ".join(str(v) for v in show_ids)
        )
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        bluff_info = {}
        for row in results:
            if row["showid"] not in bluff_info:
                bluff_info[row["showid"]] = []

            if not row["chosen_id"] and not row["correct_id"]:
                bluff_info[row["showid"]].append(
                    {
                        "segment": row["segment"],
                        "chosen_panelist": None,
                        "correct_panelist": None,
                    }
                )
            elif row["chosen_id"] and not row["correct_id"]:
                bluff_info[row["showid"]].append(
                    {
                        "segment": row["segment"],
                        "chosen_panelist": {
                            "id": row["chosen_id"],
                            "name": self.panelists[row["chosen_id"]]["name"],
                            "slug": (
                                self.panelists[row["chosen_id"]]["slug"]
                                if self.panelists[row["chosen_id"]]["slug"]
                                else slugify(self.panelists[row["chosen_id"]]["name"])
                            ),
                        },
                        "correct_panelist": None,
                    }
                )
            elif row["correct_id"] and not row["chosen_id"]:
                bluff_info[row["showid"]].append(
                    {
                        "segment": row["segment"],
                        "chosen_panelist": None,
                        "correct_panelist": {
                            "id": row["correct_id"],
                            "name": self.panelists[row["correct_id"]]["name"],
                            "slug": (
                                self.panelists[row["correct_id"]]["slug"]
                                if self.panelists[row["correct_id"]]["slug"]
                                else slugify(self.panelists[row["correct_id"]]["name"])
                            ),
                        },
                    }
                )
            else:
                bluff_info[row["showid"]].append(
                    {
                        "segment": row["segment"],
                        "chosen_panelist": {
                            "id": row["chosen_id"],
                            "name": self.panelists[row["chosen_id"]]["name"],
                            "slug": (
                                self.panelists[row["chosen_id"]]["slug"]
                                if self.panelists[row["chosen_id"]]["slug"]
                                else slugify(self.panelists[row["chosen_id"]]["name"])
                            ),
                        },
                        "correct_panelist": {
                            "id": row["correct_id"],
                            "name": self.panelists[row["correct_id"]]["name"],
                            "slug": (
                                self.panelists[row["correct_id"]]["slug"]
                                if self.panelists[row["correct_id"]]["slug"]
                                else slugify(self.panelists[row["correct_id"]]["name"])
                            ),
                        },
                    }
                )

        return bluff_info

    def retrieve_core_info_all(self) -> dict[int, dict[str, Any]]:
        """Retrieves core information for all shows.

        :return: A dictionary containing host, scorekeeper, location,
            description and notes
        """
        query = """
            SELECT s.showid AS show_id, s.showdate AS date,
            s.bestof AS best_of, s.repeatshowid AS repeat_show_id,
            s.showurl AS show_url,
            l.locationid AS location_id, l.city, l.state,
            pa.name AS state_name, l.venue, l.latitude, l.longitude,
            l.locationslug AS location_slug,
            h.hostid AS host_id, h.host, h.hostslug AS host_slug,
            hm.guest as host_guest,
            sk.scorekeeperid AS scorekeeper_id, sk.scorekeeper,
            sk.scorekeeperslug AS scorekeeper_slug,
            skm.guest AS scorekeeper_guest,
            skm.description AS scorekeeper_description,
            sd.showdescription AS show_description,
            sn.shownotes AS show_notes
            FROM ww_shows s
            JOIN ww_showlocationmap lm ON lm.showid = s.showid
            JOIN ww_locations l ON l.locationid = lm.locationid
            LEFT JOIN ww_postal_abbreviations pa ON pa.postal_abbreviation = l.state
            JOIN ww_showhostmap hm ON hm.showid = s.showid
            JOIN ww_hosts h ON h.hostid = hm.hostid
            JOIN ww_showskmap skm ON skm.showid = s.showid
            JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
            JOIN ww_showdescriptions sd ON sd.showid = s.showid
            JOIN ww_shownotes sn ON sn.showid = s.showid
            ORDER BY s.showdate ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        shows = {}
        for show in results:
            if not show["latitude"] and not show["longitude"]:
                coordinates = None
            else:
                coordinates = {
                    "latitude": show["latitude"] if show["latitude"] else None,
                    "longitude": show["longitude"] if show["longitude"] else None,
                }

            location_info = {
                "id": show["location_id"],
                "slug": show["location_slug"],
                "city": show["city"],
                "state": show["state"],
                "state_name": show["state_name"],
                "venue": show["venue"],
                "coordinates": coordinates,
            }

            if not show["location_slug"]:
                location_info["slug"] = self.loc_util.slugify_location(
                    location_id=show["location_id"],
                    venue=show["venue"],
                    city=show["city"],
                    state=show["state"],
                )

            host_info = {
                "id": show["host_id"],
                "name": show["host"],
                "slug": (
                    show["host_slug"] if show["host_slug"] else slugify(show["host"])
                ),
                "guest": bool(show["host_guest"]),
            }

            scorekeeper_info = {
                "id": show["scorekeeper_id"],
                "name": show["scorekeeper"],
                "slug": (
                    show["scorekeeper_slug"]
                    if show["scorekeeper_slug"]
                    else slugify(show["scorekeeper"])
                ),
                "guest": bool(show["scorekeeper_guest"]),
                "description": (
                    show["scorekeeper_description"]
                    if show["scorekeeper_description"]
                    else None
                ),
            }

            if show["show_description"]:
                description = str(show["show_description"]).strip()
            else:
                description = None

            notes = str(show["show_notes"]).strip() if show["show_notes"] else None

            show_info = {
                "id": show["show_id"],
                "date": show["date"].isoformat(),
                "best_of": bool(show["best_of"]),
                "repeat_show": bool(show["repeat_show_id"]),
                "original_show_id": None,
                "original_show_date": None,
                "show_url": show["show_url"],
                "description": description,
                "notes": notes,
                "location": location_info,
                "host": host_info,
                "scorekeeper": scorekeeper_info,
            }

            repeat_show_id = show["repeat_show_id"]
            if repeat_show_id:
                original_date = self.utility.convert_id_to_date(repeat_show_id)
                show_info["original_show_id"] = repeat_show_id
                show_info["original_show_date"] = original_date
            else:
                show_info.pop("original_show_id", None)
                show_info.pop("original_show_date", None)

            shows[show["show_id"]] = show_info

        return shows

    def retrieve_core_info_by_ids(
        self, show_ids: list[int]
    ) -> dict[int, dict[str, Any]]:
        """Retrieves core information for a list of shows.

        :param show_ids: A list of show IDs
        :return: A dictionary containing host, scorekeeper, location,
            description and notes
        """
        for show_id in show_ids:
            if not valid_int_id(show_id):
                return {}

        query = """
            SELECT s.showid AS show_id, s.showdate AS date,
            s.bestof AS best_of, s.repeatshowid AS repeat_show_id,
            s.showurl AS show_url,
            l.locationid AS location_id, l.city, l.state,
            pa.name AS state_name, l.venue, l.latitude, l.longitude,
            l.locationslug AS location_slug,
            h.hostid AS host_id, h.host, h.hostslug AS host_slug,
            hm.guest as host_guest,
            sk.scorekeeperid AS scorekeeper_id, sk.scorekeeper,
            sk.scorekeeperslug AS scorekeeper_slug,
            skm.guest AS scorekeeper_guest,
            skm.description AS scorekeeper_description,
            sd.showdescription AS show_description,
            sn.shownotes AS show_notes
            FROM ww_shows s
            JOIN ww_showlocationmap lm ON lm.showid = s.showid
            JOIN ww_locations l ON l.locationid = lm.locationid
            LEFT JOIN ww_postal_abbreviations pa ON pa.postal_abbreviation = l.state
            JOIN ww_showhostmap hm ON hm.showid = s.showid
            JOIN ww_hosts h ON h.hostid = hm.hostid
            JOIN ww_showskmap skm ON skm.showid = s.showid
            JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
            JOIN ww_showdescriptions sd ON sd.showid = s.showid
            JOIN ww_shownotes sn ON sn.showid = s.showid
            WHERE s.showid IN ({ids})
            ORDER BY s.showdate ASC;""".format(ids=", ".join(str(v) for v in show_ids))
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        shows = {}
        for show in results:
            if not show["latitude"] and not show["longitude"]:
                coordinates = None
            else:
                coordinates = {
                    "latitude": show["latitude"] if show["latitude"] else None,
                    "longitude": show["longitude"] if show["longitude"] else None,
                }

            location_info = {
                "id": show["location_id"],
                "slug": show["location_slug"],
                "city": show["city"],
                "state": show["state"],
                "state_name": show["state_name"],
                "venue": show["venue"],
                "coordinates": coordinates,
            }

            if not show["location_slug"]:
                location_info["slug"] = self.loc_util.slugify_location(
                    location_id=show["location_id"],
                    venue=show["venue"],
                    city=show["city"],
                    state=show["state"],
                )

            host_info = {
                "id": show["host_id"],
                "name": show["host"],
                "slug": (
                    show["host_slug"] if show["host_slug"] else slugify(show["host"])
                ),
                "guest": bool(show["host_guest"]),
            }

            scorekeeper_info = {
                "id": show["scorekeeper_id"],
                "name": show["scorekeeper"],
                "slug": (
                    show["scorekeeper_slug"]
                    if show["scorekeeper_slug"]
                    else slugify(show["scorekeeper"])
                ),
                "guest": bool(show["scorekeeper_guest"]),
                "description": (
                    show["scorekeeper_description"]
                    if show["scorekeeper_description"]
                    else None
                ),
            }

            if show["show_description"]:
                description = str(show["show_description"]).strip()
            else:
                description = None

            notes = str(show["show_notes"]).strip() if show["show_notes"] else None

            show_info = {
                "id": show["show_id"],
                "date": show["date"].isoformat(),
                "best_of": bool(show["best_of"]),
                "repeat_show": bool(show["repeat_show_id"]),
                "original_show_id": None,
                "original_show_date": None,
                "show_url": show["show_url"],
                "description": description,
                "notes": notes,
                "location": location_info,
                "host": host_info,
                "scorekeeper": scorekeeper_info,
            }

            repeat_show_id = show["repeat_show_id"]
            if repeat_show_id:
                original_date = self.utility.convert_id_to_date(repeat_show_id)
                show_info["original_show_id"] = repeat_show_id
                show_info["original_show_date"] = original_date
            else:
                show_info.pop("original_show_id", None)
                show_info.pop("original_show_date", None)

            shows[show["show_id"]] = show_info

        return shows

    def retrieve_guest_info_all(self) -> dict[int, list[dict[str, Any]]]:
        """Retrieves Not My Job guest information for all shows.

        :return: A dictionary containing Not My Job guest information,
            including score and scoring exception for each guest
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
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        shows = {}
        for guest in results:
            if guest["show_id"] not in shows:
                shows[guest["show_id"]] = []

            shows[guest["show_id"]].append(
                {
                    "id": guest["guest_id"],
                    "name": guest["name"],
                    "slug": guest["slug"] if guest["slug"] else slugify(guest["name"]),
                    "score": guest["score"],
                    "score_exception": bool(guest["score_exception"]),
                }
            )

        return shows

    def retrieve_guest_info_by_ids(
        self, show_ids: list[int]
    ) -> dict[int, list[dict[str, Any]]]:
        """Retrieves Not My Job guest information for all shows.

        :param show_ids: A list of show IDs
        :return: A dictionary containing Not My Job guest information,
            including score and scoring exception for each guest.
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
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        shows = {}
        for guest in results:
            if guest["show_id"] not in shows:
                shows[guest["show_id"]] = []

            shows[guest["show_id"]].append(
                {
                    "id": guest["guest_id"],
                    "name": guest["name"],
                    "slug": guest["slug"] if guest["slug"] else slugify(guest["name"]),
                    "score": guest["score"],
                    "score_exception": bool(guest["score_exception"]),
                }
            )

        return shows

    def retrieve_panelist_info_all(
        self, include_decimal_scores: bool = False
    ) -> dict[int, list[dict[str, Any]]]:
        """Retrieves panelist information for all shows.

        :param use_decimal_scores: A boolean to determine if decimal
            scores should be used and returned instead of integer scores
        :return: A dictionary containing panelist information, scores
            and rankings
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
                ORDER by s.showdate ASC, pm.panelistscore_decimal DESC,
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
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        panelists = {}
        for panelist in results:
            if panelist["show_id"] not in panelists:
                panelists[panelist["show_id"]] = []

            panelists[panelist["show_id"]].append(
                {
                    "id": panelist["panelist_id"],
                    "name": panelist["name"],
                    "slug": (
                        panelist["slug"]
                        if panelist["slug"]
                        else slugify(panelist["name"])
                    ),
                    "lightning_round_start": panelist["start"],
                    "lightning_round_start_decimal": panelist.get(
                        "start_decimal", None
                    ),
                    "lightning_round_correct": panelist["correct"],
                    "lightning_round_correct_decimal": panelist.get(
                        "correct_decimal", None
                    ),
                    "score": panelist["score"],
                    "score_decimal": panelist.get("score_decimal", None),
                    "rank": panelist["pnl_rank"] if panelist["pnl_rank"] else None,
                }
            )

        return panelists

    def retrieve_panelist_info_by_ids(
        self, show_ids: list[int], include_decimal_scores: bool = False
    ) -> dict[int, list[dict[str, Any]]]:
        """Retrieves panelist information for a list of shows.

        :param show_ids: A list of show IDs
        :param use_decimal_scores: A boolean to determine if decimal
            scores should be used and returned instead of integer scores
        :return: A dictionary containing panelist information, scores
            and rankings
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
                ORDER by s.showdate ASC, pm.panelistscore_decimal DESC,
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

        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return {}

        panelists = {}
        for panelist in results:
            if panelist["show_id"] not in panelists:
                panelists[panelist["show_id"]] = []

            panelists[panelist["show_id"]].append(
                {
                    "id": panelist["panelist_id"],
                    "name": panelist["name"],
                    "slug": (
                        panelist["slug"]
                        if panelist["slug"]
                        else slugify(panelist["name"])
                    ),
                    "lightning_round_start": (
                        panelist["start"] if panelist["start"] else None
                    ),
                    "lightning_round_start_decimal": panelist.get(
                        "start_decimal", None
                    ),
                    "lightning_round_correct": (
                        panelist["correct"] if panelist["correct"] else None
                    ),
                    "lightning_round_correct_decimal": panelist.get(
                        "correct_decimal", None
                    ),
                    "score": panelist["score"],
                    "score_decimal": panelist.get("score_decimal", None),
                    "rank": panelist["pnl_rank"] if panelist["pnl_rank"] else None,
                }
            )

        return panelists
