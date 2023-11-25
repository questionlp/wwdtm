******************
Migrating to wwdtm
******************

This section of the documentation covers the changes were made for ``wwdtm``
version 2. Those changes include a complete re-factor of the architecture
for each module within the library.

Below are links to documents that cover changes made for each of the ``wwdtm``
modules:

.. toctree::
    :maxdepth: 1

    guest
    host
    location
    panelist
    scorekeeper
    show

Python Version
==============

Starting with version 2.5.0, ``wwdtm`` has deprecated all versions of Python
prior to 3.10.

All development and testing of ``wwdtm`` is done using Python 3.10 and
3.12.

Handling Database Connections
=============================

In addition to the architectural changes that were made within each model,
one of the bigger changes is that database connections are no longer passed
into each function.

Instead, when you instantiate an instance of an object, you can either pass in
a dictionary containing the database connection information that
:py:class:`mysql.connector.connect` will use create a database connection; or,
you can pass in an existing :py:class:`mysql.connector.connect` connection
object.

The following example show either passing in a dictionary containing the
required database connection information or an existing database connection:

.. code-block:: python

    from mysql.connector import connect
    from wwdtm.show import Show

    # Dictionary containing the required information for mysql.connector
    connect_dict = {
        "database": {
            "host": "localhost",
            "user": "app",
            "password": "...",
            "database": "wwdtm"
        }
    }

    # Option 1:
    # Passing in the database connection information dictionary
    show = Show(connect_dict=connect_dict)

    # Option 2:
    # Passing in an existing database connection
    database_connection = connect(**connect_dict)
    guest = Guest(database_connection=database_connection)

The latter option may be useful if you are using connection pooling within
your application and you're just passing in a connection created from that
connection pool.

Method Output Type Matches Type Hinting
=======================================

With version 1 of ``wwdtm``, if the requested data could not be retrieved from
the database, most functions that would normally return a list or a dictionary
would return ``None`` or ``False`` instead.

This behavior is changed in version 2 in which methods that have type hinting
stating that a method returns a ``Dict`` will return an empty dictionary.
Methods that have type hinting stating that the method returns a list will
return an empty list.

Methods that are designed to return ``int`` or ``string`` will continue to
return ``None`` if the requested data could not be retrieved.
