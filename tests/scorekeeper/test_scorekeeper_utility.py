# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing for object: :py:class:`wwdtm.scorekeeper.ScorekeeperUtility`."""

import json
from pathlib import Path
from typing import Any

import pytest

from wwdtm.scorekeeper import ScorekeeperUtility


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


@pytest.mark.parametrize("scorekeeper_id", [2])
def test_scorekeeper_utility_convert_id_to_slug(scorekeeper_id: int):
    """Testing for :py:meth:`wwdtm.scorekeeper.ScorekeeperUtility.convert_id_to_slug`.

    :param scorekeeper_id: Scorekeeper ID to test converting into
        scorekeeper slug string
    """
    utility = ScorekeeperUtility(connect_dict=get_connect_dict())
    slug = utility.convert_id_to_slug(scorekeeper_id)

    assert slug, f"Scorekeeper slug for ID {scorekeeper_id} was not found"
    assert isinstance(slug, str), f"Invalid value returned for ID {scorekeeper_id}"


@pytest.mark.parametrize("scorekeeper_id", [-1])
def test_scorekeeper_utility_convert_invalid_id_to_slug(scorekeeper_id: int):
    """Negative testing for :py:meth:`wwdtm.scorekeeper.ScorekeeperUtility.convert_id_to_slug`.

    :param scorekeeper_id: Scorekeeper ID to test failing to convert
        into scorekeeper slug string
    """
    utility = ScorekeeperUtility(connect_dict=get_connect_dict())
    slug = utility.convert_id_to_slug(scorekeeper_id)

    assert not slug, f"Scorekeeper slug for ID {scorekeeper_id} was found"


@pytest.mark.parametrize("scorekeeper_slug", ["korva-coleman"])
def test_scorekeeper_utility_convert_slug_to_id(scorekeeper_slug: str):
    """Testing for :py:meth:`wwdtm.scorekeeper.ScorekeeperUtility.convert_slug_to_id`.

    :param scorekeeper_slug: Scorekeeper slug string to test converting
        into scorekeeper ID
    """
    utility = ScorekeeperUtility(connect_dict=get_connect_dict())
    id_ = utility.convert_slug_to_id(scorekeeper_slug)

    assert id_, f"Scorekeeper ID for slug {scorekeeper_slug} was found"
    assert isinstance(id_, int), f"Invalid value returned for slug {scorekeeper_slug}"


@pytest.mark.parametrize("scorekeeper_slug", ["corva-coleman"])
def test_scorekeeper_utility_convert_invalid_slug_to_id(scorekeeper_slug: str):
    """Negative testing for :py:meth:`wwdtm.scorekeeper.ScorekeeperUtility.convert_slug_to_id`.

    :param scorekeeper_slug: Scorekeeper slug string to test failing to
        convert into scorekeeper ID
    """
    utility = ScorekeeperUtility(connect_dict=get_connect_dict())
    id_ = utility.convert_slug_to_id(scorekeeper_slug)

    assert not id_, f"Scorekeeper ID for slug {scorekeeper_slug} was not found"


@pytest.mark.parametrize("scorekeeper_id", [2])
def test_scorekeeper_utility_id_exists(scorekeeper_id: int):
    """Testing for :py:meth:`wwdtm.scorekeeper.ScorekeeperUtility.id_exists`.

    :param scorekeeper_id: Scorekeeper ID to test if a scorekeeper
        exists
    """
    utility = ScorekeeperUtility(connect_dict=get_connect_dict())
    result = utility.id_exists(scorekeeper_id)

    assert result, f"Scorekeeper ID {scorekeeper_id} does not exist"


@pytest.mark.parametrize("scorekeeper_id", [-1])
def test_scorekeeper_utility_id_not_exists(scorekeeper_id: int):
    """Negative testing for :py:meth:`wwdtm.scorekeeper.ScorekeeperUtility.id_exists`.

    :param scorekeeper_id: Scorekeeper ID to test if a scorekeeper does
        not exist
    """
    utility = ScorekeeperUtility(connect_dict=get_connect_dict())
    result = utility.id_exists(scorekeeper_id)

    assert not result, f"Scorekeeper ID {scorekeeper_id} exists"


@pytest.mark.parametrize("scorekeeper_slug", ["korva-coleman"])
def test_scorekeeper_utility_slug_exists(scorekeeper_slug: str):
    """Testing for :py:meth:`wwdtm.scorekeeper.ScorekeeperUtility.slug_exists`.

    :param scorekeeper_slug: Scorekeeper slug string to test if a
        scorekeeper exists
    """
    utility = ScorekeeperUtility(connect_dict=get_connect_dict())
    result = utility.slug_exists(scorekeeper_slug)

    assert result, f"Scorekeeper slug {scorekeeper_slug} does not exist"


@pytest.mark.parametrize("scorekeeper_slug", ["corva-coleman"])
def test_scorekeeper_utility_slug_not_exists(scorekeeper_slug: str):
    """Negative testing for :py:meth:`wwdtm.scorekeeper.ScorekeeperUtility.slug_exists`.

    :param scorekeeper_slug: Scorekeeper slug string to test if a
        scorekeeper does not exist
    """
    utility = ScorekeeperUtility(connect_dict=get_connect_dict())
    result = utility.slug_exists(scorekeeper_slug)

    assert not result, f"Scorekeeper slug {scorekeeper_slug} exists"
