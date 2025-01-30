# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing for object: :py:class:`wwdtm.pronoun.Pronouns`."""

import json
from pathlib import Path
from typing import Any

import pytest

from wwdtm.pronoun import Pronouns


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


def test_pronouns_retrieve_all():
    """Testing for :py:meth:`wwdtm.pronoun.Pronouns.retrieve_all`."""
    pn = Pronouns(connect_dict=get_connect_dict())
    all_pronouns = pn.retrieve_all()

    assert all_pronouns, "No pronouns could be retrieved"
    assert "id" in all_pronouns[0], "'id' was not returned for the first list item"
    assert "pronouns" in all_pronouns[0], (
        "'pronouns' was not returned for the first list item"
    )


def test_pronouns_retrieve_all_ids():
    """Testing for :py:meth:`wwdtm.pronoun.Pronouns.retrieve_all_ids`."""
    pn = Pronouns(connect_dict=get_connect_dict())
    ids = pn.retrieve_all_ids()

    assert ids, "No pronouns IDs could be retrieved"


def test_pronouns_retrieve_all_as_dict():
    """Testing for :py:meth:`wwdtm.pronoun.Pronouns.retrieve_all_as_dict`."""
    pn = Pronouns(connect_dict=get_connect_dict())
    all_pronouns = pn.retrieve_all_as_dict()

    assert all_pronouns, "No pronouns could be retrieved"


def test_pronouns_retrieve_all_pronouns():
    """Testing for :py:meth:`wwdtm.pronoun.Pronouns.retrieve_all_pronouns`."""
    pn = Pronouns(connect_dict=get_connect_dict())
    all_pronouns = pn.retrieve_all_pronouns()

    assert all_pronouns, "No pronouns strings could be retrieved"


@pytest.mark.parametrize("pronouns_id", [1])
def test_pronouns_retrieve_by_id(pronouns_id: int):
    """Testing for :py:meth:`wwdtm.pronoun.Pronouns.retrieve_by_id`.

    :param pronouns_id: Pronouns ID to test retrieving pronouns
        information
    """
    pn = Pronouns(connect_dict=get_connect_dict())
    info = pn.retrieve_by_id(pronouns_id)

    assert info, f"Pronouns ID {pronouns_id} not found"
    assert "id" in info, f"'id' was not returned for ID {pronouns_id}"
    assert "pronouns" in info, f"'pronouns' was not returned for ID {pronouns_id}"
