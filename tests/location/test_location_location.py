# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing for object: :py:class:`wwdtm.location.Location`."""
import json
from pathlib import Path
from typing import Any

import pytest

from wwdtm.location import Location


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


def test_location_retrieve_all():
    """Testing for :py:meth:`wwdtm.location.Location.retrieve_all`."""
    location = Location(connect_dict=get_connect_dict())
    locations = location.retrieve_all()

    assert locations, "No locations could be retrieved"
    assert "id" in locations[0], "'id' was not returned for the first list item"
    assert "venue" in locations[0], "'venue' was not returned for the first list item"
    assert (
        "coordinates" in locations[0]
    ), "'coordinates' was not returned for the first list item"
    if locations[0]["coordinates"]:
        assert (
            "latitude" in locations[0]["coordinates"]
        ), "'latitude' was not returned for the first list item"
        assert (
            "longitude" in locations[0]["coordinates"]
        ), "'longitude' was not returned for the first list item"


def test_location_retrieve_all_details():
    """Testing for :py:meth:`wwdtm.location.Location.retrieve_all_details`."""
    location = Location(connect_dict=get_connect_dict())
    locations = location.retrieve_all_details()

    assert locations, "No locations could be retrieved"
    assert "id" in locations[0], "'id' was not returned for first list item"
    assert "venue" in locations[0], "'venue' was not returned for the first list item"
    assert (
        "coordinates" in locations[0]
    ), "'coordinates' was not returned for the first list item"
    if locations[0]["coordinates"]:
        assert (
            "latitude" in locations[0]["coordinates"]
        ), "'latitude' was not returned for the first list item"
        assert (
            "longitude" in locations[0]["coordinates"]
        ), "'longitude' was not returned for the first list item"
    assert (
        "recordings" in locations[0]
    ), "'recordings' was not returned for the first list item"


def test_location_retrieve_all_ids():
    """Testing for :py:meth:`wwdtm.location.Location.retrieve_all_ids`."""
    location = Location(connect_dict=get_connect_dict())
    ids = location.retrieve_all_ids()

    assert ids, "No location IDs could be retrieved"


def test_location_retrieve_all_slugs():
    """Testing for :py:meth:`wwdtm.location.Location.retrieve_all_slugs`."""
    location = Location(connect_dict=get_connect_dict())
    slugs = location.retrieve_all_slugs()

    assert slugs, "No location slug strings could be retrieved"


@pytest.mark.parametrize("location_id", [95])
def test_location_retrieve_by_id(location_id: int):
    """Testing for :py:meth:`wwdtm.location.Location.retrieve_by_id`.

    :param location_id: Location ID to test retrieving location
        information
    """
    location = Location(connect_dict=get_connect_dict())
    info = location.retrieve_by_id(location_id)

    assert info, f"Location ID {location_id} not found"
    assert "venue" in info, f"'venue' was not returned for ID {location_id}"
    assert "coordinates" in info, f"'coordinates' was not returned for ID {location_id}"
    if info["coordinates"]:
        assert (
            "latitude" in info["coordinates"]
        ), f"'latitude' was not returned for ID {location_id}"
        assert (
            "longitude" in info["coordinates"]
        ), f"'longitude' was not returned for ID {location_id}"


@pytest.mark.parametrize("location_id", [95])
def test_location_retrieve_details_by_id(location_id: int):
    """Testing for :py:meth:`wwdtm.location.location.retrieve_details_by_id`.

    :param location_id: Location ID to test retrieving location details
    """
    location = Location(connect_dict=get_connect_dict())
    info = location.retrieve_details_by_id(location_id)

    assert info, f"Location ID {location_id} not found"
    assert "venue" in info, f"'venue' was not returned for ID {location_id}"
    assert "coordinates" in info, f"'coordinates' was not returned for ID {location_id}"
    if info["coordinates"]:
        assert (
            "latitude" in info["coordinates"]
        ), f"'latitude' was not returned for ID {location_id}"
        assert (
            "longitude" in info["coordinates"]
        ), f"'longitude' was not returned for ID {location_id}"
    assert "recordings" in info, f"'recordings' was not returned for ID {location_id}"


@pytest.mark.parametrize("location_slug", ["the-chicago-theatre-chicago-il"])
def test_location_retrieve_by_slug(location_slug: str):
    """Testing for :py:meth:`wwdtm.location.Location.retrieve_by_slug`.

    :param location_slug: Location slug string to test retrieving
        location information
    """
    location = Location(connect_dict=get_connect_dict())
    info = location.retrieve_by_slug(location_slug)

    assert info, f"Location slug {location_slug} not found"
    assert "venue" in info, f"'venue' was not returned for slug {location_slug}"
    assert (
        "coordinates" in info
    ), f"'coordinates' was not returned for slug {location_slug}"
    if info["coordinates"]:
        assert (
            "latitude" in info["coordinates"]
        ), f"'latitude' was not returned for slug {location_slug}"
        assert (
            "longitude" in info["coordinates"]
        ), f"'longitude' was not returned for slug {location_slug}"


@pytest.mark.parametrize("location_slug", ["the-chicago-theatre-chicago-il"])
def test_location_retrieve_details_by_slug(location_slug: str):
    """Testing for :py:meth:`wwdtm.location.Location.retrieve_details_by_slug`.

    :param location_slug: Location slug string to test retrieving
        location details
    """
    location = Location(connect_dict=get_connect_dict())
    info = location.retrieve_details_by_slug(location_slug)

    assert info, f"Location slug {location_slug} not found"
    assert "venue" in info, f"'venue' was not returned for slug {location_slug}"
    assert (
        "coordinates" in info
    ), f"'coordinates' was not returned for slug {location_slug}"
    if info["coordinates"]:
        assert (
            "latitude" in info["coordinates"]
        ), f"'latitude' was not returned for slug {location_slug}"
        assert (
            "longitude" in info["coordinates"]
        ), f"'longitude' was not returned for slug {location_slug}"
    assert (
        "recordings" in info
    ), f"'recordings' was not returned for slug {location_slug}"
