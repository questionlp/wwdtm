# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
"""Testing for object: :py:class:`wwdtm.scorekeeper.Scorekeeper`
"""
import json
from typing import Any, Dict

import pytest
from wwdtm.scorekeeper import Scorekeeper


@pytest.mark.skip
def get_connect_dict() -> Dict[str, Any]:
    """Read in database connection settings and return values as a
    dictionary.
    """
    with open("config.json", "r") as config_file:
        config_dict = json.load(config_file)
        if "database" in config_dict:
            return config_dict["database"]


@pytest.mark.parametrize("exclude_nulls", [True, False])
def test_scorekeeper_retrieve_all(exclude_nulls: bool):
    """Testing for :py:meth:`wwdtm.scorekeeper.Scorekeeper.retrieve_all`

    :param exclude_nulls: Toggle whether to exclude results that have
        SQL ``NULL`` for the scorekeeper name
    """
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    scorekeepers = scorekeeper.retrieve_all(exclude_nulls)

    assert scorekeepers, "No scorekeepers could be retrieved"
    assert "id" in scorekeepers[0], "'id' was not returned for the first list item"


@pytest.mark.parametrize("exclude_nulls", [True, False])
def test_scorekeeper_retrieve_all_details(exclude_nulls: bool):
    """Testing for :py:meth:`wwdtm.scorekeeper.Scorekeeper.retrieve_all_details`

    :param exclude_nulls: Toggle whether to exclude results that have
        SQL ``NULL`` value for the scorekeeper name and show dates
    """
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    scorekeepers = scorekeeper.retrieve_all_details(exclude_nulls)

    assert scorekeepers, "No scorekeepers could be retrieved"
    assert "id" in scorekeepers[0], "'id' was not returned for first list item"
    assert "appearances" in scorekeepers[0], ("'appearances' was not returned "
                                              "for the first list item")


def test_scorekeeper_retrieve_all_ids():
    """Testing for :py:meth:`wwdtm.scorekeeper.Scorekeeper.retrieve_all_ids`
    """
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    ids = scorekeeper.retrieve_all_ids()

    assert ids, "No scorekeeper IDs could be retrieved"


def test_scorekeeper_retrieve_all_slugs():
    """Testing for :py:meth:`wwdtm.scorekeeper.Scorekeeper.retrieve_all_slugs`
    """
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    slugs = scorekeeper.retrieve_all_slugs()

    assert slugs, "No scorekeeper slug strings could be retrieved"


@pytest.mark.parametrize("scorekeeper_id, exclude_null",
                         [(13, True), (13, False)])
def test_scorekeeper_retrieve_by_id(scorekeeper_id: int, exclude_null: bool):
    """Testing for :py:meth:`wwdtm.scorekeeper.Scorekeeper.retrieve_by_id`

    :param scorekeeper_id: Scorekeeper ID to test retrieving scorekeeper
        information
    :param exclude_null: Toggle whether to exclude results that have
        SQL ``NULL`` for the scorekeeper name
    """
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    info = scorekeeper.retrieve_by_id(scorekeeper_id, exclude_null)

    assert info, f"Scorekeeper ID {scorekeeper_id} not found"
    assert "name" in info, f"'name' was not returned for ID {scorekeeper_id}"


@pytest.mark.parametrize("scorekeeper_id, exclude_null",
                         [(13, True), (13, False)])
def test_scorekeeper_retrieve_details_by_id(scorekeeper_id: int,
                                            exclude_null: bool):
    """Testing for :py:meth:`wwdtm.scorekeeper.Scorekeeper.retrieve_details_by_id`

    :param scorekeeper_id: Scorekeeper ID to test retrieving scorekeeper
        details
    :param exclude_null: Toggle whether to exclude results that have
        SQL ``NULL`` for the scorekeeper name and show dates
    """
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    info = scorekeeper.retrieve_details_by_id(scorekeeper_id, exclude_null)

    assert info, f"Scorekeeper ID {scorekeeper_id} not found"
    assert "name" in info, f"'name' was not returned for ID {scorekeeper_id}"
    assert "appearances" in info, f"'appearances' was not returned for ID {scorekeeper_id}"


@pytest.mark.parametrize("scorekeeper_slug, exclude_null",
                         [("chioke-i-anson", True), ("chioke-i-anson", False)])
def test_scorekeeper_retrieve_by_slug(scorekeeper_slug: str,
                                      exclude_null: bool):
    """Testing for :py:meth:`wwdtm.scorekeeper.Scorekeeper.retrieve_by_slug`

    :param scorekeeper_slug: Scorekeeper slug string to test retrieving
        scorekeeper information
    :param exclude_null: Toggle whether to exclude results that have
        SQL ``NULL`` for the scorekeeper name
    """
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    info = scorekeeper.retrieve_by_slug(scorekeeper_slug, exclude_null)

    assert info, f"Scorekeeper slug {scorekeeper_slug} not found"
    assert "name" in info, f"'name' was not returned for slug {scorekeeper_slug}"


@pytest.mark.parametrize("scorekeeper_slug, exclude_null",
                         [("chioke-i-anson", True), ("chioke-i-anson", False)])
def test_scorekeeper_retrieve_details_by_slug(scorekeeper_slug: str,
                                              exclude_null: bool):
    """Testing for :py:meth:`wwdtm.scorekeeper.Scorekeeper.retrieve_details_by_slug`

    :param scorekeeper_slug: Scorekeeper slug string to test retrieving
        scorekeeper details
    :param exclude_null: Toggle whether to exclude results that have
        SQL ``NULL`` for the scorekeeper name and show dates
    """
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    info = scorekeeper.retrieve_details_by_slug(scorekeeper_slug, exclude_null)

    assert info, f"Scorekeeper slug {scorekeeper_slug} not found"
    assert "name" in info, f"'name' was not returned for slug {scorekeeper_slug}"
    assert "appearances" in info, f"'appearances' was not returned for slug {scorekeeper_slug}"
