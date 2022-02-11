# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
"""Performance testing script for the core modules for wwdtm"""

import json
import time
from typing import Any, Dict

from wwdtm.guest import Guest
from wwdtm.host import Host
from wwdtm.location import Location
from wwdtm.panelist import Panelist, PanelistScores
from wwdtm.scorekeeper import Scorekeeper
from wwdtm.show import Show


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


def perf_test_guest(connect_dict: Dict[str, Any]) -> float:
    """Run performance test for the wwdtm.guest module

    :param connect_dict: A dictionary containing database connection
        settings for use by mysql.connector
    :type connect_dict: Dict[str, Any]
    :return: Duration of the performance test
    :rtype: float
    """
    guest = Guest(connect_dict=connect_dict)

    # Performance run start time
    start_time = time.perf_counter()

    _ = guest.retrieve_all()
    _ = guest.retrieve_all_details()
    _ = guest.retrieve_all_ids()
    _ = guest.retrieve_all_slugs()

    for i in range(3):
        _ = guest.retrieve_by_id(guest_id=54)

    _ = guest.retrieve_by_id(guest_id=116)

    for i in range(3):
        _ = guest.retrieve_by_slug(guest_slug="tom-hanks")

    _ = guest.retrieve_by_slug(guest_slug="tom-bodett")

    for i in range(3):
        _ = guest.retrieve_details_by_id(guest_id=54)

    _ = guest.retrieve_details_by_id(guest_id=116)

    for i in range(3):
        _ = guest.retrieve_details_by_slug(guest_slug="tom-hanks")

    _ = guest.retrieve_details_by_slug(guest_slug="tom-bodett")

    # Performance run end time
    end_time = time.perf_counter()
    return round(end_time - start_time, 5)


def perf_test_host(connect_dict: Dict[str, Any]) -> float:
    """Run performance test for the wwdtm.host module

    :param connect_dict: A dictionary containing database connection
        settings for use by mysql.connector
    :type connect_dict: Dict[str, Any]
    :return: Duration of the performance test
    :rtype: float
    """
    host = Host(connect_dict=connect_dict)

    # Performance run start time
    start_time = time.perf_counter()

    _ = host.retrieve_all()
    _ = host.retrieve_all_details()
    _ = host.retrieve_all_ids()
    _ = host.retrieve_all_slugs()

    for i in range(3):
        _ = host.retrieve_by_id(host_id=1)

    _ = host.retrieve_by_id(host_id=2)

    for i in range(3):
        _ = host.retrieve_by_slug(host_slug="peter-sagal")

    _ = host.retrieve_by_slug(host_slug="luke-burbank")

    for i in range(3):
        _ = host.retrieve_details_by_id(host_id=1)

    _ = host.retrieve_details_by_id(host_id=2)

    for i in range(3):
        _ = host.retrieve_details_by_slug(host_slug="peter-sagal")

    _ = host.retrieve_details_by_slug(host_slug="luke-burbank")

    # Performance run end time
    end_time = time.perf_counter()
    return round(end_time - start_time, 5)


def perf_test_location(connect_dict: Dict[str, Any]) -> float:
    """Run performance test for the wwdtm.location module

    :param connect_dict: A dictionary containing database connection
        settings for use by mysql.connector
    :type connect_dict: Dict[str, Any]
    :return: Duration of the performance test
    :rtype: float
    """
    location = Location(connect_dict=connect_dict)

    # Performance run start time
    start_time = time.perf_counter()

    _ = location.retrieve_all()
    _ = location.retrieve_all_details()
    _ = location.retrieve_all_ids()
    _ = location.retrieve_all_slugs()

    for i in range(3):
        _ = location.retrieve_by_id(location_id=2)

    _ = location.retrieve_by_id(location_id=64)

    for i in range(3):
        _ = location.retrieve_by_slug(location_slug="chase-auditorium-chicago-il")

    _ = location.retrieve_by_slug(location_slug="nourse-theater-san-francisco-ca")

    for i in range(3):
        _ = location.retrieve_details_by_id(location_id=2)

    _ = location.retrieve_details_by_id(location_id=64)

    for i in range(3):
        _ = location.retrieve_details_by_slug(
            location_slug="chase-auditorium-chicago-il"
        )

    _ = location.retrieve_details_by_slug(
        location_slug="nourse-theater-san-francisco-ca"
    )

    # Performance run end time
    end_time = time.perf_counter()
    return round(end_time - start_time, 5)


