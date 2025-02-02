# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing for object: :py:class:`wwdtm.panelist.Panelist`."""

import json
from pathlib import Path
from typing import Any

import pytest

from wwdtm.panelist import Panelist


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


def test_panelist_retrieve_all():
    """Testing for :py:meth:`wwdtm.panelist.Panelist.retrieve_all`."""
    panelist = Panelist(connect_dict=get_connect_dict())
    panelists = panelist.retrieve_all()

    assert panelists, "No panelists could be retrieved"
    assert "id" in panelists[0], "'id' was not returned for the first list item"
    assert "name" in panelists[0], "'name' was not returned for the first list item"
    assert "slug" in panelists[0], "'slug' was not returned for the first list item"
    assert "pronouns" in panelists[0], (
        "'pronouns' was not returned for the first list item"
    )


@pytest.mark.parametrize("use_decimal_scores", [True, False])
def test_panelist_retrieve_all_details(use_decimal_scores: bool):
    """Testing for :py:meth:`wwdtm.panelist.Panelist.retrieve_all_details`.

    :param use_decimal_scores: Flag set to use decimal score columns
        and values
    """
    panelist = Panelist(connect_dict=get_connect_dict())
    panelists = panelist.retrieve_all_details(use_decimal_scores=use_decimal_scores)

    assert panelists, "No panelists could be retrieved"
    assert "id" in panelists[0], "'id' was not returned for first list item"
    assert "name" in panelists[0], "'name' was not returned for the first list item"
    assert "slug" in panelists[0], "'slug' was not returned for the first list item"
    assert "pronouns" in panelists[0], (
        "'pronouns' was not returned for the first list item"
    )
    assert "appearances" in panelists[0], (
        "'appearances' was not returned for the first list item"
    )


def test_panelist_retrieve_all_ids():
    """Testing for :py:meth:`wwdtm.panelist.Panelist.retrieve_all_ids`."""
    panelist = Panelist(connect_dict=get_connect_dict())
    ids = panelist.retrieve_all_ids()

    assert ids, "No panelist IDs could be retrieved"


def test_panelist_retrieve_all_slugs():
    """Testing for :py:meth:`wwdtm.panelist.Panelist.retrieve_all_slugs`."""
    panelist = Panelist(connect_dict=get_connect_dict())
    slugs = panelist.retrieve_all_slugs()

    assert slugs, "No panelist slug strings could be retrieved"


@pytest.mark.parametrize("panelist_id", [14])
def test_panelist_retrieve_by_id(panelist_id: int):
    """Testing for :py:meth:`wwdtm.panelist.Panelist.retrieve_by_id`.

    :param panelist_id: Panelist ID to test retrieving panelist
        information
    """
    panelist = Panelist(connect_dict=get_connect_dict())
    info = panelist.retrieve_by_id(panelist_id)

    assert info, f"Panelist ID {panelist_id} not found"
    assert "name" in info, f"'name' was not returned for ID {panelist_id}"
    assert "slug" in info, f"'slug' was not returned for ID {panelist_id}"
    assert "pronouns" in info, f"'pronouns' was not returned for ID {panelist_id}"


@pytest.mark.parametrize("panelist_id, use_decimal_scores", [(14, True), (14, False)])
def test_panelist_retrieve_details_by_id(panelist_id: int, use_decimal_scores: bool):
    """Testing for :py:meth:`wwdtm.panelist.Panelist.retrieve_details_by_id`.

    :param panelist_id: Panelist ID to test retrieving panelist details
    :param use_decimal_scores: Flag set to use decimal score columns
        and values
    """
    panelist = Panelist(connect_dict=get_connect_dict())
    info = panelist.retrieve_details_by_id(
        panelist_id, use_decimal_scores=use_decimal_scores
    )

    assert info, f"Panelist ID {panelist_id} not found"
    assert "name" in info, f"'name' was not returned for ID {panelist_id}"
    assert "slug" in info, f"'slug' was not returned for ID {panelist_id}"
    assert "pronouns" in info, f"'pronouns' was not returned for ID {panelist_id}"
    assert "appearances" in info, f"'appearances' was not returned for ID {panelist_id}"


