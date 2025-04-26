*******
Changes
*******

2.18.0
======

Application Changes
-------------------

* Adding :py:meth:`wwdtm.show.Show.retrieve_counts_by_year` to retrieve a count of regular, Best Of, repeat, repeat Best Of and a total count of shows
* Adding :py:meth:`wwdtm.show.Show.retrieve_all_counts_by_year` to retrieve a count of regular, Best Of, repeat, repeat Best Of and a total count of shows for all years, grouped by year

Component Changes
-----------------

* Upgrade pytz from 2024.2 to 2025.2

2.17.2
======

Application Changes
-------------------

* Added missing ``use_decimal_scores`` method parameter to :py:meth:`wwdtm.panelist.Panelist.retrieve_random_details`

Development Changes
-------------------

* Updated test for :py:meth:`wwdtm.panelist.Panelist.retrieve_random_details` to including passing in values for ``use_decimal_scores``

2.17.1
======

Application Changes
-------------------

* Added missing ``include_decimal_scores`` method parameter to :py:meth:`wwdtm.show.Show.retrieve_random_details` and :py:meth:`wwdtm.show.Show.retrieve_random_details_by_year` and passthrough to :py:meth:`wwdtm.show.Show.retrieve_details_by_id`

Development Changes
-------------------

* Updated tests for :py:meth:`wwdtm.show.Show.retrieve_random_details` and :py:meth:`wwdtm.show.Show.retrieve_random_details_by_year` to including passing in values for the corresponding ``include_decimal_scores`` parameters

2.17.0
======

Application Changes
-------------------

* Added the following methods to :py:class:`wwdtm.show.Show` to extend the random show feature

  * :py:meth:`wwdtm.show.Show.retrieve_random_id_by_year`
  * :py:meth:`wwdtm.show.Show.retrieve_random_date_by_year`
  * :py:meth:`wwdtm.show.Show.retrieve_random_by_year`
  * :py:meth:`wwdtm.show.Show.retrieve_random_details_by_year`

2.16.1
======

Application Changes
-------------------

* Fix coding issue within :py:meth:`wwdtm.location.Location.retrieve_postal_details_by_abbreviation`

Development Changes
-------------------

* Added missing tests for postal abbreviation methods in :py:class:`wwdtm.location.Location`


2.16.0
======

Application Changes
-------------------

* Add ``retrieve_random()``, ``retrieve_random_id()``, ``retrieve_random_slug()``, ``retrieve_random_date()`` and ``retrieve_random_details()`` to the following classes that mirror the corresponding feature in the `Wait Wait Stats Page`_

  * :py:class:`wwdtm.guest.Guest`
  * :py:class:`wwdtm.host.Host`
  * :py:class:`wwdtm.location.Location`
  * :py:class:`wwdtm.panelist.Panelist`
  * :py:class:`wwdtm.scorekeeper.Scorekeeper`
  * :py:class:`wwdtm.show.Show`

Development Changes
-------------------

* Add corresponding tests for the new series of retrieve random items
* Fixed typos in docstrings or testing assertion messages

2.15.0
======

Application Changes
-------------------

* Change SQL joins from ``JOIN`` to ``LEFT JOIN`` in :py:class:`wwdtm.location.Location` to properly handle ``NULL`` values in the ``state`` column
* Add :py:meth:`wwdtm.location.Location.retrieve_postal_abbreviations` that returns postal abbreviations and their corresponding names and countries

Development Changes
-------------------

* Upgrade ruff from 0.7.0 to 0.9.3
* Remove black from required development packages as part of migrating entirely to Ruff
* Ran ``ruff format`` to format Python code files using the Ruff 2025 Style Guide

2.14.0
======

Application Changes
-------------------

* Rename two show class methods to reflect more accurate phrasing:

  * :py:meth:`wwdtm.show.Show.retrieve_all_best_of_repeats` → :py:meth:`wwdtm.show.Show.retrieve_all_repeat_best_ofs`
  * :py:meth:`wwdtm.show.Show.retrieve_all_best_of_repeats_details` → :py:meth:`wwdtm.show.Show.retrieve_all_repeat_best_ofs_details`

