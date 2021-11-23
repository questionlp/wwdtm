Wait Wait Stats Library
-----------------------

**NOTE:** This version of the Wait Wait Stats Library contained in this
repository is currently in its early stages of development and should not be
considered stable or ready for use. There will be breaking changes made and
significant amount of refactoring left to do as code is ported into this new
library.

For the current version of the library, check out the `libwwdtm`_ repository.

Overview
========

This project provides a Python library that provides an interface to
retrieve data from a copy of the `Wait Wait Stats database`_.

Requirements
============

This version of the library is developed to use features that are included
in Python 3.8; and, thus, is the minimum version of Python supported.

In addition to the Python version requirement, the library depends on a copy
of the `Wait Wait Stats Database`_ that runs on MariaDB or MySQL.

Running Tests
=============

Included in this repository are tests that are written for use with ``pytest``.
To run the tests, simply run: ``pytest`` from the root of the repository.

Code of Conduct
===============

This projects follows version 2.1 of the `Contributor Convenant's`_ Code of
Conduct. A copy of the `Code of Conduct`_ document is included in this
repository.

.. _Contributor Convenant's: https://www.contributor-covenant.org/
.. _Code of Conduct: https://github.com/questionlp/wwdtm/CODE_OF_CONDUCT.md

License
=======

This library is licensed under the terms of the `Apache License 2.0`_.

.. _libwwdtm: https://github.com/questionlp/libwwdtm
.. _Wait Wait Stats Database: https://github.com/questionlp/wwdtm_database
.. _Apache License 2.0: https://github.com/questionlp/wwdtm/LICENSE
