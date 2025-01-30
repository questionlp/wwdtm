# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing for object: :py:class:`wwdtm.location.LocationUtility`."""

import json
from pathlib import Path
from typing import Any

import pytest

from wwdtm.location import LocationUtility


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


@pytest.mark.parametrize("location_id", [95])
def test_location_utility_convert_id_to_slug(location_id: int):
    """Testing for :py:meth:`wwdtm.location.LocationUtility.convert_id_to_slug`.

    :param location_id: Location ID to test converting into location
        slug string
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    slug = utility.convert_id_to_slug(location_id)

    assert slug, f"Location slug for ID {location_id} was not found"


@pytest.mark.parametrize("location_id", [-1])
def test_location_utility_convert_invalid_id_to_slug(location_id: int):
    """Negative testing for :py:meth:`wwdtm.location.LocationUtility.convert_id_to_slug`.

    :param location_id: Location ID to test failing to convert into
        location slug string
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    slug = utility.convert_id_to_slug(location_id)

    assert not slug, f"Location slug for ID {location_id} was found"


@pytest.mark.parametrize("location_slug", ["the-chicago-theatre-chicago-il"])
def test_location_utility_convert_slug_to_id(location_slug: str):
    """Testing for :py:meth:`wwdtm.location.LocationUtility.convert_slug_to_id`.

    :param location_slug: Location slug string to test converting into
        location ID
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    id_ = utility.convert_slug_to_id(location_slug)

    assert id_, f"Location ID for slug {location_slug} was not found"


@pytest.mark.parametrize("location_slug", ["the-chicago-theatre-chicago-li"])
def test_location_utility_convert_invalid_slug_to_id(location_slug: str):
    """Negative testing for :py:meth:`wwdtm.location.LocationUtility.convert_slug_to_id`.

    :param location_slug: Location slug string to test failing to
        convert into location ID
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    id_ = utility.convert_slug_to_id(location_slug)

    assert not id_, f"Location ID for slug {location_slug} was found"


@pytest.mark.parametrize("location_id", [95])
def test_location_utility_id_exists(location_id: int):
    """Testing for :py:meth:`wwdtm.location.LocationUtility.id_exists`.

    :param location_id: Location ID to test if a location exists
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    result = utility.id_exists(location_id)

    assert result, f"Location ID {location_id} does not exist"


@pytest.mark.parametrize("location_id", [-1])
def test_location_utility_id_not_exists(location_id: int):
    """Negative testing for :py:meth:`wwdtm.location.LocationUtility.id_exists`.

    :param location_id: Location ID to test if a location does not exist
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    result = utility.id_exists(location_id)

    assert not result, f"Location ID {location_id} exists"


@pytest.mark.parametrize("location_slug", ["the-chicago-theatre-chicago-il"])
def test_location_utility_slug_exists(location_slug: str):
    """Testing for :py:meth:`wwdtm.location.LocationUtility.slug_exists`.

    :param location_slug: Location slug string to test if a location
        exists
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    result = utility.slug_exists(location_slug)

    assert result, f"Location slug {location_slug} does not exist"


@pytest.mark.parametrize("location_slug", ["the-chicago-theatre-chicago-li"])
def test_location_utility_slug_not_exists(location_slug: str):
    """Testing for :py:meth:`wwdtm.location.LocationUtility.slug_exists` with venue name.

    :param location_slug: Location slug string to test if a location
        does not exists
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    result = utility.slug_exists(location_slug)

    assert not result, f"Location slug {location_slug} exists"


@pytest.mark.parametrize("city", ["Chicago"])
def test_location_utility_slugify_location_city(city: str):
    """Negative testing for :py:meth:`wwdtm.location.LocationUtility.slugify_location`.

    Testing with city name.

    :param city: City to include in the slug string
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    with pytest.raises(ValueError) as exception_info:
        _ = utility.slugify_location(city=city)

    assert str(exception_info.value) == "Invalid location information provided"


@pytest.mark.parametrize("city, state", [("Chicago", "IL")])
def test_location_utility_slugify_location_city_state(city: str, state: str):
    """Negative testing for :py:meth:`wwdtm.location.LocationUtility.slugify_location`.

    Testing with city and state names.

    :param city: City to include in the slug string
    :param state: State to include in the slug string
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    with pytest.raises(ValueError) as exception_info:
        _ = utility.slugify_location(city=city, state=state)

    assert str(exception_info.value) == "Invalid location information provided"


@pytest.mark.parametrize(
    "location_id, venue, city, state", [(2, "Chase Auditorium", "Chicago", "IL")]
)
def test_location_utility_slugify_location_full(
    location_id: int, venue: str, city: str, state: str
):
    """Testing for :py:meth:`wwdtm.location.LocationUtility.slugify_location`.

    Testing with location ID, venue, city and state names.

    :param location_id: Location ID to include in the slug string
    :param venue: Venue name to include in the slug string
    :param city: City to include in the slug string
    :param state: State to include in the slug string
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    slug = utility.slugify_location(
        location_id=location_id, venue=venue, city=city, state=state
    )

    assert slug, "Unable to convert into a slug string"
    assert isinstance(slug, str), "Value returned is not a string"


@pytest.mark.parametrize("location_id, venue", [(2, "Chase Auditorium")])
def test_location_utility_slugify_location_venue(location_id: int, venue: str):
    """Testing for :py:meth:`wwdtm.location.LocationUtility.slugify_location` with venue name.

    :param location_id: Location ID to include in the slug string
    :param venue: Venue name to include in the slug string
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    slug = utility.slugify_location(location_id=location_id, venue=venue)

    assert slug, "Unable to convert into a slug string"
    assert isinstance(slug, str), "Value returned is not a string"


@pytest.mark.parametrize("venue, city, state", [("Chase Auditorium", "Chicago", "IL")])
def test_location_utility_slugify_location_venue_city_state(
    venue: str, city: str, state: str
):
    """Testing for :py:meth:`wwdtm.location.LocationUtility.slugify_location`.

    :param venue: Venue name to include in the slug string
    :param city: City to include in the slug string
    :param state: State to include in the slug string
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    slug = utility.slugify_location(venue=venue, city=city, state=state)

    assert slug, "Unable to convert into a slug string"
    assert isinstance(slug, str), "Value returned is not a string"


@pytest.mark.parametrize("location_id", [2])
def test_location_utility_slugify_location_id(location_id: int):
    """Testing for :py:meth:`wwdtm.location.LocationUtility.slugify_location` with venue, city and state names.

    :param location_id: Location ID to include in the slug string
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    slug = utility.slugify_location(location_id=location_id)

    assert slug, "Unable to convert into a slug string"
    assert isinstance(slug, str), "Value returned is not a string"
