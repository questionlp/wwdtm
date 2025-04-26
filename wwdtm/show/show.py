# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
# pylint: disable=C0206
"""Wait Wait Stats Show Information Retrieval Functions."""

import datetime
from decimal import Decimal
from typing import Any

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from wwdtm.show.info import ShowInfo
from wwdtm.show.info_multiple import ShowInfoMultiple
from wwdtm.show.utility import ShowUtility
from wwdtm.validation import valid_int_id


class Show:
    """Show retrieval class.

    Contains methods used to retrieve basic and detailed show
    information, including hosts, scorekeepers, guests, panelists and
    scores.

    :param connect_dict: A dictionary containing database connection
        settings as required by MySQL Connector/Python
    :param database_connection: MySQL database connection object
    """

    def __init__(
        self,
        connect_dict: dict[str, Any] = None,
        database_connection: MySQLConnection | PooledMySQLConnection = None,
    ):
        """Class initialization method."""
        if connect_dict:
            self.connect_dict = connect_dict
            self.database_connection = connect(**connect_dict)
        elif database_connection:
            if not database_connection.is_connected():
                database_connection.reconnect()

            self.database_connection = database_connection

        self.info = ShowInfo(database_connection=self.database_connection)
        self.info_multiple = ShowInfoMultiple(
            database_connection=self.database_connection
        )
        self.utility = ShowUtility(database_connection=self.database_connection)

    def retrieve_all(self) -> list[dict[str, Any]]:
        """Retrieves basic show information for all shows.

        :return: A list of dictionaries containing show ID, show date,
            Best Of show flag, repeat show ID (if applicable) and show
            URL at NPR.org
        """
        query = """
            SELECT showid AS id, showdate AS date,
            bestof AS best_of, repeatshowid AS repeat_show_id,
            showurl AS show_url
            FROM ww_shows
            ORDER BY showdate ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        shows = []
        for row in results:
            show = {
                "id": row["id"],
                "date": row["date"].isoformat(),
                "best_of": bool(row["best_of"]),
                "repeat_show": bool(row["repeat_show_id"]),
                "show_url": row["show_url"],
            }

            if row["repeat_show_id"]:
                show["original_show_id"] = row["repeat_show_id"]
                show["original_show_date"] = self.utility.convert_id_to_date(
                    row["repeat_show_id"]
                )

            shows.append(show)

        return shows

    def retrieve_all_best_ofs(self) -> list[dict[str, Any]]:
        """Retrieves basic show information for all Best Of shows.

        :return: A list of dictionaries containing show ID, show date,
            Best Of show flag, repeat show ID (if applicable) and show
            URL at NPR.org
        """
        query = """
            SELECT showid AS id, showdate AS date,
            bestof AS best_of, repeatshowid AS repeat_show_id,
            showurl AS show_url
            FROM ww_shows
            WHERE bestof = 1
            ORDER BY showdate ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        shows = []
        for row in results:
            show = {
                "id": row["id"],
                "date": row["date"].isoformat(),
                "best_of": bool(row["best_of"]),
                "repeat_show": bool(row["repeat_show_id"]),
                "show_url": row["show_url"],
            }

            if row["repeat_show_id"]:
                show["original_show_id"] = row["repeat_show_id"]
                show["original_show_date"] = self.utility.convert_id_to_date(
                    row["repeat_show_id"]
                )

            shows.append(show)

        return shows

    def retrieve_all_best_ofs_details(
        self, include_decimal_scores: bool = False
    ) -> list[dict[str, Any]]:
        """Retrieves detailed show information for all Best Of shows.

        :param include_decimal_scores: A boolean to determine if decimal
            scores should be included
        :return: A list of dictionaries containing show ID, show date,
            Best Of show flag, repeat show ID (if applicable), show URL
            at NPR.org, host, scorekeeper, location, panelists and
            guests
        """
        query = """
            SELECT showid
            FROM ww_shows
            WHERE bestof = 1
            ORDER BY showdate ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        show_ids = [v[0] for v in results]
        info = self.info_multiple.retrieve_core_info_by_ids(show_ids)

        if not info:
            return []

        shows = []
        for show in info:
            if info[show]:
                info[show]["panelists"] = self.info.retrieve_panelist_info_by_id(
                    info[show]["id"], include_decimal_scores=include_decimal_scores
                )
                info[show]["bluffs"] = self.info.retrieve_bluff_info_by_id(
                    info[show]["id"]
                )
                info[show]["guests"] = self.info.retrieve_guest_info_by_id(
                    info[show]["id"]
                )
                shows.append(info[show])

        return shows

    def retrieve_all_repeat_best_ofs(self) -> list[dict[str, Any]]:
        """Retrieves basic show information for all Repeat Best Of shows.

        :return: A list of dictionaries containing show ID, show date,
            Best Of show flag, repeat show ID (if applicable) and show
            URL at NPR.org
        """
        query = """
            SELECT showid AS id, showdate AS date,
            bestof AS best_of, repeatshowid AS repeat_show_id,
            showurl AS show_url
            FROM ww_shows
            WHERE bestof = 1 AND repeatshowid IS NOT NULL
            ORDER BY showdate ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        shows = []
        for row in results:
            show = {
                "id": row["id"],
                "date": row["date"].isoformat(),
                "best_of": bool(row["best_of"]),
                "repeat_show": bool(row["repeat_show_id"]),
                "show_url": row["show_url"],
            }

            if row["repeat_show_id"]:
                show["original_show_id"] = row["repeat_show_id"]
                show["original_show_date"] = self.utility.convert_id_to_date(
                    row["repeat_show_id"]
                )

            shows.append(show)

        return shows

    def retrieve_all_best_of_repeats(self) -> list[dict[str, Any]]:
        """Alias for :py:meth:`wwdtm.show.Show.retrieve_all_repeat_best_ofs`.

        :return: A list of dictionaries containing show ID, show date,
            Best Of show flag, repeat show ID (if applicable) and show
            URL at NPR.org
        """
        return self.retrieve_all_repeat_best_ofs()

    def retrieve_all_repeat_best_ofs_details(
        self, include_decimal_scores: bool = False
    ) -> list[dict[str, Any]]:
        """Retrieves detailed show information for all Repeat Best Of shows.

        :param include_decimal_scores: A boolean to determine if decimal
            scores should be included
        :return: A list of dictionaries containing show ID, show date,
            Best Of show flag, repeat show ID (if applicable), show URL
            at NPR.org, host, scorekeeper, location, panelists and
            guests
        """
        query = """
            SELECT showid
            FROM ww_shows
            WHERE bestof = 1 AND repeatshowid IS NOT NULL
            ORDER BY showdate ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        show_ids = [v[0] for v in results]
        info = self.info_multiple.retrieve_core_info_by_ids(show_ids)

        if not info:
            return []

        shows = []
        for show in info:
            if info[show]:
                info[show]["panelists"] = self.info.retrieve_panelist_info_by_id(
                    info[show]["id"], include_decimal_scores=include_decimal_scores
                )
                info[show]["bluffs"] = self.info.retrieve_bluff_info_by_id(
                    info[show]["id"]
                )
                info[show]["guests"] = self.info.retrieve_guest_info_by_id(
                    info[show]["id"]
                )
                shows.append(info[show])

        return shows

    def retrieve_all_best_of_repeats_details(
        self, include_decimal_scores: bool = False
    ) -> list[dict[str, Any]]:
        """Alias for :py:meth:`wwdtm.show.Show.retrieve_all_repeat_best_ofs_details`.

        :param include_decimal_scores: A boolean to determine if decimal
            scores should be included
        :return: A list of dictionaries containing show ID, show date,
            Best Of show flag, repeat show ID (if applicable), show URL
            at NPR.org, host, scorekeeper, location, panelists and
            guests
        """
        return self.retrieve_all_repeat_best_ofs_details(
            include_decimal_scores=include_decimal_scores
        )

    def retrieve_all_repeats(self) -> list[dict[str, Any]]:
        """Retrieves basic show information for all repeat shows.

        :return: A list of dictionaries containing show ID, show date,
            Best Of show flag, repeat show ID (if applicable) and show
            URL at NPR.org
        """
        query = """
            SELECT showid AS id, showdate AS date,
            bestof AS best_of, repeatshowid AS repeat_show_id,
            showurl AS show_url
            FROM ww_shows
            WHERE repeatshowid IS NOT NULL
            ORDER BY showdate ASC;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        shows = []
        for row in results:
            show = {
                "id": row["id"],
                "date": row["date"].isoformat(),
                "best_of": bool(row["best_of"]),
                "repeat_show": bool(row["repeat_show_id"]),
                "show_url": row["show_url"],
            }

            if row["repeat_show_id"]:
                show["original_show_id"] = row["repeat_show_id"]
                show["original_show_date"] = self.utility.convert_id_to_date(
                    row["repeat_show_id"]
                )

            shows.append(show)

        return shows

    def retrieve_all_repeats_details(
        self, include_decimal_scores: bool = False
    ) -> list[dict[str, Any]]:
        """Retrieves detailed show information for all repeat shows.

        :param include_decimal_scores: A boolean to determine if decimal
            scores should be included
        :return: A list of dictionaries containing show ID, show date,
            Best Of show flag, repeat show ID (if applicable), show URL
            at NPR.org, host, scorekeeper, location, panelists and
            guests
        """
        query = """
            SELECT showid
            FROM ww_shows
            WHERE repeatshowid IS NOT NULL
            ORDER BY showdate ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        show_ids = [v[0] for v in results]
        info = self.info_multiple.retrieve_core_info_by_ids(show_ids)

        if not info:
            return []

        shows = []
        for show in info:
            if info[show]:
                info[show]["panelists"] = self.info.retrieve_panelist_info_by_id(
                    info[show]["id"], include_decimal_scores=include_decimal_scores
                )
                info[show]["bluffs"] = self.info.retrieve_bluff_info_by_id(
                    info[show]["id"]
                )
                info[show]["guests"] = self.info.retrieve_guest_info_by_id(
                    info[show]["id"]
                )
                shows.append(info[show])

        return shows

    def retrieve_all_details(
        self, include_decimal_scores: bool = False
    ) -> list[dict[str, Any]]:
        """Returns a list of dictionaries with show information and details for all shows.

        :param include_decimal_scores: Flag set to include panelist decimal
            scores, if available
        :return: List of all shows and their corresponding details.
            If show information could not be retrieved, an empty list
            will be returned.
        """
        info = self.info_multiple.retrieve_core_info_all()

        if not info:
            return []

        panelists = self.info_multiple.retrieve_panelist_info_all(
            include_decimal_scores=include_decimal_scores
        )
        bluffs = self.info_multiple.retrieve_bluff_info_all()
        guests = self.info_multiple.retrieve_guest_info_all()

        shows = []
        for show in info:
            info[show]["panelists"] = panelists.get(info[show]["id"], [])
            info[show]["bluffs"] = bluffs.get(info[show]["id"], {})
            info[show]["guests"] = guests.get(info[show]["id"], [])
            shows.append(info[show])

        return shows

    def retrieve_all_ids(self) -> list[int]:
        """Retrieves all show IDs, sorted by show date.

        :return: A list of all show IDs as integers
        """
        query = """
            SELECT showid FROM ww_shows ORDER BY showdate ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [v[0] for v in results]

    def retrieve_all_dates(self) -> list[str]:
        """Retrieves all show dates, sorted by show date.

        :return: A list of all show date strings in ``YYYY-MM-DD``
            format
        """
        query = "SELECT showdate FROM ww_shows ORDER BY showdate ASC;"
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [v[0].isoformat() for v in results]

    def retrieve_all_dates_tuple(self) -> list[tuple[int, int, int]]:
        """Retrieves all show dates as a tuple.

        :return: A list of all show dates as a tuple of year, month and
            day
        """
        query = """
            SELECT YEAR(showdate), MONTH(showdate), DAY(showdate)
            FROM ww_shows
            ORDER BY YEAR(showdate) ASC, MONTH(showdate) ASC,
            DAY(showdate) ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [tuple(v) for v in results]

    def retrieve_all_show_years_months(self) -> list[str]:
        """Retrieves all show years and months.

        :return: A list of all show years and month as a string in
            ``YYYY-MM`` format
        """
        query = """
            SELECT DISTINCT YEAR(showdate), MONTH(showdate)
            FROM ww_shows
            ORDER BY YEAR(showdate) ASC, MONTH(showdate) ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [f"{v[0]}-{v[1]}" for v in results]

    def retrieve_all_shows_years_months_tuple(self) -> list[tuple[int, int]]:
        """Retrieves all show years and months as a tuple.

        :return: A list of all show dates as a tuple of year and month
        """
        query = """
            SELECT DISTINCT YEAR(showdate), MONTH(showdate)
            FROM ww_shows
            ORDER BY YEAR(showdate) ASC, MONTH(showdate) ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [tuple(v) for v in results]

    def retrieve_by_date(self, year: int, month: int, day: int) -> dict[str, Any]:
        """Retrieves basic show information.

        :param year: Four-digit year
        :param month: One or two-digit month
        :param day: One or two-digit day
        :return: A dictionary containing show ID, show date, Best Of
            show flag, repeat show ID (if applicable) and show URL at
            NPR.org
        """
        id_ = self.utility.convert_date_to_id(year, month, day)
        if not id_:
            return {}

        return self.retrieve_by_id(id_)

    def retrieve_by_date_string(self, date_string: str) -> dict[str, Any]:
        """Retrieves basic show information.

        :param date_string: Show date in ``YYYY-MM-DD`` format
        :return: A dictionary containing show ID, show date, Best Of
            show flag, repeat show ID (if applicable) and show URL at
            NPR.org
        """
        try:
            parsed_date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError:
            return {}

        id_ = self.utility.convert_date_to_id(
            parsed_date.year, parsed_date.month, parsed_date.day
        )

        return self.retrieve_by_id(id_)

    def retrieve_by_id(self, show_id: int) -> dict[str, Any]:
        """Retrieves basic show information.

        :param show_id: Show ID
        :return: A dictionary containing show ID, show date, Best Of
            show flag, repeat show ID (if applicable) and show URL at
            NPR.org
        """
        if not valid_int_id(show_id):
            return {}

        query = """
            SELECT showid AS id, showdate AS date,
            bestof AS best_of, repeatshowid AS repeat_show_id,
            showurl AS show_url
            FROM ww_shows
            WHERE showid = %s
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (show_id,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return {}

        info = {
            "id": result["id"],
            "date": result["date"].isoformat(),
            "best_of": bool(result["best_of"]),
            "repeat_show": bool(result["repeat_show_id"]),
            "show_url": result["show_url"],
        }

        if result["repeat_show_id"]:
            info["original_show_id"] = result["repeat_show_id"]
            info["original_show_date"] = self.utility.convert_id_to_date(
                result["repeat_show_id"]
            )

        return info

    def retrieve_by_month_day(self, month: int, day: int) -> list[dict[str, Any]]:
        """Retrieves basic show information for shows by month and day.

        :param month: One or two-digit month
        :param day: One or two-digit day
        :return: A list of dictionaries containing show ID, show date,
            Best Of show flag, repeat show ID (if applicable) and show
            URL at NPR.org
        """
        if not 1 <= month <= 12 or not 1 <= day <= 31:
            return []

        query = """
            SELECT showid FROM ww_shows
            WHERE MONTH(showdate) = %s AND DAY(showdate) = %s
            ORDER BY showdate ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(
            query,
            (
                month,
                day,
            ),
        )
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [self.retrieve_by_id(v[0]) for v in results]

    def retrieve_by_year(self, year: int) -> list[dict[str, Any]]:
        """Retrieves basic show information by year.

        :param year: Four-digit year
        :return: A list of dictionaries containing show ID, show date,
            Best Of show flag, repeat show ID (if applicable) and show
            URL at NPR.org
        """
        try:
            parsed_year = datetime.datetime.strptime(f"{year:04d}", "%Y")
        except ValueError:
            return []

        query = """
            SELECT showid FROM ww_shows
            WHERE YEAR(showdate) = %s
            ORDER BY showdate ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query, (parsed_year.year,))
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [self.retrieve_by_id(v[0]) for v in results]

    def retrieve_by_year_month(self, year: int, month: int) -> list[dict[str, Any]]:
        """Retrieves basic show information by year and month.

        :param year: Four-digit year
        :param month: One or two-digit month
        :return: A list of dictionaries containing show ID, show date,
            Best Of show flag, repeat show ID (if applicable) and show
            URL at NPR.org
        """
        try:
            parsed_year_month = datetime.datetime.strptime(
                f"{year:04d}-{month:02d}-01", "%Y-%m-%d"
            )
        except ValueError:
            return []

        query = """
            SELECT showid FROM ww_shows
            WHERE YEAR(showdate) = %s AND MONTH(showdate) = %s
            ORDER BY showdate ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(
            query,
            (
                parsed_year_month.year,
                parsed_year_month.month,
            ),
        )
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [self.retrieve_by_id(v[0]) for v in results]

    def retrieve_counts_by_year(self, year: int) -> dict[str, int]:
        """Retrieves show counts by year.

        :param year: Four-digit year
        :return: A dictionary containing counts for all shows, Best Of
            shows, repeat shows, and repeat Best Of shows
        """
        try:
            parsed_year = datetime.datetime.strptime(f"{year:04d}", "%Y")
        except ValueError:
            return {}

        query = """
            SELECT
            (SELECT COUNT(showid) FROM ww_shows
                WHERE YEAR(showdate) = %s AND showdate <= NOW()
                AND bestof = 0 AND repeatshowid IS NULL) AS 'regular',
            (SELECT COUNT(showid) FROM ww_shows
                WHERE YEAR(showdate) = %s AND showdate <= NOW()
                AND bestof = 1 AND repeatshowid IS NULL) AS 'bestof',
            (SELECT COUNT(showid) FROM ww_shows
                WHERE YEAR(showdate) = %s AND showdate <= NOW()
                AND bestof = 0 AND repeatshowid IS NOT NULL) AS 'repeat',
            (SELECT COUNT(showid) FROM ww_shows
                WHERE YEAR(showdate) = %s AND showdate <= NOW()
                AND bestof = 1 AND repeatshowid IS NOT NULL) AS 'repeat_bestof';
        """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(
            query,
            (
                parsed_year,
                parsed_year,
                parsed_year,
                parsed_year,
            ),
        )
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return {}

        return {
            "regular": result["regular"],
            "best_of": result["bestof"],
            "repeat": result["repeat"],
            "repeat_best_of": result["repeat_bestof"],
            "total": (
                result["regular"]
                + result["bestof"]
                + result["repeat"]
                + result["repeat_bestof"]
            ),
        }

    def retrieve_all_counts_by_year(self) -> dict[int, dict[str, int]]:
        """Retrieves show counts for all years, grouped by year.

        :return: A dictionary with year as keys with corresponding
            counts for all shows, Best Of shows, repeat shows, and
            repeat Best Of shows as values
        """
        years = self.retrieve_years()
        if not years:
            return {}

        all_counts = {}
        for year in years:
            year_counts = self.retrieve_counts_by_year(year=year)

            if year_counts:
                all_counts[year] = year_counts
            else:
                all_counts[year] = {}

        return all_counts

    def retrieve_details_by_date(
        self, year: int, month: int, day: int, include_decimal_scores: bool = False
    ) -> dict[str, Any]:
        """Retrieves detailed show information.

        :param year: Four-digit year
        :param month: One or two-digit month
        :param day: One or two digit day
        :param include_decimal_scores: A boolean to determine if decimal
            scores should be included
        :return: A dictionary containing show ID, show date, Best Of
            show flag, repeat show ID (if applicable), show URL at
            NPR.org, host, scorekeeper, location, panelists and guests
        """
        id_ = self.utility.convert_date_to_id(year, month, day)
        if not id_:
            return {}

        return self.retrieve_details_by_id(
            id_, include_decimal_scores=include_decimal_scores
        )

    def retrieve_details_by_date_string(
        self, date_string: str, include_decimal_scores: bool = False
    ) -> dict[str, Any]:
        """Retrieves detailed show information.

        :param date_string: Show date in ``YYYY-MM-DD`` format
        :param include_decimal_scores: A boolean to determine if decimal
            scores should be included
        :return: A dictionary containing show ID, show date, Best Of
            show flag, repeat show ID (if applicable), show URL at
            NPR.org, host, scorekeeper, location, panelists and guests
        """
        try:
            parsed_date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError:
            return {}

        id_ = self.utility.convert_date_to_id(
            parsed_date.year, parsed_date.month, parsed_date.day
        )

        return self.retrieve_details_by_id(
            id_, include_decimal_scores=include_decimal_scores
        )

    def retrieve_details_by_id(
        self, show_id: int, include_decimal_scores: bool = False
    ) -> dict[str, Any]:
        """Retrieve detailed show information.

        :param show_id: Show ID
        :param include_decimal_scores: A boolean to determine if decimal
            scores should be included
        :return: A dictionary containing show ID, show date, Best Of
            show flag, repeat show ID (if applicable), show URL at
            NPR.org, host, scorekeeper, location, panelists and guests
        """
        if not valid_int_id(show_id):
            return {}

        info = self.info.retrieve_core_info_by_id(show_id)
        if not info:
            return {}

        info["panelists"] = self.info.retrieve_panelist_info_by_id(
            show_id, include_decimal_scores=include_decimal_scores
        )
        info["bluffs"] = self.info.retrieve_bluff_info_by_id(show_id)
        info["guests"] = self.info.retrieve_guest_info_by_id(show_id)

        return info

    def retrieve_details_by_month_day(
        self, month: int, day: int, include_decimal_scores: bool = False
    ) -> list[dict[str, Any]]:
        """Retrieves detailed show information by month and day.

        :param month: One or two-digit month
        :param day: One or two-digit day
        :param include_decimal_scores: A boolean to determine if decimal
            scores should be included
        :return: A list of dictionaries containing show ID, show date,
            Best Of show flag, repeat show ID (if applicable), show URL
            at NPR.org, host, scorekeeper, location, panelists and
            guests
        """
        if not 1 <= month <= 12 or not 1 <= day <= 31:
            return []

        query = """
            SELECT showid FROM ww_shows
            WHERE MONTH(showdate) = %s AND DAY(showdate) = %s
            ORDER BY showdate ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(
            query,
            (
                month,
                day,
            ),
        )
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        show_ids = [v[0] for v in results]
        info = self.info_multiple.retrieve_core_info_by_ids(show_ids)

        if not info:
            return []

        shows = []
        for show in info:
            if info[show]:
                info[show]["panelists"] = self.info.retrieve_panelist_info_by_id(
                    info[show]["id"], include_decimal_scores=include_decimal_scores
                )
                info[show]["bluffs"] = self.info.retrieve_bluff_info_by_id(
                    info[show]["id"]
                )
                info[show]["guests"] = self.info.retrieve_guest_info_by_id(
                    info[show]["id"]
                )
                shows.append(info[show])

        return shows

    def retrieve_details_by_year(
        self, year: int, include_decimal_scores: bool = False
    ) -> list[dict[str, Any]]:
        """Retrieves detailed show information by year.

        :param year: Four-digit year
        :param include_decimal_scores: A boolean to determine if decimal
            scores should be included
        :return: A list of dictionaries containing show ID, show date,
            Best Of show flag, repeat show ID (if applicable), show URL
            at NPR.org, host, scorekeeper, location, panelists and
            guests
        """
        try:
            parsed_year = datetime.datetime.strptime(f"{year:04d}", "%Y")
        except ValueError:
            return []

        query = """
            SELECT showid FROM ww_shows
            WHERE YEAR(showdate) = %s
            ORDER BY showdate ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query, (parsed_year.year,))
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        show_ids = [v[0] for v in results]
        info = self.info_multiple.retrieve_core_info_by_ids(show_ids)

        if not info:
            return []

        shows = []
        for show in info:
            if info[show]:
                info[show]["panelists"] = self.info.retrieve_panelist_info_by_id(
                    info[show]["id"], include_decimal_scores=include_decimal_scores
                )
                info[show]["bluffs"] = self.info.retrieve_bluff_info_by_id(
                    info[show]["id"]
                )
                info[show]["guests"] = self.info.retrieve_guest_info_by_id(
                    info[show]["id"]
                )
                shows.append(info[show])

        return shows

    def retrieve_details_by_year_month(
        self, year: int, month: int, include_decimal_scores: bool = False
    ) -> list[dict[str, Any]]:
        """Retrieves detailed show information by year and month.

        :param year: Four-digit year
        :param month: One or two-digit month
        :param include_decimal_scores: A boolean to determine if decimal
            scores should be included
        :return: A list of dictionaries containing show ID, show date,
            Best Of show flag, repeat show ID (if applicable), show URL
            at NPR.org, host, scorekeeper, location, panelists and
            guests
        """
        try:
            parsed_year_month = datetime.datetime.strptime(
                f"{year:04d}-{month:02d}-01", "%Y-%m-%d"
            )
        except ValueError:
            return []

        query = """
            SELECT showid FROM ww_shows
            WHERE YEAR(showdate) = %s AND MONTH(showdate) = %s
            ORDER BY showdate ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(
            query,
            (
                parsed_year_month.year,
                parsed_year_month.month,
            ),
        )
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        show_ids = [v[0] for v in results]
        info = self.info_multiple.retrieve_core_info_by_ids(show_ids)

        if not info:
            return []

        shows = []
        for show in info:
            if info[show]:
                info[show]["panelists"] = self.info.retrieve_panelist_info_by_id(
                    info[show]["id"], include_decimal_scores=include_decimal_scores
                )
                info[show]["bluffs"] = self.info.retrieve_bluff_info_by_id(
                    info[show]["id"]
                )
                info[show]["guests"] = self.info.retrieve_guest_info_by_id(
                    info[show]["id"]
                )
                shows.append(info[show])

        return shows

    def retrieve_months_by_year(self, year: int) -> list[int]:
        """Retrieves show months for a year.

        :param year: Four-digit year
        :return: A list of available show months
        """
        try:
            _ = datetime.datetime.strptime(f"{year:04d}", "%Y")
        except ValueError:
            return []

        query = """
            SELECT DISTINCT MONTH(showdate)
            FROM ww_shows
            WHERE YEAR(showdate) = %s
            ORDER BY MONTH(showdate) ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query, (year,))
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [v[0] for v in results]

    def retrieve_random_id(self) -> int:
        """Retrieves an ID for a random show.

        :return: ID for a random show.
        """
        query = """
            SELECT showid FROM ww_shows
            WHERE showdate <= NOW()
            ORDER BY RAND()
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return None

        return result[0]

    def retrieve_random_id_by_year(self, year: int) -> int:
        """Retrieves an ID for a random show for a given year.

        :return: ID for a random show.
        """
        query = """
            SELECT showid FROM ww_shows
            WHERE showdate <= NOW()
            AND YEAR(showdate) = %s
            ORDER BY RAND()
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query, (year,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return None

        return result[0]

    def retrieve_random_date(self) -> str:
        """Retrieves a date for a random show.

        :return: show date string for a random show, in YYYY-MM-DD format.
        """
        query = """
            SELECT showdate FROM ww_shows
            WHERE showdate <= NOW()
            ORDER BY RAND()
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return None

        return result[0].isoformat()

    def retrieve_random_date_by_year(self, year: int) -> str:
        """Retrieves a date for a random show for a given year.

        :return: show date string for a random show, in YYYY-MM-DD format.
        """
        query = """
            SELECT showdate FROM ww_shows
            WHERE showdate <= NOW()
            AND YEAR(showdate) = %s
            ORDER BY RAND()
            LIMIT 1;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query, (year,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return None

        return result[0].isoformat()

    def retrieve_random(self) -> dict[str, Any]:
        """Retrieves information for a random show.

        :return: A dictionary containing show ID, show date, Best Of
            show flag, repeat show ID (if applicable) and show URL at
            NPR.org
        """
        _id = self.retrieve_random_id()

        if not _id:
            return None

        return self.retrieve_by_id(show_id=_id)

    def retrieve_random_by_year(self, year: int) -> dict[str, Any]:
        """Retrieves information for a random show for a given year.

        :return: A dictionary containing show ID, show date, Best Of
            show flag, repeat show ID (if applicable) and show URL at
            NPR.org
        """
        _id = self.retrieve_random_id_by_year(year=year)

        if not _id:
            return None

        return self.retrieve_by_id(show_id=_id)

    def retrieve_random_details(
        self, include_decimal_scores: bool = False
    ) -> dict[str, Any]:
        """Retrieves information and appearances for a random show.

        :return: A dictionary containing show ID, show date, Best Of
            show flag, repeat show ID (if applicable), show URL at
            NPR.org, host, scorekeeper, location, panelists and guests
        """
        _id = self.retrieve_random_id()

        if not _id:
            return None

        return self.retrieve_details_by_id(
            show_id=_id, include_decimal_scores=include_decimal_scores
        )

    def retrieve_random_details_by_year(
        self, year: int, include_decimal_scores: bool = False
    ) -> dict[str, Any]:
        """Retrieves information and appearances for a random show for a given year.

        :return: A dictionary containing show ID, show date, Best Of
            show flag, repeat show ID (if applicable), show URL at
            NPR.org, host, scorekeeper, location, panelists and guests
        """
        _id = self.retrieve_random_id_by_year(year=year)

        if not _id:
            return None

        return self.retrieve_details_by_id(
            show_id=_id, include_decimal_scores=include_decimal_scores
        )

    def retrieve_recent(
        self,
        include_days_ahead: int = 7,
        include_days_back: int = 32,
    ) -> list[dict[str, Any]]:
        """Retrieves basic show information for recent shows.

        :param include_days_ahead: Number of days in the future to
            include
        :param include_days_back: Number of days in the past to
            include
        :return: List of recent shows and corresponding information. If
            show information could not be retrieved, an empty list will
            be returned.
        """
        try:
            past_days = int(include_days_back)
            future_days = int(include_days_ahead)
        except ValueError:
            return []

        try:
            past_date = datetime.datetime.now() - datetime.timedelta(days=past_days)
            future_date = datetime.datetime.now() + datetime.timedelta(days=future_days)
        except OverflowError:
            return []

        query = """
            SELECT showid FROM ww_shows
            WHERE showdate >= %s AND showdate <= %s
            ORDER BY showdate ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(
            query,
            (
                past_date.isoformat(),
                future_date.isoformat(),
            ),
        )
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [self.retrieve_by_id(v[0]) for v in results]

    def retrieve_recent_details(
        self,
        include_days_ahead: int = 7,
        include_days_back: int = 32,
        include_decimal_scores: bool = False,
    ) -> list[dict[str, Any]]:
        """Retrieves detailed show information for recent shows.

        :param include_days_ahead: Number of days in the future to
            include
        :param include_days_back: Number of days in the past to
            include
        :param include_decimal_scores: A boolean to determine if decimal
            scores should be included
        :return: List of recent shows and corresponding details. If show
            information could not be retrieved, an empty list will be
            returned.
        """
        try:
            past_days = int(include_days_back)
            future_days = int(include_days_ahead)
        except ValueError:
            return []

        try:
            past_date = datetime.datetime.now() - datetime.timedelta(days=past_days)
            future_date = datetime.datetime.now() + datetime.timedelta(days=future_days)
        except OverflowError:
            return []

        query = """
            SELECT showid FROM ww_shows
            WHERE showdate >= %s AND showdate <= %s
            ORDER BY showdate ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(
            query,
            (
                past_date.isoformat(),
                future_date.isoformat(),
            ),
        )
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        show_ids = [v[0] for v in results]
        info = self.info_multiple.retrieve_core_info_by_ids(show_ids)

        if not info:
            return []

        shows = []
        for show in info:
            info[show]["panelists"] = self.info.retrieve_panelist_info_by_id(
                show, include_decimal_scores=include_decimal_scores
            )
            info[show]["bluffs"] = self.info.retrieve_bluff_info_by_id(show)
            info[show]["guests"] = self.info.retrieve_guest_info_by_id(show)
            shows.append(info[show])

        return shows

    def retrieve_scores_by_year(
        self, year: int, use_decimal_scores: bool = False
    ) -> list[tuple[str, int | Decimal]]:
        """Retrieves panelist scores for all shows as a tuple.

        :param year: Four-digit year
        :param use_decimal_scores: A boolean to determine if decimal
            scores should be used and returned instead of integer scores
        :return: A list of tuples each containing show date and panelist
            scores
        """
        try:
            _ = datetime.datetime.strptime(f"{year:04d}", "%Y")
        except ValueError:
            return []

        if use_decimal_scores:
            query = """
                SELECT s.showdate AS date, pm.panelistscore_decimal AS score
                FROM ww_showpnlmap pm
                JOIN ww_shows s ON s.showid = pm.showid
                WHERE s.bestof = 0 AND s.repeatshowid IS NULL
                AND pm.panelistscore_decimal IS NOT NULL
                AND YEAR(s.showdate) = %s
                ORDER BY s.showdate ASC, pm.panelistscore_decimal ASC;
                """
        else:
            query = """
                SELECT s.showdate AS date, pm.panelistscore AS score
                FROM ww_showpnlmap pm
                JOIN ww_shows s ON s.showid = pm.showid
                WHERE s.bestof = 0 AND s.repeatshowid IS NULL
                AND pm.panelistscore IS NOT NULL
                AND YEAR(s.showdate) = %s
                ORDER BY s.showdate ASC, pm.panelistscore ASC;
                """
        cursor = self.database_connection.cursor(dictionary=True)
        cursor.execute(query, (year,))
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        shows = {}
        for row in results:
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

    def retrieve_years(self) -> list[int]:
        """Retrieves show years.

        :return: A list of available show years
        """
        query = """
            SELECT DISTINCT YEAR(showdate)
            FROM ww_shows
            ORDER BY YEAR(showdate) ASC;
            """
        cursor = self.database_connection.cursor(dictionary=False)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        if not results:
            return []

        return [v[0] for v in results]
