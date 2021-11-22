# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
"""Wait Wait Don't Tell Me! Stats Host Data Retrieval Functions
"""
from functools import lru_cache
from typing import Any, Dict, List, Optional

from mysql.connector import connect
from slugify import slugify
from wwdtm.host.appearances import HostAppearances
from wwdtm.host.utility import HostUtility
from wwdtm.validation import valid_int_id


class Host:
    """This class contains functions used to retrieve host data from a
    copy of the Wait Wait Stats database.

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

        self.appearances = HostAppearances(database_connection=self.database_connection)
        self.utility = HostUtility(database_connection=self.database_connection)

    def retrieve_all(self) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing host ID,
        name and slug string for all hosts.

        :return: List of all hosts and their corresponding information.
            If hosts could not be retrieved, an empty list is returned.
        :rtype: List[Dict[str, Any]]
        """
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT hostid AS id, host, hostslug AS slug, "
                 "hostgender AS gender "
                 "FROM ww_hosts "
                 "WHERE hostslug != 'tbd' "
                 "ORDER BY host ASC;")
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        hosts = []
        for row in results:
            host = {
                "id": row["id"],
                "name": row["host"],
                "slug": row["slug"] if row["slug"] else slugify(row["host"]),
                "gender": row["gender"],
            }

            hosts.append(host)

        return hosts

    def retrieve_all_details(self) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing host ID,
        name, slug string and appearance information for all hosts.

        :return: List of all hosts and their corresponding information
            and appearances. If hosts could not be retrieved, an empty
            list is returned.
        :rtype: List[Dict[str, Any]]
        """
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT hostid AS id, host, hostslug AS slug, "
                 "hostgender AS gender "
                 "FROM ww_hosts "
                 "WHERE hostslug != 'tbd' "
                 "ORDER BY host ASC;")
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        hosts = []
        for row in results:
            appearances = self.appearances.retrieve_appearances_by_id(row["id"])
            host = {
                "id": row["id"],
                "name": row["host"],
                "slug": row["slug"] if row["slug"] else slugify(row["host"]),
                "gender": row["gender"],
                "appearances": appearances,
            }

            hosts.append(host)

        return hosts

    def retrieve_all_ids(self) -> List[int]:
        """Returns a list of all host IDs from the database, sorted by
        host name.

        :return: List of all host IDs. If host IDs could not be
            retrieved, an empty list is returned.
        :rtype: List[int]
        """
        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT hostid FROM ww_hosts "
                 "WHERE hostslug != 'tbd' "
                 "ORDER BY host ASC;")
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return []

        ids = []
        for row in result:
            ids.append(row[0])

        return ids

    def retrieve_all_slugs(self) -> List[str]:
        """Returns a list of all host slug strings from the database,
        sorted by host name.

        :return: List of all host slug strings. If host slug strings
            could not be retrieved, an empty list is returned.
        :rtype: List[str]
        """
        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT hostslug FROM ww_hosts "
                 "WHERE hostslug != 'tbd' "
                 "ORDER BY host ASC;")
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return []

        ids = []
        for row in result:
            ids.append(row[0])

        return ids

    @lru_cache(typed=True)
    def retrieve_by_id(self, host_id: int) -> Dict[str, Any]:
        """Returns a dictionary object containing host ID, name and
        slug string for the requested host ID.

        :param host_id: Host ID
        :type host_id: int
        :return: Dictionary containing host information. If host
            information could not be retrieved, an empty dictionary is
            returned.
        :rtype: Dict[str, Any]
        """
        if not valid_int_id(host_id):
            return {}

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT hostid AS id, host, hostslug AS slug, "
                 "hostgender AS gender "
                 "FROM ww_hosts "
                 "WHERE hostid = %s "
                 "LIMIT 1;")
        cursor.execute(query, (host_id, ))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return {}

        info = {
            "id": result["id"],
            "name": result["host"],
            "slug": result["slug"] if result["slug"] else slugify(result["host"]),
            "gender": result["gender"],
        }

        return info

    @lru_cache(typed=True)
    def retrieve_by_slug(self, host_slug: str) -> Dict[str, Any]:
        """Returns a dictionary object containing host ID, name and
        slug string for the requested host slug string.

        :param host_slug: Host slug string
        :type host_slug: str
        :return: Dictionary containing host information. If host
            information could be retrieved, an empty dictionary is
            returned.
        :rtype: Dict[str, Any]
        """
        try:
            slug = host_slug.strip()
            if not slug:
                return {}
        except AttributeError:
            return {}

        id_ = self.utility.convert_slug_to_id(slug)
        if not id_:
            return {}

        return self.retrieve_by_id(id_)

    @lru_cache(typed=True)
    def retrieve_details_by_id(self, host_id: int) -> Dict[str, Any]:
        """Returns a dictionary object containing host ID, name, slug
        string and appearance information for the requested host ID.

        :param host_id: Host ID
        :type host_id: int
        :return: Dictionary containing host information and their
            appearances. If host information could be retrieved, an
            empty dictionary is returned.
        :rtype: Dict[str, Any]
        """
        if not valid_int_id(host_id):
            return {}

        info = self.retrieve_by_id(host_id)
        if not info:
            return {}

        info["appearances"] = self.appearances.retrieve_appearances_by_id(host_id)

        return info

    @lru_cache(typed=True)
    def retrieve_details_by_slug(self, host_slug: str) -> Dict[str, Any]:
        """Returns a dictionary object containing host ID, name, slug
        string and appearance information for the requested host slug
        string.

        :param host_slug: Host slug string
        :type host_slug: str
        :return: Dictionary containing host information and their
            appearances. If host information could be retrieved, an
            empty dictionary is returned.
        :rtype: Dict[str, Any]
        """
        try:
            slug = host_slug.strip()
            if not slug:
                return {}
        except AttributeError:
            return {}

        id_ = self.utility.convert_slug_to_id(slug)
        if not id_:
            return {}

        return self.retrieve_details_by_id(id_)
