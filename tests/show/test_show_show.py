# Copyright (c) 2018-2023 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing for object :py:class:`wwdtm.show.Show`.
"""
import json
from pathlib import Path
from typing import Any, Dict

import pytest

from wwdtm.show import Show


@pytest.mark.skip
def get_connect_dict() -> Dict[str, Any]:
    """Read in database connection settings.
    """
    file_path = Path.cwd() / "config.json"
    with file_path.open(mode="r", encoding="utf-8") as config_file:
        config_dict = json.load(config_file)
        if "database" in config_dict:
            return config_dict["database"]


def test_show_retrieve_all():
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_all`.
    """
    show = Show(connect_dict=get_connect_dict())
    shows = show.retrieve_all()

    assert shows, "No shows could be retrieved"
    assert "id" in shows[0], "No Show ID returned for the first list item"


@pytest.mark.parametrize("include_decimal_scores", [True, False])
def test_show_retrieve_all_details(include_decimal_scores: bool):
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_all_details`.

    :param include_decimal_scores: Flag set to include decimal score columns
        and values
    """
    show = Show(connect_dict=get_connect_dict())
    shows = show.retrieve_all_details(include_decimal_scores=include_decimal_scores)

    assert shows, "No shows could be retrieved"
    assert "date" in shows[0], "'date' was not returned for the first list item"
    assert "host" in shows[0], "'host' was not returned for first list item"


def test_show_retrieve_all_ids():
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_all_ids`.
    """
    show = Show(connect_dict=get_connect_dict())
    ids = show.retrieve_all_ids()

    assert ids, "No show IDs could be retrieved"


def test_show_retrieve_all_dates():
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_all_dates`.
    """
    show = Show(connect_dict=get_connect_dict())
    dates = show.retrieve_all_dates()

    assert dates, "No show dates could be retrieved"


def test_show_retrieve_all_dates_tuple():
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_all_dates_tuple`.
    """
    show = Show(connect_dict=get_connect_dict())
    dates = show.retrieve_all_dates_tuple()

    assert dates, "No show dates could be retrieved"
    assert isinstance(dates[0], tuple), "First list item is not a tuple"


def test_show_retrieve_all_show_years_months():
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_all_show_years_months`.
    """
    show = Show(connect_dict=get_connect_dict())
    dates = show.retrieve_all_show_years_months()

    assert dates, "No dates could be retrieved"
    assert isinstance(dates[0], str), "First list item is not a string"


def test_show_retrieve_all_show_years_months_tuple():
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_all_shows_years_months_tuple`.
    """
    show = Show(connect_dict=get_connect_dict())
    dates = show.retrieve_all_shows_years_months_tuple()

    assert dates, "No dates could be retrieved"
    assert isinstance(dates[0], tuple), "First list item is not a tuple"


@pytest.mark.parametrize("year, month, day", [(2020, 4, 25)])
def test_show_retrieve_by_date(year: int, month: int, day: int):
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_by_date`.

    :param year: Four digit year to test retrieving a show's information
    :param month: One or two digit month to test retrieving a show's
        information
    :param day: One or two digit day to test retrieving a show's
        information
    """
    show = Show(connect_dict=get_connect_dict())
    info = show.retrieve_by_date(year, month, day)

    assert info, f"Show for date {year:04d}-{month:02d}-{day:02d} not found"
    assert "date" in info, (
        f"'date' was not returned for show {year:04d}-{month:02d}-{day:02d}"
    )


@pytest.mark.parametrize("date", ["2018-10-27"])
def test_show_retrieve_by_date_string(date: str):
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_by_date_string`.

    :param date: Show date string in ``YYYY-MM-DD`` format to test
        retrieving a show's information
    """
    show = Show(connect_dict=get_connect_dict())
    info = show.retrieve_by_date_string(date)

    assert info, f"Show for date {date} not found"
    assert "date" in info, f"'date' was not returned for show {date}"


@pytest.mark.parametrize("show_id", [1162])
def test_show_retrieve_by_id(show_id: int):
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_by_id`.

    :param show_id: Show ID to test retrieving show information
    """
    show = Show(connect_dict=get_connect_dict())
    info = show.retrieve_by_id(show_id)

    assert info, f"Show ID {show_id} not found"
    assert "date" in info, f"'date' was not returned for ID {show_id}"