* Create an aliases for the renamed class methods:

  * :py:meth:`wwdtm.show.Show.retrieve_all_best_of_repeats` → :py:meth:`wwdtm.show.Show.retrieve_all_repeat_best_ofs`
  * :py:meth:`wwdtm.show.Show.retrieve_all_best_of_repeats_details` → :py:meth:`wwdtm.show.Show.retrieve_all_repeat_best_ofs_details`

2.13.0
======

Application Changes
-------------------

* Add methods to ``show.show`` to retrieve information and details for Best Of, Repeat and Repeat Best Of shows
* Initial Python 3.13 support

Component Changes
-----------------

* Upgrade mysql-connector from 8.4.0 to 9.1.0
* Upgrade numpy from 2.1.0 to 2.1.2

Development Changes
-------------------

* Upgrade black from 24.8.0 to 24.10.0
* Upgrade ruff from 0.6.9 to 0.7.0
* Upgrade build from 1.2.2 to 1.2.2.post1
* Increase minimum pytest version from 8.0 to 8.3 in ``pyproject.toml``
* Add ``py313`` to ``tool.black.target-version``

Documentation Changes
---------------------

* Theme Updates

  * Replace Pallets-Sphinx-Themes/Flask theme with Furo version 2024.8.6
  * Change body text from IBM Plex Serif to IBM Plex Sans

* Sync required package versions with main package requirements
* Upgrade Sphinx from 8.0.2 to 8.1.3
* Upgrade sphinx-autobuild from 2024.9.19 to 2024.10.3
* Upgrade sphinx-autodoc-typehints from 2.4.4 to 2.5.0
* Upgrade sphinx-toolbox from 3.8.0 to 3.8.1
* Adding sphinxext-opengraph version 0.9.1

2.12.1-post0
============

Documentation Changes
---------------------

* Fix typo in CHANGES

2.12.1
======

Application Changes
-------------------

* Fix error with two f-strings in the ``panelist.decimal_scores`` module

2.12.0
======

Application Changes
-------------------

* Replace all references of ``named_tuple=`` in database cursors to ``dictionary=`` due to cursors using ``NamedTuple`` being marked for deprecation in future versions of MySQL Connector/Python
* Update code that is impacted by the database cursor type change from ``NamedTuple`` to ``dict``
* Additional code cleanup

Component Changes
-----------------

* Upgrade mysql-connector-python from 8.2.0 to 8.4.0
* Upgrade numpy from 1.26.4 to 2.1.0
* Upgrade python-slugify from 8.0.1 to 8.0.4
* Upgrade pytz from 2024.1 to 2024.2

Development Changes
-------------------

* Upgrade black from 24.4.2 to 24.8.0
* Upgrade pytest from 8.1.2 to 8.3.3
* Upgrade ruff from 0.6.7 to 0.6.9
* Add initial pytest coverage reporting using ``pytest-cov``, which can be generated by running: ``pytest --cov=wwdtm tests/``.

Document Changes
----------------

* Sync required package versions with main package requirements

2.11.0
======

Application Changes
-------------------

* Fix issues or add exceptions to Pylint errors and warnings
* Remove an errant semicolon in ``wwdtm.location.location.retrieve_all``
* Replace "Wait Wait Don't Tell Me! Stats" with "Wait Wait Stats" in docstrings

Development Changes
-------------------

* Replace deprecated ``perf_test.py`` file with a basic ``conftest.py`` file for pytest
* Update ``MANIFEST.in`` to remove ``pytest.ini`` and include ``conftest.py``
* Upgrade black from 24.3.0 to 24.4.2
* Upgrade build from 1.2.1 to 1.2.2
* Upgrade pytest from 8.1.1 to 8.1.2
* Upgrade ruff from 0.3.6 to 0.6.7
* Upgrade wheel from 0.43.0 to 0.44.0

Documentation Changes
---------------------

* Upgrade Sphinx from 7.2.6 to 8.0.2
* Upgrade sphinx-autobuild from 2021.3.14 to 2024.9.19
* Upgrade sphinx-autodoc-typehints from 1.25.2 to 2.4.4
* Upgrade sphinx-toolbox from 3.5.0 to 3.8.0
* Upgrade Pallets-Sphinx-Themes from 2.1.1 to 2.1.3
* Upgrade pytest from 8.1.1 to 8.1.2
* Upgrade black from 24.3.0 to 24.4.2
* Update ``build.os`` in ``.readtheedocs.yaml`` from ``ubuntu-22.04`` to ``ubuntu-24.04``

