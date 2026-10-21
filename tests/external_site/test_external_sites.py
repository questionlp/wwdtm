# Copyright (c) 2018-2026 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing for object: :py:class:`wwdtm.external_site.ExternalSites`."""

import json
from pathlib import Path
from typing import Any

import pytest
from mysql.connector import connect

from wwdtm.external_site import ExternalSites


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


def test_external_sites_database_connection():
    """Testing instantiating :py:class:`wwdtm.external_site.ExternalSites` with a database connection."""
    # Test with connection in a connected state
    database_connection = connect(**get_connect_dict())
    _sites = ExternalSites(database_connection=database_connection)

    assert _sites, (
        "Could not instantiate ExternalSites object using database connection"
    )
    assert isinstance(_sites, ExternalSites), (
        "Instantiated object is not an instance of ExternalSites"
    )

    # Test with connection in a disconnected state
    database_connection = connect(**get_connect_dict())
    database_connection.disconnect()
    _sites = ExternalSites(database_connection=database_connection)

    assert _sites, (
        "Could not instantiate ExternalSites object using database connection"
    )
    assert isinstance(_sites, ExternalSites), (
        "Instantiated object is not an instance of ExternalSites"
    )


def test_sites_retrieve_all() -> None:
    """Testing for :py:meth:`wwdtm.external_site.ExternalSites.retrieve_all`."""
    _sites = ExternalSites(connect_dict=get_connect_dict())
    all_sites = _sites.retrieve_all()

    assert all_sites, "No external sites could be retrieved"
    assert "id" in all_sites[0], "'id' was not returned for the first list item"
    assert "site" in all_sites[0], "'site' was not returned for the first list item"
    assert "slug" in all_sites[0], "'slug' was not returned for the first list item"
    assert "social_media" in all_sites[0], (
        "'social_media' was not returned for the first list item"
    )
    assert isinstance(all_sites[0]["social_media"], bool), (
        "'social_media' returned for the first item is not a boolean"
    )
    assert "icon" in all_sites[0], "'icon' was not returned for the first list item"


def test_sites_retrieve_all_ids():
    """Testing for :py:meth:`wwdtm.external_site.ExternalSites.retrieve_all_ids`."""
    _sites = ExternalSites(connect_dict=get_connect_dict())
    ids = _sites.retrieve_all_ids()

    assert ids, "No external site IDs could be retrieved"


def test_sites_retrieve_all_as_dict():
    """Testing for :py:meth:`wwdtm.external_site.ExternalSites.retrieve_all_as_dict`."""
    _sites = ExternalSites(connect_dict=get_connect_dict())
    all_sites = _sites.retrieve_all_as_dict()

    assert all_sites, "No external sites could be retrieved"
    assert isinstance(all_sites, dict), "Returned object is not a dictionary"


def test_sites_retrieve_all_site_names():
    """Testing for :py:meth:`wwdtm.external_site.ExternalSites.retrieve_all_site_names`."""
    _sites = ExternalSites(connect_dict=get_connect_dict())
    all_sites = _sites.retrieve_all_site_names()

    assert all_sites, "No external site names could be retrieved"


def test_sites_retrieve_all_site_slugs():
    """Testing for :py:meth:`wwdtm.external_site.ExternalSites.retrieve_all_site_slugs`."""
    _sites = ExternalSites(connect_dict=get_connect_dict())
    all_sites = _sites.retrieve_all_site_slugs()

    assert all_sites, "No external site slug strings could be retrieved"


@pytest.mark.parametrize("site_id", [16, 4])
def test_sites_retrieve_by_id(site_id: int):
    """Testing for :py:meth:`wwdtm.external_site.ExternalSites.retrieve_by_id`.

    :param site_id: External site ID to retrieve external site
        information
    """
    _sites = ExternalSites(connect_dict=get_connect_dict())
    info = _sites.retrieve_by_id(site_id)

    assert info, f"Social media site ID {site_id} not found"
    assert "id" in info, f"'id' was not returned for ID {site_id}"
    assert "site" in info, f"'site' was not returned for ID {site_id}"
    assert "slug" in info, f"'slug' was not returned for ID {site_id}"
    assert "social_media" in info, f"'social_media' was not returned for ID {site_id}"
    assert isinstance(info["social_media"], bool), (
        f"'social_media' returned for ID {site_id} is not a boolean"
    )
    assert "icon" in info, f"'icon' was not returned fir ID {site_id}"


@pytest.mark.parametrize("site_slug", ["wikipedia", "mastodon"])
def test_sites_retrieve_by_slug(site_slug: str):
    """Testing for :py:meth:`wwdtm.external_site.ExternalSites.retrieve_by_id`.

    :param site_slug: External site slug string to test retrieve
        external site information
    """
    _sites = ExternalSites(connect_dict=get_connect_dict())
    info = _sites.retrieve_by_slug(site_slug)

    assert info, f"Social media site slug string {site_slug} not found"
    assert "id" in info, f"'id' was not returned for slug string {site_slug}"
    assert "site" in info, f"'site' was not returned for slug string {site_slug}"
    assert "slug" in info, f"'slug' was not returned for slug string {site_slug}"
    assert "social_media" in info, (
        f"'social_media' was not returned for slug string {site_slug}"
    )
    assert isinstance(info["social_media"], bool), (
        f"'social_media' returned for slug string {site_slug} is not a boolean"
    )
    assert "icon" in info, f"'icon' was not returned for slug string {site_slug}"
