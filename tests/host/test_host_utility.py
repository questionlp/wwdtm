# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is relased under the terms of the Apache License 2.0
"""Testing for object: :py:class:`wwdtm.host.HostUtility`
"""
import json
from typing import Any, Dict

import pytest
from wwdtm.host import HostUtility

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

@pytest.mark.parametrize("id", [2])
def test_host_utility_convert_id_to_slug(id: int):
    """Testing for :py:meth:`wwdtm.host.HostUtility.convert_id_to_slug`

    :param id: Host ID to test converting into host slug string
    :type id: int
    """
    utility = HostUtility(connect_dict=get_connect_dict())
    slug = utility.convert_id_to_slug(id)

    assert slug, f"Host slug for ID {id} was not found"
    assert isinstance(slug, str), f"Invalid value returned for ID {id}"

@pytest.mark.parametrize("id", [-1])
def test_host_utility_convert_invalid_id_to_slug(id: int):
    """Negative testing for :py:meth:`wwdtm.host.HostUtility.convert_id_to_slug`

    :param id: Host ID to test failing to convert into host slug string
    :type id: int
    """
    utility = HostUtility(connect_dict=get_connect_dict())
    slug = utility.convert_id_to_slug(id)

    assert not slug, f"Host slug for ID {id} was found"

@pytest.mark.parametrize("slug", ["tom-hanks"])
def test_host_utility_convert_slug_to_id(slug: str):
    """Testing for :py:meth:`wwdtm.host.HostUtility.convert_slug_to_id`

    :param slug: Host slug string to test converting into host ID
    :type slug: str
    """
    utility = HostUtility(connect_dict=get_connect_dict())
    id = utility.convert_slug_to_id(slug)

    assert id, f"Host ID for slug {slug} was not found"
    assert isinstance(id, int), f"Invalid value returned for slug {slug}"

@pytest.mark.parametrize("slug", ["tom-hanx"])
def test_host_utility_convert_invalid_slug_to_id(slug: str):
    """Negative testing for :py:meth:`wwdtm.host.HostUtility.convert_slug_to_id`

    :param slug: Host slug string to test failing to convert into host
        ID
    :type slug: str
    """
    utility = HostUtility(connect_dict=get_connect_dict())
    result = utility.convert_slug_to_id(slug)

    assert not result, f"Host ID for slug {slug} found"

@pytest.mark.parametrize("id", [2])
def test_host_utility_id_exists(id: int):
    """Testing for :py:meth:`wwdtm.host.HostUtility.id_exists`

    :param id: Host ID to test if a host exists
    :type id: int
    """
    utility = HostUtility(connect_dict=get_connect_dict())
    result = utility.id_exists(id)

    assert result, f"Host ID {id} does not exist"

@pytest.mark.parametrize("id", [-1])
def test_host_utility_id_not_exists(id: int):
    """Negative testing for :py:meth:`wwdtm.host.HostUtility.id_exists()`

    :param id: Host ID to test if a host does not exist
    :type id: int
    """
    utility = HostUtility(connect_dict=get_connect_dict())
    result = utility.id_exists(id)

    assert not result, f"Host ID {id} exists"

@pytest.mark.parametrize("slug", ["tom-hanks"])
def test_host_utility_slug_exists(slug: str):
    """Testing for :py:meth:`wwdtm.host.HostUtility.slug_exists`

    :param slug: Host slug string to test if a host exists
    :type slug: str
    """
    utility = HostUtility(connect_dict=get_connect_dict())
    result = utility.slug_exists(slug)

    assert result, f"Host slug {slug} does not exist"

@pytest.mark.parametrize("slug", ["tom-hanx"])
def test_host_utility_slug_not_exists(slug: str):
    """Negative testing for :py:meth:`wwdtm.host.HostUtility.slug_exists`

    :param slug: Host slug string to test if a host does not exist
    :type slug: str
    """
    utility = HostUtility(connect_dict=get_connect_dict())
    result = utility.slug_exists(slug)

    assert not result, f"Host slug {slug} exists"
