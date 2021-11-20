# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
"""Testing for object: :py:class:`wwdtm.scorekeeper.ScorekeeperUtility`
"""
import json
from typing import Any, Dict

import pytest
from wwdtm.scorekeeper import ScorekeeperUtility


@pytest.mark.skip
def get_connect_dict() -> Dict[str, Any]:
    """Read in database connection settings and return values as a
    dictionary.
    """
    with open("config.json", "r") as config_file:
        config_dict = json.load(config_file)
        if "database" in config_dict:
            return config_dict["database"]


@pytest.mark.parametrize("id", [2])
def test_scorekeeper_utility_convert_id_to_slug(id: int):
    """Testing for :py:meth:`wwdtm.scorekeeper.ScorekeeperUtility.convert_id_to_slug`

    :param id: Scorekeeper ID to test converting into scorekeeper slug
        string
    :type id: int
    """
    utility = ScorekeeperUtility(connect_dict=get_connect_dict())
    slug = utility.convert_id_to_slug(id)

    assert slug, f"Scorekeeper slug for ID {id} was not found"
    assert isinstance(slug, str), f"Invalid value returned for ID {id}"


@pytest.mark.parametrize("id", [-1])
def test_scorekeeper_utility_convert_invalid_id_to_slug(id: int):
    """Negative testing for :py:meth:`wwdtm.scorekeeper.ScorekeeperUtility.convert_id_to_slug`

    :param id: Scorekeeper ID to test failing to convert into
        scorekeeper slug string
    :type id: int
    """
    utility = ScorekeeperUtility(connect_dict=get_connect_dict())
    slug = utility.convert_id_to_slug(id)

    assert not slug, f"Scorekeeper slug for ID {id} was found"


@pytest.mark.parametrize("slug", ["korva-coleman"])
def test_scorekeeper_utility_convert_slug_to_id(slug: str):
    """Testing for :py:meth:`wwdtm.scorekeeper.ScorekeeperUtility.convert_slug_to_id`

    :param slug: Scorekeeper slug string to test converting into
        scorekeeper ID
    :type slug: str
    """
    utility = ScorekeeperUtility(connect_dict=get_connect_dict())
    id = utility.convert_slug_to_id(slug)

    assert id, f"Scorekeeper ID for slug {slug} was found"
    assert isinstance(id, int), f"Invalid value returned for slug {slug}"


@pytest.mark.parametrize("slug", ["corva-coleman"])
def test_scorekeeper_utility_convert_invalid_slug_to_id(slug: str):
    """Negative testing for :py:meth:`wwdtm.scorekeeper.ScorekeeperUtility.convert_slug_to_id`

    :param slug: Scorekeeper slug string to test failing to convert
        into scorekeeper ID
    :type slug: str
    """
    utility = ScorekeeperUtility(connect_dict=get_connect_dict())
    slug = utility.convert_slug_to_id(slug)

    assert not slug, f"Scorekeeper ID for slug {slug} was not found"


@pytest.mark.parametrize("id", [2])
def test_scorekeeper_utility_id_exists(id: int):
    """Testing for :py:meth:`wwdtm.scorekeeper.ScorekeeperUtility.id_exists`

    :param id: Scorekeeper ID to test if a scorekeeper exists
    :type id: int
    """
    utility = ScorekeeperUtility(connect_dict=get_connect_dict())
    result = utility.id_exists(id)

    assert result, f"Scorekeeper ID {id} does not exist"


@pytest.mark.parametrize("id", [-1])
def test_scorekeeper_utility_id_not_exists(id: int):
    """Negative testing for :py:meth:`wwdtm.scorekeeper.ScorekeeperUtility.id_exists`

    :param id: Scorekeeper ID to test if a scorekeeper does not exist
    :type id: int
    """
    utility = ScorekeeperUtility(connect_dict=get_connect_dict())
    result = utility.id_exists(id)

    assert not result, f"Scorekeeper ID {id} exists"


@pytest.mark.parametrize("slug", ["korva-coleman"])
def test_scorekeeper_utility_slug_exists(slug: str):
    """Testing for :py:meth:`wwdtm.scorekeeper.ScorekeeperUtility.slug_exists`

    :param slug: Scorekeeper slug string to test if a scorekeeper exists
    :type slug: str
    """
    utility = ScorekeeperUtility(connect_dict=get_connect_dict())
    result = utility.slug_exists(slug)

    assert result, f"Scorekeeper slug {slug} does not exist"


@pytest.mark.parametrize("slug", ["corva-coleman"])
def test_scorekeeper_utility_slug_not_exists(slug: str):
    """Negative testing for :py:meth:`wwdtm.scorekeeper.ScorekeeperUtility.slug_exists`

    :param slug: Scorekeeper slug string to test if a scorekeeper does
        not exist
    :type slug: str
    """
    utility = ScorekeeperUtility(connect_dict=get_connect_dict())
    result = utility.slug_exists(slug)

    assert not result, f"Scorekeeper slug {slug} exists"
