# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2026 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
"""Testing for object: :py:class:`wwdtm.validation`."""

import json
from pathlib import Path
from typing import Any

import pytest
from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from wwdtm.validation import check_database_version, valid_int_id


@pytest.mark.skip
def get_connect_dict() -> dict[str, Any]:
    """Retrieves database connection settings.

    :return: A dictionary containing database connection
        settings as required by MySQL Connector/Python
    """
    file_path: Path = Path.cwd() / "config.json"
    with file_path.open(mode="r", encoding="utf-8") as config_file:
        config_dict: dict[str, Any] = json.load(config_file)
        if "database" in config_dict:
            return config_dict["database"]


@pytest.mark.skip
def get_database_connection() -> MySQLConnection | PooledMySQLConnection:
    """Creates a database connection object.

    :return: MySQL database connection object
    """
    connect_dict: dict[str, Any] = get_connect_dict()
    return connect(**connect_dict)


def test_validation_check_database_version_connect_dict():
    """Testing for :py:meth:`wwdtm.validation.check_database_version` with connect_dict."""
    _connect_dict: dict[str, Any] = get_connect_dict()
    _database_version_check = check_database_version(connect_dict=_connect_dict)

    assert _database_version_check, "Minimum database version not met or validated"


def test_validation_check_database_version_connection():
    """Testing for :py:meth:`wwdtm.validation.check_database_version` with database connection."""
    _database_connection = get_database_connection()
    _database_version_check = check_database_version(
        database_connection=_database_connection
    )

    assert _database_version_check, "Minimum database version not met or validated"


def test_validation_check_database_version_no_parameters():
    """Testing for :py:meth:`wwdtm.validation.check_database_version` without parameters."""
    _database_version_check = check_database_version()

    assert not _database_version_check, "Invalid database version check result returned"


@pytest.mark.parametrize("test_id", [54, 32767])
def test_validation_valid_int_id(test_id: int):
    """Testing for :py:meth:`wwdtm.validation.valid_int_id`.

    :param test_id: ID to test ID validation
    """
    assert valid_int_id(test_id), f"Provided ID {test_id} was not valid"


@pytest.mark.parametrize("test_id", [-54, 2**32, "hello", False])
def test_validation_invalid_int_id(test_id: int):
    """Negative testing for :py:meth:`wwdtm.validation.valid_int_id`.

    :param test_id: ID to test failing ID validation
    """
    assert not valid_int_id(test_id), f"Provided ID {test_id} was valid"


def test_validation_no_id():
    """Negative testing for :py:meth:`wwdtm.validation.valid_int_id`."""
    assert not valid_int_id(None), "Provided ID 'None' was valid"
