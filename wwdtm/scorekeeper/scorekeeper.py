# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Scorekeeper Data Retrieval Functions."""

from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from slugify import slugify

from wwdtm.scorekeeper.appearances import ScorekeeperAppearances
from wwdtm.scorekeeper.utility import ScorekeeperUtility
from wwdtm.validation import valid_int_id


class Scorekeeper:
    """Scorekeeper information retrieval class.

    Contains methods used to retrieve scorekeeper information, including
    IDs, names, slug strings and appearances.

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

        self.appearances = ScorekeeperAppearances(
            database_connection=self.database_connection
        )
        self.utility = ScorekeeperUtility(database_connection=self.database_connection)

    def retrieve_all(self) -> list[dict[str, Any]]:
        """Retrieves scorekeeper information for all scorekeepers.

        :return: A list of dictionaries containing scorekeeper ID, name,
            gender and slug string for each scorekeeper
        """
        query = """
            SELECT sk.scorekeeperid AS id, sk.scorekeeper AS name,
            sk.scorekeeperslug AS slug, sk.scorekeepergender AS gender
            FROM ww_scorekeepers sk
            ORDER BY scorekeeper ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        scorekeepers = []

        cursor = self.database_connection.cursor(dictionary=True)
        for row in results:
            query = """
                SELECT pn.pronouns
                FROM ww_skpronounsmap spm
                JOIN ww_pronouns pn on pn.pronounsid = spm.pronounsid
                WHERE spm.scorekeeperid = %s
                ORDER BY spm.skpronounsmapid ASC;
                """
            cursor.execute(query, (row["id"],))
            pn_results = cursor.fetchall()

            scorekeepers.append(
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

        return scorekeepers

    def retrieve_all_details(self) -> list[dict[str, Any]]:
        """Retrieves scorekeeper information and appearances for all scorekeepers.

        :return: A list of dictionaries containing scorekeeper ID, name,
            slug string, gender and a list of appearances with show
            flags for each scorekeeper
        """
        query = """
            SELECT sk.scorekeeperid AS id, sk.scorekeeper AS name,
            sk.scorekeeperslug AS slug, sk.scorekeepergender AS gender
            FROM ww_scorekeepers sk
            ORDER BY scorekeeper ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        scorekeepers = []

        cursor = self.database_connection.cursor(dictionary=True)
        for row in results:
            query = """
                SELECT pn.pronouns
                FROM ww_skpronounsmap spm
                JOIN ww_pronouns pn on pn.pronounsid = spm.pronounsid
                WHERE spm.scorekeeperid = %s
                ORDER BY spm.skpronounsmapid ASC;
                """
            cursor.execute(query, (row["id"],))
            pn_results = cursor.fetchall()

            scorekeepers.append(
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
                    "appearances": self.appearances.retrieve_appearances_by_id(
                        row["id"]
                    ),
                }
            )

        return scorekeepers

    def retrieve_all_ids(self) -> list[int]:
        """Retrieves all scorekeeper IDs, sorted by scorekeeper name.

        :return: A list of scorekeeper IDs as integers
        """
        query = """
            SELECT scorekeeperid FROM ww_scorekeepers ORDER BY scorekeeper ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [v[0] for v in results]

    def retrieve_all_slugs(self) -> list[str]:
        """Retrieves all scorekeeper slug strings, sorted by scorekeeper name.

        :return: A list of scorekeeper slug strings
        """
        query = """
            SELECT scorekeeperslug FROM ww_scorekeepers ORDER BY scorekeeper ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [v[0] for v in results]

    def retrieve_by_id(self, scorekeeper_id: int) -> dict[str, Any]:
        """Retrieves scorekeeper information.

        :param scorekeeper_id: Scorekeeper ID
        :return: A dictionary containing scorekeeper ID, name, slug
            string and gender
        """
        if not valid_int_id(scorekeeper_id):
            return {}

        query = """
            SELECT sk.scorekeeperid AS id, sk.scorekeeper AS name,
            sk.scorekeeperslug AS slug, sk.scorekeepergender AS gender
            FROM ww_scorekeepers sk
            WHERE sk.scorekeeperid = %s
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (scorekeeper_id,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return {}

        query = """
            SELECT pn.pronouns
            FROM ww_skpronounsmap spm
            JOIN ww_pronouns pn on pn.pronounsid = spm.pronounsid
            WHERE spm.scorekeeperid = %s
            ORDER BY spm.skpronounsmapid ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (scorekeeper_id,))
        results = cursor.fetchall()
        cursor.close()

        return {
            "id": result["id"],
            "name": result["name"],
            "slug": result["slug"] if result["slug"] else slugify(result["name"]),
            "gender": result["gender"],
            "pronouns": [result["pronouns"] for result in results] if results else [],
        }

    def retrieve_by_slug(self, scorekeeper_slug: str) -> dict[str, Any]:
        """Retrieves scorekeeper information.

        :param scorekeeper_slug: Scorekeeper slug string
        :return: A dictionary containing scorekeeper ID, name, slug
            string and gender
        """
        try:
            slug = scorekeeper_slug.strip()
            if not slug:
                return {}
        except AttributeError:
            return {}

        id_ = self.utility.convert_slug_to_id(slug)
        if not id_:
            return {}

        return self.retrieve_by_id(id_)

    def retrieve_details_by_id(self, scorekeeper_id: int) -> dict[str, Any]:
        """Retrieves scorekeeper information and appearances.

        :param scorekeeper_id: Scorekeeper ID
        :return: A dictionaries containing scorekeeper ID, name, slug
            string, gender and a list of appearances with show flags
        """
        if not valid_int_id(scorekeeper_id):
            return {}

        info = self.retrieve_by_id(scorekeeper_id)
        if not info:
            return {}

        info["appearances"] = self.appearances.retrieve_appearances_by_id(
            scorekeeper_id
        )

        return info

    def retrieve_details_by_slug(self, scorekeeper_slug: str) -> dict[str, Any]:
        """Retrieves scorekeeper information and appearances.

        :param scorekeeper_slug: Scorekeeper slug string
        :return: A dictionaries containing scorekeeper ID, name, slug
            string, gender and a list of appearances with show flags
        """
        try:
            slug = scorekeeper_slug.strip()
            if not slug:
                return {}
        except AttributeError:
            return {}

        id_ = self.utility.convert_slug_to_id(slug)
        if not id_:
            return {}

        return self.retrieve_details_by_id(id_)

    def retrieve_random_id(self) -> int:
        """Retrieves an ID for a random scorekeeper.

        :return: ID for a random scorekeeper.
        """
        query = """
            SELECT scorekeeperid FROM ww_scorekeepers
            WHERE scorekeeperslug <> 'tbd'
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
        """Retrieves an slug string for a random scorekeeper.

        :return: Slug string for a random scorekeeper.
        """
        query = """
            SELECT scorekeeperslug FROM ww_scorekeepers
            WHERE scorekeeperslug <> 'tbd'
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
        """Retrieves information for a random scorekeeper.

        :return: A dictionary containing scorekeeper ID, name, slug
            string and gender
        """
        _id = self.retrieve_random_id()

        if not _id:
            return None

        return self.retrieve_by_id(scorekeeper_id=_id)

    def retrieve_random_details(self) -> dict[str, Any]:
        """Retrieves information and appearances for a random scorekeeper.

        :return: A dictionaries containing scorekeeper ID, name, slug
            string, gender and a list of appearances with show flags
        """
        _id = self.retrieve_random_id()

        if not _id:
            return None

        return self.retrieve_details_by_id(scorekeeper_id=_id)
