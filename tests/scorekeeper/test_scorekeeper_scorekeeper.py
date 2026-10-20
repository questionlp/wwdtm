# Copyright (c) 2018-2026 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing for object: :py:class:`wwdtm.scorekeeper.Scorekeeper`."""

import json
from pathlib import Path
from typing import Any

import pytest
from mysql.connector import connect

from wwdtm.scorekeeper import Scorekeeper


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


def test_scorekeeper_database_connection():
    """Testing instantiating :py:class:`wwdtm.scorekeeper.Scorekeeper` with a database connection."""
    # Test with connection in a connected state
    database_connection = connect(**get_connect_dict())
    _scorekeeper = Scorekeeper(database_connection=database_connection)

    assert _scorekeeper, (
        "Could not instantiate Scorekeeper object using database connection"
    )
    assert isinstance(_scorekeeper, Scorekeeper), (
        "Instantiated object is not an instance of Scorekeeper"
    )

    # Test with connection in a disconnected state
    database_connection = connect(**get_connect_dict())
    database_connection.disconnect()
    _scorekeeper = Scorekeeper(database_connection=database_connection)

    assert _scorekeeper, (
        "Could not instantiate Scorekeeper object using database connection"
    )
    assert isinstance(_scorekeeper, Scorekeeper), (
        "Instantiated object is not an instance of Scorekeeper"
    )


def test_scorekeeper_retrieve_all():
    """Testing for :py:meth:`wwdtm.scorekeeper.Scorekeeper.retrieve_all`."""
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    scorekeepers = scorekeeper.retrieve_all()

    assert scorekeepers, "No scorekeepers could be retrieved"
    assert "id" in scorekeepers[0], "'id' was not returned for the first list item"
    assert "name" in scorekeepers[0], "'name' was not returned for the first list item"
    assert "slug" in scorekeepers[0], "'slug' was not returned for the first list item"
    assert "pronouns" in scorekeepers[0], (
        "'pronouns' was not returned for the first list item"
    )
    assert "external_sites" in scorekeepers[0], (
        "'external_sites' was not returned for the first list item"
    )
    assert "social_media_accounts" in scorekeepers[0], (
        "'social_media_accounts' was not returned for the first list item"
    )


def test_scorekeeper_retrieve_all_details():
    """Testing for :py:meth:`wwdtm.scorekeeper.Scorekeeper.retrieve_all_details`."""
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    scorekeepers = scorekeeper.retrieve_all_details()

    assert scorekeepers, "No scorekeepers could be retrieved"
    assert "id" in scorekeepers[0], "'id' was not returned for first list item"
    assert "name" in scorekeepers[0], "'name' was not returned for the first list item"
    assert "slug" in scorekeepers[0], "'slug' was not returned for the first list item"
    assert "pronouns" in scorekeepers[0], (
        "'pronouns' was not returned for the first list item"
    )
    assert "external_sites" in scorekeepers[0], (
        "'external_sites' was not returned for the first list item"
    )
    assert "social_media_accounts" in scorekeepers[0], (
        "'social_media_accounts' was not returned for the first list item"
    )
    assert "is_panelist" in scorekeepers[0], (
        "'is_panelist' was not returned for the first list item"
    )
    assert "appearances" in scorekeepers[0], (
        "'appearances' was not returned for the first list item"
    )


def test_scorekeeper_retrieve_all_ids():
    """Testing for :py:meth:`wwdtm.scorekeeper.Scorekeeper.retrieve_all_ids`."""
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    ids = scorekeeper.retrieve_all_ids()

    assert ids, "No scorekeeper IDs could be retrieved"


def test_scorekeeper_retrieve_all_slugs():
    """Testing for :py:meth:`wwdtm.scorekeeper.Scorekeeper.retrieve_all_slugs`."""
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    slugs = scorekeeper.retrieve_all_slugs()

    assert slugs, "No scorekeeper slug strings could be retrieved"


@pytest.mark.parametrize("scorekeeper_id", [13, 20])
def test_scorekeeper_retrieve_by_id(scorekeeper_id: int):
    """Testing for :py:meth:`wwdtm.scorekeeper.Scorekeeper.retrieve_by_id`.

    :param scorekeeper_id: Scorekeeper ID to test retrieving scorekeeper
        information
    """
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    info = scorekeeper.retrieve_by_id(scorekeeper_id)

    assert info, f"Scorekeeper ID {scorekeeper_id} not found"
    assert "name" in info, f"'name' was not returned for ID {scorekeeper_id}"
    assert "slug" in info, f"'slug' was not returned for ID {scorekeeper_id}"
    assert "pronouns" in info, f"'pronouns' was not returned for ID {scorekeeper_id}"
    assert "external_sites" in info, (
        f"'external_sites' was not returned for ID {scorekeeper_id}"
    )
    assert "social_media_accounts" in info, (
        f"'social_media_accounts' was not returned for ID {scorekeeper_id}"
    )