@pytest.mark.parametrize("month, day", [(10, 28), (8, 19)])
def test_show_retrieve_by_month_day(month: int, day: int):
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_by_month_day`.

    :param month: One or two digit month to test retrieving show details
    :param day: One or two digit day to test retrieving show details
    """
    show = Show(connect_dict=get_connect_dict())
    shows = show.retrieve_by_month_day(month, day)

    assert shows, (
        f"No shows could be retrieved for month {month:02d} and day {day:02d}"
    )
    assert "id" in shows[0], (
        f"'id' was not returned for the first list item "
        f"for month {month:02d} and day {day:02d}"
    )


@pytest.mark.parametrize("year", [2018])
def test_show_retrieve_by_year(year: int):
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_by_year`.

    :param year: Four digit year to test retrieving show information
    """
    show = Show(connect_dict=get_connect_dict())
    shows = show.retrieve_by_year(year)

    assert shows, f"No shows could be retrieved for year {year:04d}"
    assert "id" in shows[0], (
        f"'id' was not returned for the first list item for year {year:04d}"
    )


@pytest.mark.parametrize("year, month", [(1998, 1), (2018, 10)])
def test_show_retrieve_by_year_month(year: int, month: int):
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_by_year_month`.

    :param year: Four digit year to test retrieving show information
    :param month: One or two digit month to test retrieving show
        information
    """
    show = Show(connect_dict=get_connect_dict())
    shows = show.retrieve_by_year_month(year, month)

    assert shows, (
        f"No shows could be retrieved for year/month {year:04d}-{month:02d}"
    )
    assert "id" in shows[0], (
        f"'id' was not returned for the first list "
        f"item for year/month {year:02d}-{month:04d}"
    )


@pytest.mark.parametrize(
    "year, month, day, include_decimal_scores",
    [(2020, 4, 25, True), (2020, 4, 25, False)],
)
def test_show_retrieve_details_by_date(
    year: int, month: int, day: int, include_decimal_scores: bool
):
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_details_by_date`.

    :param year: Four digit year to test retrieving show details
    :param month: One or two digit month to test retrieving show details
    :param day: One or two digit day to test retrieving show details
    :param include_decimal_scores: Flag set to include decimal score columns
        and values
    """
    show = Show(connect_dict=get_connect_dict())
    info = show.retrieve_details_by_date(
        year, month, day, include_decimal_scores=include_decimal_scores
    )

    assert info, f"Show for date {year:04d}-{month:02d}-{day:02d} not found"
    assert "date" in info, (
        f"'date' was not returned for show {year:04d}-{month:02d}-{day:02d}"
    )
    assert "host" in info, (
        f"'host' was not returned for show {year:04d}-{month:02d}-{day:02d}"
    )


@pytest.mark.parametrize(
    "date, include_decimal_scores", [("2018-10-27", True), ("2018-10-27", False)]
)
def test_show_retrieve_details_by_date_string(date: str, include_decimal_scores: bool):
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_details_by_date_string`.

    :param date: Show date string in ``YYYY-MM-DD`` format to test
        retrieving show details
    :param include_decimal_scores: Flag set to include decimal score columns
        and values
    """
    show = Show(connect_dict=get_connect_dict())
    info = show.retrieve_details_by_date_string(
        date, include_decimal_scores=include_decimal_scores
    )

    assert info, f"Show for date {date} not found"
    assert "date" in info, f"'date' was not returned for show {date}"
    assert "host" in info, f"'host' was not returned for show {date}"


@pytest.mark.parametrize("date", ["2018-10-27"])
def test_show_retrieve_details_by_date_string_decimal(date: str):
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_details_by_date_string` with decimal scores.

    :param date: Show date string in ``YYYY-MM-DD`` format to test
        retrieving show details
    :param include_decimal_scores: Flag set to include decimal score columns
        and values
    """
    show = Show(connect_dict=get_connect_dict())
    info = show.retrieve_details_by_date_string(date, include_decimal_scores=True)

    assert info, f"Show for date {date} not found"
    assert "date" in info, f"'date' was not returned for show {date}"
    assert "host" in info, f"'host' was not returned for show {date}"


