# Copyright (c) 2018-2026 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Host Data Retrieval Functions."""

import warnings
from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from slugify import slugify

from wwdtm.guest.utility import GuestUtility
from wwdtm.host.appearances import HostAppearances
from wwdtm.host.utility import HostUtility
from wwdtm.panelist.utility import PanelistUtility
from wwdtm.scorekeeper.utility import ScorekeeperUtility
from wwdtm.validation import valid_int_id


class Host:
    """Host information retrieval class.

    Contains methods used to retrieve host information, including IDs,
    names, slug strings and appearances.

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

        self.appearances = HostAppearances(database_connection=self.database_connection)
        self.utility = HostUtility(database_connection=self.database_connection)

    def retrieve_all(self) -> list[dict[str, int | str]]:
        """Retrieves host information for all hosts.

        :return: A list of dictionaries containing host ID, name, slug
            string, gender and pronouns for each host
        """
        query = """
            SELECT h.hostid AS id, h.host AS name, h.hostslug AS slug,
            hostgender AS gender
            FROM ww_hosts h
            ORDER BY host ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        hosts = []

        for row in results:
            hosts.append(
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

        return hosts

    def retrieve_all_details(self) -> list[dict[str, Any]]:
        """Retrieves host information and appearances for all hosts.

        :return: A list of dictionaries containing host ID, name, slug
            string, gender, pronouns, whether the host is also a guest,
            host or scorekeeper, and a list of appearances with show
            flags for each host
        """
        query = """
            SELECT h.hostid AS id, h.host AS name, h.hostslug AS slug,
            h.hostgender AS gender
            FROM ww_hosts h
            ORDER BY host ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        hosts = []
        _guest_utility = GuestUtility(database_connection=self.database_connection)
        _panelist_utility = PanelistUtility(
            database_connection=self.database_connection
        )
        _scorekeeper_utility = ScorekeeperUtility(
            database_connection=self.database_connection
        )

        for row in results:
            _slug = row["slug"] if row["slug"] else slugify(row["name"])

            hosts.append(
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
                    "is_panelist": bool(_panelist_utility.slug_exists(_slug)),
                    "is_scorekeeper": bool(_scorekeeper_utility.slug_exists(_slug)),
                    "appearances": self.appearances.retrieve_appearances_by_id(
                        row["id"]
                    ),
                }
            )

        return hosts

    def retrieve_all_ids(self) -> list[int]:
        """Retrieves all host IDs, sorted by host name.

        :return: A list of host IDs as integers
        """
        cursor = self.database_connection.cursor(dictionary=False)
        query = "SELECT hostid FROM ww_hosts ORDER BY host ASC;"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [v[0] for v in results]

    def retrieve_all_slugs(self) -> list[str]:
        """Retrieves all host slug strings, sorted by host name.

        :return: A list of host slug strings
        """
        query = """
            SELECT hostslug FROM ww_hosts ORDER BY host ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [v[0] for v in results]

    def retrieve_by_id(self, host_id: int) -> dict[str, Any]:
        """Retrieves host information.

        :param host_id: Host ID
        :return: A dictionary containing host ID, name, gender and slug string
        """
        if not valid_int_id(host_id):
            return {}

        query = """
            SELECT h.hostid AS id, h.host AS name, h.hostslug AS slug,
            h.hostgender AS gender
            FROM ww_hosts h
            WHERE h.hostid = %s
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (host_id,))
        result = cursor.fetchone()

        if not result:
            return {}

        return {
            "id": result["id"],
            "name": result["name"],
            "slug": result["slug"] if result["slug"] else slugify(result["name"]),
            "gender": result["gender"],
            "pronouns": self.retrieve_pronouns_by_id(host_id),
            "external_sites": self.retrieve_external_sites_by_id(host_id),
            "social_media_accounts": self.retrieve_social_media_accounts_by_id(host_id),
        }

    def retrieve_by_slug(self, host_slug: str) -> dict[str, Any]:
        """Retrieves host information.

        :param host_slug: Host slug string
        :return: A dictionary containing host ID, name, gender and slug
            string
        """
        _id = self.utility.convert_slug_to_id(host_slug)
        if not _id:
            return {}

        return self.retrieve_by_id(_id)

    def retrieve_details_by_id(self, host_id: int) -> dict[str, Any]:
        """Retrieves host information and appearances.

        :param host_id: Host ID
        :return: A dictionary containing host ID, name, slug string,
            gender, pronouns, whether the host is also a guest, host or
            scorekeeper, and a list of appearances with show flags
        """
        if not valid_int_id(host_id):
            return {}

        info = self.retrieve_by_id(host_id)
        if not info:
            return {}

        _guest_utility = GuestUtility(database_connection=self.database_connection)
        _panelist_utility = PanelistUtility(
            database_connection=self.database_connection
        )
        _scorekeeper_utility = ScorekeeperUtility(
            database_connection=self.database_connection
        )

        info["is_guest"] = bool(_guest_utility.slug_exists(info["slug"]))
        info["is_panelist"] = bool(_panelist_utility.slug_exists(info["slug"]))
        info["is_scorekeeper"] = bool(_scorekeeper_utility.slug_exists(info["slug"]))
        info["appearances"] = self.appearances.retrieve_appearances_by_id(host_id)

        return info

    def retrieve_details_by_slug(self, host_slug: str) -> dict[str, Any]:
        """Retrieves host information and appearances.

        :param host_slug: Host slug string
        :return: A dictionary containing host ID, name, slug string,
            gender, pronouns, whether the host is also a guest, host or
            scorekeeper, and a list of appearances with show flags
        """
        _id = self.utility.convert_slug_to_id(host_slug)
        if not _id:
            return {}

        return self.retrieve_details_by_id(_id)

    def retrieve_random_id(self) -> int:
        """Retrieves an ID for a random host.

        :return: ID for a random host.
        """
        query = """
            SELECT hostid FROM ww_hosts
            WHERE hostslug <> 'tbd'
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
        """Retrieves an slug string for a random host.

        :return: Slug string for a random host.
        """
        query = """
            SELECT hostslug FROM ww_hosts
            WHERE hostslug <> 'tbd'
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

    def retrieve_pronouns_by_id(self, host_id: int) -> list[str]:
        """Retrieves preferred pronouns for a host.

        :param host_id: Host ID
        :return: A list of preferred pronouns.
        """
        if not valid_int_id(host_id):
            return []

        query = """
            SELECT pn.pronouns
            FROM ww_hostpronounsmap hpm
            JOIN ww_pronouns pn on pn.pronounsid = hpm.pronounsid
            WHERE hpm.hostid = %s
            ORDER BY hpm.hostpronounsmapid ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (host_id,))
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [result["pronouns"] for result in results]

    def retrieve_pronouns_by_slug(self, host_slug: str) -> list[str]:
        """Retrieves preferred pronouns for a host.

        :param host_slug: Host slug string
        :return: A list of preferred pronouns.
        """
        _id = self.utility.convert_slug_to_id(host_slug)
        if not _id:
            return {}

        return self.retrieve_pronouns_by_id(_id)

    def retrieve_random(self) -> dict[str, Any]:
        """Retrieves information for a random host.

        :return: A dictionary containing host ID, name, gender and slug
            string
        """
        _id = self.retrieve_random_id()

        if not _id:
            return None

        return self.retrieve_by_id(_id)

    def retrieve_random_details(self) -> dict[str, Any]:
        """Retrieves information and appearances for a random host.

        :return: A dictionary containing host ID, name, slug string,
            gender, pronouns, whether the host is also a guest, host or
            scorekeeper, and a list of appearances with show flags
        """
        _id = self.retrieve_random_id()

        if not _id:
            return None

        return self.retrieve_details_by_id(_id)

    def retrieve_external_sites_by_id(self, host_id: int) -> list[dict[str, str]]:
        """Retrieves external site information for a host.

        :param host_id: Host ID
        :return: A list of dictionaries containing external site
            information, including social media accounts.
        """
        if not valid_int_id(host_id):
            return []

        query = """
            SELECT es.site, es.siteslug, es.iconname, es.socialmedia,
            hsm.url, hsm.account
            FROM ww_hostextsitesmap hsm
            JOIN ww_externalsites es ON es.siteid = hsm.siteid
            WHERE hsm.hostid = %s
            ORDER BY es.site ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (host_id,))
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
                    "url": row["url"],
                    "account": row["account"],
                }
            )

        return accounts

    def retrieve_external_sites_by_slug(self, host_slug: str) -> list[dict[str, str]]:
        """Retrieves external site information for a host.

        :param host_slug: Host slug string
        :return: A list of dictionaries containing external site
            information, including social media accounts.
        """
        _id = self.utility.convert_slug_to_id(host_slug)
        if not _id:
            return {}

        return self.retrieve_external_sites_by_id(_id)

    def retrieve_social_media_accounts_by_id(
        self, host_id: int
    ) -> list[dict[str, str]]:
        """*Deprecated:* Retrieves social media accounts for a host.

        :param host_id: Host ID
        :return: A list of dictionaries containing social media
            account information.
        """
        warnings.warn(
            message="This method has been deprecated. Use 'Host.retrieve_external_accounts_by_id()' instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )

        if not valid_int_id(host_id):
            return []

        query = """
            SELECT es.site, es.siteslug, es.iconname, hsm.url, hsm.account
            FROM ww_hostextsitesmap hsm
            JOIN ww_externalsites es ON es.siteid = hsm.siteid
            WHERE hsm.hostid = %s AND es.socialmedia = 1
            ORDER BY es.site ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (host_id,))
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
        self, host_slug: str
    ) -> list[dict[str, str]]:
        """*Deprecated:* Retrieves social media accounts for a host.

        :param host_slug: Host slug string
        :return: A list of dictionaries containing social media
            account information.
        """
        warnings.warn(
            message="This method has been deprecated. Use 'Host.retrieve_external_accounts_by_slug()' instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )

        _id = self.utility.convert_slug_to_id(host_slug)
        if not _id:
            return {}

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return self.retrieve_social_media_accounts_by_id(_id)
