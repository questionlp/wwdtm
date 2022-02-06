# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
"""Testing for object: :py:class:`wwdtm.location.LocationRecordings`
"""
import json
from typing import Any, Dict

import pytest
from wwdtm.location import LocationRecordings


@pytest.mark.skip
def get_connect_dict() -> Dict[str, Any]:
    """Read in database connection settings and return values as a
    dictionary.

    :return: A dictionary containing database connection settings
        for use by mysql.connector
    """
    with open("config.json", "r") as config_file:
        config_dict = json.load(config_file)
        if "database" in config_dict:
            return config_dict["database"]


@pytest.mark.parametrize("location_id, exclude_null_dates",
                         [(95, True), (95, False)])
def test_location_recordings_retrieve_recordings_by_id(location_id: int,
                                                       exclude_null_dates: bool):
    """Testing for :py:meth:`wwdtm.location.LocationRecordings.retrieve_recordings_by_id`

    :param location_id: Location ID to test retrieving location
        recordings
    :param exclude_null_dates: Toggle whether to exclude results
        that have SQL ``NULL`` for show dates
    """
    recordings = LocationRecordings(connect_dict=get_connect_dict())
    recording = recordings.retrieve_recordings_by_id(location_id,
                                                     exclude_null_dates)

    assert "count" in recording, f"'count' was not returned for ID {location_id}"
    assert "shows" in recording, f"'shows' was not returned for ID {location_id}"


@pytest.mark.parametrize("location_slug, exclude_null_dates",
                         [("the-chicago-theatre-chicago-il", True),
                          ("the-chicago-theatre-chicago-il", False)])
def test_location_recordings_retrieve_recordings_by_slug(location_slug: str,
                                                         exclude_null_dates: bool):
    """Testing for :py:meth:`wwdtm.location.LocationRecordings.retrieve_recordings_by_slug`

    :param location_slug: Location slug string to test retrieving
        location recordings
    :param exclude_null_dates: Toggle whether to exclude results
        that have SQL ``NULL`` for show dates
    """
    recordings = LocationRecordings(connect_dict=get_connect_dict())
    recording = recordings.retrieve_recordings_by_slug(location_slug,
                                                       exclude_null_dates)

    assert "count" in recording, f"'count' was not returned for slug {location_slug}"
    assert "shows" in recording, f"'shows' was not returned for slug {location_slug}"
