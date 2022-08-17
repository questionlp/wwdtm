*******
Changes
*******

2.0.6
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
