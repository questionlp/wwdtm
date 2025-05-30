# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing for object: :py:class:`wwdtm.panelist.PanelistDecimalScores`."""

import json
from pathlib import Path
from typing import Any

import pytest

from wwdtm.panelist import PanelistDecimalScores


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


@pytest.mark.parametrize("panelist_id", [14])
def test_panelist_scores_retrieve_scores_by_id(panelist_id: int):
    """Testing for :py:meth:`wwdtm.panelist.PanelistDecimalScores.retrieve_scores_by_id`.

    :param panelist_id: Panelist ID to test retrieving panelist
        information
    """
    scores = PanelistDecimalScores(connect_dict=get_connect_dict())
    scoring = scores.retrieve_scores_by_id(panelist_id)

    assert scoring, f"Scoring data not returned for ID {panelist_id}"


@pytest.mark.parametrize("panelist_slug", ["luke-burbank"])
def test_panelist_scores_retrieve_scores_by_slug(panelist_slug: str):
    """Testing for :py:meth:`wwdtm.panelist.PanelistDecimalScores.retrieve_scores_by_slug`.

    :param panelist_slug: Panelist slug string to test retrieving
        panelist information
    """
    scores = PanelistDecimalScores(connect_dict=get_connect_dict())
    scoring = scores.retrieve_scores_by_slug(panelist_slug)

    assert scoring, f"Scoring data not returned for slug {panelist_slug}"


@pytest.mark.parametrize("panelist_id", [14])
def test_panelist_scores_retrieve_scores_grouped_list_by_id(panelist_id: int):
    """Testing for :py:meth:`wwdtm.panelist.PanelistDecimalScores.retrieve_scores_grouped_list_by_id`.

    :param panelist_id: Panelist ID to test retrieving panelist
        information
    """
    scores = PanelistDecimalScores(connect_dict=get_connect_dict())
    scoring = scores.retrieve_scores_grouped_list_by_id(panelist_id)

    assert "score" in scoring, f"'score' was not returned for ID {panelist_id}"
    assert "count" in scoring, f"'count' was not returned for ID {panelist_id}"


@pytest.mark.parametrize("panelist_slug", ["luke-burbank"])
def test_panelist_scores_retrieve_scores_grouped_list_by_slug(panelist_slug: str):
    """Testing for :py:meth:`wwdtm.panelist.PanelistDecimalScores.retrieve_scores_grouped_list_by_slug`.

    :param panelist_slug: Panelist slug string to test retrieving
        panelist information
    """
    scores = PanelistDecimalScores(connect_dict=get_connect_dict())
    scoring = scores.retrieve_scores_grouped_list_by_slug(panelist_slug)

    assert "score" in scoring, f"'score' was not returned for slug {panelist_slug}"
    assert "count" in scoring, f"'count' was not returned for slug {panelist_slug}"


@pytest.mark.parametrize("panelist_id", [14])
def test_panelist_scores_retrieve_scores_grouped_ordered_pair_by_id(panelist_id: int):
    """Testing for :py:meth:`wwdtm.panelist.PanelistDecimalScores.retrieve_scores_grouped_ordered_pair_by_id`.

    :param panelist_id: Panelist ID to test retrieving panelist
        information
    """
    scores = PanelistDecimalScores(connect_dict=get_connect_dict())
    scoring = scores.retrieve_scores_grouped_ordered_pair_by_id(panelist_id)

    assert scoring, f"Scoring data not returned for ID {panelist_id}"
    assert isinstance(scoring[0], tuple), "First list item is not a tuple"


@pytest.mark.parametrize("panelist_slug", ["luke-burbank"])
def test_panelist_scores_retrieve_scores_grouped_ordered_pair_by_slug(
    panelist_slug: str,
):
    """Testing for :py:meth:`wwdtm.panelist.PanelistDecimalScores.retrieve_scores_grouped_ordered_pair_by_slug`.

    :param panelist_slug: Panelist slug string to test retrieving
        panelist information
    """
    scores = PanelistDecimalScores(connect_dict=get_connect_dict())
    scoring = scores.retrieve_scores_grouped_ordered_pair_by_slug(panelist_slug)

    assert scoring, f"Scoring data not returned for slug {panelist_slug}"
    assert isinstance(scoring[0], tuple), "First list item is not a tuple"


@pytest.mark.parametrize("panelist_id", [14])
def test_panelist_scores_retrieve_scores_list_by_id(panelist_id: int):
    """Testing for :py:meth:`wwdtm.panelist.PanelistDecimalScores.retrieve_scores_list_by_id`.

    :param panelist_id: Panelist ID to test retrieving panelist information
    """
    scores = PanelistDecimalScores(connect_dict=get_connect_dict())
    scoring = scores.retrieve_scores_list_by_id(panelist_id)

    assert "shows" in scoring, f"'shows' was not returned for ID {panelist_id}"
    assert "scores" in scoring, f"'scores' was not returned for ID {panelist_id}"


@pytest.mark.parametrize("panelist_slug", ["luke-burbank"])
def test_panelist_scores_retrieve_scores_list_by_slug(panelist_slug: str):
    """Testing for :py:meth:`wwdtm.panelist.PanelistDecimalScores.retrieve_scores_list_by_slug`.

    :param panelist_slug: Panelist slug string to test retrieving
        panelist information
    """
    scores = PanelistDecimalScores(connect_dict=get_connect_dict())
    scoring = scores.retrieve_scores_list_by_slug(panelist_slug)

    assert "shows" in scoring, f"'shows' was not returned for slug {panelist_slug}"
    assert "scores" in scoring, f"'scores' was not returned for slug {panelist_slug}"


@pytest.mark.parametrize("panelist_id", [14])
def test_panelist_scores_retrieve_scores_ordered_pair_by_id(panelist_id: int):
    """Testing for :py:meth:`wwdtm.panelist.PanelistDecimalScores.retrieve_scores_ordered_pair_by_id`.

    :param panelist_id: Panelist ID to test retrieving panelist
        information
    """
    scores = PanelistDecimalScores(connect_dict=get_connect_dict())
    scoring = scores.retrieve_scores_ordered_pair_by_id(panelist_id)

    assert scoring, f"Scoring data not returned for ID {panelist_id}"


@pytest.mark.parametrize("panelist_slug", ["luke-burbank"])
def test_panelist_scores_retrieve_scores_ordered_pair_by_slug(panelist_slug: str):
    """Testing for :py:meth:`wwdtm.panelist.PanelistDecimalScores.retrieve_scores_ordered_pair_by_slug`.

    :param panelist_slug: Panelist slug string to test retrieving panelist
        information
    """
    scores = PanelistDecimalScores(connect_dict=get_connect_dict())
    scoring = scores.retrieve_scores_ordered_pair_by_slug(panelist_slug)

    assert scoring, f"Scoring data not returned for slug {panelist_slug}"
