# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is relased under the terms of the Apache License 2.0
"""Wait Wait Don't Tell Me! Stats Show Data Retrieval Functions
"""
import datetime
import dateutil.parser as date_parser
from functools import lru_cache
from typing import Any, Dict, List, Optional, Tuple

from mysql.connector import connect
from wwdtm.show.info import ShowInfo
from wwdtm.show.utility import ShowUtility

class Show:
    """This class contains functions used to retrieve show data from a
    copy of the Wait Wait Stats database.

    :param connect_dict: Dictionary containing database connection
        settings as required by mysql.connector.connect
    :type connect_dict: Dict[str, Any], optional
    :param database_connection: mysql.connector.connect database
        connection
    :type database_connection: mysql.connector.connect, optional
    """

    def __init__(self,
                 connect_dict: Optional[Dict[str, Any]] = None,
                 database_connection: Optional[connect] = None):
        """Class initialization method.
        """
        if connect_dict:
            self.connect_dict = connect_dict
            self.database_connection = connect(**connect_dict)
        elif database_connection:
            if not database_connection.is_connected():
                database_connection.reconnect()

            self.database_connection = database_connection

        self.info = ShowInfo(database_connection=self.database_connection)
        self.utility = ShowUtility(database_connection=self.database_connection)

    def retrieve_all(self) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing show ID,
        show date, Best Of and Repeat Show information for all shows.

        :return: List of all shows and their corresponding information
        :rtype: List[Dict[str, Any]]
        """
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT showid AS id, showdate AS date, "
                 "bestof AS best_of, repeatshowid "
                 "FROM ww_shows "
                 "ORDER BY showdate ASC;")
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return None

        shows = []
        for row in results:
            repeat_show_id = row["repeatshowid"]
            show = {
                "id": row["id"],
                "date": row["date"].isoformat(),
                "best_of": bool(row["best_of"]),
                "repeat_show": bool(repeat_show_id),
            }

            if repeat_show_id:
                show["original_show_id"] = repeat_show_id
                show["original_show_date"] = self.utility.convert_id_to_date(repeat_show_id)

            shows.append(show)

        return shows

    def retrieve_all_details(self) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing show ID,
        show date, host, scorekeeper, panelist and guest information
        for all shows.

        :return: List of all shows and their corresponding details
        :rtype: List[Dict[str, Any]]
        """
        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT showid AS id FROM ww_shows "
                 "ORDER BY showdate ASC;")
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return None

        shows = []
        for row in results:
            id = row["id"]
            info = self.info.retrieve_core_info_by_id(id)
            if info:
                info["panelists"] = self.info.retrieve_panelist_info_by_id(id)
                info["bluff"] = self.info.retrieve_bluff_info_by_id(id)
                info["guests"] = self.info.retrieve_guest_info_by_id(id)

            shows.append(info)

        return shows

    def retrieve_all_ids(self) -> List[int]:
        """Returns a list of all show IDs from the database, sorted by
        show date.

        :return: List of all show IDs
        :rtype: List[int]
        """
        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT showid FROM ww_shows "
                 "ORDER BY showdate ASC;")
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return None

        ids = []
        for row in result:
            ids.append(row[0])

        return ids

    def retrieve_all_dates(self) -> List[str]:
        """Returns a list of all show dates from the database, sorted
        by show date.

        :return: List of all show date strings
        :rtype: List[str]
        """
        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT showdate FROM ww_shows "
                 "ORDER BY showdate ASC;")
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return None

        ids = []
        for row in result:
            ids.append(row[0].isoformat())

        return ids

    def retrieve_all_dates_tuple(self) -> List[Tuple[int, int, int]]:
        """Returns a list of all show dates as a tuple of year, month,
        and day, sorted by show date.

        :return: List of allow show dates as a tuple of year, month
            and day
        :rtype: List[Tuple[int, int, int]]
        """
        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT YEAR(showdate), MONTH(showdate), DAY(showdate) "
                 "FROM ww_shows "
                 "ORDER BY showdate ASC;")
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        show_dates = []
        for show in result:
            show_dates.append((show[0], show[1], show[2]))

        return show_dates

    def retrieve_all_show_years_months(self) -> List[str]:
        """Returns a list of all show years and months as a string,
        sorted by year and month.

        :return: List of all show years and month in ``YYYY-MM`` format
        :rtype: List[str]
        """
        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT DISTINCT YEAR(showdate), MONTH(showdate) "
                 "FROM ww_shows "
                 "ORDER BY showdate ASC;")
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        show_years_months = []
        for row in result:
            show_years_months.append(f"{row[0]}-{row[1]}")

        return show_years_months

    def retrieve_all_shows_years_months_tuple(self) -> List[Tuple[int, int]]:
        """Returns a list of all show years and months as a tuple of
        year and month, sorted by year and month.

        :return: List of allow show dates as a tuple of year and month
        :rtype: List[Tuple[int, int]]
        """
        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT DISTINCT YEAR(showdate), MONTH(showdate) "
                 "FROM ww_shows "
                 "ORDER BY showdate ASC;")
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        show_years_months = []
        for row in result:
            show_years_months.append((row[0], row[1]))

        return show_years_months

    @lru_cache(maxsize=256, typed=True)
    def retrieve_by_date(self,
                         year: int,
                         month: int,
                         day: int) -> Dict[str, Any]:
        """Returns a dictionary object containing show ID, show date,
        Best Of and Repeat Show information for the requested show date.

        :param year: Four digit year
        :type year: int
        :param month: One or two digit month
        :type month: int
        :param day: One or two digit day
        :type day: int
        :return: Dictionary containing show information
        :rtype: Dict[str, Any]
        """
        id = self.utility.convert_date_to_id(year, month, day)
        if not id:
            return None

        return self.retrieve_by_id(id)

    @lru_cache(maxsize=256, typed=True)
    def retrieve_by_date_string(self,
                                date_string: str) -> Dict[str, Any]:
        """Returns a dictionary object containing show ID, show date,
        Best Of and Repeat Show information for the requested show date
        string.

        :param date_string: Show date in ``YYYY-MM-DD`` format
        :type date_string: str
        :return: Dictionary containing show information
        :rtype: Dict[str, Any]
        """
        try:
            parsed_date_string = date_parser.parse(date_string)
        except ValueError:
            return None

        id = self.utility.convert_date_to_id(parsed_date_string.year,
                                             parsed_date_string.month,
                                             parsed_date_string.day)

        return self.retrieve_by_id(id)

    @lru_cache(maxsize=256, typed=True)
    def retrieve_by_id(self, id: int) -> Dict[str, Any]:
        """Returns a dictionary object containing show ID, show date,
        Best Of and Repeat Show information for the requested show ID.

        :param id: Show ID
        :type id: int
        :return: Show information
        :rtype: Dict[str, Any]
        """
        try:
            id = int(id)
        except ValueError:
            return None

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT showid AS id, showdate AS date, "
                 "bestof AS best_of, repeatshowid "
                 "FROM ww_shows "
                 "WHERE showid = %s "
                 "LIMIT 1;")
        cursor.execute(query, (id, ))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return None

        repeat_show_id = result["repeatshowid"]
        info = {
            "id": result["id"],
            "date": result["date"].isoformat(),
            "best_of": bool(result["best_of"]),
            "repeat_show": bool(repeat_show_id),
        }

        if repeat_show_id:
            info["original_show_id"] = repeat_show_id
            info["original_show_date"] = self.utility.convert_id_to_date(repeat_show_id)

        return info

    @lru_cache(maxsize=256, typed=True)
    def retrieve_by_year(self, year: int) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing with show
        information for the requested year, sorted by show date.

        :param year: Four digit year
        :type year: int
        :return: List of shows for the requested year and corresponding
            information
        :rtype: List[Dict[str, Any]]
        """
        try:
            parsed_year = date_parser.parse(f"{year:04d}")
        except ValueError:
            return None

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT showid FROM ww_shows "
                 "WHERE YEAR(showdate) = %s "
                 "ORDER BY showdate ASC;")
        cursor.execute(query, (parsed_year.year, ))
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return None

        shows = []
        for show in result:
            show_info = self.retrieve_by_id(show["showid"])
            shows.append(show_info)

        return shows

    @lru_cache(maxsize=256, typed=True)
    def retrieve_by_year_month(self,
                               year: int,
                               month: int) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing show
        information for the requested year and month, sorted by show
        date.

        :param year: Four digit year
        :type year: int
        :param month: One or two digit month
        :type month: int
        :return: List of shows for the requested year and month, and
            corresponding information
        :rtype: List[Dict[str, Any]]
        """
        try:
            parsed_year_month = date_parser.parse(f"{year:04d}-{month:02d}-01")
        except ValueError:
            return None

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT showid FROM ww_shows "
                 "WHERE YEAR(showdate) = %s "
                 "AND MONTH(showdate) = %s ORDER BY showdate ASC;")
        cursor.execute(query, (parsed_year_month.year,
                               parsed_year_month.month, ))
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return None

        shows = []
        for show in result:
            show_info = self.retrieve_by_id(show["showid"])
            shows.append(show_info)

        return shows

    @lru_cache(maxsize=256, typed=True)
    def retrieve_details_by_date(self,
                                 year: int,
                                 month: int,
                                 day: int) -> Dict[str, Any]:
        """Returns a list of dictionary objects containing show ID,
        show date, host, scorekeeper, panelist and guest information
        for the requested show date.

        :param year: Four digit year
        :type year: int
        :param month: One or two digit month
        :type month: int
        :param day: One or two digit day
        :type day: int
        :return: Dictionary containing show information and details
        :rtype: Dict[str, Any]
        """
        id = self.utility.convert_date_to_id(year, month, day)
        if not id:
            return None

        return self.retrieve_details_by_id(id)

    @lru_cache(maxsize=256, typed=True)
    def retrieve_details_by_date_string(self,
                                        date_string: str) -> Dict[str, Any]:
        """Returns a list of dictionary objects containing show ID,
        show date, host, scorekeeper, panelist and guest information
        for the requested show date string.

        :param date_string: Show date in ``YYYY-MM-DD`` format
        :type date_string: str
        :return: Dictionary containing show information and details
        :rtype: Dict[str, Any]
        """
        try:
            parsed_date_string = date_parser.parse(date_string)
        except ValueError:
            return None

        id = self.utility.convert_date_to_id(parsed_date_string.year,
                                             parsed_date_string.month,
                                             parsed_date_string.day)

        return self.retrieve_details_by_id(id)

    @lru_cache(maxsize=256, typed=True)
    def retrieve_details_by_id(self, id: int) -> Dict[str, Any]:
        """Returns a list of dictionary objects containing show ID,
        show date, host, scorekeeper, panelist and guest information
        for the requested show ID.

        :param id: Show ID
        :type id: int
        :return: Dictionary containing show information and details
        :rtype: Dict[str, Any]
        """
        try:
            id = int(id)
        except ValueError:
            return None

        info = self.info.retrieve_core_info_by_id(id)
        if not info:
            return None

        info["panelists"] = self.info.retrieve_panelist_info_by_id(id)
        info["bluff"] = self.info.retrieve_bluff_info_by_id(id)
        info["guests"] = self.info.retrieve_guest_info_by_id(id)

        return info

    @lru_cache(maxsize=256, typed=True)
    def retrieve_details_by_year(self, year: int) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing show ID,
        show date, host, scorekeeper, panelist and guest information for
        the requested year, sorted by show date.

        :param year: Four digit year
        :type year: int
        :return: List of shows for the requested year and corresponding
            details
        :rtype: List[Dict[str, Any]]
        """
        try:
            parsed_year = date_parser.parse(f"{year:04d}")
        except ValueError:
            return None

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT showid AS id FROM ww_shows "
                 "WHERE YEAR(showdate) = %s "
                 "ORDER BY showdate ASC;")
        cursor.execute(query, (parsed_year.year, ))
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return None

        shows = []
        for show in result:
            shows.append(self.retrieve_details_by_id(show["id"]))

        return shows

    @lru_cache(maxsize=256, typed=True)
    def retrieve_details_by_year_month(self,
                                       year: int,
                                       month: int) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing show ID,
        show date, host, scorekeeper, panelist and guest information for
        the requested year and month, sorted by show date.

        :param year: Four digit year
        :type year: int
        :param month: One or two digit month
        :type month: int
        :return: List of shows for the requested year and month, and
            corresponding details
        :rtype: List[Dict[str, Any]]
        """
        try:
            parsed_year_month = date_parser.parse(f"{year:04d}-{month:02d}-01")
        except ValueError:
            return None

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT showid AS id FROM ww_shows "
                "WHERE YEAR(showdate) = %s "
                "AND MONTH(showdate) = %s "
                "ORDER BY showdate ASC;")
        cursor.execute(query, (parsed_year_month.year,
                               parsed_year_month.month, ))
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return None

        shows = []
        for show in result:
            shows.append(self.retrieve_details_by_id(show["id"]))

        return shows

    @lru_cache(maxsize=256, typed=True)
    def retrieve_months_by_year(self,
                                year: int) -> List[int]:
        """Returns a list of show months available for the requested
        year, sorted by month.

        :param year: Four digit year
        :type year: int
        :return: List of months
        :rtype: List[int]
        """
        try:
            _ = date_parser.parse(f"{year:04d}")
        except ValueError:
            return None

        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT DISTINCT MONTH(showdate) "
                 "FROM ww_shows "
                 "WHERE YEAR(showdate) = %s "
                 "ORDER BY MONTH(showdate) ASC;")
        cursor.execute(query, (year,))
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return None

        months = []
        for row in result:
            months.append(row[0])

        return months

    @lru_cache(maxsize=256, typed=True)
    def retrieve_recent(self,
                        include_days_ahead: int = 7,
                        include_days_back: int = 32) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing show ID,
        show date, Best Of and Repeat Show information for recent shows.

        :param include_days_ahead: Number of days in the future to
            include, defaults to 7
        :type include_days_ahead: int, optional
        :param include_days_back: Number of days in the past to
            include, defaults to 32
        :type include_days_back: int, optional
        :return: List of recent shows and corresponding information
        :rtype: List[Dict[str, Any]]
        """
        try:
            past_days = int(include_days_back)
            future_days = int(include_days_ahead)
        except ValueError:
            return None

        try:
            past_date = datetime.datetime.now() - datetime.timedelta(days=past_days)
            future_date = datetime.datetime.now() + datetime.timedelta(days=future_days)
        except OverflowError:
            return None

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT showid AS id FROM ww_shows "
                 "WHERE showdate >= %s AND "
                 "showdate <= %s ORDER BY showdate ASC;")
        cursor.execute(query, (past_date.isoformat(),
                               future_date.isoformat(), ))
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return None

        shows = []
        for show in result:
            shows.append(self.retrieve_by_id(show["id"]))

        return shows

    @lru_cache(maxsize=256, typed=True)
    def retrieve_recent_details(self,
                                include_days_ahead: int = 7,
                                include_days_back: int = 32
                               ) -> List[Dict[str, Any]]:
        """Returns a list of dictionary objects containing show ID,
        show date, host, scorekeeper, panelist and guest information
        for recent shows.

        :param include_days_ahead: Number of days in the future to
            include, defaults to 7
        :type include_days_ahead: int, optional
        :param include_days_back: Number of days in the past to
            include, defaults to 32
        :type include_days_back: int, optional
        :return: List of recent shows and corresponding details
        :rtype: List[Dict[str, Any]]
        """
        try:
            past_days = int(include_days_back)
            future_days = int(include_days_ahead)
        except ValueError:
            return None

        try:
            past_date = datetime.datetime.now() - datetime.timedelta(days=past_days)
            future_date = datetime.datetime.now() + datetime.timedelta(days=future_days)
        except OverflowError:
            return None

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT showid AS id FROM ww_shows "
                "WHERE showdate >= %s AND "
                "showdate <= %s ORDER BY showdate ASC;")
        cursor.execute(query, (past_date.isoformat(),
                               future_date.isoformat(), ))
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return None

        shows = []
        for show in result:
            shows.append(self.retrieve_details_by_id(show["id"]))

        return shows

    @lru_cache(maxsize=256, typed=True)
    def retrieve_scores_by_year(self, year: int) -> List[Tuple[str, int, int, int]]:
        """Returns a list of tuples containing panelist scores for all
        shows in the requested year, sorted by show date.

        :param year: Four digit year
        :type year: int
        :return: List of tuples each containing show date and panelist
            scores
        :rtype: List[Tuple[str, int, int, int]]
        """
        try:
            _ = date_parser.parse(f"{year:04d}")
        except ValueError:
            return None

        cursor = self.database_connection.cursor(dictionary=True)
        query = ("SELECT s.showdate AS date, pm.panelistscore AS score "
                 "FROM ww_showpnlmap pm "
                 "JOIN ww_shows s ON s.showid = pm.showid "
                 "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
                 "AND pm.panelistscore IS NOT NULL "
                 "AND YEAR(s.showdate) = %s "
                 "ORDER BY s.showdate ASC, pm.panelistscore ASC;")
        cursor.execute(query, (year, ))
        result = cursor.fetchall()

        if not result:
            return None

        shows = {}
        for row in result:
            date = row["date"].isoformat()
            if date not in shows:
                shows[date] = []

            shows[date].append(row["score"])

        show_scores = []
        for show in shows:
            show_score = shows[show]
            show_score.insert(0, show)
            show_scores.append(tuple(show_score))

        return show_scores

    def retrieve_years(self) -> List[int]:
        """Returns a list of available show years, sorted by year.

        :return: List of all show years
        :rtype: List[int]
        """
        cursor = self.database_connection.cursor(dictionary=False)
        query = ("SELECT DISTINCT YEAR(showdate) "
                 "FROM ww_shows "
                 "ORDER BY YEAR(showdate) ASC;")
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return None

        years = []
        for row in result:
            years.append(row[0])

        return years
