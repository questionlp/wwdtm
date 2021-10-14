# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is relased under the terms of the Apache License 2.0
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
    :rtype: Dict[str, Any]
    """
    with open("config.json", "r") as config_file:
        config_dict = json.load(config_file)
        if "database" in config_dict:
            return config_dict["database"]

@pytest.mark.parametrize("id", [95])
def test_location_recordings_retrieve_recordings_by_id(id: int):
    """Testing for :py:meth:`wwdtm.location.LocationRecordings.retrieve_recordings_by_id`

    :param id: Location ID to test retrieving location recordings
    :type id: int
    """
    recordings = LocationRecordings(connect_dict=get_connect_dict())
    recording = recordings.retrieve_recordings_by_id(id)

    assert "count" in recording, f"'count' was not returned for ID {id}"
    assert "shows" in recording, f"'shows' was not returned for ID {id}"

@pytest.mark.parametrize("slug", ["the-chicago-theatre-chicago-il"])
def test_location_recordings_retrieve_recordings_by_slug(slug: str):
    """Testing for :py:meth:`wwdtm.location.LocationRecordings.retrieve_recordings_by_slug`

    :param slug: Location slug string to test retrieving location
        recordings
    :type slug: str
    """
    recordings = LocationRecordings(connect_dict=get_connect_dict())
    recording = recordings.retrieve_recordings_by_slug(slug)

    assert "count" in recording, f"'count' was not returned for slug {slug}"
    assert "shows" in recording, f"'shows' was not returned for slug {slug}"
