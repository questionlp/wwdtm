# Copyright (c) 2018-2026 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing for object: :py:class:`wwdtm.host.Host`."""

import json
from pathlib import Path
from typing import Any

import pytest
from mysql.connector import connect

from wwdtm.host import Host


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


def test_host_database_connection():
    """Testing instantiating :py:class:`wwdtm.host.Host` with a database connection."""
    # Test with connection in a connected state
    database_connection = connect(**get_connect_dict())
    _host = Host(database_connection=database_connection)

    assert _host, "Could not instantiate Host object using database connection"
    assert isinstance(_host, Host), "Instantiated object is not an instance of Host"

    # Test with connection in a disconnected state
    database_connection = connect(**get_connect_dict())
    database_connection.disconnect()
    _host = Host(database_connection=database_connection)

    assert _host, "Could not instantiate Host object using database connection"
    assert isinstance(_host, Host), "Instantiated object is not an instance of Host"


def test_host_retrieve_all():
    """Testing for :py:meth:`wwdtm.host.Host.retrieve_all`."""
    host = Host(connect_dict=get_connect_dict())
    hosts = host.retrieve_all()

    assert hosts, "No hosts could be retrieved"
    assert "id" in hosts[0], "'id' was not returned for the first list item"
    assert "name" in hosts[0], "'name' was not returned for the first list item"
    assert "slug" in hosts[0], "'slug' was not returned for the first list item"
    assert "pronouns" in hosts[0], "'pronouns' was not returned for the first list item"
    assert "external_sites" in hosts[0], (
        "'external_sites' was not returned for the first list item"
    )
    assert "social_media_accounts" in hosts[0], (
        "'social_media_accounts' was not returned for the first list item"
    )


def test_host_retrieve_all_details():
    """Testing for :py:meth:`wwdtm.host.Host.retrieve_all_details`."""
    host = Host(connect_dict=get_connect_dict())
    hosts = host.retrieve_all_details()

    assert hosts, "No hosts could be retrieved"
    assert "id" in hosts[0], "'id' was not returned for first list item"
    assert "name" in hosts[0], "'name' was not returned for the first list item"
    assert "slug" in hosts[0], "'slug' was not returned for the first list item"
    assert "pronouns" in hosts[0], "'pronouns' was not returned for the first list item"
    assert "external_sites" in hosts[0], (
        "'external_sites' was not returned for the first list item"
    )
    assert "social_media_accounts" in hosts[0], (
        "'social_media_accounts' was not returned for the first list item"
    )
    assert "is_panelist" in hosts[0], (
        "'is_panelist' was not returned for first list item"
    )
    assert "appearances" in hosts[0], (
        "'appearances' was not returned for thefirst list item"
    )


def test_host_retrieve_all_ids():
    """Testing for :py:meth:`wwdtm.host.Host.retrieve_all_ids`."""
    host = Host(connect_dict=get_connect_dict())
    ids = host.retrieve_all_ids()

    assert ids, "No host IDs could be retrieved"


def test_host_retrieve_all_slugs():
    """Testing for :py:meth:`wwdtm.host.Host.retrieve_all_slugs`."""
    host = Host(connect_dict=get_connect_dict())
    slugs = host.retrieve_all_slugs()

    assert slugs, "No host slug strings could be retrieved"


@pytest.mark.parametrize("host_id", [1, 2])
def test_host_retrieve_by_id(host_id: int):
    """Testing for :py:meth:`wwdtm.host.Host.retrieve_by_id`.

    :param host_id: Host ID to test retrieving host information
    """
    host = Host(connect_dict=get_connect_dict())
    info = host.retrieve_by_id(host_id)

    assert info, f"Host ID {host_id} not found"
    assert "name" in info, f"'name' was not returned for ID {host_id}"
    assert "slug" in info, f"'slug' was not returned for ID {host_id}"
    assert "pronouns" in info, f"'pronouns' was not returned for ID {host_id}"
    assert "external_sites" in info, (
        f"'external_sites' was not returned for ID {host_id}"
    )
    assert "social_media_accounts" in info, (
        f"'social_media_accounts' was not returned for ID {host_id}"
    )


