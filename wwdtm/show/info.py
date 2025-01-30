# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Show Detailed Information Retrieval Functions."""

from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from slugify import slugify

from wwdtm.location.location import LocationUtility
from wwdtm.show.utility import ShowUtility
from wwdtm.validation import valid_int_id


class ShowInfo:
    """Show information retrieval class.

    Contains methods used to retrieve panelist, guest and Bluff the
    Listener information.

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
        """Returns a dictionary of panelist information.

        :return: Dictionary containing panelist ID as the key and
            panelist name and slug string as a dictionary as a value.
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

    def retrieve_bluff_info_by_id(self, show_id: int) -> list[dict[str, Any]]:
        """Retrieves Bluff the Listener information.

        :param show_id: Show ID
        :return: A dictionary containing Bluff the Listener segment ID
            and information about the chosen Bluff panelist and correct
            Bluff panelist.
        """
        if not valid_int_id(show_id):
            return {}

        query = """
            SELECT segment, chosenbluffpnlid AS chosen_id,
            correctbluffpnlid AS correct_id
            FROM ww_showbluffmap
            WHERE showid = %s
            ORDER BY segment ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (show_id,))
        result = cursor.fetchall()

        if not result:
            return []

        bluffs = []
        for row in result:
            if not row["chosen_id"] and not row["correct_id"]:
                bluffs.append(
                    {
                        "segment": row["segment"],
                        "chosen_panelist": None,
                        "correct_panelist": None,
                    }
                )
            elif row["chosen_id"] and not row["correct_id"]:
                bluffs.append(
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
                bluffs.append(
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
                bluffs.append(
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

        return bluffs

    def retrieve_core_info_by_id(self, show_id: int) -> dict[str, Any]:
        """Retrieves core information.

        :param show_id: Show ID
        :return: A dictionary containing host, scorekeeper, location,
            description and notes
        """
        if not valid_int_id(show_id):
            return {}

        query = """
            SELECT s.showid AS show_id, s.showdate AS date,
            s.bestof AS best_of, s.repeatshowid AS repeat_show_id,
            s.showurl AS show_url,
            l.locationid AS location_id, l.city, l.state,
            pa.name AS state_name, l.latitude, l.longitude, l.venue,
            l.locationslug AS location_slug,
            h.hostid AS host_id, h.host, h.hostslug AS host_slug,
            hm.guest as host_guest, sk.scorekeeperid AS scorekeeper_id,
            sk.scorekeeper, sk.scorekeeperslug AS scorekeeper_slug,
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
            WHERE s.showid = %s
            ORDER BY s.showdate ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (show_id,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return {}

        if not result["latitude"] and not result["longitude"]:
            coordinates = None
        else:
            coordinates = {
                "latitude": result["latitude"] if result["latitude"] else None,
                "longitude": result["longitude"] if result["longitude"] else None,
            }

        location_info = {
            "id": result["location_id"],
            "slug": result["location_slug"],
            "city": result["city"],
            "state": result["state"],
            "state_name": result["state_name"],
            "venue": result["venue"],
            "coordinates": coordinates if coordinates else None,
        }

        if not result["location_slug"]:
            location_info["slug"] = self.loc_util.slugify_location(
                location_id=result["location_id"],
                venue=result["venue"],
                city=result["city"],
                state=result["state"],
            )

        host_info = {
            "id": result["host_id"],
            "name": result["host"],
            "slug": (
                result["host_slug"] if result["host_slug"] else slugify(result["host"])
            ),
            "guest": bool(result["host_guest"]),
        }

        scorekeeper_info = {
            "id": result["scorekeeper_id"],
            "name": result["scorekeeper"],
            "slug": (
                result["scorekeeper_slug"]
                if result["scorekeeper_slug"]
                else slugify(result["scorekeeper"])
            ),
            "guest": bool(result["scorekeeper_guest"]),
            "description": (
                result["scorekeeper_description"]
                if result["scorekeeper_description"]
                else None
            ),
        }

        if result["show_description"]:
            description = str(result["show_description"]).strip()
        else:
            description = None

        notes = str(result["show_notes"]).strip() if result["show_notes"] else None

        show_info = {
            "id": result["show_id"],
            "date": result["date"].isoformat(),
            "best_of": bool(result["best_of"]),
            "repeat_show": bool(result["repeat_show_id"]),
            "original_show_id": None,
            "original_show_date": None,
            "show_url": result["show_url"],
            "description": description,
            "notes": notes,
            "location": location_info,
            "host": host_info,
            "scorekeeper": scorekeeper_info,
        }

        repeat_show_id = result["repeat_show_id"]
        if repeat_show_id:
            original_date = self.utility.convert_id_to_date(repeat_show_id)
            show_info["original_show_id"] = repeat_show_id
            show_info["original_show_date"] = original_date
        else:
            show_info.pop("original_show_id", None)
            show_info.pop("original_show_date", None)

        return show_info

    def retrieve_guest_info_by_id(self, show_id: int) -> list[dict[str, Any]]:
        """Retrieves Not My Job guest information.

        :param show_id: Show ID
        :return: A dictionary containing Not My Job guest information,
            including score and scoring exception for each guest
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
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (show_id,))
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        guests = []
        for guest in results:
            guests.append(
                {
                    "id": guest["id"],
                    "name": guest["name"],
                    "slug": guest["slug"] if guest["slug"] else slugify(guest["name"]),
                    "score": guest["score"],
                    "score_exception": bool(guest["score_exception"]),
                }
            )

        return guests

    def retrieve_panelist_info_by_id(
        self, show_id: int, include_decimal_scores: bool = False
    ) -> list[dict[str, Any]]:
        """Retrieves panelist information.

        :param show_id: Show ID
        :param use_decimal_scores: A boolean to determine if decimal
            scores should be used and returned instead of integer scores
        :return: A dictionary containing panelist information, scores
            and rankings
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
                ORDER by pm.panelistscore_decimal DESC,
                pm.showpnlmapid ASC;
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

        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (show_id,))
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        panelists = []
        for row in results:
            panelists.append(
                {
                    "id": row["id"],
                    "name": row["name"],
                    "slug": row["slug"] if row["slug"] else slugify(row["name"]),
                    "lightning_round_start": row["start"],
                    "lightning_round_start_decimal": row.get("start_decimal", None),
                    "lightning_round_correct": row["correct"],
                    "lightning_round_correct_decimal": row.get("correct_decimal", None),
                    "score": row["score"],
                    "score_decimal": row.get("score_decimal", None),
                    "rank": row["pnl_rank"] if row["pnl_rank"] else None,
                }
            )

        return panelists
