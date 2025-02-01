# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Stats Guest Data Retrieval Functions."""

from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from slugify import slugify

from wwdtm.guest.appearances import GuestAppearances
from wwdtm.guest.utility import GuestUtility
from wwdtm.validation import valid_int_id


class Guest:
    """Guest information retrieval class.

    Contains methods used to retrieve Not My Job guest information,
    including IDs, names, slug strings, appearances and scores.

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

        self.appearances = GuestAppearances(
            database_connection=self.database_connection
        )
        self.utility = GuestUtility(database_connection=self.database_connection)

    def retrieve_all(self) -> list[dict[str, int | str]]:
        """Retrieves guest information for all guests.

        :return: A list of dictionaries containing guest ID, name and
            slug string for each guest
        """
        query = """
            SELECT guestid AS id, guest AS name, guestslug AS slug
            FROM ww_guests
            WHERE guestslug != 'none'
            ORDER BY guest ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        guests = []
        for row in results:
            guests.append(
                {
                    "id": row["id"],
                    "name": row["name"],
                    "slug": row["slug"] if row["slug"] else slugify(row["name"]),
                }
            )

        return guests

    def retrieve_all_details(self) -> list[dict[str, Any]]:
        """Retrieves guest information and appearances for all guests.

        :return: A list of dictionaries containing guest ID, name, slug
            string, and a list of appearances with show flags, scores
            and scoring exceptions
        """
        query = """
            SELECT guestid AS id, guest AS name, guestslug AS slug
            FROM ww_guests
            WHERE guestslug != 'none'
            ORDER BY guest ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        guests = []
        for row in results:
            guests.append(
                {
                    "id": row["id"],
                    "name": row["name"],
                    "slug": row["slug"] if row["slug"] else slugify(row["name"]),
                    "appearances": self.appearances.retrieve_appearances_by_id(
                        row["id"]
                    ),
                }
            )

        return guests

    def retrieve_all_ids(self) -> list[int]:
        """Retrieves all guest IDs, sorted by guest name.

        :return: A list of guest IDs as integers
        """
        query = """
            SELECT guestid FROM ww_guests
            WHERE guestslug != 'none'
            ORDER BY guest ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [v[0] for v in results]

    def retrieve_all_slugs(self) -> list[str]:
        """Retrieves all guest slug strings, sorted by guest name.

        :return: A list of guest slug strings
        """
        query = """
            SELECT guestslug FROM ww_guests
            WHERE guestslug != 'none'
            ORDER BY guest ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [v[0] for v in results]

    def retrieve_by_id(self, guest_id: int) -> dict[str, int | str]:
        """Retrieves guest information.

        :param guest_id: Guest ID
        :return: A dictionary containing guest ID, name and slug string
        """
        if not valid_int_id(guest_id):
            return {}

        query = """
            SELECT guestid AS id, guest AS name, guestslug AS slug
            FROM ww_guests
            WHERE guestid = %s
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (guest_id,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return {}

        return {
            "id": result["id"],
            "name": result["name"],
            "slug": result["slug"] if result["slug"] else slugify(result["name"]),
        }

    def retrieve_by_slug(self, guest_slug: str) -> dict[str, int | str]:
        """Retrieves guest information.

        :param guest_slug: Guest slug string
        :return: A dictionary containing guest ID, name and slug string
        """
        try:
            slug = guest_slug.strip()
            if not slug:
                return {}
        except AttributeError:
            return {}

        id_ = self.utility.convert_slug_to_id(slug)
        if not id_:
            return {}

        return self.retrieve_by_id(id_)

    def retrieve_details_by_id(self, guest_id: int) -> dict[str, Any]:
        """Retrieves guest information and appearances.

        :param guest_id: Guest ID
        :return: A dictionary containing guest ID, name, slug string,
            list of appearances with show flags, scores and scoring
            exceptions
        """
        if not valid_int_id(guest_id):
            return {}

        info = self.retrieve_by_id(guest_id)
        if not info:
            return {}

        info["appearances"] = self.appearances.retrieve_appearances_by_id(guest_id)

        return info

    def retrieve_details_by_slug(self, guest_slug: str) -> dict[str, Any]:
        """Retrieves guest information and appearances.

        :param guest_slug: Guest slug string
        :return: A dictionary containing guest ID, name, slug string,
            list of appearances with show flags, scores and scoring
            exceptions
        """
        try:
            slug = guest_slug.strip()
            if not slug:
                return {}
        except AttributeError:
            return {}

        id_ = self.utility.convert_slug_to_id(slug)
        if not id_:
            return {}

        return self.retrieve_details_by_id(id_)

    def retrieve_random_id(self) -> int:
        """Retrieves an ID for a random guest.

        :return: ID for a random guest.
        """
        query = """
            SELECT guestid FROM ww_guests
            WHERE guestslug <> 'none'
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
        """Retrieves an slug string for a random guest.

        :return: Slug string for a random guest.
        """
        query = """
            SELECT guestslug FROM ww_guests
            WHERE guestslug <> 'none'
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

    def retrieve_random(self) -> dict[str, int | str]:
        """Retrieves information for a random guest.

        :return: A dictionary containing guest ID, name and slug string
        """
        _id = self.retrieve_random_id()

        if not _id:
            return None

        return self.retrieve_by_id(guest_id=_id)

    def retrieve_random_details(self) -> dict[str, Any]:
        """Retrieves information and appearances for a random guest.

        :return: A dictionary containing guest ID, name, slug string,
            list of appearances with show flags, scores and scoring
            exceptions
        """
        _id = self.retrieve_random_id()

        if not _id:
            return None

        return self.retrieve_details_by_id(guest_id=_id)
