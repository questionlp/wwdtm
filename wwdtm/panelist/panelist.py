# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Panelist Data Retrieval Functions."""

from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from slugify import slugify

from wwdtm.panelist.appearances import PanelistAppearances
from wwdtm.panelist.statistics import PanelistStatistics
from wwdtm.panelist.utility import PanelistUtility
from wwdtm.validation import valid_int_id


class Panelist:
    """Panelist information retrieval class.

    Contains methods used to retrieve panelist information, including
    IDs, names, slug strings, appearances and scores.

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

        self.appearances = PanelistAppearances(
            database_connection=self.database_connection
        )
        self.statistics = PanelistStatistics(
            database_connection=self.database_connection
        )
        self.utility = PanelistUtility(database_connection=self.database_connection)

    def retrieve_all(self) -> list[dict[str, Any]]:
        """Retrieve panelist information for all panelists.

        :return: A list of dictionaries containing panelist ID, name,
            slug string and gender for each panelist
        """
        query = """
            SELECT p.panelistid AS id, p.panelist AS name, p.panelistslug AS slug,
            panelistgender AS gender
            FROM ww_panelists p
            WHERE panelistslug != 'multiple'
            ORDER BY panelist ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        panelists = []

        cursor = self.database_connection.cursor(dictionary=True)
        for row in results:
            query = """
                SELECT pn.pronouns
                FROM ww_panelistpronounsmap ppm
                JOIN ww_pronouns pn on pn.pronounsid = ppm.pronounsid
                WHERE ppm.panelistid = %s
                ORDER BY ppm.panelistpronounsmapid ASC;
                """
            cursor.execute(query, (row["id"],))
            pn_results = cursor.fetchall()

            panelists.append(
                {
                    "id": row["id"],
                    "name": row["name"],
                    "slug": row["slug"] if row["slug"] else slugify(row["name"]),
                    "gender": row["gender"],
                    "pronouns": (
                        [result["pronouns"] for result in pn_results]
                        if pn_results
                        else []
                    ),
                }
            )

        return panelists

    def retrieve_all_details(
        self, use_decimal_scores: bool = False
    ) -> list[dict[str, Any]]:
        """Retrieves panelist information, appearances and scores for all panelists.

        :param use_decimal_scores: A boolean to determine if decimal
            scores should be used and returned instead of integer scores
        :return: A list of dictionaries containing panelist ID, name,
            slug string, gender, scoring statistics and appearances for
            each panelist
        """
        query = """
            SELECT p.panelistid AS id, p.panelist AS name, p.panelistslug AS slug,
            p.panelistgender AS gender
            FROM ww_panelists p
            WHERE panelistslug != 'multiple'
            ORDER BY panelist ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        panelists = []

        cursor = self.database_connection.cursor(dictionary=True)
        for row in results:
            query = """
                SELECT pn.pronouns
                FROM ww_panelistpronounsmap ppm
                JOIN ww_pronouns pn on pn.pronounsid = ppm.pronounsid
                WHERE ppm.panelistid = %s
                ORDER BY ppm.panelistpronounsmapid ASC;
                """
            cursor.execute(query, (row["id"],))
            pn_results = cursor.fetchall()
            panelists.append(
                {
                    "id": row["id"],
                    "name": row["name"],
                    "slug": row["slug"] if row["slug"] else slugify(row["name"]),
                    "gender": row["gender"],
                    "pronouns": (
                        [result["pronouns"] for result in pn_results]
                        if pn_results
                        else []
                    ),
                    "statistics": self.statistics.retrieve_statistics_by_id(
                        row["id"], include_decimal_scores=use_decimal_scores
                    ),
                    "bluffs": self.statistics.retrieve_bluffs_by_id(row["id"]),
                    "appearances": self.appearances.retrieve_appearances_by_id(
                        row["id"], use_decimal_scores=use_decimal_scores
                    ),
                }
            )

        return panelists

    def retrieve_all_ids(self) -> list[int]:
        """Retrieves all panelist IDs, sorted by panelist name.

        :return: A list of panelist IDs as integers
        """
        query = """
            SELECT panelistid FROM ww_panelists
            WHERE panelistslug != 'multiple'
            ORDER BY panelist ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [v[0] for v in results]

    def retrieve_all_slugs(self) -> list[str]:
        """Retrieves all panelist slug strings, sorted by panelist name.

        :return: A list of panelist slug strings
        """
        query = """
            SELECT panelistslug FROM ww_panelists
            WHERE panelistslug != 'multiple'
            ORDER BY panelist ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [v[0] for v in results]

    def retrieve_by_id(self, panelist_id: int) -> dict[str, Any]:
        """Retrieves panelist information.

        :param panelist_id: Panelist ID
        :return: A dictionary containing panelist ID, name, slug string
            and gender
        """
        if not valid_int_id(panelist_id):
            return {}

        query = """
            SELECT p.panelistid AS id, p.panelist AS name, p.panelistslug AS slug,
            p.panelistgender AS gender
            FROM ww_panelists p
            WHERE p.panelistid = %s
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (panelist_id,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return {}

        query = """
            SELECT pn.pronouns
            FROM ww_panelistpronounsmap ppm
            JOIN ww_pronouns pn on pn.pronounsid = ppm.pronounsid
            WHERE ppm.panelistid = %s
            ORDER BY ppm.panelistpronounsmapid ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (panelist_id,))
        results = cursor.fetchall()
        cursor.close()

        return {
            "id": result["id"],
            "name": result["name"],
            "slug": result["slug"] if result["slug"] else slugify(result["name"]),
            "gender": result["gender"],
            "pronouns": [result["pronouns"] for result in results] if results else [],
        }

    def retrieve_by_slug(self, panelist_slug: str) -> dict[str, Any]:
        """Retrieves panelist information.

        :param panelist_slug: Panelist slug string
        :return: A dictionary containing panelist ID, name, slug string
            and gender
        """
        try:
            slug = panelist_slug.strip()
            if not slug:
                return {}
        except AttributeError:
            return {}

        id_ = self.utility.convert_slug_to_id(slug)
        if not id_:
            return {}

        return self.retrieve_by_id(id_)

    def retrieve_details_by_id(
        self, panelist_id: int, use_decimal_scores: bool = False
    ) -> dict[str, Any]:
        """Retrieves panelist information, appearances and scores.

        :param panelist_id: Panelist ID
        :param use_decimal_scores: A boolean to determine if decimal
            scores should be used and returned instead of integer scores
        :return: A dictionary containing panelist ID, name, slug string,
            gender, scoring statistics and appearances
        """
        if not valid_int_id(panelist_id):
            return {}

        info = self.retrieve_by_id(panelist_id)
        if not info:
            return {}

        info["statistics"] = self.statistics.retrieve_statistics_by_id(
            panelist_id, include_decimal_scores=use_decimal_scores
        )
        info["bluffs"] = self.statistics.retrieve_bluffs_by_id(panelist_id)
        info["appearances"] = self.appearances.retrieve_appearances_by_id(
            panelist_id, use_decimal_scores=use_decimal_scores
        )

        return info

    def retrieve_details_by_slug(
        self, panelist_slug: str, use_decimal_scores: bool = False
    ) -> dict[str, Any]:
        """Retrieves panelist information, appearances and scores.

        :param panelist_slug: Panelist slug string
        :param use_decimal_scores: A boolean to determine if decimal
            scores should be used and returned instead of integer scores
        :return: A dictionary containing panelist ID, name, slug string,
            gender, scoring statistics and appearances
        """
        try:
            slug = panelist_slug.strip()
            if not slug:
                return {}
        except AttributeError:
            return {}

        id_ = self.utility.convert_slug_to_id(slug)
        if not id_:
            return {}

        return self.retrieve_details_by_id(id_, use_decimal_scores=use_decimal_scores)

    def retrieve_random_id(self) -> int:
        """Retrieves an ID for a random panelist.

        :return: ID for a random panelist.
        """
        query = """
            SELECT panelistid FROM ww_panelists
            WHERE panelistslug <> 'multiple'
            ORDER BY RAND()
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return None

        return result[0]

    def retrieve_random_slug(self) -> str:
        """Retrieves an slug string for a random panelist.

        :return: Slug string for a random panelist.
        """
        query = """
            SELECT panelistslug FROM ww_panelists
            WHERE panelistslug <> 'multiple'
            ORDER BY RAND()
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return None

        return result[0]

    def retrieve_random(self) -> dict[str, Any]:
        """Retrieves information for a random panelist.

        :return: A dictionary containing panelist ID, name, slug string
            and gender
        """
        _id = self.retrieve_random_id()

        if not _id:
            return None

        return self.retrieve_by_id(panelist_id=_id)

    def retrieve_random_details(
        self, use_decimal_scores: bool = False
    ) -> dict[str, Any]:
        """Retrieves information and appearances for a random panelist.

        :return: A dictionary containing panelist ID, name, slug string,
            gender, scoring statistics and appearances
        """
        _id = self.retrieve_random_id()

        if not _id:
            return None

        return self.retrieve_details_by_id(
            panelist_id=_id, use_decimal_scores=use_decimal_scores
        )
