*******
Changes
*******

2.0.9
=====

Documentation Changes
---------------------

Fixed an issue with Read the Docs build issue related to the build pipeline
using a newer version of the ``packaging`` package and the previous version of
the ``Pallets-Sphinx-Themes`` package.

* Upgrade Pallets-Sphinx-Themes from 2.0.2 to 2.0.3

Also, update the build environment from ``ubuntu-20.04`` and Python 3.8 to
``ubuntu-22.04`` and Python 3.10.

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