@pytest.mark.parametrize("scorekeeper_slug", ["chioke-i-anson", "alzo-slade"])
def test_scorekeeper_retrieve_by_slug(scorekeeper_slug: str):
    """Testing for :py:meth:`wwdtm.scorekeeper.Scorekeeper.retrieve_by_slug`.

    :param scorekeeper_slug: Scorekeeper slug string to test retrieving
        scorekeeper information
    """
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    info = scorekeeper.retrieve_by_slug(scorekeeper_slug)

    assert info, f"Scorekeeper slug {scorekeeper_slug} not found"
    assert "name" in info, f"'name' was not returned for slug {scorekeeper_slug}"
    assert "slug" in info, f"'slug' was not returned for ID {scorekeeper_slug}"
    assert "pronouns" in info, f"'pronouns' was not returned for ID {scorekeeper_slug}"
    assert "external_sites" in info, (
        f"'external_sites' was not returned for ID {scorekeeper_slug}"
    )
    assert "social_media_accounts" in info, (
        f"'social_media_accounts' was not returned for ID {scorekeeper_slug}"
    )


@pytest.mark.parametrize("scorekeeper_id", [13, 20])
def test_scorekeeper_retrieve_details_by_id(scorekeeper_id: int):
    """Testing for :py:meth:`wwdtm.scorekeeper.Scorekeeper.retrieve_details_by_id`.

    :param scorekeeper_id: Scorekeeper ID to test retrieving scorekeeper
        details
    """
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    info = scorekeeper.retrieve_details_by_id(scorekeeper_id)

    assert info, f"Scorekeeper ID {scorekeeper_id} not found"
    assert "name" in info, f"'name' was not returned for ID {scorekeeper_id}"
    assert "slug" in info, f"'slug' was not returned for ID {scorekeeper_id}"
    assert "pronouns" in info, f"'pronouns' was not returned for ID {scorekeeper_id}"
    assert "external_sites" in info, (
        f"'external_sites' was not returned for ID {scorekeeper_id}"
    )
    assert "social_media_accounts" in info, (
        f"'social_media_accounts' was not returned for ID {scorekeeper_id}"
    )
    assert "is_panelist" in info, (
        f"'is_panelist' was not returned for ID {scorekeeper_id}"
    )
    assert "appearances" in info, (
        f"'appearances' was not returned for ID {scorekeeper_id}"
    )


@pytest.mark.parametrize("scorekeeper_slug", ["chioke-i-anson", "alzo-slade"])
def test_scorekeeper_retrieve_details_by_slug(scorekeeper_slug: str):
    """Testing for :py:meth:`wwdtm.scorekeeper.Scorekeeper.retrieve_details_by_slug`.

    :param scorekeeper_slug: Scorekeeper slug string to test retrieving
        scorekeeper details
    """
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    info = scorekeeper.retrieve_details_by_slug(scorekeeper_slug)

    assert info, f"Scorekeeper slug {scorekeeper_slug} not found"
    assert "name" in info, f"'name' was not returned for slug {scorekeeper_slug}"
    assert "slug" in info, f"'slug' was not returned for slug {scorekeeper_slug}"
    assert "pronouns" in info, (
        f"'pronouns' was not returned for slug {scorekeeper_slug}"
    )
    assert "external_sites" in info, (
        f"'external_sites' was not returned for ID {scorekeeper_slug}"
    )
    assert "social_media_accounts" in info, (
        f"'social_media_accounts' was not returned for ID {scorekeeper_slug}"
    )
    assert "is_panelist" in info, (
        f"'is_panelist' was not returned for slug {scorekeeper_slug}"
    )
    assert "appearances" in info, (
        f"'appearances' was not returned for slug {scorekeeper_slug}"
    )


@pytest.mark.parametrize("scorekeeper_id", [13])
def test_scorekeeper_retrieve_pronouns_by_id(scorekeeper_id: int):
    """Testing for :py:meth`wwdtm.scorekeeper.Scorekeeper.retrieve_pronouns_by_id`."""
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    _pronouns = scorekeeper.retrieve_pronouns_by_id(scorekeeper_id)

    assert isinstance(_pronouns, list), (
        f"Returned value for scorekeeper ID {scorekeeper_id} was not of type list"
    )
    assert _pronouns, (
        f"No preferred pronouns were returned for scorekeeper ID {scorekeeper_id}"
    )


@pytest.mark.parametrize("scorekeeper_slug", ["chioke-i-anson"])
def test_scorekeeper_retrieve_pronouns_by_slug(scorekeeper_slug: str):
    """Testing for :py:meth`wwdtm.scorekeeper.Scorekeeper.retrieve_pronouns_by_id`."""
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    _pronouns = scorekeeper.retrieve_pronouns_by_slug(scorekeeper_slug)

    assert isinstance(_pronouns, list), (
        f"Returned value for scorekeeper slug string {scorekeeper_slug} was not of type list"
    )
    assert _pronouns, (
        f"No preferred pronouns were returned for scorekeeper slug string {scorekeeper_slug}"
    )


def test_scorekeeper_retrieve_random_id() -> None:
    """Testing for :py:meth`wwdtm.scorekeeper.Scorekeeper.retrieve_random_id`."""
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    _id = scorekeeper.retrieve_random_id()

    assert _id, "Returned random scorekeeper ID is not valid"
    assert isinstance(_id, int), "Returned random scorekeeper ID is not an integer"


