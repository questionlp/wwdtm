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

from wwdtm.validation import check_database_version, valid_int_id, valid_rounding_digits


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


@pytest.mark.parametrize("number_digits", [0, 1, 2, 5, 10, 20])
def test_validation_valid_rounding_digits(number_digits: int):
    """Testing for :py:meth:`wwdtm.validation.valid_rounding_digits`.

    :param number_digits: Number of rounding digits to validate
    """
    assert valid_rounding_digits(number_digits=number_digits)


@pytest.mark.parametrize(
    "number_digits, min_digits", [(0, 0), (5, 1), (10, 5), (20, 10)]
)
def test_validation_valid_rounding_digits_with_min(number_digits: int, min_digits: int):
    """Testing for :py:meth:`wwdtm.validation.valid_rounding_digits`.

    :param number_digits: Number of rounding digits to validate
    :param min_digits: Minimum of rounding digits
    """
    assert valid_rounding_digits(number_digits=number_digits, min_digits=min_digits)


@pytest.mark.parametrize(
    "number_digits, max_digits", [(0, 0), (1, 5), (5, 10), (10, 20)]
)
def test_validation_valid_rounding_digits_with_max(number_digits: int, max_digits: int):
    """Testing for :py:meth:`wwdtm.validation.valid_rounding_digits`.

    :param number_digits: Number of rounding digits to validate
    :param max_digits: Maximum of rounding digits
    """
    assert valid_rounding_digits(number_digits=number_digits, max_digits=max_digits)


@pytest.mark.parametrize(
    "number_digits, min_digits, max_digits",
    [(0, 0, 1), (1, 0, 5), (5, 2, 10), (10, 2, 20)],
)
def test_validation_valid_rounding_digits_with_min_max(
    number_digits: int, min_digits: int, max_digits: int
):
    """Testing for :py:meth:`wwdtm.validation.valid_rounding_digits`.

    :param number_digits: Number of rounding digits to validate
    :param min_digits: Minimum of rounding digits
    :param max_digits: Maximum of rounding digits
    """
    assert valid_rounding_digits(
        number_digits=number_digits, min_digits=min_digits, max_digits=max_digits
    )