@pytest.mark.parametrize("host_slug", ["peter-sagal", "luke-burbank"])
def test_host_retrieve_by_slug(host_slug: str):
    """Testing for :py:meth:`wwdtm.host.Host.retrieve_by_slug`.

    :param host_slug: Host slug string to test retrieving host
        information
    """
    host = Host(connect_dict=get_connect_dict())
    info = host.retrieve_by_slug(host_slug)

    assert info, f"Host slug {host_slug} not found"
    assert "name" in info, f"'name' was not returned for slug {host_slug}"
    assert "slug" in info, f"'slug' was not returned for slug {host_slug}"
    assert "pronouns" in info, f"'pronouns' was not returned for slug {host_slug}"
    assert "external_sites" in info, (
        f"'external_sites' was not returned for slug {host_slug}"
    )
    assert "social_media_accounts" in info, (
        f"'social_media_accounts' was not returned for ID {host_slug}"
    )


@pytest.mark.parametrize("host_id", [1, 2])
def test_host_retrieve_details_by_id(host_id: int):
    """Testing for :py:meth:`wwdtm.host.Host.retrieve_details_by_id`.

    :param host_id: Host ID to test retrieving host details
    """
    host = Host(connect_dict=get_connect_dict())
    info = host.retrieve_details_by_id(host_id)

    assert info, f"Host ID {host_id} not found"
    assert "name" in info, f"'name' was not returned for ID {host_id}"
    assert "slug" in info, f"'slug' was not returned for ID {host_id}"
    assert "pronouns" in info, f"'pronouns' was not returned for ID {host_id}"
    assert "external_sites" in info, (
        f"'external_sites' was not returned for ID {host_id}"
    )
    assert "social_media_accounts" in info, (
        f"'social_media_accounts' was not returned for ID {host_id}"
    )
    assert "is_panelist" in info, f"'is_panelist' was not returned for ID {host_id}"
    assert "appearances" in info, f"'appearances' was not returned for ID {host_id}"


@pytest.mark.parametrize("host_slug", ["peter-sagal", "luke-burbank"])
def test_host_retrieve_details_by_slug(host_slug: str):
    """Testing for :py:meth:`wwdtm.host.Host.retrieve_details_by_slug`.

    :param host_slug: Host slug string to test retrieving host details
    """
    host = Host(connect_dict=get_connect_dict())
    info = host.retrieve_details_by_slug(host_slug)

    assert info, f"Host slug {host_slug} not found"
    assert "name" in info, f"'name' was not returned for slug {host_slug}"
    assert "slug" in info, f"'slug' was not returned for slug {host_slug}"
    assert "pronouns" in info, f"'pronouns' was not returned for slug {host_slug}"
    assert "external_sites" in info, (
        f"'external_sites' was not returned for slug {host_slug}"
    )
    assert "social_media_accounts" in info, (
        f"'social_media_accounts' was not returned for ID {host_slug}"
    )
    assert "is_panelist" in info, f"'is_panelist' was not returned for slug {host_slug}"
    assert "appearances" in info, f"'appearances' was not returned for slug {host_slug}"


@pytest.mark.parametrize("host_id", [11, 24])
def test_host_retrieve_pronouns_by_id(host_id: int):
    """Testing for :py:meth`wwdtm.host.Host.retrieve_pronouns_by_id`."""
    host = Host(connect_dict=get_connect_dict())
    _pronouns = host.retrieve_pronouns_by_id(host_id)

    assert isinstance(_pronouns, list), (
        f"Returned value for host ID {host_id} was not of type list"
    )
    assert _pronouns, f"No preferred pronouns were returned for host ID {host_id}"


@pytest.mark.parametrize("host_slug", ["peter-grosz", "karen-chee"])
def test_host_retrieve_pronouns_by_slug(host_slug: str):
    """Testing for :py:meth`wwdtm.host.Host.retrieve_pronouns_by_id`."""
    host = Host(connect_dict=get_connect_dict())
    _pronouns = host.retrieve_pronouns_by_slug(host_slug)

    assert isinstance(_pronouns, list), (
        f"Returned value for host slug string {host_slug} was not of type list"
    )
    assert _pronouns, (
        f"No preferred pronouns were returned for host slug string {host_slug}"
    )


def test_host_retrieve_random_id() -> None:
    """Testing for :py:meth`wwdtm.host.Host.retrieve_random_id`."""
    host = Host(connect_dict=get_connect_dict())
    _id = host.retrieve_random_id()

    assert _id, "Returned random host ID is not valid"
    assert isinstance(_id, int), "Returned random host ID is not an integer"


