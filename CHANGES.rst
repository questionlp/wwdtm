*******
Changes
*******

2.5.0
=====

**Starting with version 2.5.0, support for all versions of Python prior to 3.10 have been deprecated.**

Application Changes
-------------------

* Remove use of ``dateutil`` from the ``show`` module as it uses methods that have been marked for deprecated
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

* Correct the value set for show ``bluff`` value in ``Show.retrieve_all_details``, which should return an empty dictionary and not an empty list when no Bluff the Listener data is available

Component Changes
-----------------

* Upgrade numpy from 1.24.3 to 1.24.4
* Upgrade pytz from 2023.3 to 2023.3.post1

2.4.0
=====

Application Changes
-------------------

* Remove unnecessary checks for existence of the panelist decimal score columns
* This change means that this library only supports version 4.3 of the Wait Wait Stats Database when ``include_decimal_scores`` or ``use_decimal_scores`` parameters are set to ``True``.
  Usage with older versions of the database will result in errors.

Development Changes
-------------------

* Re-work ``panelist`` and ``show`` tests to remove separate tests for decimal scores and use ``@pytest.mark.parameterize`` to test including or using decimal scores or not
* Update documentation to provide details for ``include_decimal_scores`` and ``use_decimal_scores`` testing parameters

2.3.0
=====

Application Changes
-------------------

* Add support for decimal column and values for panelist Lightning round start and correct

2.2.0
=====

Application Changes
-------------------

* Adding support for panelist decimal scores in ``panelist`` and ``show`` modules and defaulting existing methods to not use decimal scores for backwards compatibility. View docs for more information.
* Add ``encoding="utf-8"`` to every instance of ``with open()``
* Re-work SQL query strings to use triple-quotes rather than multiple strings wrapped in parentheses
* Changed rounding of decimals or floats that return values with 4 places after the decimal point to 5 places

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