2.10.1
======

Development Changes
-------------------

* Add Python 3.11 and 3.12 version classifiers in ``pyproject.toml``
* Use absolute imports in each of the module's respective ``__init__.py``

Documentation Changes
---------------------

* Correct header formatting for ``wwdtm.pronoun.Pronouns``

2.10.0
======

Application Changes
-------------------

* Starting with version 2.10.0 of this library, the minimum required
  version of the Wait Wait Stats Database is 4.7
* Change handling of Host, Panelist and Scorekeeper pronouns to reflect
  the addition of corresponding pronouns mapping tables introduced with
  Wait Wait Stats Database version 4.7
* The ``pronouns`` property for Hosts, Panelists and Scorekeepers is now
  in the form of a list of pronouns strings
* Add ``Pronouns`` class that retrieves information from

2.9.1
=====

Application Changes
-------------------

* Encapsulate ``latitude`` and ``longitude`` under the ``coordinates`` property for Locations

2.9.0
=====

Application Changes
-------------------

* Add ``latitude`` and ``longitude`` properties to Locations
* Add ``pronouns`` property to Hosts, Panelists and Scorekeepers

Component Changes
-----------------

* Upgrade numpy from 1.26.3 to 1.26.4
* Upgrade pytz from 2023.3.post1 to 2024.1

Development Changes
-------------------

* Upgrade build from 1.0.3 to 1.2.1
* Upgrade pytest from 7.4.4 to 8.1.1
* Upgrade ruff from 0.1.13 to 0.3.6
* Upgrade wheel from 0.42.0 to 0.43.0

2.8.2
=====

Development Changes
-------------------

* Upgrade black from 23.12.1 to 24.3.0

2.8.1
=====

Application Changes
-------------------

* Correct sorting of panelists when retrieving panelist information for show details with
  decimal scores. Previously, the sorting was based on integer score, which causes
  panelists to be ordered incorrectly.

2.8.0
=====

Application Changes
-------------------

* Starting with version 2.8.0 of this library, the minimum required version of the Wait Wait
  Stats Database is 4.5
* Adds support for returning the NPR.org show URL with the show basic and detailed information
  retrieved from the ``showurl`` column from the ``ww_shows`` database table. If ``showurl``
  value is ``NULL`` in the database, a value of ``None`` will be returned

Development Changes
-------------------

* Upgrade black from 23.12.0 to 23.12.1

2.7.0
=====

Application Changes
-------------------

* Update type hints for parameters and return values to be more specific and to replace the use
  of :py:class:`typing.Optional` and :py:class:`typing.Union` with the conventions documented in PEP-484 and PEP-604.
* Replace use of :py:class:`typing.Dict`, :py:class:`typing.List` and :py:class:`typing.Tuple` with :py:class:`dict`,
  :py:class:`list` and :py:class:`tuple` respectively in type hints
* Remove use of :py:meth:`functools.lru_cache` as caching should be done by the application consuming
  the library

Component Changes
-----------------

* Upgrade NumPy from 1.26.0 to 1.26.3

Development Changes
-------------------

* Switch to Ruff for code linting and formatting (with the help of Black)
* Deprecate ``perf_test.py`` for performance testing
* Upgrade pytest from 7.4.3 to 7.4.4
* Upgrade black from 23.11.0 to 23.12.0
* Upgrade wheel from 0.41.3 to 0.42.0

Documentation Changes
---------------------

* Update Sphinx configuration to be more similar to the conventions used by Pallets projects
* Change the base font from IBM Plex Sans to IBM Plex Serif
* Clean up and rewrite docstrings to be more consistent and succinct
* Add table of contents to each module page
* Update the copyright block at the top of each file to remove ``coding`` line and to include
  the appropriate SPDX license identifier

2.6.1
=====

Application Changes
-------------------

* Change ordering of bluff information to be sorted by segment number for individual shows, or
  sorted by either show ID or show date when retrieving information for multiple shows.

2.6.0
=====

