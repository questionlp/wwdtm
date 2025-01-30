# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing for object: :py:class:`wwdtm.location.LocationRecordings`."""

import json
from pathlib import Path
from typing import Any

import pytest

from wwdtm.location import LocationRecordings


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
def test_location_recordings_retrieve_recordings_by_id(location_id: int):
    """Testing for :py:meth:`wwdtm.location.LocationRecordings.retrieve_recordings_by_id`.

    :param location_id: Location ID to test retrieving location
        recordings
    """
    recordings = LocationRecordings(connect_dict=get_connect_dict())
    recording = recordings.retrieve_recordings_by_id(location_id)

    assert "count" in recording, f"'count' was not returned for ID {location_id}"
    assert "shows" in recording, f"'shows' was not returned for ID {location_id}"


@pytest.mark.parametrize("location_slug", ["the-chicago-theatre-chicago-il"])
def test_location_recordings_retrieve_recordings_by_slug(location_slug: str):
    """Testing for :py:meth:`wwdtm.location.LocationRecordings.retrieve_recordings_by_slug`.

    :param location_slug: Location slug string to test retrieving
        location recordings
    """
    recordings = LocationRecordings(connect_dict=get_connect_dict())
    recording = recordings.retrieve_recordings_by_slug(location_slug)

    assert "count" in recording, f"'count' was not returned for slug {location_slug}"
    assert "shows" in recording, f"'shows' was not returned for slug {location_slug}"