def perf_test_panelist(connect_dict: Dict[str, Any]) -> float:
    """Run performance test for the wwdtm.panelist module

    :param connect_dict: A dictionary containing database connection
        settings for use by mysql.connector
    :type connect_dict: Dict[str, Any]
    :return: Duration of the performance test
    :rtype: float
    """
    panelist = Panelist(connect_dict=connect_dict)
    scores = PanelistScores(connect_dict=connect_dict)

    # Performance run start time
    start_time = time.perf_counter()

    _ = panelist.retrieve_all()
    _ = panelist.retrieve_all_details()
    _ = panelist.retrieve_all_ids()
    _ = panelist.retrieve_all_slugs()

    for i in range(3):
        _ = panelist.retrieve_by_id(panelist_id=5)

    _ = panelist.retrieve_by_id(panelist_id=14)

    for i in range(3):
        _ = panelist.retrieve_by_slug(panelist_slug="adam-felber")

    _ = panelist.retrieve_by_slug(panelist_slug="luke-burbank")

    for i in range(3):
        _ = panelist.retrieve_details_by_id(panelist_id=5)

    _ = panelist.retrieve_details_by_id(panelist_id=14)

    for i in range(3):
        _ = panelist.retrieve_details_by_slug(panelist_slug="adam-felber")

    _ = panelist.retrieve_details_by_slug(panelist_slug="luke-burbank")

    _ = scores.retrieve_scores_by_id(panelist_id=5)
    _ = scores.retrieve_scores_by_slug(panelist_slug="adam-felber")
    _ = scores.retrieve_scores_grouped_list_by_id(panelist_id=5)
    _ = scores.retrieve_scores_grouped_list_by_slug(panelist_slug="adam-felber")
    _ = scores.retrieve_scores_grouped_ordered_pair_by_id(panelist_id=5)
    _ = scores.retrieve_scores_grouped_ordered_pair_by_slug(panelist_slug="adam-felber")
    _ = scores.retrieve_scores_list_by_id(panelist_id=5)
    _ = scores.retrieve_scores_list_by_slug(panelist_slug="adam-felber")
    _ = scores.retrieve_scores_ordered_pair_by_id(panelist_id=5)
    _ = scores.retrieve_scores_ordered_pair_by_slug(panelist_slug="adam-felber")

    # Performance run end time
    end_time = time.perf_counter()
    return round(end_time - start_time, 5)


def perf_test_scorekeeper(connect_dict: Dict[str, Any]) -> float:
    """Run performance test for the wwdtm.scorekeeper module

    :param connect_dict: A dictionary containing database connection
        settings for use by mysql.connector
    :type connect_dict: Dict[str, Any]
    :return: Duration of the performance test
    :rtype: float
    """
    scorekeeper = Scorekeeper(connect_dict=connect_dict)

    # Performance run start time
    start_time = time.perf_counter()

    _ = scorekeeper.retrieve_all()
    _ = scorekeeper.retrieve_all_details()
    _ = scorekeeper.retrieve_all_ids()
    _ = scorekeeper.retrieve_all_slugs()

    for i in range(3):
        _ = scorekeeper.retrieve_by_id(scorekeeper_id=1)

    _ = scorekeeper.retrieve_by_id(scorekeeper_id=11)

    for i in range(3):
        _ = scorekeeper.retrieve_by_slug(scorekeeper_slug="carl-kasell")

    _ = scorekeeper.retrieve_by_slug(scorekeeper_slug="bill-kurtis")

    for i in range(3):
        _ = scorekeeper.retrieve_details_by_id(scorekeeper_id=1)

    _ = scorekeeper.retrieve_details_by_id(scorekeeper_id=11)

    for i in range(3):
        _ = scorekeeper.retrieve_details_by_slug(scorekeeper_slug="carl-kasell")

    _ = scorekeeper.retrieve_details_by_slug(scorekeeper_slug="bill-kurtis")

    # Performance run end time
    end_time = time.perf_counter()
    return round(end_time - start_time, 5)


