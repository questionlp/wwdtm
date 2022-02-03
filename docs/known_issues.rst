************
Known Issues
************

This page documents known issues that have come up during the development of
the ``wwdtm`` library. Although many of the issues have been resolved or
mitigated by version 2.0.0 of the library, there are some that might pop up
in some circumstances.

MySQL Connection Pooling
========================

As of the time of writing this documentation, the use of MySQL Connection
Pooling is not officially supported and has not been fully vetted. As such,
it is recommended to not use the following configuration keys in the
``database`` section of the ``config.json`` file.

* use_pool

  * This key may not be supported by all version of MySQL or MySQL-compatible
    database servers

* pool_name
* pool_size

MySQL sql_mode Flags
====================

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