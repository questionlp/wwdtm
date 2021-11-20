# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
"""Testing for object :py:class:`wwdtm.show.ShowUtility`
"""
import json
from typing import Any, Dict

import pytest
from wwdtm.show import ShowUtility


@pytest.mark.skip
def get_connect_dict() -> Dict[str, Any]:
    """Read in database connection settings and return values as a
    dictionary.
    """
    with open("config.json", "r") as config_file:
        config_dict = json.load(config_file)
        if "database" in config_dict:
            return config_dict["database"]


@pytest.mark.parametrize("year, month, day", [(2018, 10, 27)])
def test_show_utility_convert_date_to_id(year: int,
                                         month: int,
                                         day: int):
    """Testing for :py:meth:`wwdtm.show.ShowUtility.convert_date_to_id`

    :param year: Four digit year to test converting into show ID
    :type year: int
    :param month: One or two digit month to test converting into show ID
    :type month: int
    :param day: One or two digit day to test converting into show ID
    :type day: int
    """
    utility = ShowUtility(connect_dict=get_connect_dict())
    id = utility.convert_date_to_id(year, month, day)

    assert id, f"Show ID for date {year:04d}-{month:02d}-{day:02d} not found"
    assert isinstance(id, int), (f"Invalid value returned for date "
                                 f"{year:04d}-{month:02d}-{day:02d}")


@pytest.mark.parametrize("year, month, day", [(2018, 10, 26)])
def test_show_utility_convert_invalid_date_to_id(year: int,
                                                 month: int,
                                                 day: int):
    """Negative testing for :py:meth:`wwdtm.show.ShowUtility.convert_date_to_id`

    :param year: Four digit year to test failing to convert into show ID
    :type year: int
    :param month: One or two digit month to test failing to convert
        into show ID
    :type month: int
    :param day: One or two digit day to test failing to convert into
        show ID
    :type day: int
    """
    utility = ShowUtility(connect_dict=get_connect_dict())
    id = utility.convert_date_to_id(year, month, day)

    assert not id, f"Show ID for date {year:04d}-{month:02d}-{day:02d} was found"


@pytest.mark.parametrize("id", [1162])
def test_show_utility_convert_id_to_date(id: int):
    """Testing for :py:meth:`wwdtm.show.ShowUtility.convert_id_to_date`

    :param id: Show ID to test converting into show date
    :type id: int
    """
    utility = ShowUtility(connect_dict=get_connect_dict())
    date = utility.convert_id_to_date(id)

    assert date, f"Show date for ID {id} was not found"
    assert isinstance(date, str), f"Invalid value returned for ID {date}"


@pytest.mark.parametrize("id", [-1])
def test_show_utility_convert_invalid_id_to_date(id: int):
    """Negative testing for :py:meth:`wwdtm.show.ShowUtility.convert_id_to_date`

    :param id: Show ID to test failing to convert into show date
    :type id: int
    """
    utility = ShowUtility(connect_dict=get_connect_dict())
    date = utility.convert_id_to_date(id)

    assert not date, f"Show date for ID {id} was found"


@pytest.mark.parametrize("year, month, day", [(2020, 4, 25)])
def test_show_utility_date_exists(year: int,
                                  month: int,
                                  day: int):
    """Testing for :py:meth:`wwdtm.show.ShowUtility.date_exists`

    :param year: Four digit year to test if a show exists
    :type year: int
    :param month: One or two digit month to test if a show exists
    :type month: int
    :param day: One or two digit day to test if a show exists
    :type day: int
    """
    utility = ShowUtility(connect_dict=get_connect_dict())
    result = utility.date_exists(year, month, day)

    assert result, f"Show date {year:04d}-{month:02d}-{day:02d} was not found"


@pytest.mark.parametrize("year, month, day", [(2020, 4, 24)])
def test_show_utility_date_not_exists(year: int,
                                      month: int,
                                      day: int):
    """Negative testing for :py:meth:`wwdtm.show.ShowUtility.date_exists`

    :param year: Four digit year to test if a show does not exist
    :type year: int
    :param month: One or two digit month to test if a show does not
        exist
    :type month: int
    :param day: One or two digit day to test if a show does not exist
    :type day: int
    """
    utility = ShowUtility(connect_dict=get_connect_dict())
    result = utility.date_exists(year, month, day)

    assert not result, f"Show date {year:04d}-{month:02d}-{day:02d} was found"


@pytest.mark.parametrize("id", [1162])
def test_show_utility_id_exists(id: int):
    """Testing for :py:meth:`wwdtm.show.ShowUtility.id_exists`

    :param id: Show ID to test if a show exists
    :type id: int
    """
    utility = ShowUtility(connect_dict=get_connect_dict())
    result = utility.id_exists(id)

    assert result, f"Show ID {id} was not found"


@pytest.mark.parametrize("id", [-1])
def test_show_utility_id_not_exists(id: int):
    """Negative testing for :py:meth:`wwdtm.show.ShowUtility.id_exists`

    :param id: Show ID to test if a show does not exist
    :type id: int
    """
    utility = ShowUtility(connect_dict=get_connect_dict())
    result = utility.id_exists(id)

    assert not result, f"Show ID {id} was found"
