# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing for object: :py:class:`wwdtm.scorekeeper.ScorekeeperAppearances`."""

import json
from pathlib import Path
from typing import Any

import pytest

from wwdtm.scorekeeper import ScorekeeperAppearances


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


@pytest.mark.parametrize("scorekeeper_id", [13])
def test_scorekeeper_appearance_retrieve_appearances_by_id(scorekeeper_id: int):
    """Testing for :py:meth:`wwdtm.scorekeeper.ScorekeeperAppearances.retrieve_appearances_by_id`.

    :param scorekeeper_id: Scorekeeper ID to test retrieving scorekeeper
        appearances
    """
    appearances = ScorekeeperAppearances(connect_dict=get_connect_dict())
    appearance = appearances.retrieve_appearances_by_id(scorekeeper_id)

    assert "count" in appearance, f"'count' was not returned for ID {scorekeeper_id}"
    assert "shows" in appearance, f"'shows' was not returned for ID {scorekeeper_id}"


@pytest.mark.parametrize("scorekeeper_slug", ["chioke-i-anson"])
def test_scorekeeper_appearance_retrieve_appearances_by_slug(scorekeeper_slug: str):
    """Testing for :py:meth:`wwdtm.scorekeeper.ScorekeeperAppearances.retrieve_appearances_by_slug`.

    :param scorekeeper_slug: Scorekeeper slug string to test retrieving
        scorekeeper appearances
    """
    appearances = ScorekeeperAppearances(connect_dict=get_connect_dict())
    appearance = appearances.retrieve_appearances_by_slug(scorekeeper_slug)

    assert "count" in appearance, (
        f"'count' was not returned for slug {scorekeeper_slug}"
    )
    assert "shows" in appearance, (
        f"'shows' was not returned for slug {scorekeeper_slug}"
    )
