************
Known Issues
************

This page documents known issues that have come up during the development of
the ``wwdtm`` library. Although many of the issues have been resolved or
mitigated by version 2.0.0 of the library, there are some that might pop up
in some circumstances.

MySQL Connector/Python "Out of Memory" or Host Resolution Errors
================================================================

There is a known issue in which using the C Extension module included with
certain builds of the MySQL Connector/Python driver that can cause ``out of
memory`` or hostname resolution errors.

While the C Extension module can help improve performance over using the pure
Python implementation of the driver, the C Extension module is only available
for certain combination of Python version, operating systems and versions, and
system architectures.

To use the pure Python implementation instead of the C Extension module, for
installations that include and enable the C Extension module, add or set the
``use_pure`` configuration value in the ``database`` section of the
``config.json`` file to ``true``.


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
database it is pulling from runs on a MySQL Server 5.7 or newer due to a
violation of ``sql_mode`` flag ``ONLY_FULL_GROUP_BY``. The scripts have caused
the violations have been updated and the issue should be resolved starting
with the pre-release version 2.0.0-rc.3.

To remove the ``ONLY_FULL_GROUP_BY`` flag from the global ``sql_mode``
variable, you will first need to query the current value of ``sql_mode`` by
running:

.. code-block:: mysql

    select @@sql_mode;

Copy the result and remove the ``ONLY_FULL_GROUP_BY`` flag from the list and
run the following command to unset the flag globally:

.. code-block:: mysql

    set global sql_mode='<flags>';

That will set the ``sql_mode`` to the correct value until the service is 
restarted. To make it persist, you will need to update the ``mysqld.cnf``
file on the server with the following configuration line:

.. code-block::

    sql-mode = <flags>

This will set the ``sql_mode`` variable to the list of flags each time the
service starts.

A way to validate that the variable change is working as expected, if you
have a working copy of the Git repository, is to run ``pytest`` to check for
errors and messages pertaining to the ``ONLY_FULL_GROUP_BY`` flag.