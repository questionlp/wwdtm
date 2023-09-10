# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2023 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
"""Testing for object: :py:class:`wwdtm.panelist.PanelistStatistics`
"""
import json
from typing import Any, Dict

import pytest
from wwdtm.panelist import PanelistStatistics


@pytest.mark.skip
def get_connect_dict() -> Dict[str, Any]:
    """Read in database connection settings and return values as a
    dictionary.

    :return: A dictionary containing database connection settings
        for use by mysql.connector
    """
    with open("config.json", "r", encoding="utf-8") as config_file:
        config_dict = json.load(config_file)
        if "database" in config_dict:
            return config_dict["database"]


@pytest.mark.parametrize("panelist_id", [14])
def test_panelist_statistics_retrieve_bluffs_by_id(panelist_id: int):
    """Testing for :py:meth:`wwdtm.panelist.PanelistStatistics.retrieve_bluffs_by_id`

    :param panelist_id: Panelist ID to test retrieving panelist
        information
    """
    statistics = PanelistStatistics(connect_dict=get_connect_dict())
    bluffs = statistics.retrieve_bluffs_by_id(panelist_id)

    assert "chosen" in bluffs, f"'chosen' was not returned for ID {panelist_id}"
    assert "correct" in bluffs, f"'correct' was not returned for ID {panelist_id}"


@pytest.mark.parametrize("panelist_slug", ["luke-burbank"])
def test_panelist_statistics_retrieve_bluffs_by_slug(panelist_slug: str):
    """Testing for :py:meth:`wwdtm.panelist.PanelistStatistics.retrieve_bluffs_by_slug`

    :param panelist_slug: Panelist slug string to test retrieving
        panelist information
    """
    statistics = PanelistStatistics(connect_dict=get_connect_dict())
    bluffs = statistics.retrieve_bluffs_by_slug(panelist_slug)

    assert "chosen" in bluffs, f"'chosen' was not returned for slug {panelist_slug}"
    assert "correct" in bluffs, f"'correct' was not returned for slug {panelist_slug}"


@pytest.mark.parametrize("panelist_id", [14])
def test_panelist_statistics_retrieve_rank_info_by_id(panelist_id: int):
    """Testing for :py:meth:`wwdtm.panelist.PanelistStatistics.retrieve_rank_info_by_id`

    :param panelist_id: Panelist ID to test retrieving panelist
        information
    """
    statistics = PanelistStatistics(connect_dict=get_connect_dict())
    ranks = statistics.retrieve_rank_info_by_id(panelist_id)

    assert "first" in ranks, f"'first' was not returned for ID {panelist_id}"


@pytest.mark.parametrize("panelist_slug", ["luke-burbank"])
def test_panelist_statistics_retrieve_rank_info_by_slug(panelist_slug: str):
    """Testing for :py:meth:`wwdtm.panelist.PanelistStatistics.retrieve_rank_info_by_slug`

    :param panelist_slug: Panelist slug string to test retrieving
        panelist information
    """
    statistics = PanelistStatistics(connect_dict=get_connect_dict())
    ranks = statistics.retrieve_rank_info_by_slug(panelist_slug)

    assert "first" in ranks, f"'first' was not returned for slug {panelist_slug}"


@pytest.mark.parametrize(
    "panelist_id, include_decimal_scores", [(14, True), (14, False)]
)
def test_panelist_statistics_retrieve_statistics_by_id(
    panelist_id: int, include_decimal_scores: bool
):
    """Testing for :py:meth:`wwdtm.panelist.PanelistStatistics.retrieve_statistics_by_id`

    :param panelist_id: Panelist ID to test retrieving panelist
        information
    :param include_decimal_scores: Flag set to include decimal score columns
        and values
    """
    statistics = PanelistStatistics(connect_dict=get_connect_dict())
    stats = statistics.retrieve_statistics_by_id(
        panelist_id, include_decimal_scores=include_decimal_scores
    )

    assert "scoring" in stats, f"'scoring' was not returned for ID {panelist_id}"
    if include_decimal_scores:
        assert (
            "scoring_decimal" in stats
        ), f"'scoring' was not returned for ID {panelist_id}"
    assert "ranking" in stats, f"'ranking' was not returned for ID {panelist_id}"


@pytest.mark.parametrize(
    "panelist_slug, include_decimal_scores",
    [("luke-burbank", True), ("luke-burbank", False)],
)
def test_panelist_statistics_retrieve_statistics_by_slug(
    panelist_slug: str, include_decimal_scores: bool
):
    """Testing for :py:meth:`wwdtm.panelist.PanelistStatistics.retrieve_statistics_by_slug`

    :param panelist_slug: Panelist slug string to test retrieving
        panelist information
    :param include_decimal_scores: Flag set to include decimal score columns
        and values
    """
    statistics = PanelistStatistics(connect_dict=get_connect_dict())
    stats = statistics.retrieve_statistics_by_slug(
        panelist_slug, include_decimal_scores=include_decimal_scores
    )

    assert "scoring" in stats, f"'scoring' was not returned for slug {panelist_slug}"
    if include_decimal_scores:
        assert (
            "scoring_decimal" in stats
        ), f"'scoring' was not returned for ID {panelist_slug}"
    assert "ranking" in stats, f"'ranking' was not returned for slug {panelist_slug}"
