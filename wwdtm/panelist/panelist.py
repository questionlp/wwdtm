# Copyright (c) 2018-2026 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Panelist Data Retrieval Functions."""

import warnings
from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from slugify import slugify

from wwdtm.guest.utility import GuestUtility
from wwdtm.host.utility import HostUtility
from wwdtm.panelist.appearances import PanelistAppearances
from wwdtm.panelist.statistics import PanelistStatistics
from wwdtm.panelist.utility import PanelistUtility
from wwdtm.scorekeeper.utility import ScorekeeperUtility
from wwdtm.validation import valid_int_id, valid_rounding_decimal_places


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
            slug string, gender and pronouns for each panelist
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

        for row in results:
            panelists.append(
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

        return panelists

    def retrieve_all_details(
        self, number_decimal_places: int = 5
    ) -> list[dict[str, Any]]:
        """Retrieves panelist information, appearances and scores for all panelists.

        :param number_decimal_places: Number of decimal places to
            include when rounding (valid range: 0 through 20)
        :return: A list of dictionaries containing panelist ID, name,
            slug string, gender, pronouns, whether the panelist is
            also a guest, host or scorekeeper, scoring statistics and
            appearances for each panelist

        .. version-changed:: 3.2.0
            Added ``number_decimal_places`` parameter
        """
        if not valid_rounding_decimal_places(
            number_decimal_places=number_decimal_places
        ):
            return {}

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
        _guest_utility = GuestUtility(database_connection=self.database_connection)
        _host_utility = HostUtility(database_connection=self.database_connection)
        _scorekeeper_utility = ScorekeeperUtility(
            database_connection=self.database_connection
        )

        for row in results:
            _slug = row["slug"] if row["slug"] else slugify(row["name"])

            panelists.append(
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
                    "is_scorekeeper": bool(_scorekeeper_utility.slug_exists(_slug)),
                    "statistics": self.statistics.retrieve_statistics_by_id(
                        row["id"], number_decimal_places=number_decimal_places
                    ),
                    "bluffs": self.statistics.retrieve_bluffs_by_id(row["id"]),
                    "appearances": self.appearances.retrieve_appearances_by_id(
                        row["id"]
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
        :return: A dictionary containing panelist ID, name, slug string,
            gender and pronouns
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

        return {
            "id": result["id"],
            "name": result["name"],
            "slug": result["slug"] if result["slug"] else slugify(result["name"]),
            "gender": result["gender"],
            "pronouns": self.retrieve_pronouns_by_id(panelist_id),
            "external_sites": self.retrieve_external_sites_by_id(panelist_id),
            "social_media_accounts": self.retrieve_social_media_accounts_by_id(
                panelist_id
            ),
        }

    def retrieve_by_slug(self, panelist_slug: str) -> dict[str, Any]:
        """Retrieves panelist information.

        :param panelist_slug: Panelist slug string
        :return: A dictionary containing panelist ID, name, slug string,
            gender and pronouns
        """
        _id = self.utility.convert_slug_to_id(panelist_slug)
        if not _id:
            return {}

        return self.retrieve_by_id(_id)

    def retrieve_details_by_id(
        self, panelist_id: int, number_decimal_places: int = 5
    ) -> dict[str, Any]:
        """Retrieves panelist information, appearances and scores.

        :param panelist_id: Panelist ID
        :param number_decimal_places: Number of decimal places to
            include when rounding (valid range: 0 through 20)
        :return: A dictionary containing panelist ID, name, slug string,
            gender, pronouns, whether the panelist is also a guest, host
            or scorekeeper, scoring statistics and appearances

        .. version-changed:: 3.2.0
            Added ``number_decimal_places`` parameter
        """
        if not valid_int_id(panelist_id):
            return {}

        info = self.retrieve_by_id(panelist_id)
        if not info:
            return {}

        if not valid_rounding_decimal_places(
            number_decimal_places=number_decimal_places
        ):
            return {}

        _guest_utility = GuestUtility(database_connection=self.database_connection)
        _host_utility = HostUtility(database_connection=self.database_connection)
        _scorekeeper_utility = ScorekeeperUtility(
            database_connection=self.database_connection
        )

        info["is_guest"] = bool(_guest_utility.slug_exists(info["slug"]))
        info["is_host"] = bool(_host_utility.slug_exists(info["slug"]))
        info["is_scorekeeper"] = bool(_scorekeeper_utility.slug_exists(info["slug"]))

        info["statistics"] = self.statistics.retrieve_statistics_by_id(
            panelist_id, number_decimal_places=number_decimal_places
        )
        info["bluffs"] = self.statistics.retrieve_bluffs_by_id(panelist_id)
        info["appearances"] = self.appearances.retrieve_appearances_by_id(panelist_id)

        return info

    def retrieve_details_by_slug(
        self, panelist_slug: str, number_decimal_places: int = 5
    ) -> dict[str, Any]:
        """Retrieves panelist information, appearances and scores.

        :param panelist_slug: Panelist slug string
        :param number_decimal_places: Number of decimal places to
            include when rounding (valid range: 0 through 20)
        :return: A dictionary containing panelist ID, name, slug string,
            gender, pronouns, whether the panelist is also a guest, host
            or scorekeeper, scoring statistics and appearances

        .. version-changed:: 3.2.0
            Added ``number_decimal_places`` parameter
        """
        _id = self.utility.convert_slug_to_id(panelist_slug)
        if not _id:
            return {}

        if not valid_rounding_decimal_places(
            number_decimal_places=number_decimal_places
        ):
            return {}

        return self.retrieve_details_by_id(
            _id, number_decimal_places=number_decimal_places
        )

    def retrieve_pronouns_by_id(self, panelist_id: int) -> list[str]:
        """Retrieves preferred pronouns for a panelist.

        :param panelist_id: Panelist ID
        :return: A list of preferred pronouns.

        .. version-added:: 3.3.0
        """
        if not valid_int_id(panelist_id):
            return []

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

        if not results:
            return []

        return [result["pronouns"] for result in results]

    def retrieve_pronouns_by_slug(self, panelist_slug: str) -> list[str]:
        """Retrieves preferred pronouns for a panelist.

        :param panelist_slug: Panelist slug string
        :return: A list of preferred pronouns.

        .. version-added:: 3.3.0
        """
        _id = self.utility.convert_slug_to_id(panelist_slug)
        if not _id:
            return {}

        return self.retrieve_pronouns_by_id(_id)

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

        return self.retrieve_by_id(_id)

    def retrieve_random_details(self, number_decimal_places: int = 5) -> dict[str, Any]:
        """Retrieves information and appearances for a random panelist.

        :param number_decimal_places: Number of decimal places to
            include when rounding (valid range: 0 through 20)
        :return: A dictionary containing panelist ID, name, slug string,
            gender, pronouns, whether the panelist is also a guest, host
            or scorekeeper, scoring statistics and appearances

        .. version-changed:: 3.2.0
            Added ``number_decimal_places`` parameter
        """
        _id = self.retrieve_random_id()

        if not _id:
            return None

        if not valid_rounding_decimal_places(
            number_decimal_places=number_decimal_places
        ):
            return {}

        return self.retrieve_details_by_id(
            _id, number_decimal_places=number_decimal_places
        )

    def retrieve_external_sites_by_id(self, panelist_id: int) -> list[dict[str, str]]:
        """Retrieves external site information for a panelist.

        :param panelist_id: Panelist ID
        :return: A list of dictionaries containing external site
            information, including social media accounts.

        .. version-added:: 3.4.0
        """
        if not valid_int_id(panelist_id):
            return []

        query = """
            SELECT es.site, es.siteslug, es.iconname, es.socialmedia,
            psm.url, psm.account
            FROM ww_panelistextsitesmap psm
            JOIN ww_externalsites es ON es.siteid = psm.siteid
            WHERE psm.panelistid = %s
            ORDER BY es.site ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (panelist_id,))
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
        self, panelist_slug: str
    ) -> list[dict[str, str]]:
        """Retrieves external site information for a panelist.

        :param panelist_slug: Panelist slug string
        :return: A list of dictionaries containing external site
            information, including social media accounts.

        .. version-added:: 3.4.0
        """
        _id = self.utility.convert_slug_to_id(panelist_slug)
        if not _id:
            return {}

        return self.retrieve_external_sites_by_id(_id)

    def retrieve_social_media_accounts_by_id(
        self, panelist_id: int
    ) -> list[dict[str, str]]:
        """Retrieves social media accounts for a panelist.

        :param panelist_id: Panelist ID
        :return: A list of dictionaries containing social media
            account information.

        .. version-deprecated:: 3.4.0
            Use :py:meth:`retrieve_external_sites_by_id` instead.
        .. version-added:: 3.3.0
        """
        warnings.warn(
            message="Use 'retrieve_external_sites_by_id()' instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        if not valid_int_id(panelist_id):
            return []

        query = """
            SELECT es.site, es.siteslug, es.iconname, psm.url, psm.account
            FROM ww_panelistextsitesmap psm
            JOIN ww_externalsites es ON es.siteid = psm.siteid
            WHERE psm.panelistid = %s AND es.socialmedia = 1
            ORDER BY es.site ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (panelist_id,))
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
        self, panelist_slug: str
    ) -> list[dict[str, str]]:
        """Retrieves social media accounts for a panelist.

        :param panelist_slug: Panelist slug string
        :return: A list of dictionaries containing social media
            account information.

        .. version-deprecated:: 3.4.0
            Use :py:meth:`retrieve_external_sites_by_slug` instead.
        .. version-added:: 3.3.0
        """
        warnings.warn(
            message="Use 'retrieve_external_sites_by_slug()' instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        _id = self.utility.convert_slug_to_id(panelist_slug)
        if not _id:
            return {}

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return self.retrieve_social_media_accounts_by_id(_id)
