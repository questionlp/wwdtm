# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing for object: :py:class:`wwdtm.host.HostAppearances`."""

import json
from pathlib import Path
from typing import Any

import pytest

from wwdtm.host import HostAppearances


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


@pytest.mark.parametrize("host_id", [2])
def test_host_appearances_retrieve_appearances_by_id(host_id: int):
    """Testing for :py:meth:`wwdtm.host.HostAppearances.retrieve_appearances_by_id`.

    :param host_id: Host ID to test retrieving host appearances
    """
    appearances = HostAppearances(connect_dict=get_connect_dict())
    appearance = appearances.retrieve_appearances_by_id(host_id)

    assert "count" in appearance, f"'count' was not returned for ID {host_id}"
    assert "shows" in appearance, f"'shows' was not returned for ID {host_id}"


@pytest.mark.parametrize("host_slug", ["luke-burbank"])
def test_host_appearances_retrieve_appearances_by_slug(host_slug: str):
    """Testing for :py:meth:`wwdtm.host.HostAppearances.retrieve_appearances_by_slug`.

    :param host_slug: Host slug string to test retrieving host
        appearances
    """
    appearances = HostAppearances(connect_dict=get_connect_dict())
    appearance = appearances.retrieve_appearances_by_slug(host_slug)

    assert "count" in appearance, f"'count' was not returned for slug {host_slug}"
    assert "shows" in appearance, f"'shows' was not returned for slug {host_slug}"
