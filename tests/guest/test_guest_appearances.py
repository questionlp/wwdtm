# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing for object: :py:class:`wwdtm.guest.GuestAppearances`."""

import json
from pathlib import Path
from typing import Any

import pytest

from wwdtm.guest import GuestAppearances


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


@pytest.mark.parametrize("guest_id", [976])
def test_guest_appearances_retrieve_appearances_by_id(guest_id: int):
    """Testing for :py:meth:`wwdtm.guest.Appearances.retrieve_appearances_by_id`.

    :param guest_id: Guest ID to test retrieving guest appearances
    """
    appearances = GuestAppearances(connect_dict=get_connect_dict())
    appearance = appearances.retrieve_appearances_by_id(guest_id)

    assert "count" in appearance, f"'count' was not returned for ID {guest_id}"
    assert "shows" in appearance, f"'shows' was not returned for ID {guest_id}"


@pytest.mark.parametrize("guest_slug", ["tom-hanks"])
def test_guest_appearances_retrieve_appearances_by_slug(guest_slug: str):
    """Testing for :py:meth:`wwdtm.guest.Appearances.retrieve_appearances_by_slug`.

    :param guest_slug: Guest slug string to test retrieving guest appearances
    """
    appearances = GuestAppearances(connect_dict=get_connect_dict())
    appearance = appearances.retrieve_appearances_by_slug(guest_slug)

    assert "count" in appearance, f"'count' was not returned for slug {guest_slug}"
    assert "shows" in appearance, f"'shows' was not returned for slug {guest_slug}"
