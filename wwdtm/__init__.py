# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Explicitly listing all modules in this package."""

from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from wwdtm import validation
from wwdtm.guest import Guest, GuestAppearances, GuestUtility
from wwdtm.host import Host, HostAppearances, HostUtility
from wwdtm.location import Location, LocationRecordings, LocationUtility
from wwdtm.panelist import (
    Panelist,
    PanelistAppearances,
    PanelistDecimalScores,
    PanelistScores,
    PanelistStatistics,
    PanelistUtility,
)
from wwdtm.scorekeeper import Scorekeeper, ScorekeeperAppearances, ScorekeeperUtility
from wwdtm.show import Show, ShowInfo, ShowInfoMultiple, ShowUtility

VERSION = "2.18.0"


def database_version(
    connect_dict: dict[str, Any] = None,
    database_connection: MySQLConnection | PooledMySQLConnection = None,
) -> tuple[int] | None:
    """Returns Stats Database version, if available.

    :param connect_dict: A dictionary containing database connection
        settings as required by MySQL Connector/Python
    :param database_connection: MySQL database connection object
    :return: A tuple containg major, minor and revision numbers if
        available. If a version number is not available, None is
        returned.
    """
    if connect_dict:
        _connect_dict = connect_dict
        _database_connection = connect(**_connect_dict)
    elif database_connection:
        _database_connection = database_connection
        if not _database_connection.is_connected():
            _database_connection.reconnect()

    cursor = _database_connection.cursor(dictionary=True)
    query = """
            SELECT keyname, value
            FROM __metadata
            WHERE keyname = 'database_version'
            ORDER BY id DESC LIMIT 1;
            """
    cursor.execute(query)
    result = cursor.fetchone()

    if not result:
        return None

    version_info = str(result["value"]).split(".")
    if len(version_info) == 3:
        return int(version_info[0]), int(version_info[1]), int(version_info[2])
    elif len(version_info) == 2:
        return int(version_info[0]), int(version_info[1]), 0

    return None
