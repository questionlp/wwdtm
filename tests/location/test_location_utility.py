# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is relased under the terms of the Apache License 2.0
"""Testing for object: :py:class:`wwdtm.location.LocationUtility`
"""
import json
from typing import Any, Dict

import pytest
from wwdtm.location import LocationUtility

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

@pytest.mark.parametrize("id", [95])
def test_location_utility_convert_id_to_slug(id: int):
    """Testing for :py:meth:`wwdtm.location.LocationUtility.convert_id_to_slug`

    :param id: Location ID to test converting into location slug string
    :type id: int
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    slug = utility.convert_id_to_slug(id)

    assert slug, f"Location slug for ID {id} was not found"

@pytest.mark.parametrize("id", [-1])
def test_location_utility_convert_invalid_id_to_slug(id: int):
    """Negative testing for :py:meth:`wwdtm.location.LocationUtility.convert_id_to_slug`

    :param id: Location ID to test failing to convert into location
        slug string
    :type id: int
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    slug = utility.convert_id_to_slug(id)

    assert not slug, f"Location slug for ID {id} was found"

@pytest.mark.parametrize("slug", ["the-chicago-theatre-chicago-il"])
def test_location_utility_convert_slug_to_id(slug: str):
    """Testing for :py:meth:`wwdtm.location.LocationUtility.convert_slug_to_id`

    :param slug: Location slug string to test converting into location
        ID
    :type slug: str
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    id = utility.convert_slug_to_id(slug)

    assert id, f"Location ID for slug {slug} was not found"

@pytest.mark.parametrize("slug", ["the-chicago-theatre-chicago-li"])
def test_location_utility_convert_invalid_slug_to_id(slug: str):
    """Negative testing for :py:meth:`wwdtm.location.LocationUtility.convert_slug_to_id`

    :param slug: Location slug string to test failing to convert into
        location ID
    :type slug: str
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    id = utility.convert_slug_to_id(slug)

    assert not id, f"Location ID for slug {slug} was found"

@pytest.mark.parametrize("id", [95])
def test_location_utility_id_exists(id: int):
    """Testing for :py:meth:`wwdtm.location.LocationUtility.id_exists`

    :param id: Location ID to test if a location exists
    :type id: int
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    result = utility.id_exists(id)

    assert result, f"Location ID {id} does not exist"

@pytest.mark.parametrize("id", [-1])
def test_location_utility_id_not_exists(id: int):
    """Negative testing for :py:meth:`wwdtm.location.LocationUtility.id_exists`

    :param id: Location ID to test if a location does not exist
    :type id: int
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    result = utility.id_exists(id)

    assert not result, f"Location ID {id} exists"

@pytest.mark.parametrize("slug", ["the-chicago-theatre-chicago-il"])
def test_location_utility_slug_exists(slug: str):
    """Testing for :py:meth:`wwdtm.location.LocationUtility.slug_exists`

    :param slug: Location slug string to test if a location exists
    :type slug: str
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    result = utility.slug_exists(slug)

    assert result, f"Location slug {slug} does not exist"

@pytest.mark.parametrize("slug", ["the-chicago-theatre-chicago-li"])
def test_location_utility_slug_not_exists(slug: str):
    """Testing for :py:meth:`wwdtm.location.LocationUtility.slug_exists`
    with venue name

    :param slug: Location slug string to test if a location
        does not exists
    :type slug: str
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    result = utility.slug_exists(slug)

    assert not result, f"Location slug {slug} exists"

@pytest.mark.parametrize("city",
                         ["Chicago"])
def test_location_utility_slugify_location_city(city: str):
    """Negative testing for :py:meth:`wwdtm.location.LocationUtility.slugify_location`
    with city name

    :param city: City to include in the slug string
    :type city: str
    """
    with pytest.raises(ValueError):
        utility = LocationUtility(connect_dict=get_connect_dict())
        slug = utility.slugify_location(city=city)

@pytest.mark.parametrize("city, state",
                         [("Chicago", "IL")])
def test_location_utility_slugify_location_city_state(city: str, state: str):
    """Negative testing for :py:meth:`wwdtm.location.LocationUtility.slugify_location`
    with city and state names

    :param city: City to include in the slug string
    :type city: str
    :param state: State to include in the slug string
    :type state: str
    """
    with pytest.raises(ValueError):
        utility = LocationUtility(connect_dict=get_connect_dict())
        slug = utility.slugify_location(city=city, state=state)

@pytest.mark.parametrize("id, venue, city, state",
                         [("2", "Chase Auditorium", "Chicago", "IL")])
def test_location_utility_slugify_location_full(id: int,
                                                venue: str,
                                                city: str,
                                                state: str):
    """Testing for :py:meth:`wwdtm.location.LocationUtility.slugify_location`
    with location ID, venue, city and state names

    :param id: Location ID to include in the slug string
    :type id: int
    :param venue: Venue name to include in the slug string
    :type venue: str
    :param city: City to include in the slug string
    :type city: str
    :param state: State to include in the slug string
    :type state: str
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    slug = utility.slugify_location(id=id, venue=venue, city=city, state=state)

    assert slug, "Unable to convert into a slug string"
    assert isinstance(slug, str), "Value returned is not a string"

@pytest.mark.parametrize("venue", ["Chase Auditorium"])
def test_location_utility_slugify_location_venue(venue: str):
    """Testing for :py:meth:`wwdtm.location.LocationUtility.slugify_location`
    with venue name

    :param venue: Venue name to include in the slug string
    :type venue: str
    :param city: City to include in the slug string
    :type city: str
    :param state: State to include in the slug string
    :type state: str
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    slug = utility.slugify_location(venue=venue)

    assert slug, "Unable to convert into a slug string"
    assert isinstance(slug, str), "Value returned is not a string"


@pytest.mark.parametrize("venue, city, state",
                         [("Chase Auditorium", "Chicago", "IL")])
def test_location_utility_slugify_location_venue_city_state(venue: str,
                                                            city: str,
                                                            state: str):
    """Testing for :py:meth:`wwdtm.location.LocationUtility.slugify_location`

    :param venue: Venue name to include in the slug string
    :type venue: str
    :param city: City to include in the slug string
    :type city: str
    :param state: State to include in the slug string
    :type state: str
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    slug = utility.slugify_location(venue=venue, city=city, state=state)

    assert slug, "Unable to convert into a slug string"
    assert isinstance(slug, str), "Value returned is not a string"

@pytest.mark.parametrize("id", [2])
def test_location_utility_slugify_location_id(id: int):
    """Testing for :py:meth:`wwdtm.location.LocationUtility.slugify_location`
    with venue, city and state names

    :param id: Location ID to include in the slug string
    :type id: int
    """
    utility = LocationUtility(connect_dict=get_connect_dict())
    slug = utility.slugify_location(id=id)

    assert slug, "Unable to convert into a slug string"
    assert isinstance(slug, str), "Value returned is not a string"
