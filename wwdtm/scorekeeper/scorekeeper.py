# Copyright (c) 2018-2026 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Scorekeeper Data Retrieval Functions."""

import warnings
from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from slugify import slugify

from wwdtm.guest.utility import GuestUtility
from wwdtm.host.utility import HostUtility
from wwdtm.panelist.utility import PanelistUtility
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
            gender, pronouns and slug string for each scorekeeper
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

        for row in results:
            scorekeepers.append(
                {
                    "id": row["id"],
                    "name": row["name"],
                    "slug": row["slug"] if row["slug"] else slugify(row["name"]),
                    "gender": row["gender"],
                    "pronouns": self.retrieve_pronouns_by_id(row["id"]),
                    "external_sites": self.retrieve_external_sites_by_id(row["id"]),
                    "social_media_accounts": self.retrieve_social_media_accounts_by_id(
                        row["id"]
                    ),
                }
            )

        return scorekeepers

    def retrieve_all_details(self) -> list[dict[str, Any]]:
        """Retrieves scorekeeper information and appearances for all scorekeepers.

        :return: A list of dictionaries containing scorekeeper ID, name,
            slug string, gender, pronouns, whether the scorekeeper is also
            a guest, host or panelist, and a list of appearances with show
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
        _guest_utility = GuestUtility(database_connection=self.database_connection)
        _host_utility = HostUtility(database_connection=self.database_connection)
        _panelist_utility = PanelistUtility(
            database_connection=self.database_connection
        )

        for row in results:
            _slug = row["slug"] if row["slug"] else slugify(row["name"])

            scorekeepers.append(
                {
                    "id": row["id"],
                    "name": row["name"],
                    "slug": _slug,
                    "gender": row["gender"],
                    "pronouns": self.retrieve_pronouns_by_id(row["id"]),
                    "external_sites": self.retrieve_external_sites_by_id(row["id"]),
                    "social_media_accounts": self.retrieve_social_media_accounts_by_id(
                        row["id"]
                    ),
                    "is_guest": bool(_guest_utility.slug_exists(_slug)),
                    "is_host": bool(_host_utility.slug_exists(_slug)),
                    "is_panelist": bool(_panelist_utility.slug_exists(_slug)),
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
            string, gender and pronouns
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

        return {
            "id": result["id"],
            "name": result["name"],
            "slug": result["slug"] if result["slug"] else slugify(result["name"]),
            "gender": result["gender"],
            "pronouns": self.retrieve_pronouns_by_id(scorekeeper_id),
            "external_sites": self.retrieve_external_sites_by_id(scorekeeper_id),
            "social_media_accounts": self.retrieve_social_media_accounts_by_id(
                scorekeeper_id
            ),
        }

    def retrieve_by_slug(self, scorekeeper_slug: str) -> dict[str, Any]:
        """Retrieves scorekeeper information.

        :param scorekeeper_slug: Scorekeeper slug string
        :return: A dictionary containing scorekeeper ID, name, slug
            string, gender and pronouns
        """
        _id = self.utility.convert_slug_to_id(scorekeeper_slug)
        if not _id:
            return {}

        return self.retrieve_by_id(_id)

    def retrieve_details_by_id(self, scorekeeper_id: int) -> dict[str, Any]:
        """Retrieves scorekeeper information and appearances.

        :param scorekeeper_id: Scorekeeper ID
        :return: A dictionaries containing scorekeeper ID, name, slug
            string, gender, pronouns, whether the scorekeeper is also
            a guest, host or panelist, and a list of appearances with
            show flags
        """
        if not valid_int_id(scorekeeper_id):
            return {}

        info = self.retrieve_by_id(scorekeeper_id)
        if not info:
            return {}

        _guest_utility = GuestUtility(database_connection=self.database_connection)
        _host_utility = HostUtility(database_connection=self.database_connection)
        _panelist_utility = PanelistUtility(
            database_connection=self.database_connection
        )

        info["is_guest"] = bool(_guest_utility.slug_exists(info["slug"]))
        info["is_host"] = bool(_host_utility.slug_exists(info["slug"]))
        info["is_panelist"] = bool(_panelist_utility.slug_exists(info["slug"]))
        info["appearances"] = self.appearances.retrieve_appearances_by_id(
            scorekeeper_id
        )

        return info

    def retrieve_details_by_slug(self, scorekeeper_slug: str) -> dict[str, Any]:
        """Retrieves scorekeeper information and appearances.

        :param scorekeeper_slug: Scorekeeper slug string
        :return: A dictionaries containing scorekeeper ID, name, slug
            string, gender, pronouns, whether the scorekeeper is also
            a guest, host or panelist, and a list of appearances with
            show flags
        """
        _id = self.utility.convert_slug_to_id(scorekeeper_slug)
        if not _id:
            return {}

        return self.retrieve_details_by_id(_id)

    def retrieve_pronouns_by_id(self, scorekeeper_id: int) -> list[str]:
        """Retrieves preferred pronouns for a scorekeeper.

        :param scorekeeper_id: Scorekeeper ID
        :return: A list of preferred pronouns.
        """
        if not valid_int_id(scorekeeper_id):
            return []

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

        if not results:
            return []

        return [result["pronouns"] for result in results]

    def retrieve_pronouns_by_slug(self, scorekeeper_slug: str) -> list[str]:
        """Retrieves preferred pronouns for a scorekeeper.

        :param scorekeeper_slug: Scorekeeper slug string
        :return: A list of preferred pronouns.
        """
        _id = self.utility.convert_slug_to_id(scorekeeper_slug)
        if not _id:
            return {}

        return self.retrieve_pronouns_by_id(_id)

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
            string, gender and pronouns
        """
        _id = self.retrieve_random_id()

        if not _id:
            return None

        return self.retrieve_by_id(_id)

    def retrieve_random_details(self) -> dict[str, Any]:
        """Retrieves information and appearances for a random scorekeeper.

        :return: A dictionaries containing scorekeeper ID, name, slug
            string, gender, pronouns, whether the scorekeeper is also
            a guest, host or panelist, and a list of appearances with
            show flags
        """
        _id = self.retrieve_random_id()

        if not _id:
            return None

        return self.retrieve_details_by_id(_id)

    def retrieve_external_sites_by_id(
        self, scorekeeper_id: int
    ) -> list[dict[str, str]]:
        """Retrieves external site information for a scorekeeper.

        :param scorekeeper_id: Scorekeeper ID
        :return: A list of dictionaries containing external site
            information, including social media accounts.
        """
        if not valid_int_id(scorekeeper_id):
            return []

        query = """
            SELECT es.site, es.siteslug, es.iconname, es.socialmedia,
            ssm.url, ssm.account
            FROM ww_skextsitesmap ssm
            JOIN ww_externalsites es ON es.siteid = ssm.siteid
            WHERE ssm.scorekeeperid = %s
            ORDER BY es.site ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (scorekeeper_id,))
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        accounts = []
        for row in results:
            accounts.append(
                {
                    "site": row["site"],
                    "slug": row["siteslug"],
                    "icon": row["iconname"],
                    "social_media": bool(row["socialmedia"]),
                    "account": row["account"],
                    "url": row["url"],
                }
            )

        return accounts

    def retrieve_external_sites_by_slug(
        self, scorekeeper_slug: str
    ) -> list[dict[str, str]]:
        """Retrieves external site information for a scorekeeper.

        :param scorekeeper_slug: Scorekeeper slug string
        :return: A list of dictionaries containing external site
            information, including social media accounts.
        """
        _id = self.utility.convert_slug_to_id(scorekeeper_slug)
        if not _id:
            return {}

        return self.retrieve_external_sites_by_id(_id)

    def retrieve_social_media_accounts_by_id(
        self, scorekeeper_id: int
    ) -> list[dict[str, str]]:
        """*Deprecated:* Retrieves social media accounts for a scorekeeper.

        :param scorekeeper_id: Scorekeeper ID
        :return: A list of dictionaries containing social media
            account information.
        """
        warnings.warn(
            message="This method has been deprecated. Use 'Scorekeeper.retrieve_external_accounts_by_id()' instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )

        if not valid_int_id(scorekeeper_id):
            return []

        query = """
            SELECT es.site, es.siteslug, es.iconname, ssm.url, ssm.account
            FROM ww_skextsitesmap ssm
            JOIN ww_externalsites es ON es.siteid = ssm.siteid
            WHERE ssm.scorekeeperid = %s AND es.socialmedia = 1
            ORDER BY es.site ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (scorekeeper_id,))
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        accounts = []
        for row in results:
            accounts.append(
                {
                    "network": row["site"],
                    "slug": row["iconname"],
                    "account": row["account"],
                    "url": row["url"],
                }
            )

        return accounts

    def retrieve_social_media_accounts_by_slug(
        self, scorekeeper_slug: str
    ) -> list[dict[str, str]]:
        """*Deprecated:* Retrieves social media accounts for a scorekeeper.

        :param scorekeeper_slug: Scorekeeper slug string
        :return: A list of dictionaries containing social media
            account information.
        """
        warnings.warn(
            message="This method has been deprecated. Use 'Scorekeeper.retrieve_external_accounts_by_slug()' instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        _id = self.utility.convert_slug_to_id(scorekeeper_slug)
        if not _id:
            return {}

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return self.retrieve_social_media_accounts_by_id(_id)