def test_scorekeeper_retrieve_random_slug() -> None:
    """Testing for :py:meth`wwdtm.scorekeeper.Scorekeeper.retrieve_random_slug`."""
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    _slug = scorekeeper.retrieve_random_slug()

    assert _slug, "Returned random scorekeeper slug string is not valid"
    assert isinstance(_slug, str), (
        "Returned random scorekeeper slug string is not a string"
    )


def test_scorekeeper_retrieve_random() -> None:
    """Testing for :py:meth:`wwdtm.scorekeeper.Scorekeeper.retrieve_random`."""
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    info = scorekeeper.retrieve_random()

    assert info, "Random scorekeeper not found"
    assert "name" in info, "'name' attribute was not returned for a random scorekeeper"
    assert "slug" in info, "'slug' was not returned for a random scorekeeper"
    assert "pronouns" in info, "'pronouns' was not returned for a random scorekeeper"


def test_scorekeeper_retrieve_random_details() -> None:
    """Testing for :py:meth:`wwdtm.scorekeeper.Scorekeeper.retrieve_random_details`."""
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    info = scorekeeper.retrieve_random_details()

    assert info, "Random scorekeeper not found"
    assert "name" in info, "'name' attribute was not returned for a random scorekeeper"
    assert "slug" in info, "'slug' was not returned for a random scorekeeper"
    assert "pronouns" in info, "'pronouns' was not returned for a random scorekeeper"
    assert "appearances" in info, (
        "'appearances' was not returned for a random scorekeeper"
    )


@pytest.mark.parametrize("scorekeeper_id", [2, 20])
def test_scorekeeper_retrieve_external_sites_by_id(scorekeeper_id: int):
    """Testing for :py:meth`wwdtm.scorekeeper.Scorekeeper.retrieve_external_sites_by_id`."""
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    _sites = scorekeeper.retrieve_external_sites_by_id(scorekeeper_id)

    assert isinstance(_sites, list), (
        f"Returned value for scorekeeper ID {scorekeeper_id} was not of type list"
    )

    if _sites:
        assert "site" in _sites[0], "Site name was not returned in the first list item"
        assert "icon" in _sites[0], (
            "Site icon name was not returned in the first list item"
        )


@pytest.mark.parametrize("scorekeeper_slug", ["korva-coleman", "alzo-slade"])
def test_scorekeeper_retrieve_external_sites_by_slug(scorekeeper_slug: str):
    """Testing for :py:meth`wwdtm.scorekeeper.Scorekeeper.retrieve_external_sites_by_id`."""
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    _sites = scorekeeper.retrieve_external_sites_by_slug(scorekeeper_slug)

    assert isinstance(_sites, list), (
        f"Returned value for scorekeeper slug string {scorekeeper_slug} was not of type list"
    )

    if _sites:
        assert "site" in _sites[0], "Site name was not returned in the first list item"
        assert "icon" in _sites[0], (
            "Site icon name was not returned in the first list item"
        )


@pytest.mark.parametrize("scorekeeper_id", [2, 20])
def test_scorekeeper_retrieve_social_acounts_by_id(scorekeeper_id: int):
    """Testing for :py:meth`wwdtm.scorekeeper.Scorekeeper.retrieve_social_media_accounts_by_id`."""
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    with pytest.deprecated_call():
        _accounts = scorekeeper.retrieve_social_media_accounts_by_id(scorekeeper_id)

        assert isinstance(_accounts, list), (
            f"Returned value for scorekeeper ID {scorekeeper_id} was not of type list"
        )
        assert _accounts, (
            f"No social media accounts were returned for scorekeeper ID {scorekeeper_id}"
        )

        if _accounts:
            assert "network" in _accounts[0], (
                "Site name was not returned in the first list item"
            )
            assert "account" in _accounts[0], (
                "Account name was not returned in the first list item"
            )

            assert "url" in _accounts[0], "URL was not returned in the first list item"


@pytest.mark.parametrize("scorekeeper_slug", ["korva-coleman", "alzo-slade"])
def test_scorekeeper_retrieve_social_media_accounts_by_slug(scorekeeper_slug: str):
    """Testing for :py:meth`wwdtm.scorekeeper.Scorekeeper.retrieve_social_media_accounts_by_id`."""
    scorekeeper = Scorekeeper(connect_dict=get_connect_dict())
    with pytest.deprecated_call():
        _accounts = scorekeeper.retrieve_social_media_accounts_by_slug(scorekeeper_slug)

        assert isinstance(_accounts, list), (
            f"Returned value for scorekeeper slug string {scorekeeper_slug} was not of type list"
        )
        assert _accounts, (
            f"No social media accounts were returned for scorekeeper slug string {scorekeeper_slug}"
        )

        if _accounts:
            assert "network" in _accounts[0], (
                "Site name was not returned in the first list item"
            )
            assert "account" in _accounts[0], (
                "Account name was not returned in the first list item"
            )

            assert "url" in _accounts[0], "URL was not returned in the first list item"