@pytest.mark.parametrize(
    "show_id, include_decimal_scores",
    [(1162, True), (1162, False), (1246, True), (1246, False)],
)
def test_show_retrieve_details_by_id(show_id: int, include_decimal_scores: bool):
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_details_by_id`.

    :param show_id: Show ID to test retrieving show details
    :param include_decimal_scores: Flag set to include decimal score columns
        and values
    """
    show = Show(connect_dict=get_connect_dict())
    info = show.retrieve_details_by_id(
        show_id, include_decimal_scores=include_decimal_scores
    )

    assert info, f"Show ID {show_id} not found"
    assert "date" in info, f"'date' was not returned for ID {show_id}"
    assert "host" in info, f"'host' was not returned for ID {show_id}"


@pytest.mark.parametrize(
    "month, day, include_decimal_scores",
    [(10, 28, True), (10, 28, False), (8, 19, True), (8, 19, False)],
)
def test_show_retrieve_details_by_month_day(
    month: int, day: int, include_decimal_scores: bool
):
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_details_by_month_day`.

    :param month: One or two digit month to test retrieving show details
    :param day: One or two digit day to test retrieving show details
    :param include_decimal_scores: Flag set to include decimal score columns
        and values
    """
    show = Show(connect_dict=get_connect_dict())
    shows = show.retrieve_details_by_month_day(
        month, day, include_decimal_scores=include_decimal_scores
    )

    assert shows, (
        f"No shows could be retrieved for month {month:02d} and day {day:02d}"
    )
    assert "id" in shows[0], (
        f"'id' was not returned for the first list item "
        f"for month {month:02d} and day {day:02d}"
    )


@pytest.mark.parametrize("year, include_decimal_scores", [(2021, True), (2021, False)])
def test_show_retrieve_details_by_year(year: int, include_decimal_scores: bool):
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_details_by_year`.

    :param year: Four digit year to test retrieving show details
    """
    show = Show(connect_dict=get_connect_dict())
    info = show.retrieve_details_by_year(
        year, include_decimal_scores=include_decimal_scores
    )

    assert info, f"No shows could be retrieved for year {year:04d}"
    assert "date" in info[0], (
        f"'date' was not returned for first list item for year {year:04d}"
    )
    assert "host" in info[0], (
        f"'host' was not returned for first list item for year {year:04d}"
    )


@pytest.mark.parametrize(
    "year, month, include_decimal_scores", [(2020, 4, True), (2020, 4, False)]
)
def test_show_retrieve_details_by_year_month(
    year: int, month: int, include_decimal_scores: bool
):
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_details_by_year_month`.

    :param year: Four digit year to test retrieving show details
    :param month: One or two digit year to test retrieving show details
    """
    show = Show(connect_dict=get_connect_dict())
    info = show.retrieve_details_by_year_month(
        year, month, include_decimal_scores=include_decimal_scores
    )

    assert info, (
        f"No shows could be retrieved for year/month {year:04d}-{month:02d}"
    )
    assert "date" in info[0], (
        f"'date' was not returned for first list item "
        f"for year/month {year:04d}-{month:02d}"
    )
    assert "host" in info[0], (
        f"'host' was not returned for first list item "
        f"for year/month {year:04d}-{month:02d}"
    )


@pytest.mark.parametrize("year", [2018])
def test_show_retrieve_months_by_year(year: int):
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_months_by_year`.

    :param year: Four digit year to test retrieving a list of months
    """
    show = Show(connect_dict=get_connect_dict())
    months = show.retrieve_months_by_year(year)

    assert months, f"No months could be retrieved for year {year:04d}"


def test_show_retrieve_recent():
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_recent`.
    """
    show = Show(connect_dict=get_connect_dict())
    shows = show.retrieve_recent()

    assert shows, "No shows could be retrieved"
    assert "id" in shows[0], "No Show ID returned for the first list item"


@pytest.mark.parametrize("include_decimal_scores", [True, False])
def test_show_retrieve_recent_details(include_decimal_scores: bool):
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_recent_details`.
    """
    show = Show(connect_dict=get_connect_dict())
    shows = show.retrieve_recent_details(include_decimal_scores=include_decimal_scores)

    assert shows, "No shows could be retrieved"
    assert "date" in shows[0], "'date' was not returned for the first list item"
    assert "host" in shows[0], "'host' was not returned for first list item"


@pytest.mark.parametrize("year, use_decimal_scores", [(2018, True), (2018, False)])
def test_show_retrieve_scores_by_year(year: int, use_decimal_scores: bool):
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_scores_by_year`.

    :param year: Four digit year to test retrieving scores for a show
        year
    :param use_decimal_scores: Flag set to use decimal score columns
        and values
    """
    show = Show(connect_dict=get_connect_dict())
    scores = show.retrieve_scores_by_year(year, use_decimal_scores=use_decimal_scores)

    assert scores, f"No scores could be retrieved by year {year:04d}"
    assert isinstance(scores[0], tuple), "First list item is not a tuple"


def test_show_retrieve_years():
    """Testing for :py:meth:`wwdtm.show.Show.retrieve_years`.
    """
    show = Show(connect_dict=get_connect_dict())
    years = show.retrieve_years()

    assert years, "No years could be retrieved"
    assert isinstance(years[0], int), "First list item is not a number"