Application Changes
-------------------

* Starting with version 2.6.0 of this library, the minimum required version of the Wait Wait
  Stats Database is 4.4.
* Add support for shows that contain multiple Bluff the Listener-like segments by returning Bluff
  information as a list of dictionaries. Each dictionary contains a segment number and both the
  chosen and correct panelist information.

2.5.0
=====

**Starting with version 2.5.0, support for all versions of Python prior to 3.10 have been
deprecated.**

Application Changes
-------------------

* Remove use of ``dateutil`` from the ``show`` module as it uses methods that have been marked as
  deprecated
* Replace ``dateutil.parser.parse`` with ``datetime.datetime.strptime``

Component Changes
-----------------

* Upgrade MySQL Connector/Python from 8.0.33 to 8.2.0
* Upgrade numpy from 1.24.4 to 1.26.0
* Remove python-dateutil from dependencies

Documentation Changes
---------------------

* Change Python version from 3.10 to 3.12
* Upgrade Sphinx from 6.1.2 to 7.2.6
* Upgrade sphinx-autodoc-typehints from 1.23.0 to 1.25.2
* Upgrade sphinx-toolbox from 3.4.0 to 3.5.0
* Upgrade Pallets-Sphinx-Themes from 2.0.3 to 2.1.1
* Sync up dependency versions in ``docs/requirements.txt`` with ``requirements-dev.txt``

Development Changes
-------------------

* Upgrade pytest from 7.3.1 to 7.4.3
* Upgrade black from 23.7.0 to 23.11.0
* Upgrade wheel from 0.41.2 to 0.41.3
* Upgrade build from 0.10.0 to 1.0.3
* Remove ``py38`` and ``py39`` from ``tool.black`` in ``pyproject.toml``
* Bump minimum pytest version from 7.0 to 7.4 in ``pyproject.toml``

2.4.1
=====

Application Changes
-------------------

* Correct the value set for show ``bluff`` value in ``Show.retrieve_all_details``, which should
  return an empty dictionary and not an empty list when no Bluff the Listener data is available

Component Changes
-----------------

* Upgrade numpy from 1.24.3 to 1.24.4
* Upgrade pytz from 2023.3 to 2023.3.post1

2.4.0
=====

Application Changes
-------------------

* Remove unnecessary checks for existence of the panelist decimal score columns
* This change means that this library only supports version 4.3 of the Wait Wait Stats Database
  when ``include_decimal_scores`` or ``use_decimal_scores`` parameters are set to ``True``.
  Usage with older versions of the database will result in errors.

Development Changes
-------------------

* Re-work ``panelist`` and ``show`` tests to remove separate tests for decimal scores and use
  ``@pytest.mark.parameterize`` to test including or using decimal scores or not
* Update documentation to provide details for ``include_decimal_scores`` and ``use_decimal_scores``
  testing parameters

2.3.0
=====

Application Changes
-------------------

* Add support for decimal column and values for panelist Lightning round start and correct

2.2.0
=====

Application Changes
-------------------

* Adding support for panelist decimal scores in ``panelist`` and ``show`` modules and defaulting
  existing methods to not use decimal scores for backwards compatibility. View docs for more information.
* Add ``encoding="utf-8"`` to every instance of ``with open()``
* Re-work SQL query strings to use triple-quotes rather than multiple strings wrapped in parentheses
* Changed rounding of decimals or floats that return values with 4 places after the decimal point
  to 5 places

Component Changes
-----------------

* Upgrade NumPy from 1.24.2 to 1.24.3

Development Changes
-------------------

* Upgrade Black from 23.3.0 to 23.7.0
* Upgrade flake8 from 6.0.0 to 6.1.0
* Upgrade pycodestyle form 2.10.0 to 2.11.0
* Upgrade pytest from 7.3.1 to 7.4.0
* Upgrade wheel from 0.40.0 to 0.41.2

2.1.0
=====

Development Changes
-------------------

* Build out ``pyproject.toml`` so that it can be used for package building and pytest
* Deprecate ``pytest.ini``, ``setup.cfg`` and ``setup.py``

2.0.9
=====

Component Changes
-----------------

