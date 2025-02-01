# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing for object: :py:class:`wwdtm.guest.Guest`."""

import json
from pathlib import Path
from typing import Any

import pytest

from wwdtm.guest import Guest


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


def test_guest_retrieve_all():
    """Testing for :py:meth:`wwdtm.guest.Guest.retrieve_all`."""
    guest = Guest(connect_dict=get_connect_dict())
    guests = guest.retrieve_all()

    assert guests, "No guests could be retrieved"
    assert "id" in guests[0], "'id' was not returned for the first list item"


def test_guest_retrieve_all_details():
    """Testing for :py:meth:`wwdtm.guest.Guest.retrieve_all_details`."""
    guest = Guest(connect_dict=get_connect_dict())
    guests = guest.retrieve_all_details()

    assert guests, "No guests could be retrieved"
    assert "id" in guests[0], "'id' was not returned for first list item"
    assert "appearances" in guests[0], (
        "'appearances' was not returned for the first list item"
    )


def test_guest_retrieve_all_ids():
    """Testing for :py:meth:`wwdtm.guest.Guest.retrieve_all_ids`."""
    guest = Guest(connect_dict=get_connect_dict())
    ids = guest.retrieve_all_ids()

    assert ids, "No guest IDs could be retrieved"


def test_guest_retrieve_all_slugs():
    """Testing for :py:meth:`wwdtm.guest.Guest.retrieve_all_slugs`."""
    guest = Guest(connect_dict=get_connect_dict())
    slugs = guest.retrieve_all_slugs()

    assert slugs, "No guest slug strings could be retrieved"


@pytest.mark.parametrize("guest_id", [976])
def test_guest_retrieve_by_id(guest_id: int):
    """Testing for :py:meth:`wwdtm.guest.Guest.retrieve_by_id`.

    :param guest_id: Guest ID to test retrieving guest information
    """
    guest = Guest(connect_dict=get_connect_dict())
    info = guest.retrieve_by_id(guest_id)

    assert info, f"Guest ID {guest_id} not found"
    assert "name" in info, f"'name' was not returned for ID {guest_id}"


@pytest.mark.parametrize("guest_slug", ["tom-hanks"])
def test_guest_retrieve_by_slug(guest_slug: str):
    """Testing for :py:meth:`wwdtm.guest.Guest.retrieve_by_slug`.

    :param guest_slug: Guest slug string to test retrieving guest
        information
    """
    guest = Guest(connect_dict=get_connect_dict())
    info = guest.retrieve_by_slug(guest_slug)

    assert info, f"Guest slug {guest_slug} not found"
    assert "name" in info, f"'name' was not returned for slug {guest_slug}"


@pytest.mark.parametrize("guest_id", [976])
def test_guest_retrieve_details_by_id(guest_id: int):
    """Testing for :py:meth:`wwdtm.guest.Guest.retrieve_details_by_id`.

    :param guest_id: Guest ID to test retrieving guest details
    """
    guest = Guest(connect_dict=get_connect_dict())
    info = guest.retrieve_details_by_id(guest_id)

    assert info, f"Guest ID {guest_id} not found"
    assert "name" in info, f"'name' attribute was not returned for ID {guest_id}"
    assert "appearances" in info, f"'appearances' was not returned for ID {guest_id}"


@pytest.mark.parametrize("guest_slug", ["tom-hanks"])
def test_guest_guest_retrieve_details_by_slug(guest_slug: str):
    """Testing for :py:meth:`wwdtm.guest.Guest.retrieve_details_by_slug`.

    :param guest_slug: Guest slug string to test retrieving guest details
    """
    guest = Guest(connect_dict=get_connect_dict())
    info = guest.retrieve_details_by_slug(guest_slug)

    assert info, f"Guest slug {guest_slug} not found"
    assert "name" in info, f"'name' was not returned for slug {guest_slug}"
    assert "appearances" in info, (
        f"'appearances' was not returned for slug {guest_slug}"
    )


def test_guest_retrieve_random_id() -> None:
    """Testing for :py:meth`wwdtm.guest.Guest.retrieve_random_id`."""
    guest = Guest(connect_dict=get_connect_dict())
    _id = guest.retrieve_random_id()

    assert _id, "Returned random guest ID is not valid"
    assert isinstance(_id, int), "Returned random guest ID is not an integer"


def test_guest_retrieve_random_slug() -> None:
    """Testing for :py:meth`wwdtm.guest.Guest.retrieve_random_slug`."""
    guest = Guest(connect_dict=get_connect_dict())
    _slug = guest.retrieve_random_slug()

    assert _slug, "Returned random guest slug string is not valid"
    assert isinstance(_slug, str), "Returned random guest slug string is not a string"


def test_guest_retrieve_random() -> None:
    """Testing for :py:meth:`wwdtm.guest.Guest.retrieve_random`."""
    guest = Guest(connect_dict=get_connect_dict())
    info = guest.retrieve_random()

    assert info, "Random guest not found"
    assert "name" in info, "'name' attribute was not returned for a random guest"


def test_guest_retrieve_random_details() -> None:
    """Testing for :py:meth:`wwdtm.guest.Guest.retrieve_random_details`."""
    guest = Guest(connect_dict=get_connect_dict())
    info = guest.retrieve_random_details()

    assert info, "Random guest not found"
    assert "name" in info, "'name' attribute was not returned for a random guest"
    assert "appearances" in info, "'appearances' was not returned for a random guest"
