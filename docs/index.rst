Wait Wait Stats Library
-----------------------

The Wait Wait Stats Library, ``wwdtm`` is a Python library that is used to
query data regarding guests, hosts, locations, panelists, scorekeepers and
shows from a copy of the Wait Wait Stats database.

wwdtm Library
=============

The Wait Wait Stats Library includes a set of modules and a corresponding set
of ``pytest`` testing modules. The documentation for each module is available
via the links below.

Migrating to v2
===============

With the new major version bump for the ``wwdtm`` library, there have been a
large number of API changes from ``wwdtm`` version 1.x to the current version.
This section of the documentation will provide a summary of changes and
changes to function/method locations.

Known Issues
============

Earlier pre-release versions of wwdtm 2.0 had some incompatibilities if the
database it is pulling from runs MySQL 5.7 or newer due to a violation of
``sql_mode`` flag ``ONLY_FULL_GROUP_BY``. The scripts have caused the
violations have been updated and the issue should be resolved starting with
the pre-release version 2.0.0-rc.3.

To remove the ``ONLY_FULL_GROUP_BY`` flag from the global ``sql_mode``
variable, you will first need to query the current value of ``sql_mode`` by
running:

.. code-block:: mysql

    select @@sql_mode;

Copy the result and remove the ``ONLY_FULL_GROUP_BY`` flag from the list and
run the following command to unset the flag globally:

.. code-block:: mysql

    set global sql_mode='<flags>';

Although a restart of the MySQL database service is not required, the existing
connection does need to be closed and re-opened for the change to take effect
from the MySQL tool of choice.

A way to validate that the variable change is working as expected, if you
have a working copy of the Git repository, is to run ``pytest`` to check for
errors and messages pertaining to the ``ONLY_FULL_GROUP_BY`` flag.


Table of Contents
=================

.. toctree::
    :maxdepth: 2

    wwdtm/index
    tests/index
    migrating/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