* Upgrade MySQL Connector/Python from 8.0.31 to 8.0.33
* Upgrade NumPy from 1.23.4 to 1.24.2
* Upgrade python-slugify from 6.1.2 to 8.0.1
* Upgrade pytz from 2022.6 to 2023.3

Development Changes
-------------------

* Upgrade flake8 from 5.0.4 to 6.0.0
* Upgrade pycodestyle from 2.9.1 to 2.10.0
* Upgrade pytest from 7.2.0 to 7.3.1
* Upgrade Black from 22.10.0 to 23.3.0

Documentation Changes
---------------------

* Upgrade Sphinx from 5.3.0 to 6.1.3
* Upgrade sphinx-autodoc-typehints from 1.19.5 to 1.23.0
* Upgrade sphinx-copybutton from 0.5.0 to 0.5.2
* Upgrade sphinx-toolbox from 3.2.0 to 3.4.0
* Upgrade Pallets-Sphinx-Themes from 2.0.2 to 2.0.3
* Update the Read the Docs build environment from ``ubuntu-20.04`` and Python
  3.8 to ``ubuntu-22.04`` and Python 3.10.

2.0.8
=====

Update required components and development tools to newer versions to include
preliminary support for Python 3.11.

Component Changes
-----------------

* Upgrade MySQL Connector/Python from 8.0.30 to 8.0.31
* Upgrade NumPy from 1.23.2 to 1.23.4
* Upgrade python-slugify from 5.0.2 to 6.1.2
* Upgrade pytz from 2022.2.1 to 2022.6

Development Changes
-------------------

* Upgrade flake8 from 4.0.1 to 5.0.4
* Upgrade pycodestyle from 2.8.0 to 2.9.1
* Upgrade pytest from 7.1.2 to 7.2.0
* Upgrade Black from 22.6.0 to 22.10.0

Documentation Changes
---------------------

In addition to the aforementioned component updates listed in the above sections,
the following lists the components updated related to documentation building.

* Upgrade Sphinx from 5.1.1 to 5.3.0
* Upgrade sphinx-autodoc-typehints from 1.19.1 to 1.19.5
* Upgrade sphinx-toolbox from 3.1.2 to 3.2.0

2.0.7
=====

Component Changes
-----------------

* Upgrade MySQL Connector/Python from 8.0.28 to 8.0.30
* Upgrade NumPy from 1.22.3 to 1.23.2
* Upgrade pytz from 2022.1 to 2022.2.1

Application Changes
-------------------

* Officially dropping support for MariaDB Server and only supporting MySQL
  Server 8.0 or higher

Development Changes
-------------------

* Upgrade Black from 22.1.0 to 22.6.0
* Upgrade pytest from 6.2.5 to 7.1.2
* Change Black ``target-version`` to remove ``py36`` and ``py37``, and add
  ``py310``

2.0.6
=====

This release was abandoned and therefore not available for download.

2.0.5
=====

Application Changes
-------------------

* Update required versions of NumPy and pytz to the correct versions in ``setup.py``

2.0.4
=====

Component Changes
-----------------

* Upgrade NumPy from 1.22.1 to 1.22.3
* Upgrade pytz from 2021.3 to 2022.1

2.0.3.1
=======

Application Changes
-------------------

* Update Development Status in ``setup.cfg`` to be Production/Stable

Documentation Changes
---------------------

* Correct ``mysqld.cnf`` filename in ``docs/known_issues.rst``

2.0.3
=====

Application Changes
-------------------

* Fix panelist and guest appearance scores so that zero is returned as zero
  and not ``None``

2.0.2
=====

Application Changes
-------------------

* Change panelist and guest appearance score as-is rather than return ``None``

Development Changes
-------------------

* Update ``test_panelist_appearances`` tests to add additional values to test
  against

2.0.1
=====

Development Changes
-------------------

* Run the Black code formatter against all of the Python files
* Update copyright strings

2.0.0
=====

Application Changes
-------------------

* A complete rearchitecting of the library that includes encapsulating functions
  within respectively classes
* More detailed documentation, including changes from the previous library to
  ``wwdtm`` version 2, is available under ``docs/`` and is published at:
  https://docs.wwdt.me/en/latest/migrating/index.html


.. _Wait Wait Stats Page: https://stats.wwdt.me/