# Copyright (c) 2018-2026 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing for object: :py:class:`wwdtm.social_media.SocialMediaNetworks`."""

import json
from pathlib import Path
from typing import Any

import pytest
from mysql.connector import connect

from wwdtm.social_media import SocialMediaNetworks


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


def test_social_media_networks_database_connection():
    """Testing instantiating :py:class:`wwdtm.social_media.SocialMediaNetworks` with a database connection."""
    # Test with connection in a connected state
    database_connection = connect(**get_connect_dict())
    with pytest.deprecated_call():
        _social_media = SocialMediaNetworks(database_connection=database_connection)

        assert _social_media, (
            "Could not instantiate SocialMediaNetworks object using database connection"
        )
        assert isinstance(_social_media, SocialMediaNetworks), (
            "Instantiated object is not an instance of SocialMediaNetworks"
        )

    # Test with connection in a disconnected state
    database_connection = connect(**get_connect_dict())
    database_connection.disconnect()
    with pytest.deprecated_call():
        _social_media = SocialMediaNetworks(database_connection=database_connection)

        assert _social_media, (
            "Could not instantiate SocialMediaNetworks object using database connection"
        )
        assert isinstance(_social_media, SocialMediaNetworks), (
            "Instantiated object is not an instance of SocialMediaNetworks"
        )


def test_networks_retrieve_all() -> None:
    """Testing for :py:meth:`wwdtm.social_media.SocialMediaNetworks.retrieve_all`."""
    with pytest.deprecated_call():
        networks = SocialMediaNetworks(connect_dict=get_connect_dict())
        all_networks = networks.retrieve_all()

        assert all_networks, "No social media networks could be retrieved"
        assert "id" in all_networks[0], "'id' was not returned for the first list item"
        assert "network" in all_networks[0], (
            "'network' was not returned for the first list item"
        )


def test_networks_retrieve_all_ids():
    """Testing for :py:meth:`wwdtm.social_media.SocialMediaNetworks.retrieve_all_ids`."""
    with pytest.deprecated_call():
        networks = SocialMediaNetworks(connect_dict=get_connect_dict())
        ids = networks.retrieve_all_ids()

        assert ids, "No social media network IDs could be retrieved"


def test_networks_retrieve_all_as_dict():
    """Testing for :py:meth:`wwdtm.social_media.SocialMediaNetworks.retrieve_all_as_dict`."""
    with pytest.deprecated_call():
        networks = SocialMediaNetworks(connect_dict=get_connect_dict())
        all_networks = networks.retrieve_all_as_dict()

        assert all_networks, "No social media networks could be retrieved"


def test_networks_retrieve_all_network_names():
    """Testing for :py:meth:`wwdtm.social_media.SocialMediaNetworks.retrieve_all_network_names`."""
    with pytest.deprecated_call():
        networks = SocialMediaNetworks(connect_dict=get_connect_dict())
        all_networks = networks.retrieve_all_network_names()

        assert all_networks, "No social media network names could be retrieved"


def test_networks_retrieve_all_network_slugs():
    """Testing for :py:meth:`wwdtm.social_media.SocialMediaNetworks.retrieve_all_network_slugs`."""
    with pytest.deprecated_call():
        networks = SocialMediaNetworks(connect_dict=get_connect_dict())
        all_networks = networks.retrieve_all_network_slugs()

        assert all_networks, "No social media network slugs could be retrieved"


@pytest.mark.parametrize("network_id", [1])
def test_networks_retrieve_by_id(network_id: int):
    """Testing for :py:meth:`wwdtm.social_media.SocialMediaNetworks.retrieve_by_id`.

    :param network_id: Social media network ID to test retrieving social
        media network information
    """
    with pytest.deprecated_call():
        networks = SocialMediaNetworks(connect_dict=get_connect_dict())
        info = networks.retrieve_by_id(network_id)

        assert info, f"Social media network ID {network_id} not found"
        assert "id" in info, f"'id' was not returned for ID {network_id}"
        assert "network" in info, f"'network' was not returned for ID {network_id}"
        assert "slug" in info, f"'slug' was not returned for ID {network_id}"


@pytest.mark.parametrize("network_slug", ["mastodon"])
def test_networks_retrieve_by_slug(network_slug: str):
    """Testing for :py:meth:`wwdtm.social_media.SocialMediaNetworks.retrieve_by_id`.

    :param network_slug: Social media network slug string to test
        retrieving social media network information
    """
    with pytest.deprecated_call():
        networks = SocialMediaNetworks(connect_dict=get_connect_dict())
        info = networks.retrieve_by_slug(network_slug)

        assert info, f"Social media network slug string {network_slug} not found"
        assert "id" in info, f"'id' was not returned for ID {network_slug}"
        assert "network" in info, f"'network' was not returned for ID {network_slug}"
        assert "slug" in info, f"'slug' was not returned for ID {network_slug}"