def perf_test_show(connect_dict: Dict[str, Any]) -> float:
    """Run performance test for the wwdtm.show module

    :param connect_dict: A dictionary containing database connection
        settings for use by mysql.connector
    :type connect_dict: Dict[str, Any]
    :return: Duration of the performance test
    :rtype: float
    """
    show = Show(connect_dict=connect_dict)

    # Performance run start time
    start_time = time.perf_counter()

    _ = show.retrieve_all()
    _ = show.retrieve_all_details()
    _ = show.retrieve_all_dates()
    _ = show.retrieve_all_dates_tuple()
    _ = show.retrieve_all_ids()
    _ = show.retrieve_all_show_years_months()
    _ = show.retrieve_all_shows_years_months_tuple()

    for i in range(3):
        _ = show.retrieve_by_date(year=2018, month=10, day=27)

    _ = show.retrieve_by_date(year=2006, month=8, day=19)

    for i in range(3):
        _ = show.retrieve_by_date_string(date_string="2018-10-27")

    _ = show.retrieve_by_date_string(date_string="2006-08-19")

    for i in range(3):
        _ = show.retrieve_by_id(show_id=1083)

    _ = show.retrieve_by_id(show_id=47)

    for i in range(3):
        _ = show.retrieve_by_year(year=2018)

    _ = show.retrieve_by_year(year=2006)

    for i in range(3):
        _ = show.retrieve_by_year_month(year=2018, month=10)

    _ = show.retrieve_by_year_month(year=2006, month=8)

    for i in range(3):
        _ = show.retrieve_details_by_date(year=2018, month=10, day=27)

    _ = show.retrieve_details_by_date(year=2006, month=8, day=19)

    for i in range(3):
        _ = show.retrieve_details_by_date_string(date_string="2018-10-27")

    _ = show.retrieve_details_by_date_string(date_string="2006-08-19")

    for i in range(3):
        _ = show.retrieve_details_by_id(show_id=1083)

    _ = show.retrieve_details_by_id(show_id=47)

    for i in range(3):
        _ = show.retrieve_details_by_year(year=2018)

    _ = show.retrieve_details_by_year(year=2006)

    for i in range(3):
        _ = show.retrieve_details_by_year_month(year=2018, month=10)

    _ = show.retrieve_details_by_year_month(year=2018, month=10)

    _ = show.retrieve_recent()
    _ = show.retrieve_recent_details()

    # Performance run end time
    end_time = time.perf_counter()
    return round(end_time - start_time, 5)


def main():
    """Runs performance testing against each of the wwdtm modules"""
    # Load configuration and set up database connection
    config = get_connect_dict()

    # Performance run start time
    start_time = time.perf_counter()

    # Run tests
    time_guest = perf_test_guest(config)
    time_host = perf_test_host(config)
    time_location = perf_test_location(config)
    time_panelist = perf_test_panelist(config)
    time_scorekeeper = perf_test_scorekeeper(config)
    time_show = perf_test_show(config)

    # Performance run end time
    end_time = time.perf_counter()
    elapsed_time = round(end_time - start_time, 5)

    # Print out run times
    print("Performance testing completed")
    print(f"Guest:          {time_guest}s")
    print(f"Host:           {time_host}s")
    print(f"Location:       {time_location}s")
    print(f"Panelist:       {time_panelist}s")
    print(f"Scorekeeper:    {time_scorekeeper}s")
    print(f"Show:           {time_show}s")
    print(f"Total:          {elapsed_time}s")


# Only run if this file is executed as a script and not imported
if __name__ == "__main__":
    main()
