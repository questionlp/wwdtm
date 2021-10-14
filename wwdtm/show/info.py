# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is relased under the terms of the Apache License 2.0
"""Wait Wait Don't Tell Me! Stats Supplemental Show Information
Retrieval Functions
"""
from functools import lru_cache
from typing import Any, Dict, List, Optional

from mysql.connector import connect
from mysql.connector.errors import DatabaseError, ProgrammingError
from slugify import slugify
from wwdtm.show.utility import ShowUtility
from wwdtm.location.location import LocationUtility

class ShowInfo:
    """This class contains functions that retrieve show supplemental
    show information, including panelist, guest and Bluff the Listener
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

        self.utility = ShowUtility(database_connection=self.database_connection)
        self.loc_util = LocationUtility(database_connection=self.database_connection)

    @lru_cache(maxsize=256, typed=True)
    def retrieve_bluff_info_by_id(self, id: int) -> Dict[str, Any]:
        """Returns a dictionary containing Bluff the Listener information
        for the requested show ID.

        :param id: Show ID
        :type id: int
        :return: Dictionary containing correct and chosen Bluff the
            Listener information
        :rtype: Dict[str, Any]
        """
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT blm.chosenbluffpnlid AS id, "
                 "p.panelist AS name, p.panelistslug As slug "
                 "FROM ww_showbluffmap blm "
                 "JOIN ww_shows s ON s.showid = blm.showid "
                 "JOIN ww_panelists p ON "
                 "p.panelistid = blm.chosenbluffpnlid "
                 "WHERE s.showid = %s;")
        cursor.execute(query, (id, ))
        chosen_result = cursor.fetchone()

        if chosen_result:
            chosen_bluff_info = {
                "id": chosen_result["id"],
                "name": chosen_result["name"],
                "slug": chosen_result["slug"] if chosen_result["slug"] else slugify(chosen_result["name"]),
            }
        else:
            chosen_bluff_info = None

        query = ("SELECT blm.correctbluffpnlid AS id, "
                 "p.panelist AS name, p.panelistslug AS slug "
                 "FROM ww_showbluffmap blm "
                 "JOIN ww_shows s ON s.showid = blm.showid "
                 "JOIN ww_panelists p ON "
                 "p.panelistid = blm.correctbluffpnlid "
                 "WHERE s.showid = %s;")
        cursor.execute(query, (id, ))
        correct_result = cursor.fetchone()
        cursor.close()

        if correct_result:
            correct_bluff_info = {
                "id": correct_result["id"],
                "name": correct_result["name"],
                "slug": correct_result["slug"] if correct_result["slug"] else slugify(correct_result["name"]),
            }
        else:
            correct_bluff_info = None

        bluff_info = {
            "chosen_panelist": chosen_bluff_info,
            "correct_panelist": correct_bluff_info,
        }

        return bluff_info

    @lru_cache(maxsize=256, typed=True)
    def retrieve_core_info_by_id(self, id: int) -> Dict[str, Any]:
        """Returns a dictionary with core information for the requested
        show ID.

        :param id: Show ID
        :type id: int
        :return: Dictionary containing host, scorekeeper, location,
            description and notes
        :rtype: Dict[str, Any]
        """
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT s.showid, s.showdate, s.bestof, "
                 "s.repeatshowid, l.locationid, l.city, l.state, "
                 "l.venue, l.locationslug , h.hostid, h.host, "
                 "h.hostslug, hm.guest as hostguest, "
                 "sk.scorekeeperid, sk.scorekeeper, "
                 "sk.scorekeeperslug, skm.guest AS scorekeeperguest, "
                 "skm.description, sd.showdescription, sn.shownotes "
                 "FROM ww_shows s "
                 "JOIN ww_showlocationmap lm ON lm.showid = s.showid "
                 "JOIN ww_locations l ON l.locationid = lm.locationid "
                 "JOIN ww_showhostmap hm ON hm.showid = s.showid "
                 "JOIN ww_hosts h ON h.hostid = hm.hostid "
                 "JOIN ww_showskmap skm ON skm.showid = s.showid "
                 "JOIN ww_scorekeepers sk ON "
                 "sk.scorekeeperid = skm.scorekeeperid "
                 "JOIN ww_showdescriptions sd ON sd.showid = s.showid "
                 "JOIN ww_shownotes sn ON sn.showid = s.showid "
                 "WHERE s.showid = %s;")
        cursor.execute(query, (id, ))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return None

        location_info = {
            "id": result["locationid"],
            "slug": result["locationslug"],
            "city": result["city"],
            "state": result["state"],
            "venue": result["venue"],
        }

        if not result["locationslug"]:
            location_info["slug"] = self.loc_util.slugify_location(id=result["locationid"],
                                                                   venue=result["venue"],
                                                                   city=result["city"],
                                                                   state=result["state"])

        host_info = {
            "id": result["hostid"],
            "name": result["host"],
            "slug": result["hostslug"] if result["hostslug"] else slugify(result["host"]),
            "guest": bool(result["hostguest"]),
        }

        scorekeeper_info = {
            "id": result["scorekeeperid"],
            "name": result["scorekeeper"],
            "slug": result["scorekeeperslug"] if result["scorekeeperslug"] else slugify(result["scorekeeper"]),
            "guest": bool(result["scorekeeperguest"]),
            "description": result["description"] if result["description"] else None,
        }

        if result["showdescription"]:
            description = str(result["showdescription"]).strip()
        else:
            description = None

        if result["shownotes"]:
            notes = str(result["shownotes"]).strip()
        else:
            notes = None

        show_info = {
            "id": id,
            "date": result["showdate"].isoformat(),
            "best_of": bool(result["bestof"]),
            "repeat_show": bool(result["repeatshowid"]),
            "original_show_id": None,
            "original_show_date": None,
            "description": description,
            "notes": notes,
            "location": location_info,
            "host": host_info,
            "scorekeeper": scorekeeper_info,
        }

        repeat_show_id = result["repeatshowid"]
        if repeat_show_id:
            original_date = self.utility.convert_id_to_date(repeat_show_id)
            show_info["original_show_id"] = repeat_show_id
            show_info["original_show_date"] = original_date
        else:
            show_info.pop("original_show_id", None)
            show_info.pop("original_show_date", None)

        return show_info

    @lru_cache(maxsize=256, typed=True)
    def retrieve_guest_info_by_id(self, id: int) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing Not My Job
        guest information for the requested show ID.

        :param id: Show ID
        :type id: int
        :return: Dictionary containing Not My Job guest information
        :rtype: List[Dict[str, Any]]
        """
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT gm.guestid AS id, g.guest AS name, "
                 "g.guestslug AS slug, gm.guestscore AS score, "
                 "gm.exception AS score_exception "
                 "FROM ww_showguestmap gm "
                 "JOIN ww_guests g on g.guestid = gm.guestid "
                 "JOIN ww_shows s on s.showid = gm.showid "
                 "WHERE gm.showid = %s "
                 "ORDER by gm.showguestmapid ASC;")
        cursor.execute(query, (id, ))
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return None

        guests = []
        for guest in result:
            info = {
                "id": guest["id"],
                "name": guest["name"],
                "slug": guest["slug"] if guest["slug"] else slugify(guest["name"]),
                "score": guest["score"],
                "score_exception": guest["score_exception"],
            }

            guests.append(info)

        return guests

    @lru_cache(maxsize=256, typed=True)
    def retrieve_panelist_info_by_id(self, id: int) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing panelist
        information for the requested show ID.

        :param id: Show ID
        :type id: int
        :return: List of panelists with corresponding scores and
            ranking information
        :rtype: List[Dict[str, Any]]
        """
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT pm.panelistid AS id, p.panelist AS name, "
                 "p.panelistslug AS slug, "
                 "pm.panelistlrndstart AS start, "
                 "pm.panelistlrndcorrect AS correct, "
                 "pm.panelistscore AS score, pm.showpnlrank AS rank "
                 "FROM ww_showpnlmap pm "
                 "JOIN ww_panelists p on p.panelistid = pm.panelistid "
                 "WHERE pm.showid = %s "
                 "ORDER by pm.panelistscore DESC, pm.showpnlmapid ASC;")
        cursor.execute(query, (id, ))
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return None

        panelists = []
        for row in result:
            info = {
                "id": row["id"],
                "name": row["name"],
                "slug": row["slug"] if row["slug"] else slugify(row["name"]),
                "lightning_round_start": row["start"],
                "lightning_round_correct": row["correct"],
                "score": row["score"],
                "rank": row["rank"],
            }

            panelists.append(info)

        return panelists
