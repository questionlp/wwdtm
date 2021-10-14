# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is relased under the terms of the Apache License 2.0
"""Testing for object: :py:class:`wwdtm.host.HostAppearances`
"""
import json
from typing import Any, Dict

import pytest
from wwdtm.host import HostAppearances

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
def test_host_appearances_retrieve_appearances_by_id(id: int):
    """Testing for :py:meth:`wwdtm.host.HostAppearances.retrieve_appearances_by_id`

    :param id: Host ID to test retrieving host appearances
    :type id: int
    """
    appearances = HostAppearances(connect_dict=get_connect_dict())
    appearance = appearances.retrieve_appearances_by_id(id)

    assert "count" in appearance, f"'count' was not returned for ID {id}"
    assert "shows" in appearance, f"'shows' was not returned for ID {id}"

@pytest.mark.parametrize("slug", ["luke-burbank"])
def test_host_appearances_retrieve_appearances_by_slug(slug: str):
    """Testing for :py:meth:`wwdtm.host.HostAppearances.retrieve_appearances_by_slug`

    :param slug: Host slug string to test retrieving host appearances
    :type slug: str
    """
    appearances = HostAppearances(connect_dict=get_connect_dict())
    appearance = appearances.retrieve_appearances_by_slug(slug)

    assert "count" in appearance, f"'count' was not returned for slug {slug}"
    assert "shows" in appearance, f"'shows' was not returned for slug {slug}"
