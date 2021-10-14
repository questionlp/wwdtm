# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is relased under the terms of the Apache License 2.0
"""Testing for object: :py:class:`wwdtm.scorekeeper.ScorekeeperAppearances`
"""
import json
from typing import Any, Dict

import pytest
from wwdtm.scorekeeper import ScorekeeperAppearances

@pytest.mark.skip
def get_connect_dict() -> Dict[str, Any]:
    """Read in database connection settings and return values as a
    dictionary.
    """
    with open("config.json", "r") as config_file:
        config_dict = json.load(config_file)
        if "database" in config_dict:
            return config_dict["database"]

@pytest.mark.parametrize("id", [13])
def test_scorekeeper_appearance_retrieve_appearances_by_id(id: int):
    """Testing for :py:meth:`wwdtm.scorekeeper.ScorekeeperAppearances.retrieve_appearances_by_id`

    :param id: Scorekeeper ID to test retrieving scorekeeper
        appearances
    :type id: int
    """
    appearances = ScorekeeperAppearances(connect_dict=get_connect_dict())
    appearance = appearances.retrieve_appearances_by_id(id)

    assert "count" in appearance, f"'count' was not returned for ID {id}"
    assert "shows" in appearance, f"'shows' was not returned for ID {id}"

@pytest.mark.parametrize("slug", ["chioke-i-anson"])
def test_scorekeeper_appearance_retrieve_appearances_by_slug(slug: str):
    """Testing for :py:meth:`wwdtm.scorekeeper.ScorekeeperAppearances.retrieve_appearances_by_slug`

    :param slug: Scorekeeper slug string to test retrieving scorekeeper
        appearances
    :type slug: str
    """
    appearances = ScorekeeperAppearances(connect_dict=get_connect_dict())
    appearance = appearances.retrieve_appearances_by_slug(slug)

    assert "count" in appearance, f"'count' was not returned for slug {slug}"
    assert "shows" in appearance, f"'shows' was not returned for slug {slug}"