def test_host_retrieve_random_slug() -> None:
    """Testing for :py:meth`wwdtm.host.Host.retrieve_random_slug`."""
    host = Host(connect_dict=get_connect_dict())
    _slug = host.retrieve_random_slug()

    assert _slug, "Returned random host slug string is not valid"
    assert isinstance(_slug, str), "Returned random host slug string is not a string"


def test_host_retrieve_random() -> None:
    """Testing for :py:meth:`wwdtm.host.Host.retrieve_random`."""
    host = Host(connect_dict=get_connect_dict())
    info = host.retrieve_random()

    assert info, "Random host not found"
    assert "name" in info, "'name' attribute was not returned for a random host"
    assert "slug" in info, "'slug' was not returned for a random host"
    assert "pronouns" in info, "'pronouns' was not returned for a random host"


def test_host_retrieve_random_details() -> None:
    """Testing for :py:meth:`wwdtm.host.Host.retrieve_random_details`."""
    host = Host(connect_dict=get_connect_dict())
    info = host.retrieve_random_details()

    assert info, "Random host not found"
    assert "name" in info, "'name' attribute was not returned for a random host"
    assert "slug" in info, "'slug' was not returned for a random host"
    assert "pronouns" in info, "'pronouns' was not returned for a random host"
    assert "social_media_accounts" in info, (
        "'social_media_accounts' was not returned for a random host"
    )
    assert "appearances" in info, "'appearances' was not returned for a random host"


@pytest.mark.parametrize("host_id", [1, 2])
def test_host_retrieve_external_sites_by_id(host_id: int):
    """Testing for :py:meth`wwdtm.host.Host.retrieve_external_sites_by_id`."""
    host = Host(connect_dict=get_connect_dict())
    _sites = host.retrieve_external_sites_by_id(host_id)

    assert isinstance(_sites, list), (
        f"Returned value for host ID {host_id} was not of type list"
    )

    if _sites:
        assert "site" in _sites[0], "Site name was not returned in the first list item"
        assert "icon" in _sites[0], (
            "Site icon name was not returned in the first list item"
        )


@pytest.mark.parametrize("host_slug", ["peter-sagal", "luke-burbank"])
def test_host_retrieve_external_sites_by_slug(host_slug: str):
    """Testing for :py:meth`wwdtm.host.Host.retrieve_external_sites_by_id`."""
    host = Host(connect_dict=get_connect_dict())
    _sites = host.retrieve_external_sites_by_slug(host_slug)

    assert isinstance(_sites, list), (
        f"Returned value for host slug string {host_slug} was not of type list"
    )

    if _sites:
        assert "site" in _sites[0], "Site name was not returned in the first list item"
        assert "icon" in _sites[0], (
            "Site icon name was not returned in the first list item"
        )


@pytest.mark.parametrize("host_id", [1, 2])
def test_host_retrieve_social_acounts_by_id(host_id: int):
    """Testing for :py:meth`wwdtm.host.Host.retrieve_social_media_accounts_by_id`."""
    host = Host(connect_dict=get_connect_dict())
    with pytest.deprecated_call():
        _accounts = host.retrieve_social_media_accounts_by_id(host_id)

        assert isinstance(_accounts, list), (
            f"Returned value for host ID {host_id} was not of type list"
        )
        assert _accounts, (
            f"No social media accounts were returned for host ID {host_id}"
        )

        if _accounts:
            assert "network" in _accounts[0], (
                "Site name was not returned in the first list item"
            )
            assert "account" in _accounts[0], (
                "Account name was not returned in the first list item"
            )

            assert "url" in _accounts[0], "URL was not returned in the first list item"


@pytest.mark.parametrize("host_slug", ["peter-sagal", "luke-burbank"])
def test_host_retrieve_social_media_accounts_by_slug(host_slug: str):
    """Testing for :py:meth`wwdtm.host.Host.retrieve_social_media_accounts_by_id`."""
    host = Host(connect_dict=get_connect_dict())
    with pytest.deprecated_call():
        _accounts = host.retrieve_social_media_accounts_by_slug(host_slug)

        assert isinstance(_accounts, list), (
            f"Returned value for host slug string {host_slug} was not of type list"
        )
        assert _accounts, (
            f"No social media accounts were returned for host slug string {host_slug}"
        )

        if _accounts:
            assert "network" in _accounts[0], (
                "Site name was not returned in the first list item"
            )
            assert "account" in _accounts[0], (
                "Account name was not returned in the first list item"
            )

            assert "url" in _accounts[0], "URL was not returned in the first list item"
