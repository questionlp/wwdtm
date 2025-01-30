# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing for object: :py:module:`wwdtm`."""

import json
from pathlib import Path
from typing import Any

import pytest

from wwdtm import database_version


@pytest.mark.skip
def get_connect_dict() -> dict[str, Any]:
    """Retrieves database connection settings.

    :return: A dictionary containing database connection
        settings as required by MySQL Connector/Python
    """
    file_path = Path.cwd() / "config.json"
    with file_path.open(mode="r", encoding="utf-8") as config_file:
        config_dict = json.load(config_file)
        if "database" in config_dict:
            return config_dict["database"]

    return None


def test_database_version():
    """Testing for :py:func:`wwdtm.database_version`."""
    _database_version = database_version(connect_dict=get_connect_dict())

    assert isinstance(_database_version, tuple), (
        "Invalid database version value type returned"
    )

    if isinstance(_database_version, tuple):
        assert len(_database_version) == 2 or len(_database_version) == 3, (
            "Invalid database version value returned"
        )