@pytest.mark.parametrize("panelist_slug", ["luke-burbank", "drew-carey"])
def test_panelist_retrieve_by_slug(panelist_slug: str):
    """Testing for :py:meth:`wwdtm.panelist.Panelist.retrieve_by_slug`.

    :param panelist_slug: Panelist slug string to test retrieving
        panelist information
    """
    panelist = Panelist(connect_dict=get_connect_dict())
    info = panelist.retrieve_by_slug(panelist_slug)

    assert info, f"Panelist slug {panelist_slug} not found"
    assert "name" in info, f"'name' was not returned for slug {panelist_slug}"
    assert "slug" in info, f"'slug' was not returned for ID {panelist_slug}"
    assert "pronouns" in info, f"'pronouns' was not returned for ID {panelist_slug}"


@pytest.mark.parametrize(
    "panelist_slug, use_decimal_scores",
    [("luke-burbank", True), ("luke-burbank", False)],
)
def test_panelist_retrieve_details_by_slug(
    panelist_slug: str, use_decimal_scores: bool
):
    """Testing for :py:meth:`wwdtm.panelist.Panelist.retrieve_details_by_slug`.

    :param panelist_slug: Panelist slug string to test retrieving
        panelist details
    :param use_decimal_scores: Flag set to use decimal score columns
        and values
    """
    panelist = Panelist(connect_dict=get_connect_dict())
    info = panelist.retrieve_details_by_slug(
        panelist_slug, use_decimal_scores=use_decimal_scores
    )

    assert info, f"Panelist slug {panelist_slug} not found"
    assert "name" in info, f"'name' was not returned for slug {panelist_slug}"
    assert "slug" in info, f"'slug' was not returned for ID {panelist_slug}"
    assert "pronouns" in info, f"'pronouns' was not returned for ID {panelist_slug}"
    assert "appearances" in info, (
        f"'appearances' was not returned for slug {panelist_slug}"
    )


def test_panelist_retrieve_random_id() -> None:
    """Testing for :py:meth`wwdtm.panelist.Panelist.retrieve_random_id`."""
    panelist = Panelist(connect_dict=get_connect_dict())
    _id = panelist.retrieve_random_id()

    assert _id, "Returned random panelist ID is not valid"
    assert isinstance(_id, int), "Returned random panelist ID is not an integer"


def test_panelist_retrieve_random_slug() -> None:
    """Testing for :py:meth`wwdtm.panelist.Panelist.retrieve_random_slug`."""
    panelist = Panelist(connect_dict=get_connect_dict())
    _slug = panelist.retrieve_random_slug()

    assert _slug, "Returned random panelist slug string is not valid"
    assert isinstance(_slug, str), (
        "Returned random panelist slug string is not a string"
    )


def test_panelist_retrieve_random() -> None:
    """Testing for :py:meth:`wwdtm.panelist.Panelist.retrieve_random`."""
    panelist = Panelist(connect_dict=get_connect_dict())
    info = panelist.retrieve_random()

    assert info, "Random panelist not found"
    assert "name" in info, "'name' attribute was not returned for a random panelist"
    assert "slug" in info, "'slug' was not returned for a random panelist"
    assert "pronouns" in info, "'pronouns' was not returned for a random panelist"


@pytest.mark.parametrize("use_decimal_scores", [True, False])
def test_panelist_retrieve_random_details(use_decimal_scores: bool) -> None:
    """Testing for :py:meth:`wwdtm.panelist.Panelist.retrieve_random_details`."""
    panelist = Panelist(connect_dict=get_connect_dict())
    info = panelist.retrieve_random_details(use_decimal_scores=use_decimal_scores)

    assert info, "Random panelist not found"
    assert "name" in info, "'name' attribute was not returned for a random panelist"
    assert "slug" in info, "'slug' was not returned for a random panelist"
    assert "pronouns" in info, "'pronouns' was not returned for a random panelist"
    assert "appearances" in info, "'appearances' was not returned for a random panelist"
