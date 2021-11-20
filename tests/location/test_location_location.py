# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
"""Testing for object: :py:class:`wwdtm.location.Location`
"""
import json
from typing import Any, Dict

import pytest
from wwdtm.location import Location


@pytest.mark.skip
def get_connect_dict() -> Dict[str, Any]:
    """Read in database connection settings and return values as a
    dictionary.

    :return: A dictionary containing database connection settings
        for use by mysql.connector
    :rtype: Dict[str, Any]
    """
    with open("config.json", "r") as config_file:
        config_dict = json.load(config_file)
        if "database" in config_dict:
            return config_dict["database"]


def test_location_retrieve_all():
    """Testing for :py:meth:`wwdtm.location.Location.retrieve_all`
    """
    location = Location(connect_dict=get_connect_dict())
    locations = location.retrieve_all()

    assert locations, "No locations could be retrieved"
    assert "id" in locations[0], "'id' was not returned for the first list item"


def test_location_retrieve_all_details():
    """Testing for :py:meth:`wwdtm.location.Location.retrieve_all_details`
    """
    location = Location(connect_dict=get_connect_dict())
    locations = location.retrieve_all_details()

    assert locations, "No locations could be retrieved"
    assert "id" in locations[0], "'id' was not returned for first list item"
    assert "recordings" in locations[0], ("'recordings' was not returned for "
                                          "the first list item")


def test_location_retrieve_all_ids():
    """Testing for :py:meth:`wwdtm.location.Location.retrieve_all_ids`
    """
    location = Location(connect_dict=get_connect_dict())
    ids = location.retrieve_all_ids()

    assert ids, "No location IDs could be retrieved"


def test_location_retrieve_all_slugs():
    """Testing for :py:meth:`wwdtm.location.Location.retrieve_all_slugs`
    """
    location = Location(connect_dict=get_connect_dict())
    slugs = location.retrieve_all_slugs()

    assert slugs, "No location slug strings could be retrieved"


@pytest.mark.parametrize("id", [95])
def test_location_retrieve_by_id(id: int):
    """Testing for :py:meth:`wwdtm.location.Location.retrieve_by_id`

    :param id: Location ID to test retrieving location information
    :type id: int
    """
    location = Location(connect_dict=get_connect_dict())
    info = location.retrieve_by_id(id)

    assert info, f"Location ID {id} not found"
    assert "venue" in info, f"'venue' was not returned for ID {id}"


@pytest.mark.parametrize("id", [95])
def test_location_retrieve_details_by_id(id: int):
    """Testing for :py:meth:`wwdtm.location.location.retrieve_details_by_id`

    :param id: Location ID to test retrieving location details
    :type id: int
    """
    location = Location(connect_dict=get_connect_dict())
    info = location.retrieve_details_by_id(id)

    assert info, f"Location ID {id} not found"
    assert "venue" in info, f"'venue' was not returned for ID {id}"
    assert "recordings" in info, f"'recordings' was not returned for ID {id}"


@pytest.mark.parametrize("slug", ["the-chicago-theatre-chicago-il"])
def test_location_retrieve_by_slug(slug: str):
    """Testing for :py:meth:`wwdtm.location.Location.retrieve_by_slug`

    :param slug: Location slug string to test retrieving location
        information
    :type slug: str
    """
    location = Location(connect_dict=get_connect_dict())
    info = location.retrieve_by_slug(slug)

    assert info, f"Location slug {slug} not found"
    assert "venue" in info, f"'venue' was not returned for slug {slug}"


@pytest.mark.parametrize("slug", ["the-chicago-theatre-chicago-il"])
def test_location_retrieve_details_by_slug(slug: str):
    """Testing for :py:meth:`wwdtm.location.Location.retrieve_details_by_slug`

    :param slug: Location slug string to test retrieving location
        details
    :type slug: str
    """
    location = Location(connect_dict=get_connect_dict())
    info = location.retrieve_details_by_slug(slug)

    assert info, f"Location slug {slug} not found"
    assert "venue" in info, f"'venue' was not returned for slug {slug}"
    assert "recordings" in info, f"'recordings' was not returned for slug {slug}"
